---
layout: post
title: Security IronPLCs GitHub Resources - three pull requests, one weekend, and a CI gate that turned out to be theatre
date: 2026-04-27
---

Three pull requests landed on [IronPLC's GitHub Repository](www.github.com/ironplc/ironplc) in
four days from the same first-time contributor. The first was easy to reject.
The second was easy to reject. The third was two lines (and a good change),
and I almost waved it through with a "what could possibly
go wrong with two lines?" — and that was the one that made me audit my CI
configuration and realise the gate I had implemented was doing approximately nothing.

This post is about the pattern I almost missed, the thing it nearly cost me,
and what I changed.

## The three PRs

The [first PR](https://github.com/ironplc/ironplc/pull/968) arrived on a Thursday.
Seven hundred and forty-six lines of new
content across nineteen files: `SAGE.md`, `AGENTS.md`, `ROADMAP.md`, a custom
`tools/lint-docs.sh` shell script, a markdownlint config, five new GitHub issue
templates, and edits to `CLAUDE.md`, `CURSOR.md`, and the README. The PR title
was *"feat(strategy): Initialize Sovridium Strategy Lattice"*. The body
introduced terms like "Industrial Divinity (Rank Ω)", the "E3 Endogenous
Eudaimonic Ecosystem", "Skill Augmented GRPO", and the "Sovridium™" framework.
The new shell script offered to run `sudo npm install -g markdownlint-cli` as
part of a "documentation linter". The new `AGENTS.md` instructed any future AI
agent working in the repository to follow the "Sovridium" protocol and treat
its specifications as a Single Source of Truth. The `AGENTS.md` file linked to
a website. Here is what I found when I looked:

![Sovridium website screenshot](/static/img/blog/securing-ironplc-github-resources/sovridium.png)

The co-author trailer credited *"Google Antigravity IDE with Gemini 3 flash"*.

This one was easy. I closed it with one comment: "I have no idea what this is."

The [second](https://github.com/ironplc/ironplc/pull/975) arrived two days later, much smaller. It added `.secrets/` to
`.gitignore` and rewrote a section of `CONTRIBUTING.md` to reframe my CI
pipeline as a *"Circuit Integrity Audit"* with "Grounded" tests acting as a
"Circuit Breaker" against "accidental credential leakage". The same author,
the same LLM-co-author trailer. I asked, plainly: *"If there is a person
behind these PRs, please reach out to me directly to explain what this is
for."* The author replied that they were a retired distributed-control-systems
engineer with thirty years' experience, that they would close the PR, and
that they would submit "a few smaller better aligned PRs for consideration,
which should over a longer period start to make logical sense." That last
clause stayed with me longer than it should have at the time.

Thirty years of experience. Here is what I found when I looked:

![LinkedIn profile search screenshot](/static/img/blog/securing-ironplc-github-resources/linkedin.png)

No profile. Odd.

The [third](https://github.com/ironplc/ironplc/pull/979) arrived the next morning. Just `.gitignore`. Just two lines. Just
`.secrets/`, with no `CONTRIBUTING.md` change attached. The PR description
was has two parts - one part that was clear and one part that was obscure:

> This .secrets folder helps keep the repository clean and ensures that any
> internal development or strategic private documentation remains isolated
> from the main circuit, and supports multi-tenant Agentic workflows for the
> strength of LLM diversity of frontier models, while minimizing monopolistic
> predatory propensity.

The *change* was, on its merits, fine. Adding a directory to
`.gitignore` cannot break anything and it is common practice to ignore
`.secrets`. I thought about just making the change myself but ultimately
decided to "give credit" to the author by accepting the change. After all,
it cannot exfiltrate anything. And what could possibly go wrong with two lines?

Believing nothing could go wrong, I merged it. And I sat with the discomfort, suspicion and curiosity that something was up. To some degree, I wanted to know where this was going.

## What I found when I went and read

I was suspicious of the actor. 
I knew about the threat of credential stealing from GitHub repositories, and
I believed I had handled it. But when I sat down to think through whether
I was actually safe, I realised I wasn't.

I am not claiming the contributor to IronPLC was running any attack. Although doubtful, they may genuinely be a retired engineer with an LLM-heavy
writing style and an eccentric taste in industrial metaphors. The point is
that the shorter-horizon variant of the same pattern is now widespread enough
that maintainers across the ecosystem have started writing about it.
LLMs make it cheap to generate plausible-looking PRs in volume. A small
fraction of them are part of a strategy. The strategy works because each
individual PR is innocuous, and because I had built a CI gate that, under
scrutiny, turned out not to be a gate at all.

## The gate I had built, and what I had been afraid of

I was already configured the repository so that you had to be a contributor before any GitHub action would run on a PR. GitHub is generous giving free action time for open source projects but I wanted to be respectful of that gift. 

I improved things in March 2025 after learning about 
the [tj-actions/changed-files compromise](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-github-action), where a
popular third-party action was modified to dump runner memory into the build
log, leaking `GITHUB_TOKEN`s, OIDC tokens, and any in-scope secrets across
thousands of repositories, I treated my GitHub Actions configuration as part
of the attack surface for the first time. I pinned every third-party action
to a 40-character commit SHA instead of a tag and looked at what else could go wrong. The thing that came
out of the "what else can go wrong" review was a per-job `if:` clause on every job in
`integration.yaml`:

```yaml
if: >-
  github.event_name != 'pull_request' ||
  contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR"]'),
           github.event.pull_request.author_association)
```

The configuration was on top of the repository-level control - just in case. It felt clever.  I deployed it and stopped thinking about it.

When the `.secrets/` PR came in, none of the CI jobs ran. They didn't fail.
They didn't queue. They were skipped. The PR sat in `blocked` mergeable state
with no path forward — no "approve and run" button, no UI affordance to opt
in to this specific commit. The only ways out were to merge over branch
protection, dismiss the rule, or push my own commit to the contributor's
branch. None of those were the right shape for what I actually wanted, which
was *"vet this person's PR once."*

That was the prompt. Looking at the gate from the perspective of an attacker
rather than the perspective of its author, three things came out at once.

## Three problems with the gate

**The gate is in the file the attacker controls.** The workflow YAML on a
`pull_request` event is read from the PR branch. Anything I write inside that
YAML — the `if:`, a `needs:`, a label check is editable by the PR
author in the same commit that adds the malicious payload. My gate worked
only against contributors who weren't trying to defeat it.

**One approved commit felt like proof.** This is the one the
three-PR sequence sharpened for me. My repo-level GitHub settings treat a
first approved PR from a new contributor as enough to prove the author.
Once they have one commit approved, future PRs from that account can run
without the same gate being re-evaluated. That means the trust boundary is
not per-PR, it's per-author — and it only moves in one direction.

One innocuous merged PR, or one approved CI run, and the door is open from
then on. If a patient adversary is willing to land three plausible doc-only
PRs over a month to clear that threshold, every clever `if:` I write
afterwards is working from a contaminated premise.

**My publish secrets were sitting at the repository level.** This is the one
that actually scared me. `IRONPLC_WORKFLOW_PUBLISH_ACCESS_TOKEN` is a
fine-grained PAT with `Contents: write` on three repositories, and it sits
in the branch-protection bypass list on `main` because the release workflow
needs it. `VS_MARKETPLACE_TOKEN` and `OVSX_PAT` can ship a tampered VS Code
extension to every IronPLC user. Repo-level secrets are reachable by any
workflow that references them. Even if the `if:` gate had worked, a fork PR
could in principle have edited `deployment.yaml` to inject a release step
and reached those secrets. The gate was the only thing standing between an
attacker and the publish keys, and the gate was inside the file the attacker
was editing. That is not a defence. That is a sign on the door.

## What I built instead

The fix is two GitHub Environments, and it leans on the fact that
**environment configuration lives at the repository level, not in the YAML.**
Edits to a workflow file in a PR cannot change which secrets an environment
exposes, who has to approve a deployment, or which branches are allowed to
deploy to it.

The first environment, `pr-ci`, has required reviewers and no secrets. There
is exactly one job that references it — a zero-step `approve` job at the top
of `integration.yaml`. Every other job in the workflow declares
`needs: approve`. When a PR opens, the workflow run pauses on `approve` with
"Awaiting maintainer approval", and I get a UI affordance — a real button —
that approves that exact commit. Push a new commit, the approval is
invalidated and a fresh one queues up. This is per-PR and per-commit, not
per-author, so the contributor-ratchet problem does not exist: yesterday's
approval does not authorise today's commit.

The second environment, `production`, holds the publish secrets and is
branch-restricted to `main`. It has no required reviewers, because the
weekly release cron has to run unattended. The jobs that consume publish
secrets — the version bumper, the dependency updater, the marketplace
publisher, the playground deployer, the Homebrew tap pusher — all declare
`environment: production`. Because the environment is restricted to `main`,
no `workflow_dispatch` from a feature branch and no `pull_request` from a
fork can deploy to it. Even a fully tampered fork-PR workflow file cannot
reach those secrets, because the secrets are not in repository scope at all
and the environment that holds them refuses to attach to a non-`main` ref.

The two layers compose. `pr-ci` answers "is this code allowed to run on my
runners?" `production` answers "is this code allowed to publish?" The set of
jobs that need each is disjoint. The authorisation surface is obvious by
reading the YAML, not by reasoning about which `if:` conditions hold under
which trigger.

The whole decision is written up in [ADR 0032](https://github.com/ironplc/ironplc/blob/main/specs/adrs/0032-ci-gating-and-secret-scoping.md) in the repo, with the
threat model, the alternatives I rejected (per-job `if:` gates, the
first-time contributor toggle, label-gated workflows, `pull_request_target`
for everything — that last one is famously a foot-gun), and the one-time
GitHub UI setup any future maintainer will need to recreate.

On the one had, I want to know the actor's next move. Is this a short game or long game. On the other hand, I don't want to risk the actor stealing credentials or otherwise gaining access to IronPLC. To address that, I've banned the user account. 

## If you maintain an open-source repository

Two suggestions.

First, look at where your secrets actually live. "Repo-level" is a much
wider blast radius than most people realise: every workflow in the
repository can reference them, including a workflow file edited in a fork
PR. Move publish-class secrets into a GitHub Environment, restrict the
environment to `main`, and have the consuming jobs declare it. Any gate you
were relying on inside the YAML stops being load-bearing.

Second, look at your fork-PR gating from the perspective of someone who is
going to edit the gate in the same commit they attack you with — and from
the perspective of someone willing to land three boring PRs first. The YAML
on a `pull_request` event is theirs, not yours. The author-association
whitelist is monotonic and accumulating. The fix isn't more clever YAML.
It's pushing the decision out of the file the attacker controls, and
re-asking it on every commit instead of on every author.
