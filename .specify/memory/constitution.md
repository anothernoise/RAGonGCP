# RAGonGCP Constitution

The non-negotiable principles every change, spec, plan, and AI agent must honor.
These are stronger than convenience: a plan or task that violates a principle is
wrong and must be revised (or must motivate an ADR that amends this document).

## Article I — Backend-agnostic core

The application core (`domain/`, `pipeline/`) MUST NOT import any vendor SDK.
Cloud-specific code lives only in `adapters/` and `generation/`, selected at
runtime by `adapters/factory.py`. New backends implement the `domain/` ports;
they do not change the core. (See [ADR-0001](../../docs/adr/0001-ports-and-adapters-architecture.md).)

## Article II — Config over code

A new use case is a new `config/<profile>.yaml`, never a core code edit. Anything
an operator might change per deployment lives in YAML or `RAGONGCP_*` env vars —
never hardcoded. (See [ADR-0005](../../docs/adr/0005-config-driven-use-case-profiles.md).)

## Article III — Offline-first and tested

The full pipeline and API MUST run and be unit-tested with no GCP credentials via
the `fake` backend and `echo` generator. Every behavior change ships with tests.
`make lint` and `make test` MUST pass before a change is considered done.

## Article IV — Grounded, cited answers

Generators answer ONLY from retrieved context and MUST surface inline `[n]`
citations mapped to source chunks. They MUST NOT fabricate sources. When context
is insufficient, the correct answer is "I don't know."

## Article V — Security and least privilege

No secrets in source. External fetching is allowlisted (see the web source).
IAM grants are least-privilege and scoped (bucket-level, not project-wide, where
possible). New external surfaces require a security note and, if significant, an
ADR.

## Article VI — Decisions are recorded

Architecturally significant decisions get an ADR (see [docs/adr/](../../docs/adr/README.md)).
Non-trivial features start from a spec (`/specify`) before a plan or code.
Accepted ADRs are immutable; change them by superseding.

## Article VII — Simplicity and small steps

Prefer the smallest change that satisfies the spec. Favor small, composable
functions, explicit types, and concise docstrings where intent isn't obvious.
PRs stay focused and reviewable.

---

*Amendments to this constitution are made via an ADR that supersedes the
relevant article, and a corresponding edit here referencing that ADR.*
