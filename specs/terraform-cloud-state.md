# Spec: Terraform Cloud Remote State

## Context

The current Terraform configuration uses local state, which is lost between
GitHub Actions runs. Each CI run starts with empty state and attempts to
recreate all resources. Terraform Cloud's free tier provides remote state
storage, solving this without additional infrastructure.

## Goal

Configure Terraform Cloud as the state backend so that `terraform plan` and
`terraform apply` work correctly across CI runs and local development.

## Design

### Execution Mode

Use **local** execution mode in Terraform Cloud. This means:
- State is stored in Terraform Cloud
- Plan and apply run locally (in GitHub Actions or on the developer's machine)
- No need to configure Cloudflare credentials in Terraform Cloud

### Changes

**`infra/terraform/versions.tf`** — Add a `cloud` block:

```hcl
terraform {
  cloud {
    organization = "garretfick"

    workspaces {
      name = "ask-ai"
    }
  }

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

**`.github/workflows/deploy.yaml`** — Add `TF_API_TOKEN` env var to the deploy step:

```yaml
      - name: Deploy
        run: just deploy
        env:
          TF_API_TOKEN: ${{ secrets.TF_API_TOKEN }}
          TF_VAR_cloudflare_api_token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          TF_VAR_cloudflare_account_id: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

**`specs/cloudflare-ask-ai.md`** — Update prerequisites to mention Terraform Cloud
account, organization, workspace, and `TF_API_TOKEN` secret.

### Prerequisites (manual steps)

1. Create a free Terraform Cloud account at app.terraform.io
2. Create an organization (e.g., `garretfick`)
3. Create a workspace named `ask-ai` with execution mode set to **Local**
4. Generate a user API token: User Settings > Tokens > Create an API token
5. Add `TF_API_TOKEN` as a GitHub repository secret

### Files Changed

| File | Change |
|------|--------|
| `infra/terraform/versions.tf` | Add `cloud` block |
| `.github/workflows/deploy.yaml` | Add `TF_API_TOKEN` env var |
| `specs/cloudflare-ask-ai.md` | Update prerequisites |

### Verification

1. Run `just infra/test` locally (with `TF_API_TOKEN` set) — terraform init
   should connect to Terraform Cloud and validate succeeds
2. Push to GitHub — deploy-worker job should run terraform init successfully
   with remote state
