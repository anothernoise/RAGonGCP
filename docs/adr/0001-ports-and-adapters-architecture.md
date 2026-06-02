# ADR-0001: Ports-and-adapters architecture for backend pluggability

- **Status:** Accepted
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, downstream engagement teams
- **Version:** 1

## Context

RAGonGCP is an accelerator intended to be reused across many client engagements.
Each client may need a different retrieval backend (a managed service for speed,
or a fully self-managed vector store for control/cost). If the application core
depended directly on a specific GCP retrieval SDK, every reuse would require
editing core code, and swapping backends would ripple through the codebase.

## Decision

We will structure the codebase as **ports and adapters (hexagonal)**:

- `domain/` defines backend-agnostic models and **ports** (`Retriever`,
  `Ingestor`, `Generator` Protocols).
- `pipeline/` orchestrates the use case (`RagService`) depending only on ports.
- `adapters/` provide concrete implementations selected at runtime by
  `adapters/factory.py` from configuration.

No module above the adapters layer may import a vendor SDK.

## Consequences

- **Positive:** Backends are swappable via config; the core is unit-testable
  offline with a `fake` adapter; new engagements add an adapter, not edits to
  core logic.
- **Negative / trade-offs:** Extra indirection (ports + factory) and some
  boilerplate per adapter.
- **Risks & mitigations:** Port interfaces could leak backend specifics — keep
  them expressed purely in `domain/models.py` types and review additions.
- **Follow-ups:** [ADR-0002](0002-vertex-ai-rag-engine-default-backend.md) picks
  the default adapter.

## Alternatives considered

- **Direct SDK calls in the service layer** — fastest to write, but couples the
  core to one backend and blocks reuse/testing offline.
- **Plugin system with entry points** — more flexible discovery, but overkill
  for a small set of first-party adapters and harder to reason about.
