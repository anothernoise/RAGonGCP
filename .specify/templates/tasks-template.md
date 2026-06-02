# Tasks: <feature name>

- **Feature ID:** NNNN-kebab-slug
- **Plan:** [plan.md](plan.md)
- **Date:** YYYY-MM-DD

> Small, ordered, independently testable steps. Prefer test-first. Each task
> names the files it touches and its acceptance check. Keep tasks to roughly one
> commit each.

| # | Task | Files | Acceptance check | Done |
|---|------|-------|------------------|------|
| 1 | Write failing test for FR-1 | `tests/…` | test exists and fails for the right reason | [ ] |
| 2 | Implement FR-1 | `src/ragongcp/…` | test 1 passes; `make lint test` green | [ ] |
| 3 | … | … | … | [ ] |

## Definition of done

- [ ] All tasks checked; every FR/NFR in the spec is covered by a test.
- [ ] `make lint` and `make test` pass.
- [ ] Docs updated (README/architecture) if behavior or surface changed.
- [ ] New significant decisions captured as ADRs.
