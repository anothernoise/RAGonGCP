# Plan: <feature name>

- **Feature ID:** NNNN-kebab-slug
- **Spec:** [spec.md](spec.md)
- **Status:** Draft <!-- Draft | Ready -->
- **Date:** YYYY-MM-DD

> The technical **how**. Must satisfy every requirement in the spec and comply
> with the [constitution](../../.specify/memory/constitution.md). Reuse existing
> utilities; name concrete files.

## Constitution check

Confirm compliance (or justify a deviation that needs an ADR):

- Article I (backend-agnostic core): …
- Article II (config over code): …
- Article III (offline-first, tested): …
- Article IV (grounded/cited): …
- Article V (security/least privilege): …

## Approach

The chosen technical approach and why. Reference relevant ADRs; note if this
feature needs a **new ADR** (significant decision).

## Affected components

- `src/ragongcp/…` — what changes and why (name files; reuse existing functions).
- `config/…`, `infra/terraform/…`, `tests/…` as applicable.

## Data / control flow

How a request or ingestion flows through the change (brief).

## Testing strategy

- Unit tests (offline, `fake`/`echo`) covering each FR.
- Any eval/golden-set additions.

## Risks & rollback

Risks, mitigations, and how to back the change out.

## ADRs

- New ADR needed? <yes/no> — if yes, title + what it decides.
