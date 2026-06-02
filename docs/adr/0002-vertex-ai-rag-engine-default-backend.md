# ADR-0002: Vertex AI RAG Engine as the default retrieval backend

- **Status:** Accepted
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, downstream engagement teams
- **Version:** 1

## Context

Given the pluggable architecture ([ADR-0001](0001-ports-and-adapters-architecture.md)),
we must choose which backend ships as the default. Options on GCP range from
fully managed (Vertex AI Search / Agent Builder) to fully self-managed (Vertex AI
Vector Search + embeddings). The accelerator's priority is fast, credible POCs
for enterprise clients while retaining enough control to tune retrieval.

## Decision

We will ship **Vertex AI RAG Engine** as the default backend
(`backend: vertex_rag_engine`). It provides managed corpora that handle
chunking, embeddings (`text-embedding-005`), and the vector store, while still
exposing chunk size, top-k, and distance thresholds for tuning. `vertex_search`
and `custom_vector` remain documented stubs as alternative adapters.

## Consequences

- **Positive:** Balanced speed-to-POC and control; managed ingestion from GCS
  and Google Drive fits the Workspace use case; Gemini grounding is native.
- **Negative / trade-offs:** Less control than a hand-built pipeline; tied to a
  Google-managed service's evolving SDK surface.
- **Risks & mitigations:** The RAG SDK namespace has moved
  (`vertexai.preview.rag` → `vertexai.rag`); we isolate this behind
  `adapters/vertex_rag_engine/_sdk.py` so adapter code is version-tolerant.
- **Follow-ups:** Implement `vertex_search` / `custom_vector` adapters when a
  client need arises (each via the spec-driven flow).

## Alternatives considered

- **Vertex AI Search (Agent Builder)** — fastest managed demo with connectors,
  but least control over chunking/retrieval internals.
- **Custom Vector Search + embeddings** — maximum control and cost tuning, but
  the most code to build and maintain; not justified for a POC default.
