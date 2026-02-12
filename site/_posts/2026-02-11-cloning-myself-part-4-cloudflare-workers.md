---
layout: post
title: Cloning Myself - Cloudflare Workers (Part 4)
date: 2026-02-11
---

_This post is the part of a series._

In Part 3, I'd improved the embeddings and seen marginally better results from my in-browser AI clone. But let's be honest: distilgpt2 running in a browser tab was never going to produce coherent answers. The responses were still gibberish, just slightly more organized gibberish. It was time to break the constraint.

My original rule was that everything had to run client-side because GitHub Pages is free and I didn't want to pay for hosting. But Cloudflare Workers has a generous free tier, and their Workers AI platform lets you run real models without managing infrastructure. So the new plan: keep the in-browser option for anyone who wants it, but add a cloud-powered mode backed by a proper language model. My tool of choice this time: Claude Code, Anthropic's CLI agent.

## Restructuring the Repository

Before writing any worker code, the repository needed some reorganization. What had been a flat Jekyll site was about to grow infrastructure concerns, and mixing Terraform files with blog posts felt wrong.

I restructured into a monorepo:

- `site/` for the Jekyll blog, embeddings generation, and everything front-end
- `infra/cloudflare-worker/` for the Worker's TypeScript source
- `infra/terraform/` for infrastructure-as-code

To tie it all together, I set up [Just](https://github.com/casey/just) as a command runner. I've been using Just for my other main project, [IronPLC](https://www.ironplc.com/), so it felt like a natural choice. The delegation pattern worked well here too. The root `justfile` delegates to subdirectory justfiles, so `just build` at the top level calls `just site/build`, which runs Jekyll and verifies the embeddings files exist. `just deploy` delegates to the infrastructure side, which builds the Worker and runs Terraform. The `*ARGS` pattern lets the CI pipeline pass `--baseurl` through the chain when deploying to GitHub Pages.

## Building the Worker

The Worker itself is a straightforward RAG pipeline in TypeScript. A POST to `/ask` triggers three steps:

1. **Embed the question** using `bge-small-en-v1.5`, the same model used to pre-compute the document embeddings
2. **Retrieve context** by loading pre-computed embeddings from KV, ranking them by cosine similarity, and taking the top three chunks
3. **Generate an answer** using Llama 3.1 8B Instruct, with a system prompt that constrains it to answer only from the provided context

This meant I needed a second set of embeddings. The in-browser mode uses `all-MiniLM-L6-v2` via Transformers.js, but the cloud mode needs `bge-small-en-v1.5` to match what Cloudflare Workers AI serves. I updated `generate_embeddings.py` to produce both embedding files on every build, one for each model.

The embeddings live in Cloudflare KV, uploaded separately from the Worker deployment since they depend on the site build output. A `just infra/upload-embeddings` recipe grabs the KV namespace ID from Terraform output and pushes the file via the Cloudflare API.

## Infrastructure as Code

This is where things got rocky.

I wanted all the Cloudflare resources managed by Terraform: the KV namespace, the Worker script, the AI binding. Simple enough in theory. I started with the Cloudflare Terraform provider v5.

The first attempt used `cloudflare_workers_script` with a `metadata` block for bindings. CI failed immediately:

```
Error: Unsupported argument
  metadata is not a valid argument
```

A quick search turned up a [GitHub issue](https://github.com/cloudflare/terraform-provider-cloudflare/issues/5439) where Cloudflare themselves recommended holding off on v5 migration for Workers. Not encouraging.

So I fell back to the v4 provider. It had `cloudflare_worker_script` with explicit binding blocks. That also failed:

```
Error: Unsupported block type
  Blocks of type "ai_binding" are not expected here.
```

The v4 provider simply didn't support AI bindings. Dead end.

Back to v5, I discovered it actually has two resource models. The old `cloudflare_workers_script` resource was buggy and incomplete, but starting in v5.9, Cloudflare introduced a new three-resource pattern:

- `cloudflare_worker` for the worker's identity
- `cloudflare_worker_version` for the code and bindings
- `cloudflare_workers_deployment` to route traffic to a specific version

This is the approach Cloudflare's own [IaC documentation](https://developers.cloudflare.com/workers/platform/infrastructure-as-code/) recommends. After being burned twice, I ran `terraform validate` locally against v5.16.0 before committing. It passed.

But getting Terraform Cloud working for state persistence introduced its own issues. The first CI run after adding remote state failed because the resources already existed in Cloudflare from my earlier manual deployments. And the authentication took a couple of attempts to get right. The `TF_API_TOKEN` environment variable doesn't work the way you'd expect; you need `hashicorp/setup-terraform`'s `cli_config_credentials_token` parameter to write the token to `~/.terraformrc`.

## The CORS Saga

With everything deployed, I opened the site, selected "Cloud" mode, typed a question, and hit Ask. A CORS error. Of course.

The first problem was embarrassingly simple: the Worker URL in my frontend JavaScript still had a placeholder `account_id` in it instead of my actual Cloudflare subdomain. After fixing that, I found the real URL but noticed the `workers.dev` route was showing as "disabled" in the Cloudflare dashboard. I enabled it manually and tried again.

It worked! Briefly. The next Terraform deployment disabled the route again, and I was back to CORS errors. But this time the browser was hiding the real problem. The error message said:

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading
the remote resource. (Reason: CORS header 'Access-Control-Allow-Origin'
missing). Status code: 404.
```

The critical detail was hiding at the end: **Status code: 404**. The browser was reporting it as a CORS error because the 404 response lacked CORS headers, but the actual problem was that the Worker wasn't serving traffic at all. A `curl` to the endpoint confirmed it: Cloudflare was returning error code 1042, which means the worker's route is disabled.

The permanent fix was adding a `cloudflare_workers_script_subdomain` Terraform resource with `enabled = true`. Now every deployment keeps the route active automatically, no more manual toggling in the dashboard.

## The Result

It works! Selecting "Cloud (Llama 3.1 8B)" from the dropdown sends the question to the Cloudflare Worker, which returns a coherent, contextual answer. Compared to distilgpt2's "What is an Maze? Question: What does an Maz?", the cloud mode produces actual sentences that reference actual content from my blog posts.

The toggle UI lets visitors choose their experience: in-browser for the privacy-conscious (or the curious), cloud for anyone who wants a real answer. Both modes use the same chunking strategy and the same embedding pipeline, just different models at each stage.
