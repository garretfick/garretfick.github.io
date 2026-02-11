resource "cloudflare_workers_kv_namespace" "ask_ai_embeddings" {
  account_id = var.cloudflare_account_id
  title      = "ask-ai-embeddings"
}

resource "cloudflare_workers_script" "ask_ai" {
  account_id  = var.cloudflare_account_id
  script_name = "ask-ai"
  content     = file("${path.module}/../cloudflare-worker/dist/index.js")

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
  value        = file("${path.module}/../../site/_site/static/model/embeddings-bge-small-en-v1.5.json")
}
