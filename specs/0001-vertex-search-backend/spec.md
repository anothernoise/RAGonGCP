# Spec: Vertex AI Search retrieval backend

- **Feature ID:** 0001-vertex-search-backend
- **Status:** Draft
- **Author:** dmansh
- **Date:** 2026-06-02

> Worked example demonstrating the `/specify` output format. Describes the
> **what & why** only.

## Problem / motivation

Some engagements prioritize the fastest possible managed setup with built-in
connectors (Google Drive, websites) over fine-grained retrieval control. Today
`vertex_search` is a stub, so those clients can't use the accelerator without
falling back to the RAG Engine default. We want a fully-managed retrieval option
selectable purely by config.

## Users & scenarios

- **As an** engagement engineer **I want** to select a fully-managed search
  backend via config **so that** I can stand up a grounded assistant with minimal
  setup for a new client.
- Scenario: Given a profile with `backend: vertex_search`, when I run ingestion
  and then `POST /query`, then I receive a grounded answer with citations sourced
  from the managed data store — with no core code changes.

## Requirements

- **FR-1** The system MUST provide a `vertex_search` backend selectable via
  `backend: vertex_search` in a profile, with no edits to `domain/` or `pipeline/`.
- **FR-2** The backend MUST create/get its retrieval resource idempotently
  (`ensure_corpus`).
- **FR-3** The backend MUST ingest the same `Document` set the other backends
  accept (`upsert`).
- **FR-4** The backend MUST return ranked `Chunk`s with `source_uri` and score
  for a `Query` (`retrieve`).
- **FR-5** Retrieved chunks MUST carry enough provenance for the generator to
  emit `[n]` citations.

## Non-functional requirements

- **NFR-1** (Constitution Art. I) No vendor SDK imports leak above `adapters/`.
- **NFR-2** (Art. III) Behavior is unit-tested with the GCP client mocked; the
  suite still runs offline.
- **NFR-3** (Art. IV) Answers remain grounded and cited.
- **NFR-4** (Art. V) IAM/access additions are least-privilege and documented.

## Out of scope

- Conversational/multi-turn search features of Agent Builder.
- Migrating existing RAG Engine corpora to Vertex Search.

## Success criteria

- A profile using `backend: vertex_search` answers golden-set questions with
  citations against a real data store.
- `make lint` and `make test` pass with the new adapter mocked.

## Open questions

- `[NEEDS CLARIFICATION: data store schema — unstructured website + Drive blended, or separate stores per source type?]`
- `[NEEDS CLARIFICATION: which Vertex Search edition/tier is the deployment target?]`
