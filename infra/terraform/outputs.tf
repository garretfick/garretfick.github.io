output "worker_name" {
  description = "Name of the deployed Cloudflare Worker"
  value       = cloudflare_workers_script.ask_ai.name
}

output "worker_url" {
  description = "URL of the deployed ask-ai Worker"
  value       = "https://ask-ai.${var.cloudflare_account_id}.workers.dev"
}
