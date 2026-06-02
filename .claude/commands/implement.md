---
description: Implement the current feature's tasks, test-first, gates green
argument-hint: [feature-id, defaults to newest spec]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

You are running the **/implement** phase of spec-driven development for RAGonGCP.

Target feature: $ARGUMENTS (if empty, use the highest-numbered folder in `specs/`).

Steps:
1. Read the feature's `spec.md`, `plan.md`, `tasks.md`, and
   `.specify/memory/constitution.md`. Confirm no unresolved clarifications remain.
2. If `plan.md` says a new ADR is required, create it first via the ADR template
   (`docs/adr/template.md`) in **Proposed** state and reference it.
3. Work tasks **in order**. For each: write/adjust the test first, then the
   implementation, then run `make test` (and `make lint`). Check the task's box in
   `tasks.md` only when its acceptance check passes. Track progress with the todo
   list.
4. Honor the constitution at every step (backend-agnostic core, config-over-code,
   offline-first, grounded/cited, least privilege).
5. When all tasks are done: run `make lint` and `make test`, update README/
   architecture docs if the surface changed, set the spec status to `Implemented`,
   and summarize what changed. Do not commit unless asked.
