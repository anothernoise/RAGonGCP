# ADR-0004: Terraform for infrastructure as code

- **Status:** Accepted
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, downstream engagement teams
- **Version:** 1

## Context

As a reusable accelerator, RAGonGCP must stand up its GCP footprint (API
enablement, a staging bucket, a least-privilege service account, and an optional
Cloud Run service) repeatably across client projects. Manual console setup is
not reproducible and drifts.

## Decision

We will define infrastructure with **Terraform** under `infra/terraform/`, split
by concern (`apis.tf`, `storage.tf`, `iam.tf`, `cloud_run.tf`) and parameterized
by the use-case `profile`. Cloud Run deployment is gated behind
`deploy_cloud_run` so data/IAM can be provisioned without an image present.
`terraform validate` is part of verification; `apply` is left to the operator.

## Consequences

- **Positive:** Reproducible, reviewable, least-privilege-by-default infra that
  ports across engagements; resource naming derives from the profile.
- **Negative / trade-offs:** Contributors need Terraform installed; state
  management must be configured per deployment.
- **Risks & mitigations:** State backend is unset by default — operators choose
  a remote backend; secrets are never committed (`.gitignore` covers tfvars).
- **Follow-ups:** CI-managed `terraform plan`/`apply` is a deferred extension.

## Alternatives considered

- **gcloud shell scripts** — faster for a throwaway POC, but imperative, not
  idempotent, and poor for reuse.
- **Pulumi / Config Connector** — viable, but Terraform is the most widely known
  in the target ecosystem, lowering adoption friction.
