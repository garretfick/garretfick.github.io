# Development Standards

This file defines conventions, content standards, code quality expectations, and documentation practices for the garretfick.github.io project.

## Content Standards

### Blog Posts

Blog posts live in `site/_posts/` and follow Jekyll conventions:

- **Filename format:** `YYYY-MM-DD-title-slug.md`
- **Markdown flavor:** kramdown with GitHub Flavored Markdown parser (`kramdown-parser-gfm`)
- **Permalink pattern:** `/blog/:title` (configured in `site/_config.yml`)

**Required YAML front matter:**

```yaml
---
layout: post
title: "Post Title Here"
---
```

**Content guidelines:**
- Write in plain, direct English
- Use code blocks with language identifiers (e.g., ````python`, ````javascript`)
- Prefer inline code for short references (e.g., `variable_name`)
- Use heading levels consistently (H2 for main sections, H3 for subsections)
- All content must pass spell check (see below)

### Spell Checking

All generated HTML is checked with GNU Aspell during `just test`.

- Dictionary: English (`en`)
- Custom words: `site/aspell-dict.txt` (one word per line, alphabetically sorted)
- Tags skipped: `<script>`, `<style>`, `<pre>`, `<code>`

**When adding new content:**
1. Run `just build && just test`
2. If spell check fails, review the reported words
3. Fix genuine misspellings in the source Markdown
4. Add legitimate technical terms, proper nouns, or abbreviations to `site/aspell-dict.txt`

### HTML Validity

All generated HTML must pass Nokogiri HTML5 validation. Common issues:
- Unclosed tags
- Invalid nesting (e.g., block element inside inline element)
- Duplicate `id` attributes

Fix issues in the relevant layout (`site/_layouts/`), include (`site/_includes/`), or post content.

## Code Standards

### Jekyll / Ruby

- Gemfile pins Jekyll to `~> 4.3`
- Plugins are in `site/_plugins/` (currently: embedding generation hook)
- Layouts use Liquid templating
- Data files in `site/_data/` use YAML format

### Cloudflare Worker (TypeScript)

- Source: `infra/cloudflare-worker/src/index.ts`
- ES module format with ES2022 target
- Bundled with esbuild
- All responses are JSON with proper CORS headers
- Input validation at the boundary (question length, type checks)

### Terraform (HCL)

- Configuration: `infra/terraform/`
- Provider: Cloudflare `~> 5.0`
- Remote state: Terraform Cloud (organization `garretfick`, workspace `ask-ai`)
- Variables for sensitive values (API tokens, account IDs) - never hardcode secrets
- Validate with `just infra/test` before committing

### Python (Embeddings)

- Script: `site/generate_embeddings.py`
- Dependencies: `sentence-transformers`, `numpy`
- Invoked automatically by Jekyll post-write hook
- Must produce deterministic chunking across runs

## Build System

The project uses [just](https://github.com/casey/just) as the task runner. Justfiles are at the root, `site/`, and `infra/` levels. The root justfile delegates to component justfiles.

See [common-tasks.md](common-tasks.md) for the full command reference.

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yaml`) runs on pushes to `master` and manual dispatch:

1. **Build job:** Ruby setup, Python setup, dependency install, Jekyll build, test suite, artifact upload
2. **Deploy job:** Deploy to GitHub Pages (conditional)
3. **Deploy-worker job:** Build Cloudflare Worker, Terraform plan and apply, upload embeddings to KV

### Required GitHub Secrets

| Secret | Purpose |
|--------|---------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API access for Worker deployment |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account identifier |
| `TF_API_TOKEN` | Terraform Cloud authentication |

## Design Specifications

Major features are documented as design specs in `specs/` before implementation:

- `specs/cloudflare-ask-ai.md` - RAG pipeline with Cloudflare Workers AI
- `specs/terraform-cloud-state.md` - Remote state management

Specs describe goals, architecture, implementation steps, and verification criteria. Each implementation step should leave the build in a passing state.
