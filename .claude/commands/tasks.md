---
description: Break the plan into small, testable, ordered tasks
argument-hint: [feature-id, defaults to newest spec]
allowed-tools: Read, Write, Bash(ls:*), Glob
---

You are running the **/tasks** phase of spec-driven development for RAGonGCP.

Target feature: $ARGUMENTS (if empty, use the highest-numbered folder in `specs/`).

Steps:
1. Read the feature's `spec.md`, `plan.md`, and `.specify/templates/tasks-template.md`.
2. Write `specs/NNNN-slug/tasks.md` from the template: an ordered list of small,
   independently testable tasks. Prefer **test-first** (a failing test task before
   its implementation task). Each task names the files it touches and an
   acceptance check. Roughly one commit per task.
3. Ensure every FR/NFR in the spec maps to at least one task, and complete the
   definition-of-done checklist section.
4. Print the path written and the task count. Stop — next step is `/implement`.
