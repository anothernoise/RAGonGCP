---
description: Produce a technical plan for the current feature spec
argument-hint: [feature-id, defaults to newest spec]
allowed-tools: Read, Write, Edit, Bash(ls:*), Glob, Grep
---

You are running the **/plan** phase of spec-driven development for RAGonGCP.

Target feature: $ARGUMENTS (if empty, use the highest-numbered folder in `specs/`).

Steps:
1. Read the feature's `spec.md`, `.specify/memory/constitution.md`, and
   `.specify/templates/plan-template.md`. Skim `docs/adr/` for relevant decisions.
2. If the spec still has unresolved `[NEEDS CLARIFICATION]` markers, stop and ask
   the user to resolve them first.
3. Explore the codebase to ground the plan in real files and reusable utilities
   (use Grep/Glob/Read). Do not invent modules that exist already.
4. Write `specs/NNNN-slug/plan.md` from the template: complete the **constitution
   check** honestly, the approach, affected components (name real files), data/
   control flow, testing strategy, risks/rollback, and whether a **new ADR** is
   required (significant decision → yes).
5. Print the path written and any required ADRs. Stop — next step is `/tasks`.
