variable "cloudflare_api_token" {
  description = "Cloudflare API token with Workers Scripts: Edit and Workers AI permissions"
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
