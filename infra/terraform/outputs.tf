output "worker_name" {
  description = "Name of the deployed Cloudflare Worker"
  value       = cloudflare_worker_script.ask_ai.name
}

output "worker_url" {
  description = "URL of the deployed ask-ai Worker"
  value       = "https://ask-ai.${var.cloudflare_account_id}.workers.dev"
}

output "kv_namespace_id" {
  description = "KV namespace ID for uploading embeddings"
  value       = cloudflare_workers_kv_namespace.ask_ai_embeddings.id
}
