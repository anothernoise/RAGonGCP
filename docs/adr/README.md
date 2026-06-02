# Architecture Decision Records (ADRs)

An **Architecture Decision Record** captures a single architecturally significant
decision: its context, the decision itself, and its consequences. Together the
ADRs form a **decision log** — the project's history of *why* it is built the way
it is. This process follows the
[AWS Prescriptive Guidance ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
and the [MADR](https://adr.github.io/madr/) template style.

> An ADR explains **why**, not how. Understanding the reason behind a decision
> makes it easier to adopt — and prevents people who weren't in the room from
> silently overruling it later.

## When to write an ADR

Create an ADR for any decision that affects ([Richards & Ford, 2020](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/)):

- **Structure** — patterns and boundaries (e.g. ports-and-adapters).
- **Non-functional requirements** — security, availability, cost, latency.
- **Dependencies** — coupling to a cloud service, SDK, or framework.
- **Interfaces** — public APIs and contracts.
- **Construction** — libraries, tools, and processes (e.g. IaC choice).

If a code reviewer would reasonably ask "why was it done this way?", it deserves
an ADR.

## Lifecycle

ADRs have states and follow a lifecycle:

```
Proposed ──▶ Accepted ──▶ Superseded (by ADR-NNNN)
   │                └────▶ Deprecated
   └──▶ Rejected
```

- **Proposed** — drafted and ready for review.
- **Accepted** — approved by the team. **Once accepted, an ADR is immutable.**
- **Rejected** — not adopted; the ADR records *why*, to prevent re-litigation.
- **Superseded** — replaced by a newer ADR (link it). The original is kept.
- **Deprecated** — no longer relevant, but not directly replaced.

To change an accepted decision you do **not** edit the old ADR — you write a new
one and mark the old one `Superseded by ADR-NNNN`.

## Ownership & review

- Anyone may author an ADR; the author is its **owner** and maintains it.
- The owner opens it in **Proposed** state via a pull request.
- Reviewers spend ~10–15 min reading, then comment. The owner addresses
  comments. The team decides: **Accept**, **rework** (stays Proposed), or
  **Reject**.
- On acceptance, the owner fills in the date, version, and stakeholders and
  flips the status to **Accepted** in the same or a follow-up PR.
- ADRs are consulted during code and design review; a change that violates an
  accepted ADR should be revised or motivate a superseding ADR.

## Conventions

- One file per ADR: `docs/adr/NNNN-kebab-case-title.md` (zero-padded, monotonic).
- Start from [`template.md`](template.md).
- Keep the title imperative and specific (the decision, not the topic).
- `0001` is the first real decision; never reuse or renumber.

## Creating one

Run the Claude Code command [`/adr <title>`](../../.claude/commands/adr.md), or
copy `template.md` to the next number by hand.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-ports-and-adapters-architecture.md) | Ports-and-adapters architecture for backend pluggability | Accepted |
| [0002](0002-vertex-ai-rag-engine-default-backend.md) | Vertex AI RAG Engine as the default retrieval backend | Accepted |
| [0003](0003-fastapi-as-service-interface.md) | FastAPI as the service interface | Accepted |
| [0004](0004-terraform-for-infrastructure.md) | Terraform for infrastructure as code | Accepted |
| [0005](0005-config-driven-use-case-profiles.md) | Config-driven use-case profiles (layered YAML) | Accepted |
| [0006](0006-adopt-adr-and-spec-driven-development.md) | Adopt ADRs and spec-driven development | Accepted |
| [0007](0007-establish-cost-tracking-and-finops-guardrails.md) | Establish cost tracking and FinOps guardrails | Proposed |
| [0008](0008-adopt-chainlit-for-demo-chat-ui.md) | Adopt Chainlit for demo chat UI | Proposed |
