# Specs — spec-driven development

This project uses **spec-driven development** (the
[GitHub Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
flow): write the intent down first so humans and AI agents build the intended
thing instead of guessing. The stable **what** (spec) is separated from the
flexible **how** (plan), which keeps us free to change implementation without
re-deciding intent.

## Workflow

```
constitution  ──►  /specify  ──►  /plan  ──►  /tasks  ──►  /implement
(principles)       spec.md        plan.md      tasks.md      code + tests
```

1. **Constitution** — `.specify/memory/constitution.md` holds the project's
   non-negotiable principles. Every phase must comply with it.
2. **`/specify <description>`** — creates `specs/NNNN-slug/spec.md`: user
   journeys, testable requirements, success criteria. No tech, no file names.
3. **`/plan`** — creates `plan.md`: the technical approach, affected files, a
   constitution check, testing strategy, and whether a new ADR is needed.
4. **`/tasks`** — creates `tasks.md`: small, ordered, test-first work items.
5. **`/implement`** — executes the tasks, test-first, keeping `make lint test`
   green and updating docs/ADRs as needed.

The slash commands live in [`.claude/commands/`](../.claude/commands/) and the
templates in [`.specify/templates/`](../.specify/templates/).

## Relationship to ADRs

Specs capture **what to build** for a feature; [ADRs](../docs/adr/README.md)
capture **why we made a significant decision**. A plan flags when a feature needs
a new ADR; `/implement` creates it before coding.

## Layout

```
specs/
  README.md
  NNNN-feature-slug/
    spec.md     # /specify  — the what & why
    plan.md     # /plan     — the how
    tasks.md    # /tasks    — the steps
```

## Example

[`0001-vertex-search-backend/`](0001-vertex-search-backend/) is a worked spec for
implementing the `vertex_search` adapter (currently a stub). It shows the format
`/specify` produces; run `/plan` and `/tasks` on it to continue the flow.
