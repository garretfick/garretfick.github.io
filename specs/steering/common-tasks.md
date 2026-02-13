# Common Development Tasks

This file documents build commands, testing workflows, and development tasks using the project's justfile-based build system.

## Justfile Locations

| Location | Scope |
|----------|-------|
| `justfile` (root) | Delegates to component justfiles |
| `site/justfile` | Jekyll site build, test, and serve |
| `infra/justfile` | Cloudflare Worker build, Terraform validate/deploy |

## Most Common Commands

### Root Level

| Command | What It Does |
|---------|--------------|
| `just build` | Build the Jekyll site (delegates to `site/justfile`) |
| `just test` | Run all tests: site tests + infrastructure tests |
| `just deploy` | Deploy infrastructure via Terraform |

### Site (`site/justfile`)

| Command | What It Does |
|---------|--------------|
| `cd site && just` | Run default target: install, build, test |
| `cd site && just install` | Install Ruby gem dependencies via Bundler |
| `cd site && just build` | Build Jekyll site and verify embedding files exist |
| `cd site && just test` | Run HTML validation, spell check, and retrieval evaluation |
| `cd site && just run` | Start local dev server at http://localhost:4000 |

### Infrastructure (`infra/justfile`)

| Command | What It Does |
|---------|--------------|
| `just infra/build` | Install npm dependencies and build the Cloudflare Worker |
| `just infra/test` | Initialize Terraform (no backend) and validate configuration |
| `just infra/deploy` | Build Worker, then Terraform plan and apply |
| `just infra/upload-embeddings <file>` | Upload embeddings JSON to Cloudflare KV |

## Pre-PR Requirements

Before creating a pull request, run:

```bash
just build && just test
```

This runs the full pipeline:

1. **Build** - Jekyll generates the site, including embedding generation via a post-write hook
2. **Verify embeddings** - Checks that both `embeddings-all-MiniLM-L6-v2.json` and `embeddings-bge-small-en-v1.5.json` exist
3. **HTML validation** - Nokogiri checks all generated HTML5 files for syntax errors
4. **Spell check** - Aspell checks all HTML files against English dictionary plus custom dictionary (`site/aspell-dict.txt`)
5. **Retrieval evaluation** - Python script evaluates RAG retrieval quality against golden test set

All checks must pass.

## Test Details

### HTML Validation
- Uses Nokogiri HTML5 parser with `max_errors: 10`
- Scans all files matching `site/_site/**/*.html`
- Fails if any file has parse errors

### Spell Check
- Uses GNU Aspell with English dictionary
- Custom dictionary: `site/aspell-dict.txt` (add false positives here)
- Skips `<script>`, `<style>`, `<pre>`, and `<code>` tags
- Requires locale `en_US.UTF-8`

### Retrieval Quality Evaluation
- Script: `site/tests/eval_retrieval.py`
- Golden test set: `site/tests/golden_retrieval.json`
- Tests both embedding models (MiniLM and BGE)
- Pass threshold: 75% of test cases must hit expected keywords/titles
- Exit code non-zero on failure

## Embedding Generation

Embeddings are generated as a Jekyll post-write hook (`site/_plugins/generate_embeddings.rb`) which calls `site/generate_embeddings.py`. The Python script:

1. Loads two models: `all-MiniLM-L6-v2` and `BAAI/bge-small-en-v1.5`
2. Chunks all blog posts by headers (400-word max, 100-word overlap)
3. Encodes chunks with both models
4. Writes two output files to `site/_site/static/model/`

**Dependencies:** `pip install sentence-transformers numpy`

## Troubleshooting

### `just build` fails with missing embeddings
Ensure Python dependencies are installed: `pip install sentence-transformers numpy`. The embedding models are downloaded automatically on first run.

### Spell check fails
Check the error output for misspelled words. If a word is a legitimate technical term or proper noun, add it to `site/aspell-dict.txt` (one word per line). Then re-run `just test`.

### Locale errors during spell check
Aspell requires `en_US.UTF-8` locale. On Ubuntu: `sudo apt-get install locales && sudo locale-gen en_US.UTF-8`.

### Terraform validation fails
Run `just infra/test` to see the error. Common issues: missing provider plugins (run `terraform init` in `infra/terraform/`), or syntax errors in `.tf` files.
