# CLAUDE.md

Guidance for Claude Code (and other AI agents) working in this repository. Keep
it short and current; it is loaded into context every session.

## What this is

RAGonGCP is a **reusable enterprise RAG accelerator** on Google Cloud (Vertex AI
/ Gemini), built **ports-and-adapters** so the retrieval backend is swappable and
new use cases are added by config, not code. First use case: a BC (Vancouver)
real estate assistant. See [docs/architecture.md](docs/architecture.md).

## Commands

```bash
make setup     # uv sync --extra dev (creates/updates .venv)
make test      # offline unit tests (no GCP creds)  — must pass before done
make lint      # ruff                                — must pass before done
make run       # API on :8080 with the fake backend (RAGONGCP_BACKEND=fake)
make ingest    # ingest active profile (needs GCP creds)
make tf-validate
```

Run a single test: `uv run pytest tests/test_rag_service.py -q`.

## Architecture map

- `src/ragongcp/domain/` — backend-agnostic models + ports (`Retriever`,
  `Ingestor`, `Generator`). **No vendor SDK imports here or in `pipeline/`.**
- `src/ragongcp/pipeline/rag_service.py` — orchestration (retrieve → generate).
- `src/ragongcp/adapters/` — backends, chosen in `factory.py`:
  `vertex_rag_engine` (default), `vertex_search`/`custom_vector` (stubs), `fake`.
- `src/ragongcp/generation/` — `gemini` (default), `echo` (offline), `prompt.py`
  (assembly + citation extraction; pure, well-tested).
- `src/ragongcp/ingestion/` — sources (`gcs`, `drive`, `web`) + `run.py` CLI.
- `src/ragongcp/api/` — FastAPI app, routes, schemas.
- `config/` — `default.yaml` + `<profile>.yaml` (deep-merged); `RAGONGCP_*` env.
- `infra/terraform/` — APIs, bucket, least-priv SA, optional Cloud Run.

## How we work here

This repo uses **spec-driven development** and **ADRs**. The
[constitution](.specify/memory/constitution.md) is binding — read it.

- **Significant decision?** Write an ADR ([docs/adr/](docs/adr/README.md), or
  `/adr <title>`). Accepted ADRs are immutable — supersede, don't edit.
- **Non-trivial feature?** Follow `/specify → /plan → /tasks → /implement`
  (see [specs/README.md](specs/README.md)). Spec = the *what*; plan = the *how*.
- **Small fix?** Just do it, with a test.

General loop: **explore → plan → code → verify → (commit when asked)**. Read
before you edit; reuse existing utilities over adding new ones.

## Conventions

- Python ≥3.10, ruff (line length 100), explicit types, concise docstrings only
  where intent isn't obvious. Match surrounding style.
- Config over hardcoding; secrets via env/Secret Manager, never in source.
- Generators answer only from retrieved context and cite `[n]`; never fabricate
  sources. "I don't know" is a valid answer.
- New backend = implement the `domain/` ports + a branch in `adapters/factory.py`;
  no core edits.

## Definition of done

1. `make lint` and `make test` pass (tests added for behavior changes).
2. Docs updated (README/architecture) if the surface changed.
3. Significant decisions captured as ADRs; feature specs marked `Implemented`.
4. Change is focused and reviewable. **Commit/push only when the user asks.**

## Don't

- Don't import GCP SDKs in `domain/` or `pipeline/`.
- Don't add a new use case by editing core code — add a `config/<profile>.yaml`.
- Don't fetch external content outside a source's allowlist.
- Don't edit an Accepted ADR; supersede it.
