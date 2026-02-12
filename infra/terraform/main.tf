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

resource "cloudflare_workers_script_subdomain" "ask_ai" {
  account_id = var.cloudflare_account_id
  script_name = cloudflare_worker.ask_ai.name
  enabled = true
}

# Embeddings KV data is uploaded separately via the deploy pipeline,
# not via Terraform, because it depends on the site build output.
