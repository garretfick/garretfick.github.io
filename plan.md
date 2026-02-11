# Plan: Cloudflare Workers AI "Ask" Feature

## Goal
Replace the in-browser LLM (distilgpt2 via Transformers.js) with a Cloudflare Worker
calling Llama 3.1 8B via Workers AI. Deploy with Terraform. Result: a production RAG
system you can cite in job interviews as "I deployed an LLM to a production environment."

---

## Current State

- **Frontend** (`site/ask/index.html`): Loads `embeddings.json`, computes query
  embedding with `Xenova/all-MiniLM-L6-v2`, does cosine similarity, generates answer
  with `Xenova/distilgpt2` -- all in-browser via Transformers.js.
- **Embeddings pipeline** (`site/generate_embeddings.py`): At build time, chunks all
  blog posts, generates embeddings with `all-MiniLM-L6-v2`, writes
  `_site/static/model/embeddings.json`.
- **Deployment**: GitHub Actions builds Jekyll site and deploys to GitHub Pages.

## Target State

- **Cloudflare Worker** handles the entire RAG pipeline server-side:
  query embedding, similarity search, and text generation.
- **KV namespace** stores pre-computed blog post embeddings.
- **Workers AI** provides both embedding (`bge-small-en-v1.5`) and text generation
  (`llama-3.1-8b-instruct`).
- **Terraform** manages all Cloudflare infrastructure.
- **Frontend** becomes a thin client: sends question, displays answer.

---

## Architecture

```
Browser (ask page)
  |
  | POST /ask  { "question": "..." }
  v
Cloudflare Worker (ask-ai.<account>.workers.dev)
  |
  |-- 1. Compute query embedding via Workers AI (bge-small-en-v1.5)
  |-- 2. Load blog embeddings from KV namespace
  |-- 3. Cosine similarity search (top 3 chunks)
  |-- 4. Build RAG prompt with retrieved context
  |-- 5. Generate answer via Workers AI (llama-3.1-8b-instruct)
  |
  v
JSON response { "answer": "...", "sources": [...] }
```

**Why these models:**
- `@cf/baai/bge-small-en-v1.5` -- 384-dim embeddings, same dimensionality as
  the current model, good quality, low neuron cost.
- `@cf/meta/llama-3.1-8b-instruct` -- massive quality upgrade over distilgpt2,
  follows instructions well, fits within free tier neuron budget for moderate usage.

**Free tier budget:**
- 10,000 neurons/day (Workers AI), 100,000 requests/day (Workers), KV free tier
  gives 100,000 reads/day. More than sufficient for a personal site.

---

## Monorepo Directory Structure

New files to add (existing site structure unchanged):

```
garretfick.github.io/
+-- workers/
|   +-- ask-ai/
|       +-- src/
|       |   +-- index.js          # Worker entry point
|       +-- package.json          # For local dev tooling (wrangler)
|       +-- wrangler.toml         # For local dev/testing only
+-- terraform/
|   +-- main.tf                   # Provider, worker script, KV, AI binding
|   +-- variables.tf              # account_id, api_token, etc.
|   +-- outputs.tf                # Worker URL output
|   +-- terraform.tfvars.example  # Example values (no secrets)
+-- site/
    +-- generate_embeddings.py    # MODIFIED: switch to bge-small-en-v1.5 model
    +-- ask/
        +-- index.html            # MODIFIED: thin client calling Worker API
```

---

## Implementation Steps

### Step 1: Create the Cloudflare Worker (`workers/ask-ai/src/index.js`)

A single Worker script that:

1. **Handles CORS** -- `OPTIONS` preflight + `Access-Control-Allow-Origin` header
   scoped to the GitHub Pages origin (`https://garretfick.github.io`).
2. **Accepts POST /ask** with JSON body `{ "question": "..." }`.
3. **Computes query embedding** by calling `env.AI.run("@cf/baai/bge-small-en-v1.5", ...)`.
4. **Loads embeddings from KV** -- single key `embeddings` containing the full JSON
   array of `{ chunk, embedding }` objects.
5. **Cosine similarity search** -- rank all chunks, take top 3.
6. **Builds RAG prompt** -- system message constraining the model to answer only from
   context, plus the user question and retrieved chunks.
7. **Generates answer** by calling `env.AI.run("@cf/meta/llama-3.1-8b-instruct", ...)`.
8. **Returns JSON** `{ "answer": "...", "sources": ["chunk1...", "chunk2...", "chunk3..."] }`.
9. **Error handling** -- returns structured JSON errors with appropriate HTTP status codes.

Add `workers/ask-ai/package.json` with `wrangler` as a dev dependency for local
testing. Add `workers/ask-ai/wrangler.toml` for `wrangler dev` (local development
only; production deployment is via Terraform).

### Step 2: Create Terraform Configuration (`terraform/`)

**`terraform/main.tf`:**

```hcl
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# KV namespace for storing embeddings
resource "cloudflare_workers_kv_namespace" "ask_ai_embeddings" {
  account_id = var.cloudflare_account_id
  title      = "ask-ai-embeddings"
}

# Worker script with AI and KV bindings
resource "cloudflare_workers_script" "ask_ai" {
  account_id  = var.cloudflare_account_id
  script_name = "ask-ai"
  content     = file("${path.module}/../workers/ask-ai/src/index.js")

  metadata = {
    main_module        = "index.js"
    compatibility_date = "2025-01-01"
    bindings = [
      {
        type = "ai"
        name = "AI"
      },
      {
        type           = "kv_namespace"
        name           = "EMBEDDINGS_KV"
        namespace_id   = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
      }
    ]
  }
}
```

**`terraform/variables.tf`:**
- `cloudflare_api_token` (sensitive)
- `cloudflare_account_id`
- `allowed_origin` (default: `https://garretfick.github.io`)

**`terraform/outputs.tf`:**
- Worker URL (`ask-ai.<account>.workers.dev`)

**`terraform/terraform.tfvars.example`:**
- Template with placeholder values, no secrets.

### Step 3: Switch Embedding Model (`site/generate_embeddings.py`)

Change the model from `all-MiniLM-L6-v2` to `BAAI/bge-small-en-v1.5` so that
pre-computed embeddings are compatible with the Workers AI embedding model.

Changes:
- Line 9: `SentenceTransformer('all-MiniLM-L6-v2')` -> `SentenceTransformer('BAAI/bge-small-en-v1.5')`
- Both models output 384-dim vectors, so no structural changes needed.

### Step 4: Create an Embeddings Upload Script

Add a script (`scripts/upload-embeddings.sh` or similar) that:
1. Reads `site/_site/static/model/embeddings.json`
2. Uploads it to the KV namespace as a single key `embeddings` using
   the Cloudflare API (via `curl` or `wrangler kv:key put`)

This runs after the Jekyll build generates embeddings and before/after Terraform apply.
The KV namespace ID comes from Terraform output.

Alternatively, add a `cloudflare_workers_kv` resource in Terraform that reads the
local embeddings file:

```hcl
resource "cloudflare_workers_kv" "embeddings_data" {
  account_id   = var.cloudflare_account_id
  namespace_id = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
  key_name     = "embeddings"
  value        = file("${path.module}/../site/_site/static/model/embeddings.json")
}
```

This is cleaner -- Terraform manages everything. The tradeoff is that `terraform plan`
needs the Jekyll build to have run first (so the file exists).

### Step 5: Update the Ask Page Frontend (`site/ask/index.html`)

Replace the entire Transformers.js client-side RAG with a simple fetch call:

- Remove the `<script type="module">` block with Transformers.js imports.
- Add vanilla JS that:
  1. On button click, POST to the Worker URL with `{ "question": questionInput.value }`.
  2. Show loading state ("Thinking...").
  3. Display the response `answer` field.
  4. Optionally show source chunks for transparency.
- The Worker URL should be configurable -- either hardcoded or injected at build time
  via Jekyll config. Hardcoding is fine for a personal site.

The page will load instantly (no more downloading 50MB+ of ML models to the browser).

### Step 6: Update CI/CD Pipeline (`.github/workflows/deploy.yaml`)

Add a job (or extend the existing one) that runs after the Jekyll build:

1. **Setup Terraform** -- use `hashicorp/setup-terraform` action.
2. **Terraform init + apply** -- deploys the Worker and KV namespace. Uses secrets
   `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from GitHub repo settings.
3. The embeddings upload happens implicitly via the `cloudflare_workers_kv` Terraform
   resource that reads the built `embeddings.json`.

**Sequencing:**
```
Jekyll build (generates embeddings.json)
  -> Terraform apply (deploys Worker + uploads embeddings to KV)
  -> GitHub Pages deploy (deploys updated frontend)
```

### Step 7: Update .gitignore and Dev Container

- Add `terraform/.terraform/`, `terraform/*.tfstate*`, `terraform/.terraform.lock.hcl`
  to `.gitignore`.
- Optionally add Terraform and wrangler to the dev container for local development.

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Embedding storage | KV (single key) | Simple, free tier allows 100K reads/day, embeddings fit in one value (25MB limit) |
| Embedding model | bge-small-en-v1.5 | Available on both Workers AI and as a local model, 384-dim, good quality |
| Text generation model | Llama 3.1 8B Instruct | Huge quality upgrade over distilgpt2, instruction-following, fits free tier |
| IaC tool | Terraform (not Wrangler) | User requirement; demonstrates IaC skills for interviews |
| CORS strategy | Allowlist GitHub Pages origin | Security best practice; no wildcard |
| Embeddings in Terraform | `cloudflare_workers_kv` resource | Single tool manages everything; no separate upload script needed |
| Worker URL | `*.workers.dev` subdomain | Free, no custom domain needed, avoids DNS complexity |

---

## What Makes This Interview-Ready

1. **Production LLM deployment** -- Llama 3.1 8B running on Cloudflare's global edge
   network, not a toy model in the browser.
2. **Infrastructure as Code** -- Full Terraform configuration, reproducible deployments.
3. **RAG architecture** -- Semantic search over real content with retrieval-augmented
   generation. Industry-standard pattern.
4. **CI/CD pipeline** -- Automated build, embed, deploy cycle via GitHub Actions.
5. **Cost engineering** -- Designed to run entirely within free tier limits.
6. **Production concerns** -- CORS security, error handling, structured API responses.

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Embeddings JSON too large for KV value (>25MB) | Current ~155 posts with 384-dim floats should be ~2-5MB. Monitor size. |
| 10ms CPU time limit on free tier | Cosine similarity over ~500 chunks should be well under 10ms. AI calls are I/O wait, not CPU. |
| 10,000 neurons/day limit | Personal site traffic is low. Each query costs ~100-200 neurons (embedding + generation). Budget for ~50-100 queries/day. |
| Terraform Cloudflare provider v5 API changes | Pin provider version in `required_providers`. |
| `bge-small-en-v1.5` local vs Workers AI produces slightly different embeddings | Use identical model names; both are the same BAAI model. Test similarity scores. |

---

## Out of Scope (for now)

- Streaming responses (would require SSE/WebSocket -- keep it simple with JSON)
- Custom domain for the Worker (workers.dev is fine)
- Rate limiting beyond Cloudflare's built-in free tier limits
- Vectorize (Cloudflare's vector DB) -- KV is simpler and sufficient for this scale
- Caching responses -- could add later with Workers Cache API
