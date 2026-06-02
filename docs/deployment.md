# Deployment Guide

This guide covers deploying RAGonGCP on Google Cloud with Terraform and Cloud
Run.

## 1) Prerequisites

- GCP project with billing enabled
- Terraform `>=1.5`
- `gcloud` CLI authenticated for your target project
- A container image registry path (for Cloud Run deployment)

## 2) Provision baseline infrastructure

From `infra/terraform/`:

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars and set at least project_id
terraform init
terraform validate
terraform plan
terraform apply
```

By default, Terraform creates:

- required project APIs
- staging GCS bucket
- runtime service account and IAM roles

Cloud Run is optional and disabled by default (`deploy_cloud_run = false`).

## 3) Build and push container image

Example flow:

```bash
docker build -t us-central1-docker.pkg.dev/<PROJECT>/<REPO>/ragongcp:latest .
docker push us-central1-docker.pkg.dev/<PROJECT>/<REPO>/ragongcp:latest
```

## 4) Enable Cloud Run deployment in Terraform

In `terraform.tfvars`, set:

```hcl
deploy_cloud_run = true
container_image  = "us-central1-docker.pkg.dev/<PROJECT>/<REPO>/ragongcp:latest"
```

Then apply:

```bash
terraform apply
```

Terraform injects `RAGONGCP_*` environment variables into the Cloud Run service.

## 5) Configure profile and ingest data

Before serving production traffic:

- set up `config/<profile>.yaml`
- configure ingestion sources (Drive folder IDs, allowlisted web URLs)
- run ingestion pipeline to populate corpus

Example:

```bash
uv run python -m ragongcp.ingestion.run --profile bc_real_estate
```

## 6) Verify deployment

- Check `terraform output cloud_run_url`
- Call `/healthz`
- Send a small `/query` smoke test

## Operational notes

- Keep staging bucket lifecycle and retention aligned to your governance policy.
- Restrict service exposure and authentication based on environment requirements.
- Review IAM roles periodically and prefer least privilege.
