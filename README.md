# RAGonGCP

A reusable **enterprise RAG starter on Google Cloud** (Vertex AI + Gemini).

This repository is meant to be copied and adapted for new RAG engagements. It
ships with backend-agnostic core orchestration, grounded generation with
citations, a FastAPI service, ingestion pipelines, evaluation scaffolding, and
Terraform for baseline cloud setup.

## Why use this starter

- **Backend-agnostic core:** ports-and-adapters architecture keeps domain logic
  independent from cloud vendor SDK details.
- **Grounded answers:** responses include inline citations mapped to retrieved
  source chunks.
- **Config-first multi-domain setup:** switch use cases via profile YAML rather
  than code edits.
- **Offline developer path:** fake backend enables local tests/run without GCP
  credentials.
- **Cloud bootstrap included:** Terraform provisions APIs, IAM, bucket, and
  optional Cloud Run deployment.

## Documentation map

- Architecture: [docs/architecture.md](docs/architecture.md)
- Architecture decisions (ADRs): [docs/adr/](docs/adr/README.md)
- Spec-driven development: [specs/](specs/README.md)
- Project constitution: [.specify/memory/constitution.md](.specify/memory/constitution.md)
- Working with AI agents: [CLAUDE.md](CLAUDE.md)
- Deployment guide: [docs/deployment.md](docs/deployment.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)

## How we develop

This project follows two lightweight, AI-agent-friendly processes:

- **Architecture Decision Records** — significant decisions are recorded as
  immutable [ADRs](docs/adr/README.md) (AWS-style lifecycle).
- **Spec-driven development** — non-trivial features flow through
  `/specify → /plan → /tasks → /implement` against a binding
  [constitution](.specify/memory/constitution.md). See [specs/](specs/README.md).

## Requirements

- Python `>=3.10`
- [`uv`](https://docs.astral.sh/uv/) (Python package/dependency manager)
- `make`
- For cloud mode: `gcloud` CLI, Terraform `>=1.5`, and a GCP project

## Quickstart (offline, no GCP required)

```bash
make setup
make lint
make test
make run
```

In another terminal:

```bash
curl localhost:8080/healthz
curl -X POST localhost:8080/query \
  -H 'content-type: application/json' \
  -d '{"question":"What duties does a brokerage owe its clients under RESA?"}'
```

Run the toy evaluation set:

```bash
RAGONGCP_BACKEND=fake uv run python scripts/eval.py
```

## Quickstart (real GCP)

1. Provision baseline infrastructure:

   ```bash
   cd infra/terraform
   cp terraform.tfvars.example terraform.tfvars
   # edit terraform.tfvars and set project_id at minimum
   terraform init
   terraform validate
   terraform apply
   ```

2. Configure runtime environment:

   ```bash
   cp .env.example .env
   # set RAGONGCP_PROJECT_ID, RAGONGCP_LOCATION, RAGONGCP_STAGING_BUCKET
   gcloud auth application-default login
   ```

3. Configure sources in `config/<profile>.yaml` (Drive folder, web URLs).
4. Ingest data:

   ```bash
   uv run python -m ragongcp.ingestion.run --profile bc_real_estate
   ```

5. Serve API:

   ```bash
   uv run uvicorn ragongcp.api.main:app --port 8080
   ```

For Cloud Run deployment details, see [docs/deployment.md](docs/deployment.md).

## Configuration model

- `config/default.yaml`: base retrieval/generation/ingestion defaults
- `config/<profile>.yaml`: use-case overrides (deep merged onto default)
- `.env` / `RAGONGCP_*`: deployment environment settings
- `RAGONGCP_PROFILE=<name>`: select active use case
- `RAGONGCP_BACKEND=<backend>`: optional backend override at runtime
- `RAGONGCP_COST_TRACKING_*`: optional FinOps telemetry controls (disabled by default)

## API endpoints

- `GET /healthz` - liveness + active profile/backend
- `POST /query` - grounded answer with citations
- `POST /ingest` - ingest supplied documents into active corpus

## Repository layout

```text
config/             Base config + per-use-case profiles
src/ragongcp/
  domain/           Backend-agnostic models + ports
  adapters/         Concrete backends (Vertex RAG Engine, fake, stubs)
  generation/       Prompt assembly + Gemini/echo generators
  pipeline/         Retrieve -> generate orchestration
  ingestion/        Source collectors and ingestion CLI
  api/              FastAPI app, routes, schemas
infra/terraform/    APIs, IAM, bucket, optional Cloud Run service
eval/               Golden set for lightweight regression checks
tests/              Offline unit tests
```

## Current scope

Implemented in this starter:

- Vertex RAG Engine retrieval + ingestion adapter
- Gemini generation adapter
- GCS / Google Drive / allowlisted web ingestion sources
- FastAPI endpoints and test suite
- Terraform scaffolding for GCP bootstrap

Intentionally not complete yet (extension points):

- `vertex_search` backend adapter (stub)
- `custom_vector` backend adapter (stub)
- Enterprise auth/SSO and production hardening defaults
- CI/CD-managed Terraform apply workflows
