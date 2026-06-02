# ADR-0008: Adopt Chainlit for demo chat UI

- **Status:** Proposed
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, solution engineers, demo users
- **Version:** 1

## Context

RAGonGCP already provides a production-facing API (`/query`, `/ingest`) and a
CLI sample agent, but demos for stakeholders benefit from a lightweight web chat
experience that is fast to launch and easy to understand.

Building and maintaining a custom frontend for demo purposes would add recurring
UI maintenance overhead that is not core to this repository's architecture goals.
We need a simple, low-friction demo interface that can call the existing API,
show answers and citations, and support sample-document ingestion for local
walkthroughs.

## Decision

We will use **Chainlit** as the default demo chat UI framework for this
repository's sample app.

Implementation shape:

- Keep Chainlit as an **optional dependency** (`demo` extra), not a core runtime
  dependency.
- Keep the demo as a small adapter over the existing API contract (no business
  logic duplication).
- Support local and deployed API endpoints via environment variables.
- Keep demo behavior explicitly non-production (developer/demo convenience first).

## Consequences

- **Positive:** Fast demo setup; minimal code; improved stakeholder experience;
  avoids custom frontend maintenance burden.
- **Negative / trade-offs:** Additional optional dependency tree and lockfile
  churn; framework-specific behavior for the demo layer.
- **Risks & mitigations:** Demo assumptions can be mistaken for production UX;
  mitigate via clear docs that Chainlit app is a sample/demo interface only.
- **Follow-ups:** If production UI requirements emerge, evaluate a dedicated UI
  architecture and capture that decision in a new ADR.

## Alternatives considered

- **Custom React/Next.js demo frontend** — flexible and brandable, but higher
  implementation and maintenance cost for a starter accelerator.
- **CLI-only demo flow** — lowest complexity, but less accessible and less
  compelling for non-technical stakeholders.
