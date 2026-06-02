# RAGonGCP

A reusable **enterprise RAG accelerator on Google Cloud** (Vertex AI / Gemini).
It's a starting point you drop into any RAG engagement: a pluggable retrieval
layer, grounded Gemini generation with first-class citations, a FastAPI service,
and Terraform. The default backend is **Vertex AI RAG Engine**; the first use
case is a **BC (Vancouver) real estate** assistant grounded in company Google
Workspace content + BC real estate governance sources (BCFSA, the Real Estate
Services Act, BCREA/CREA forms).

## Why it's reusable

Ports-and-adapters design (see [docs/architecture.md](docs/architecture.md)):
the core never imports a concrete backend. To take it to a new client you add a
config profile and ingestion sources — not code.

- **Pluggable backends:** `vertex_rag_engine` (default), `vertex_search` (stub),
  `custom_vector` (stub), `fake` (offline).
- **Config-driven use cases:** `RAGONGCP_PROFILE=<name>` selects
  `config/<name>.yaml` (corpus, model, prompt, sources), deep-merged over
  `config/default.yaml`.
- **Citations are first-class** — essential for compliance-sensitive domains.

## Quickstart (offline, no GCP needed)

```bash
make setup                 # venv + install (.[dev])
make test                  # unit tests, all green without GCP creds
make run                   # API on :8080 using the in-memory fake backend
```

Then:

```bash
curl localhost:8080/healthz
curl -X POST localhost:8080/query -H 'content-type: application/json' \
  -d '{"question":"What duties does a brokerage owe its clients under RESA?"}'
```

`RAGONGCP_BACKEND=fake python scripts/eval.py` runs the golden set in `eval/`.

## Running against real GCP

1. **Provision infra** (Terraform):
   ```bash
   cd infra/terraform
   cp terraform.tfvars.example terraform.tfvars   # set project_id
   terraform init && terraform validate
   terraform apply                                # creates bucket, SA, APIs
   ```
2. **Configure env:** copy `.env.example` → `.env`, set `RAGONGCP_PROJECT_ID`,
   `RAGONGCP_LOCATION`, `RAGONGCP_STAGING_BUCKET`, and authenticate with ADC
   (`gcloud auth application-default login`).
3. **Point the profile at your sources:** edit `config/bc_real_estate.yaml`
   (Drive `folder_id`, governance URLs — kept to the `web_allowlist`).
4. **Ingest:**
   ```bash
   python -m ragongcp.ingestion.run --profile bc_real_estate
   ```
5. **Serve:** `uvicorn ragongcp.api.main:app --port 8080` (or deploy to Cloud
   Run via the Dockerfile + Terraform `deploy_cloud_run = true`).

## Layout

```
config/        default.yaml + per-use-case profiles
src/ragongcp/
  domain/      backend-agnostic models + ports (Retriever/Ingestor/Generator)
  adapters/    vertex_rag_engine (default), vertex_search*, custom_vector*, fake
  generation/  gemini (default), echo (offline), prompt assembly + citations
  pipeline/    rag_service.py — retrieve → generate orchestration
  ingestion/   sources (gcs/drive/web) + run.py CLI
  api/         FastAPI app, routes, schemas
infra/terraform/  APIs, GCS bucket, service account/IAM, Cloud Run
eval/          golden_set.jsonl + scripts/eval.py
tests/         offline unit tests (fakes; no GCP)
```
\* stub in this POC.

## Status / scope

POC. Implemented: Vertex RAG Engine retrieval+ingestion, Gemini generation,
FastAPI, GCS/Drive/web ingestion, Terraform, offline test suite. Out of scope:
the two stub backends, API auth/SSO, prod hardening, Terraform `apply` in CI.
See [docs/architecture.md](docs/architecture.md) for how to extend it.
