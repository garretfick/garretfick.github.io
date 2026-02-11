resource "cloudflare_workers_kv_namespace" "ask_ai_embeddings" {
  account_id = var.cloudflare_account_id
  title      = "ask-ai-embeddings"
}

resource "cloudflare_worker_script" "ask_ai" {
  account_id = var.cloudflare_account_id
  name       = "ask-ai"
  content    = file("${path.module}/../cloudflare-worker/dist/index.js")
  module     = true

  ai_binding {
    name = "AI"
  }

  kv_namespace_binding {
    name         = "EMBEDDINGS_KV"
    namespace_id = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
  }
}

# Embeddings KV data is uploaded separately via the deploy pipeline,
# not via Terraform, because it depends on the site build output.
