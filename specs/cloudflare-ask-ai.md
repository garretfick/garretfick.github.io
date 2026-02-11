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

1. On page load, fetches `/static/model/embeddings-all-MiniLM-L6-v2.json` (pre-computed at build time).
2. On question submit, computes a query embedding with `Xenova/all-MiniLM-L6-v2`
   via Transformers.js.
3. Ranks chunks by cosine similarity, takes top 3.
4. Feeds context + question to `Xenova/distilgpt2` for answer generation.
5. Displays the generated text.

The embeddings are generated at build time by `site/generate_embeddings.py`, which is
invoked by a Jekyll post-write hook (`site/_plugins/generate_embeddings.rb`). The hook
currently does not fail the Jekyll build if the Python script errors.

The CI pipeline (`.github/workflows/deploy.yaml`) runs:
`Jekyll build` (triggers embeddings) -> `upload artifact` -> `deploy to GitHub Pages`.

### Repository Structure

The repository is a monorepo with clear separation of concerns:

```
garretfick.github.io/
├── site/                    # Jekyll website (GitHub Pages)
│   ├── _posts/              # 160+ blog posts
│   ├── _layouts/
│   ├── _includes/
│   ├── _plugins/
│   ├── _config.yml
│   ├── ask/
│   ├── static/
│   ├── generate_embeddings.py
│   ├── Gemfile
│   └── ...
├── infra/                   # Infrastructure code
│   ├── terraform/           # Terraform IaC
│   └── cloudflare-worker/   # Cloudflare Worker source code
├── .github/
│   └── workflows/
│       └── deploy.yaml      # CI/CD for both site and Worker
└── .devcontainer/           # Development environment (stays at root)
```

The `infra/` directory is structured to support additional backends in the future
(e.g., `infra/other-backend/`). The `cloudflare-worker/` subdirectory is specific
to the Cloudflare implementation. Terraform in `infra/terraform/` manages all
infrastructure and can grow to include additional providers.

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
  |     Loads: /static/model/embeddings-all-MiniLM-L6-v2.json
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
| `embeddings-all-MiniLM-L6-v2.json` | `all-MiniLM-L6-v2` | In-browser Transformers.js |
| `embeddings-bge-small-en-v1.5.json` | `BAAI/bge-small-en-v1.5` | Cloudflare Worker via KV |

### Worker API Contract

**Endpoint:** `POST /ask`

Full RAG pipeline: computes query embedding, retrieves relevant chunks from KV,
and generates an answer.

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

---

**Endpoint:** `GET /health`

Health check endpoint.

**Response (HTTP 200):**
```json
{
  "status": "ok"
}
```

---

**Response (error, HTTP 4xx/5xx):**
```json
{
  "error": "Description of what went wrong"
}
```

**CORS:**
- `Access-Control-Allow-Origin`: Check the request `Origin` header against an
  allowlist and reflect the matching origin. Allowlist:
  - `https://garretfick.com`
  - `https://www.garretfick.com`
  - `https://garretfick.github.io`
  - `http://localhost:4000` (local dev)
- `Access-Control-Allow-Methods`: `POST, GET, OPTIONS`
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
| `cloudflare_worker.ask_ai` | Worker | Worker identity and settings |
| `cloudflare_worker_version.ask_ai` | Worker version | Code + bindings (AI + KV namespace) |
| `cloudflare_workers_deployment.ask_ai` | Deployment | Deploys the version at 100% |

Embeddings KV data is uploaded separately (not via Terraform) because it
depends on the site build output.

### Embedding Generation Changes

Current `site/generate_embeddings.py` loads one model and writes one file. The
modification loads two models and writes two files. The chunking logic is untouched.

**Current flow:**
```
Load all-MiniLM-L6-v2
For each post: chunk -> encode -> append to documents[]
Write documents[] to _site/static/model/embeddings-all-MiniLM-L6-v2.json
```

**New flow:**
```
Load all-MiniLM-L6-v2
Load BAAI/bge-small-en-v1.5
For each post: chunk -> collect chunks_with_title[]
Encode chunks_with_title[] with all-MiniLM-L6-v2 -> documents_minilm[]
Encode chunks_with_title[] with bge-small-en-v1.5 -> documents_bge[]
Write documents_minilm[] to _site/static/model/embeddings-all-MiniLM-L6-v2.json
Write documents_bge[] to _site/static/model/embeddings-bge-small-en-v1.5.json
```

The `embeddings-all-MiniLM-L6-v2.json` output must be identical to what the current
script produces as `embeddings.json` (same model, same chunking, same JSON format
with `indent=2`). The filename changes but the content does not.

### Frontend Toggle Design

Add a `<select>` element before the question textarea. Two options:

| Value | Label | Behavior |
|-------|-------|----------|
| `browser` | In-Browser (distilgpt2) | Runs existing Transformers.js pipeline. Default. |
| `cloud` | Cloud (Llama 3.1 8B) | POSTs to Worker URL. No model downloads. |

**Mode behavior:**

- **Browser mode:** Identical to current behavior. `answerWithBrowser()` uses
  Transformers.js. Embeddings are loaded lazily (see loading behavior below).
- **Cloud mode:** `answerWithCloudflare()` POSTs to the Worker URL, shows
  "Thinking..." in the status div, and displays the response in the output div.
  If the fetch fails (Worker not deployed, network error), show a user-friendly
  error message in the output div.
- **Loading behavior:** `loadEmbeddings()` is **not** called on page load. Instead,
  embeddings are loaded on-demand the first time the user submits a question in
  browser mode. Once loaded, the embeddings are cached in memory so subsequent
  browser-mode questions don't re-fetch. This avoids a ~2-5 MB download for users
  who only use cloud mode.

**Worker URL:** Hardcode as a `const` at the top of the script block. Use a
placeholder like `https://ask-ai.ACCOUNT_ID.workers.dev` initially. Update after
deployment.

### CI/CD Changes

Add a separate `deploy-worker` job in `.github/workflows/deploy.yaml` for
Cloudflare Worker deployment:

```yaml
deploy-worker:
    if: github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && inputs.deploy_worker == true)
    runs-on: ubuntu-latest
    environment:
      name: cloudflare-worker
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Worker dependencies
        working-directory: infra/cloudflare-worker
        run: npm install

      - name: Build Worker
        working-directory: infra/cloudflare-worker
        run: npm run build

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        working-directory: infra/terraform
        run: terraform init

      - name: Terraform Plan
        working-directory: infra/terraform
        run: terraform plan -out=tfplan
        env:
          TF_VAR_cloudflare_api_token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          TF_VAR_cloudflare_account_id: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}

      - name: Terraform Apply
        working-directory: infra/terraform
        run: terraform apply -auto-approve tfplan
        env:
          TF_VAR_cloudflare_api_token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          TF_VAR_cloudflare_account_id: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

Also add an embeddings verification step to the `build` job, after the Jekyll build
and before artifact upload:

```yaml
    - name: Verify embeddings
      run: |
        test -f site/_site/static/model/embeddings-all-MiniLM-L6-v2.json
        test -f site/_site/static/model/embeddings-bge-small-en-v1.5.json
```

Also add a `deploy_worker` workflow dispatch input:

```yaml
      deploy_worker:
        description: 'Deploy Cloudflare Worker'
        required: false
        default: 'true'
        type: boolean
```

`CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` must be configured as
repository secrets. A `cloudflare-worker` GitHub environment must be created
for deployment protection.

### Free Tier Budget

| Resource | Limit | Expected Usage |
|----------|-------|----------------|
| Workers AI neurons | 10,000/day | ~100-200 per query (embedding + generation). Budget ~50-100 queries/day. |
| Workers requests | 100,000/day | Well within limits for personal site. |
| KV reads | 100,000/day | One read per query. |
| KV storage | 1 GB | Embeddings ~2-5 MB. |
| Worker size | 10 MB | Actual ~3 MB. |

---

## File Map

### New Files

| File | Purpose |
|------|---------|
| `infra/cloudflare-worker/src/index.ts` | Worker entry point (TypeScript) |
| `infra/cloudflare-worker/package.json` | Dev dependencies: `@cloudflare/workers-types`, `esbuild`, `typescript`, `wrangler` |
| `infra/cloudflare-worker/tsconfig.json` | TypeScript config (ES2022, ESM) |
| `infra/cloudflare-worker/wrangler.toml` | Local dev config (production deployment via Terraform) |
| `infra/terraform/main.tf` | Worker script, KV namespace, KV entry resources |
| `infra/terraform/variables.tf` | Input variables: `cloudflare_api_token`, `cloudflare_account_id`, `worker_name`, `allowed_origins` |
| `infra/terraform/outputs.tf` | Worker name and URL outputs |
| `infra/terraform/versions.tf` | Provider version constraints (Cloudflare `~> 5.0`) |
| `infra/terraform/terraform.tfvars.example` | Example values (no secrets) |

### Modified Files

| File | Change |
|------|--------|
| `.gitignore` | Add terraform state, node_modules, worker dist |
| `site/generate_embeddings.py` | Rename output file, dual model loading, dual output files |
| `site/ask/index.html` | Update embeddings path to new filename, add mode toggle, cloud fetch logic |
| `site/_plugins/generate_embeddings.rb` | Fail the Jekyll build if embedding generation fails |
| `.github/workflows/deploy.yaml` | Add embeddings verification step, Worker deployment job, `deploy_worker` input |

### Unchanged Files

| File | Why |
|------|-----|
| `site/_config.yml` | `keep_files: [static/model/]` already covers new files |
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
infra/terraform/.terraform/
infra/terraform/*.tfstate
infra/terraform/*.tfstate.*
infra/terraform/.terraform.lock.hcl
infra/terraform/terraform.tfvars

# Node.js
node_modules/
infra/cloudflare-worker/dist/
```

**Verification:** `just build` passes. No functional changes.

---

### Step 2: Cloudflare Worker

**Files added:**
- `infra/cloudflare-worker/src/index.ts`
- `infra/cloudflare-worker/package.json`
- `infra/cloudflare-worker/tsconfig.json`
- `infra/cloudflare-worker/wrangler.toml`

**`infra/cloudflare-worker/src/index.ts`** must implement the Worker API contract
described in the Design section above. Key requirements:

- TypeScript with ES module format (`export default { async fetch(request, env) { ... } }`).
- CORS handling: respond to OPTIONS with 204 and appropriate headers. Add CORS
  headers to all responses. Check the request `Origin` header against a configurable
  allowlist and reflect the matching origin in the `Access-Control-Allow-Origin`
  response header.
- Route `POST /ask` to the RAG pipeline.
- Route `GET /health` to the health check handler.
- Return 405 for other methods, 404 for other paths.
- All responses are JSON with `Content-Type: application/json`.
- Cosine similarity: since both query and stored embeddings are L2-normalized,
  use dot product (`sum(a[i] * b[i])`).

**`infra/cloudflare-worker/package.json`:**
```json
{
  "name": "ask-ai",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "esbuild src/index.ts --bundle --outfile=dist/index.js --format=esm --target=es2022",
    "dev": "wrangler dev",
    "deploy": "wrangler deploy"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20240129.0",
    "esbuild": "^0.20.0",
    "typescript": "^5.3.0",
    "wrangler": "^3.0.0"
  }
}
```

**`infra/cloudflare-worker/tsconfig.json`:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types"],
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
```

**`infra/cloudflare-worker/wrangler.toml`:**
```toml
# Wrangler configuration for local development
# Production deployment is handled by Terraform
name = "ask-ai"
main = "src/index.ts"
compatibility_date = "2025-01-01"

[ai]
binding = "AI"

[[kv_namespaces]]
binding = "EMBEDDINGS_KV"
id = "placeholder-for-local-dev"
```

**Verification:** `just build` passes (new files outside `site/`).

---

### Step 3: Terraform Configuration

**Files added:**
- `infra/terraform/versions.tf`
- `infra/terraform/main.tf`
- `infra/terraform/variables.tf`
- `infra/terraform/outputs.tf`
- `infra/terraform/terraform.tfvars.example`

**`infra/terraform/versions.tf`:**

```hcl
terraform {
  required_version = ">= 1.0"
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
```

**`infra/terraform/main.tf`:**

```hcl
resource "cloudflare_workers_kv_namespace" "ask_ai_embeddings" {
  account_id = var.cloudflare_account_id
  title      = "ask-ai-embeddings"
}

resource "cloudflare_worker" "ask_ai" {
  account_id = var.cloudflare_account_id
  name       = "ask-ai"
}

resource "cloudflare_worker_version" "ask_ai" {
  account_id         = var.cloudflare_account_id
  worker_id          = cloudflare_worker.ask_ai.id
  compatibility_date = "2025-01-01"
  main_module        = "index.js"

  modules = [{
    name         = "index.js"
    content_type = "application/javascript+module"
    content_file = "${path.module}/../cloudflare-worker/dist/index.js"
  }]

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

resource "cloudflare_workers_deployment" "ask_ai" {
  account_id  = var.cloudflare_account_id
  script_name = cloudflare_worker.ask_ai.name
  strategy    = "percentage"

  versions = [{
    percentage = 100
    version_id = cloudflare_worker_version.ask_ai.id
  }]
}

# Embeddings KV data is uploaded separately via the deploy pipeline,
# not via Terraform, because it depends on the site build output.
```

**`infra/terraform/variables.tf`:**

```hcl
variable "cloudflare_api_token" {
  description = "Cloudflare API token with Workers Scripts: Edit, Workers KV Storage: Edit, and Workers AI permissions"
  type        = string
  sensitive   = true
}

variable "cloudflare_account_id" {
  description = "Cloudflare Account ID"
  type        = string
}

variable "worker_name" {
  description = "Name of the Cloudflare Worker"
  type        = string
  default     = "ask-ai"
}

variable "allowed_origins" {
  description = "Allowed CORS origins for the Worker"
  type        = list(string)
  default     = [
    "https://garretfick.com",
    "https://www.garretfick.com",
    "https://garretfick.github.io",
    "http://localhost:4000"
  ]
}
```

**`infra/terraform/outputs.tf`:**

```hcl
output "worker_name" {
  description = "Name of the deployed Cloudflare Worker"
  value       = cloudflare_worker.ask_ai.name
}

output "worker_url" {
  description = "URL of the deployed ask-ai Worker"
  value       = "https://ask-ai.${var.cloudflare_account_id}.workers.dev"
}

output "kv_namespace_id" {
  description = "KV namespace ID for uploading embeddings"
  value       = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
}
```

**`infra/terraform/terraform.tfvars.example`:**

```hcl
# Copy this file to terraform.tfvars and fill in your values
# DO NOT commit terraform.tfvars to version control
cloudflare_api_token  = "your-api-token-here"
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
   output_file_minilm = '_site/static/model/embeddings-all-MiniLM-L6-v2.json'
   output_file_bge = '_site/static/model/embeddings-bge-small-en-v1.5.json'
   ```

4. The `embeddings-all-MiniLM-L6-v2.json` output must use the same model
   (`all-MiniLM-L6-v2`) and produce content identical to the current script's
   `embeddings.json` output.

**Verification:**
```
just build
ls site/_site/static/model/embeddings-all-MiniLM-L6-v2.json    # must exist
ls site/_site/static/model/embeddings-bge-small-en-v1.5.json   # must exist
# Both files have the same number of chunks
# Ask page in-browser mode works (loads embeddings-all-MiniLM-L6-v2.json)
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

3. Add `async function answerWithBrowser()` that refactors the existing
   `answerQuestion()` logic (same behavior, clearer name):
   - Gets the question text.
   - Lazily loads embeddings if not yet loaded (see loading behavior below).
   - Computes query embedding, finds top 3 chunks, generates answer with distilgpt2.
   - Displays the generated text.

4. Add `async function answerWithCloudflare()` that:
   - Gets the question text.
   - Sets status to "Thinking...".
   - Disables the ask button.
   - Fetches `WORKER_URL + '/ask'` with POST, JSON body `{ "question": query }`.
   - On success: displays `response.answer` in the output div.
   - On error (network, non-200, JSON parse failure): displays a friendly error
     message like "Cloud service is unavailable. Try the in-browser option."
   - Re-enables the ask button and resets status.

5. Modify the ask button event listener to dispatch based on mode:
   ```javascript
   askButton.addEventListener('click', () => {
       if (modeSelect.value === 'cloud') {
           answerWithCloudflare();
       } else {
           answerWithBrowser();
       }
   });
   ```

6. **Lazy-load embeddings:** Remove the `loadEmbeddings()` call from page load.
   Instead, call `loadEmbeddings()` at the start of `answerWithBrowser()` if
   embeddings haven't been loaded yet. Guard with a simple flag or null check so
   the fetch only happens once. This avoids downloading embeddings for users who
   only use cloud mode.

**Verification:**
```
just build
# Open ask page -> select "In-Browser" -> ask question -> works as before
# Open ask page -> select "Cloud" -> ask question -> shows graceful error
#   (Worker not deployed yet, fetch fails)
```

---

### Step 6: Fail Build on Embedding Errors

**Files changed:** `site/_plugins/generate_embeddings.rb`

The current hook silently swallows embedding generation failures. Change it to
raise an error so Jekyll aborts the build:

```ruby
module Jekyll
  Hooks.register :site, :post_write do |site|
    puts "Generating embeddings..."
    result = system("python3 ./generate_embeddings.py")
    unless result
      raise "Embedding generation failed"
    end
    puts "Embeddings generated successfully"
  end
end
```

**Verification:**
```
just build   # must succeed end-to-end with embeddings generated
# Temporarily break generate_embeddings.py -> just build must FAIL
```

---

### Step 7: CI/CD Pipeline

**Files changed:** `.github/workflows/deploy.yaml`

Add an embeddings verification step to the `build` job and a separate
`deploy-worker` job for Cloudflare Worker deployment (see CI/CD Changes
section in Design for full YAML).

**Verification:**
```
just build   # Jekyll build passes (unaffected)
# Push to branch -> CI runs -> embeddings verified -> Worker deployed
```

---

### Step 8: Blog Posts (after implementation)

Create two posts continuing the "Cloning Myself" series:

**Part 4: Technical Journey**
(`site/_posts/YYYY-MM-DD-cloning-myself-part-4-cloudflare-workers.md`)
- Adding a hosted LLM backend
- Repository restructuring (site/ vs infra/)
- Terraform IaC setup for Cloudflare
- Worker implementation details
- CI/CD integration

**Part 5: Comparison & Results** (future post)
- Side-by-side comparison of browser vs cloud modes
- Response quality differences
- Trade-offs: privacy, cost, complexity

---

### Post-Deployment Follow-Up

After the Worker is deployed and confirmed working:

1. Update `WORKER_URL` in `site/ask/index.html` to the real Worker URL.
2. Optionally change the default `<select>` option to `cloud`.

---

## Prerequisites

1. Create Cloudflare account at cloudflare.com
2. Enable Workers AI: Dashboard -> AI -> Workers AI -> Get Started
3. Note your Account ID (found in Cloudflare dashboard URL or Overview page)
4. Generate API token (Dashboard -> My Profile -> API Tokens -> Create Token):
   - Workers Scripts: Edit (Account scope)
   - Workers KV Storage: Edit (Account scope)
   - Workers AI: Read (Account scope)
   - Workers AI: Edit (Account scope)
5. Create Terraform Cloud account at app.terraform.io:
   - Create organization `garretfick`
   - Create workspace `ask-ai` with CLI-Driven Workflow
   - Generate user API token: User Settings > Tokens > Create an API token
6. Add GitHub secrets:
   - `CLOUDFLARE_API_TOKEN` - The Cloudflare API token
   - `CLOUDFLARE_ACCOUNT_ID` - Your Cloudflare account ID
   - `TF_API_TOKEN` - Terraform Cloud API token
7. Create GitHub environment: `cloudflare-worker`
8. (Optional) Install Terraform locally for testing

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Embeddings JSON exceeds KV 25MB value limit | ~155 posts with 384-dim floats should be ~2-5 MB. Monitor. |
| Workers free tier 10ms CPU limit | Cosine similarity over ~500 chunks is well under 10ms. AI calls are I/O, not CPU. |
| 10,000 neurons/day exhausted | Personal site has low traffic. ~50-100 queries/day budget. |
| Dual embedding generation doubles build time | ~30s per model. Acceptable. |
| `bge-small-en-v1.5` local vs Workers AI produces slightly different embeddings | Same BAAI model weights. Test after deployment. |
| Terraform provider breaking changes | Pinned to `~> 5.0`. Uses the v5.9+ resource model (`cloudflare_worker` + `cloudflare_worker_version` + `cloudflare_workers_deployment`). |

## Out of Scope

- Streaming responses (SSE/WebSocket)
- Custom domain for the Worker
- Rate limiting beyond Cloudflare defaults
- Vectorize (KV is sufficient at this scale)
- Response caching
