# ADR-0006: Adopt ADRs and spec-driven development

- **Status:** Accepted
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, contributors, AI coding agents
- **Version:** 1

## Context

RAGonGCP is open source and developed substantially with AI coding agents. Two
recurring problems need a process: (1) architectural decisions were implicit in
code and undocumented, making reuse and review harder; and (2) AI agents execute
unreliably when intent is implicit — "language models are exceptional at pattern
completion, but not at mind reading." We want a repeatable way to capture *why*
and to specify *what* before *how*.

## Decision

We will adopt two complementary, lightweight processes:

1. **Architecture Decision Records** ([docs/adr/](README.md)) following the AWS
   Prescriptive Guidance lifecycle (Proposed → Accepted/Rejected → Superseded/
   Deprecated; accepted ADRs are immutable). Significant decisions get an ADR.
2. **Spec-driven development** following the GitHub Spec Kit flow: a project
   **constitution** (`.specify/memory/constitution.md`) plus a per-feature
   `/specify → /plan → /tasks → /implement` workflow producing `spec.md`,
   `plan.md`, and `tasks.md` under `specs/NNNN-feature/`. Claude Code slash
   commands in `.claude/commands/` drive the flow, and `CLAUDE.md` captures
   agent working conventions.

## Consequences

- **Positive:** Decisions are discoverable and durable; features start from
  reviewable intent; AI agents have explicit, enforceable context, reducing
  rework. Stable "what" is separated from flexible "how".
- **Negative / trade-offs:** Process overhead for small changes — mitigated by
  scoping ADRs to *significant* decisions and specs to non-trivial features.
- **Risks & mitigations:** Specs/ADRs going stale — the constitution makes
  keeping them current part of the definition of done, and PR review checks it.
- **Follow-ups:** Backfilled ADRs 0001–0005 document existing decisions.

## Alternatives considered

- **Wiki / external docs** — drifts from code and is easy to skip; in-repo,
  PR-reviewed ADRs stay close to the change.
- **Ad-hoc prompting without specs** — the status quo that produces the
  mind-reading failures this ADR addresses.
