# ADR-0003: FastAPI as the service interface

- **Status:** Accepted
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, downstream engagement teams
- **Version:** 1

## Context

The accelerator needs a reusable interface that any frontend (chat UI, internal
tool, automation) can sit on, and that deploys cleanly to Cloud Run. It must
expose query and ingestion operations and run locally without GCP credentials
for development.

## Decision

We will expose the core as a **FastAPI** REST service with `POST /query`,
`POST /ingest`, and `GET /healthz`. The `RagService` is wired via dependency
injection in `api/main.py` and resolved lazily, so the app boots (and `/healthz`
works) even without backend credentials; `/query` and `/ingest` build the real
backend on first use.

## Consequences

- **Positive:** Typed request/response via Pydantic; OpenAPI docs for free;
  trivial Cloud Run packaging; testable with `TestClient` against the `fake`
  backend.
- **Negative / trade-offs:** A running service is heavier than a library-only
  surface for pure notebook experimentation.
- **Risks & mitigations:** No auth in the POC — documented as out of scope and
  flagged in [SECURITY.md](../../SECURITY.md); add SSO before any exposure.
- **Follow-ups:** Auth/SSO and rate limiting are deferred extension points.

## Alternatives considered

- **Notebook-only** — great for proving the loop, but not a reusable service.
- **gRPC** — efficient and strongly typed, but higher friction for the broad set
  of clients we expect to integrate.
