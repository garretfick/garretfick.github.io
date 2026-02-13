# Project Architecture

This file describes the high-level architecture, monorepo structure, and key subsystems of the garretfick.github.io project.

## Overview

This is a personal portfolio and blog website hosted on GitHub Pages with an AI-powered question-answering feature backed by Cloudflare Workers. The repository is a monorepo with clear separation between the static site and infrastructure.

## Repository Structure

```
garretfick.github.io/
├── site/                          # Jekyll website (GitHub Pages)
│   ├── _posts/                    # Blog posts (Markdown, 160+ posts)
│   ├── _layouts/                  # Liquid templates (base, default, post, grid)
│   ├── _includes/                 # Reusable components (header, footer)
│   ├── _plugins/                  # Jekyll plugins (embedding generation hook)
│   ├── _data/                     # Structured data (languages.yml, opensource.yml)
│   ├── about/                     # About page
│   ├── ask/                       # AI question-answering page
│   ├── blog/                      # Blog index
│   ├── portfolio/                 # Portfolio section
│   ├── talks/                     # Talks section
│   ├── opensource/                # Open source contributions
│   ├── static/                    # CSS, fonts, JavaScript, images
│   ├── tests/                     # Retrieval quality evaluation
│   ├── generate_embeddings.py     # Embedding generation script
│   ├── aspell-dict.txt            # Custom spell check dictionary
│   ├── Gemfile                    # Ruby dependencies
│   ├── Rakefile                   # Ruby tasks (HTML validation, spell check)
│   ├── _config.yml                # Jekyll configuration
│   └── justfile                   # Site build/test tasks
├── infra/                         # Infrastructure code
│   ├── cloudflare-worker/         # Cloudflare Worker (TypeScript)
│   │   ├── src/index.ts           # Worker entry point
│   │   ├── package.json           # Node dependencies
│   │   ├── tsconfig.json          # TypeScript configuration
│   │   └── wrangler.toml          # Wrangler local dev config
│   └── terraform/                 # Terraform IaC
│       ├── main.tf                # Worker, KV namespace, deployment
│       ├── variables.tf           # Input variables
│       ├── outputs.tf             # Output values
│       └── versions.tf            # Provider and backend config
├── specs/                         # Design specifications
│   ├── steering/                  # AI assistant steering files
│   ├── cloudflare-ask-ai.md       # RAG pipeline design spec
│   └── terraform-cloud-state.md   # Remote state design spec
├── .devcontainer/                 # Development container
│   ├── devcontainer.json          # Container features and settings
│   └── Dockerfile                 # Ubuntu base with Ruby, Python, Node
├── .github/workflows/
│   └── deploy.yaml                # CI/CD pipeline
├── .kiro/steering/                # Kiro AI pointer files
├── justfile                       # Root task runner (delegates to components)
└── CLAUDE.md                      # Claude Code entry point
```

## Key Subsystems

### Jekyll Static Site

The core website is a Jekyll 4.3 static site using kramdown for Markdown processing. Content is organized into blog posts, portfolio items, talks, and open source contributions. The site generates to `site/_site/` and is deployed to GitHub Pages.

**Key configuration:**
- `site/_config.yml` - Jekyll settings, permalink format, exclusions
- `site/Gemfile` - Dependencies: Jekyll, kramdown-parser-gfm, nokogiri, jekyll-feed, jekyll-seo-tag, jekyll-sitemap
- Permalinks: `/blog/:title`

### RAG Pipeline (Ask Feature)

The "ask" page (`site/ask/index.html`) provides two modes for answering questions about the blog content:

**In-Browser mode:**
1. Pre-computed embeddings loaded from `/static/model/embeddings-all-MiniLM-L6-v2.json`
2. Query embedding computed with Transformers.js (`Xenova/all-MiniLM-L6-v2`)
3. Cosine similarity search over chunks, top 3 selected
4. Answer generated with `Xenova/distilgpt2`

**Cloud mode:**
1. Question POSTed to Cloudflare Worker at `/ask`
2. Worker computes query embedding with `@cf/baai/bge-small-en-v1.5`
3. Pre-computed embeddings retrieved from Cloudflare KV
4. Cosine similarity search, top 3 chunks selected
5. Answer generated with `@cf/meta/llama-3.1-8b-instruct`

**Embedding generation** happens at build time via a Jekyll post-write hook. Two embedding files are produced (one per model) because the models use different embedding spaces.

### Cloudflare Infrastructure

- **Worker:** TypeScript ES module, handles `/ask` (POST) and `/health` (GET) endpoints
- **KV namespace:** Stores pre-computed BGE embeddings for the Worker
- **Terraform:** Manages all Cloudflare resources with remote state in Terraform Cloud
- **CORS:** Restricted to `garretfick.com`, `garretfick.github.io`, and `localhost:4000`

### CI/CD

GitHub Actions workflow on push to `master`:
1. Build Jekyll site (triggers embedding generation)
2. Run test suite (HTML validation, spell check, retrieval evaluation)
3. Deploy to GitHub Pages
4. Deploy Cloudflare Worker via Terraform
5. Upload embeddings to Cloudflare KV

## Development Environment

The `.devcontainer/` provides a containerized development environment with:
- Ruby (for Jekyll)
- Python (for embedding generation)
- Node.js (for Cloudflare Worker)
- Just (task runner)
- Terraform (infrastructure management)
- Aspell (spell checking)
- Claude Code CLI

Local development: `cd site && just run` starts the Jekyll dev server at `http://localhost:4000`.
