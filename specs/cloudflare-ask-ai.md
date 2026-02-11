# Spec: Cloudflare Workers AI as Additional "Ask" Backend

## Goal

Add a Cloudflare Worker as an **additional** LLM backend for the existing "ask" page.
The current in-browser RAG pipeline (Transformers.js + distilgpt2) stays fully
functional. A frontend toggle lets users choose between the two. All Cloudflare
infrastructure is managed via Terraform. Each implementation step must leave the
Jekyll build (`just build`) in a passing state.

---

## Context

### Current System

The "ask" page at `site/ask/index.html` runs a complete RAG pipeline in the browser:

1. On page load, fetches `/static/model/embeddings.json` (pre-computed at build time).
2. On question submit, computes a query embedding with `Xenova/all-MiniLM-L6-v2`
   via Transformers.js.
3. Ranks chunks by cosine similarity, takes top 3.
4. Feeds context + question to `Xenova/distilgpt2` for answer generation.
5. Displays the generated text.

The embeddings are generated at build time by `site/generate_embeddings.py`, which is
invoked by a Jekyll post-write hook (`site/_plugins/generate_embeddings.rb`). The hook
does not fail the Jekyll build if the Python script errors.

The CI pipeline (`.github/workflows/deploy.yaml`) runs:
`Jekyll build` (triggers embeddings) -> `upload artifact` -> `deploy to GitHub Pages`.

### Limitations of Current System

- distilgpt2 produces low-quality answers (not instruction-tuned, small model).
- Initial page load downloads ~50MB+ of ML model weights to the browser.
- Quality ceiling is hard-capped by what runs client-side.

### What This Spec Adds

- A Cloudflare Worker running Llama 3.1 8B Instruct via Workers AI (server-side).
- Pre-computed embeddings using `bge-small-en-v1.5` (matching the Workers AI
  embedding model), stored in Cloudflare KV.
- A frontend toggle so both paths coexist.

---

## Design

### Architecture

```
site/ask/index.html
  |
  |-- [mode = "browser"]
  |     Uses existing Transformers.js pipeline (unchanged)
  |     Loads: /static/model/embeddings.json (all-MiniLM-L6-v2)
  |     Models: Xenova/all-MiniLM-L6-v2 + Xenova/distilgpt2
  |
  |-- [mode = "cloud"]
        POST https://ask-ai.<account>.workers.dev/ask
        Body: { "question": "..." }
        Response: { "answer": "...", "sources": ["...", "...", "..."] }
```

### Why Two Embedding Files

The in-browser path uses `all-MiniLM-L6-v2` embeddings. The Worker path uses
`bge-small-en-v1.5` embeddings (matching `@cf/baai/bge-small-en-v1.5` on Workers AI).
These models produce vectors in **different embedding spaces** -- cosine similarity
across models is meaningless. Each path needs its own pre-computed embeddings.

Both models output 384-dimensional vectors, so the data format is identical. The same
chunks are embedded by both models. Two output files:

| File | Model | Consumer |
|------|-------|----------|
| `embeddings.json` | `all-MiniLM-L6-v2` | In-browser Transformers.js |
| `embeddings-bge.json` | `BAAI/bge-small-en-v1.5` | Cloudflare Worker via KV |

### Worker API Contract

**Endpoint:** `POST /ask`

**Request:**
```json
{
  "question": "What is Garret's experience with PLCs?"
}
```

**Response (success, HTTP 200):**
```json
{
  "answer": "Based on the blog posts, Garret has worked with...",
  "sources": [
    "Title: PLC Programming\n\nContent of first matching chunk...",
    "Title: Industrial Automation\n\nContent of second matching chunk...",
    "Title: IEC 61131\n\nContent of third matching chunk..."
  ]
}
```

**Response (error, HTTP 4xx/5xx):**
```json
{
  "error": "Description of what went wrong"
}
```

**CORS:**
- `Access-Control-Allow-Origin`: `https://garretfick.github.io`
- `Access-Control-Allow-Methods`: `POST, OPTIONS`
- `Access-Control-Allow-Headers`: `Content-Type`
- Responds to `OPTIONS` preflight with 204.

### Worker Internal Flow

```
1. Parse JSON body, extract "question" string
2. Validate: question must be non-empty string, max 500 characters
3. Compute query embedding:
   env.AI.run("@cf/baai/bge-small-en-v1.5", { text: [question] })
4. Load pre-computed embeddings from KV:
   env.EMBEDDINGS_KV.get("embeddings", { type: "json" })
5. Cosine similarity search:
   - For each stored chunk, compute dot product with query embedding
     (vectors are already normalized, so dot product = cosine similarity)
   - Sort descending, take top 3
6. Build prompt:
   System: "You are a helpful assistant that answers questions about
   Garret Fick's blog. Answer based ONLY on the provided context.
   If the context doesn't contain enough information, say so."
   User: "Context:\n{chunk1}\n---\n{chunk2}\n---\n{chunk3}\n\nQuestion: {question}"
7. Generate answer:
   env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
     messages: [{ role: "system", content: ... }, { role: "user", content: ... }],
     max_tokens: 512
   })
8. Return JSON response with answer and source chunks
```

### Worker Bindings

| Binding Name | Type | Resource |
|--------------|------|----------|
| `AI` | `ai` | Workers AI |
| `EMBEDDINGS_KV` | `kv_namespace` | KV namespace `ask-ai-embeddings` |

### Terraform Resources

| Resource | Type | Purpose |
|----------|------|---------|
| `cloudflare_workers_kv_namespace.ask_ai_embeddings` | KV namespace | Store pre-computed bge embeddings |
| `cloudflare_workers_script.ask_ai` | Worker script | The RAG worker with AI + KV bindings |
| `cloudflare_workers_kv.embeddings_data` | KV entry | Upload `embeddings-bge.json` to KV |

### Embedding Generation Changes

Current `site/generate_embeddings.py` loads one model and writes one file. The
modification loads two models and writes two files. The chunking logic is untouched.

**Current flow:**
```
Load all-MiniLM-L6-v2
For each post: chunk -> encode -> append to documents[]
Write documents[] to _site/static/model/embeddings.json
```

**New flow:**
```
Load all-MiniLM-L6-v2
Load BAAI/bge-small-en-v1.5
For each post: chunk -> collect chunks_with_title[]
Encode chunks_with_title[] with all-MiniLM-L6-v2 -> documents_minilm[]
Encode chunks_with_title[] with bge-small-en-v1.5 -> documents_bge[]
Write documents_minilm[] to _site/static/model/embeddings.json
Write documents_bge[] to _site/static/model/embeddings-bge.json
```

The `embeddings.json` output must remain **byte-for-byte identical** to the current
output (same model, same chunking, same JSON format with `indent=2`).

### Frontend Toggle Design

Add a `<select>` element before the question textarea. Two options:

| Value | Label | Behavior |
|-------|-------|----------|
| `browser` | In-Browser (distilgpt2) | Runs existing Transformers.js pipeline. Default. |
| `cloud` | Cloud (Llama 3.1 8B) | POSTs to Worker URL. No model downloads. |

**Mode behavior:**

- **Browser mode:** Identical to current behavior. `loadEmbeddings()` still runs on
  page load. `answerQuestion()` still uses Transformers.js. No code changes to this path.
- **Cloud mode:** `answerQuestion()` checks the selected mode. If cloud, it POSTs to
  the Worker URL, shows "Thinking..." in the status div, and displays the response
  in the output div. If the fetch fails (Worker not deployed, network error), show a
  user-friendly error message in the output div.
- **Loading behavior:** `loadEmbeddings()` always runs (needed for browser mode). The
  cloud path doesn't need the local embeddings but loading them is harmless and keeps
  the browser path ready if the user switches modes.

**Worker URL:** Hardcode as a `const` at the top of the script block. Use a
placeholder like `https://ask-ai.ACCOUNT_ID.workers.dev` initially. Update after
deployment.

### CI/CD Changes

Add steps to the `build` job in `.github/workflows/deploy.yaml`, after the Jekyll
build and before the artifact upload:

```yaml
- name: Setup Terraform
  if: env.CLOUDFLARE_API_TOKEN != ''
  uses: hashicorp/setup-terraform@v3

- name: Deploy Worker via Terraform
  if: env.CLOUDFLARE_API_TOKEN != ''
  working-directory: terraform
  env:
    TF_VAR_cloudflare_api_token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    TF_VAR_cloudflare_account_id: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
  run: |
    terraform init
    terraform apply -auto-approve
```

The `if` condition ensures the steps are skipped when Cloudflare secrets aren't
configured. The existing Jekyll build and GitHub Pages deployment are unaffected.

### Free Tier Budget

| Resource | Limit | Expected Usage |
|----------|-------|----------------|
| Workers AI neurons | 10,000/day | ~100-200 per query (embedding + generation). Budget ~50-100 queries/day. |
| Workers requests | 100,000/day | Well within limits for personal site. |
| KV reads | 100,000/day | One read per query. |
| KV storage | 1 GB | Embeddings ~2-5 MB. |

---

## File Map

### New Files

| File | Purpose |
|------|---------|
| `workers/ask-ai/src/index.js` | Worker entry point |
| `workers/ask-ai/package.json` | Dev dependency on wrangler |
| `workers/ask-ai/wrangler.toml` | Local dev config (not used in production) |
| `terraform/main.tf` | Provider, Worker, KV namespace, KV entry |
| `terraform/variables.tf` | Input variables |
| `terraform/outputs.tf` | Worker URL output |
| `terraform/terraform.tfvars.example` | Example values (no secrets) |

### Modified Files

| File | Change |
|------|--------|
| `.gitignore` | Add terraform state, node_modules |
| `site/generate_embeddings.py` | Dual model loading, dual output files |
| `site/ask/index.html` | Add mode toggle, cloud fetch logic |
| `.github/workflows/deploy.yaml` | Add conditional Terraform steps |

### Unchanged Files

| File | Why |
|------|-----|
| `site/_plugins/generate_embeddings.rb` | Hook still calls same script |
| `site/_config.yml` | `keep_files: [static/model/]` already covers new file |
| `.devcontainer/Dockerfile` | `sentence-transformers` already installed; bge model auto-downloads |

---

## Implementation Steps

Each step is a single commit. After every commit, `just build` must pass and the
existing in-browser ask page must continue to work.

### Step 1: .gitignore Updates

**Files changed:** `.gitignore`

Append these entries:

```
# Terraform
terraform/.terraform/
terraform/*.tfstate*
terraform/.terraform.lock.hcl

# Node
workers/ask-ai/node_modules/
```

**Verification:** `just build` passes. No functional changes.

---

### Step 2: Cloudflare Worker

**Files added:**
- `workers/ask-ai/src/index.js`
- `workers/ask-ai/package.json`
- `workers/ask-ai/wrangler.toml`

**`workers/ask-ai/src/index.js`** must implement the Worker API contract described
in the Design section above. Key requirements:

- ES module format (`export default { async fetch(request, env) { ... } }`).
- CORS handling: respond to OPTIONS with 204 and appropriate headers. Add CORS
  headers to all responses. Allow origin `https://garretfick.github.io`.
- Route POST /ask to the RAG pipeline.
- Return 405 for other methods, 404 for other paths.
- All responses are JSON with `Content-Type: application/json`.
- Cosine similarity: since both query and stored embeddings are L2-normalized,
  use dot product (`sum(a[i] * b[i])`).

**`workers/ask-ai/package.json`:**
```json
{
  "name": "ask-ai",
  "version": "1.0.0",
  "private": true,
  "devDependencies": {
    "wrangler": "^3"
  }
}
```

**`workers/ask-ai/wrangler.toml`:**
```toml
name = "ask-ai"
main = "src/index.js"
compatibility_date = "2025-01-01"

[ai]
binding = "AI"

[[kv_namespaces]]
binding = "EMBEDDINGS_KV"
id = "placeholder-for-local-dev"
```

**Verification:** `just build` passes (new files outside `site/`).
`node -c workers/ask-ai/src/index.js` passes syntax check.

---

### Step 3: Terraform Configuration

**Files added:**
- `terraform/main.tf`
- `terraform/variables.tf`
- `terraform/outputs.tf`
- `terraform/terraform.tfvars.example`

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

resource "cloudflare_workers_kv_namespace" "ask_ai_embeddings" {
  account_id = var.cloudflare_account_id
  title      = "ask-ai-embeddings"
}

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
        type         = "kv_namespace"
        name         = "EMBEDDINGS_KV"
        namespace_id = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
      }
    ]
  }
}

resource "cloudflare_workers_kv" "embeddings_data" {
  account_id   = var.cloudflare_account_id
  namespace_id = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
  key_name     = "embeddings"
  value        = file("${path.module}/../site/_site/static/model/embeddings-bge.json")
}
```

**`terraform/variables.tf`:**

```hcl
variable "cloudflare_api_token" {
  description = "Cloudflare API token with Workers and KV permissions"
  type        = string
  sensitive   = true
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID"
  type        = string
}

variable "allowed_origin" {
  description = "Allowed CORS origin for the Worker"
  type        = string
  default     = "https://garretfick.github.io"
}
```

**`terraform/outputs.tf`:**

```hcl
output "worker_url" {
  description = "URL of the deployed ask-ai Worker"
  value       = "https://ask-ai.${var.cloudflare_account_id}.workers.dev"
}
```

**`terraform/terraform.tfvars.example`:**

```hcl
cloudflare_api_token = "your-api-token-here"
cloudflare_account_id = "your-account-id-here"
```

**Verification:** `just build` passes (new files outside `site/`).

---

### Step 4: Dual Embedding Generation

**Files changed:** `site/generate_embeddings.py`

Modify to load two models and write two output files. The core changes:

1. Load both models at the top:
   ```python
   model_minilm = SentenceTransformer('all-MiniLM-L6-v2')
   model_bge = SentenceTransformer('BAAI/bge-small-en-v1.5')
   ```

2. Collect all chunks first (existing chunking logic unchanged), then encode with
   both models separately.

3. Write two output files:
   ```python
   output_file_minilm = '_site/static/model/embeddings.json'
   output_file_bge = '_site/static/model/embeddings-bge.json'
   ```

4. The existing `embeddings.json` must use the same model (`all-MiniLM-L6-v2`) and
   produce identical output to the current script.

**Verification:**
```
just build
ls site/_site/static/model/embeddings.json       # must exist
ls site/_site/static/model/embeddings-bge.json    # must exist
# Both files have the same number of chunks
# Ask page in-browser mode works (loads embeddings.json as before)
```

---

### Step 5: Frontend Toggle

**Files changed:** `site/ask/index.html`

Add a mode selector and cloud fetch logic. Preserve all existing Transformers.js code.

**HTML additions** (inside the `<form>`, before the textarea):

```html
<select id="mode" class="pure-input-1-4">
    <option value="browser">In-Browser (distilgpt2)</option>
    <option value="cloud">Cloud (Llama 3.1 8B)</option>
</select>
```

**JavaScript additions:**

1. Add a `const WORKER_URL = 'https://ask-ai.ACCOUNT_ID.workers.dev';` at the top
   of the script block.

2. Add a reference: `const modeSelect = document.getElementById('mode');`

3. Add a `async function answerQuestionCloud()` function that:
   - Gets the question text.
   - Sets status to "Thinking...".
   - Disables the ask button.
   - Fetches `WORKER_URL + '/ask'` with POST, JSON body `{ "question": query }`.
   - On success: displays `response.answer` in the output div.
   - On error (network, non-200, JSON parse failure): displays a friendly error
     message like "Cloud service is unavailable. Try the in-browser option."
   - Re-enables the ask button and resets status.

4. Modify the ask button event listener to dispatch based on mode:
   ```javascript
   askButton.addEventListener('click', () => {
       if (modeSelect.value === 'cloud') {
           answerQuestionCloud();
       } else {
           answerQuestion();
       }
   });
   ```

5. The existing `answerQuestion()` function is **not modified at all**.

6. The existing `loadEmbeddings()` call on page load stays (needed for browser mode).

**Verification:**
```
just build
# Open ask page -> select "In-Browser" -> ask question -> works as before
# Open ask page -> select "Cloud" -> ask question -> shows graceful error
#   (Worker not deployed yet, fetch fails)
```

---

### Step 6: CI/CD Pipeline

**Files changed:** `.github/workflows/deploy.yaml`

Add two steps to the `build` job, after "Check site generation" and before
"Upload artifact":

```yaml
    - name: Setup Terraform
      if: ${{ secrets.CLOUDFLARE_API_TOKEN != '' }}
      uses: hashicorp/setup-terraform@v3

    - name: Deploy Worker via Terraform
      if: ${{ secrets.CLOUDFLARE_API_TOKEN != '' }}
      working-directory: terraform
      env:
        TF_VAR_cloudflare_api_token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        TF_VAR_cloudflare_account_id: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
      run: |
        terraform init
        terraform apply -auto-approve
```

Both steps are conditional on the Cloudflare API token secret being configured.
If it isn't, the steps are skipped and the existing pipeline runs unchanged.

**Verification:**
```
just build   # Jekyll build passes (unaffected)
# Push to branch -> CI runs -> Terraform steps skip (no secrets) -> rest works
```

---

### Post-Deployment Follow-Up

After the Worker is deployed and confirmed working:

1. Update `WORKER_URL` in `site/ask/index.html` to the real Worker URL.
2. Optionally change the default `<select>` option to `cloud`.

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Embeddings JSON exceeds KV 25MB value limit | ~155 posts with 384-dim floats should be ~2-5 MB. Monitor. |
| Workers free tier 10ms CPU limit | Cosine similarity over ~500 chunks is well under 10ms. AI calls are I/O, not CPU. |
| 10,000 neurons/day exhausted | Personal site has low traffic. ~50-100 queries/day budget. |
| Dual embedding generation doubles build time | ~30s per model. Acceptable. |
| `bge-small-en-v1.5` local vs Workers AI produces slightly different embeddings | Same BAAI model weights. Test after deployment. |
| Terraform provider breaking changes | Pinned to `~> 5.0`. |

## Out of Scope

- Streaming responses (SSE/WebSocket)
- Custom domain for the Worker
- Rate limiting beyond Cloudflare defaults
- Vectorize (KV is sufficient at this scale)
- Response caching
