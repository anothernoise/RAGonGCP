---
description: Create a feature specification (the what & why) from a description
argument-hint: <feature description>
allowed-tools: Read, Write, Bash(ls:*), Glob
---

You are running the **/specify** phase of spec-driven development for RAGonGCP.

Feature description: $ARGUMENTS

Steps:
1. Read `.specify/memory/constitution.md` and `.specify/templates/spec-template.md`.
2. Determine the next feature number by listing `specs/` (zero-padded, monotonic),
   pick a short kebab slug, and create `specs/NNNN-slug/spec.md` from the template.
3. Fill it in describing only the **what** and **why** — user journeys, numbered
   testable requirements (FR-/NFR-), out-of-scope, and measurable success criteria.
   Do NOT include tech stack, file names, or APIs.
4. For anything you cannot determine from the description, insert an explicit
   `[NEEDS CLARIFICATION: …]` marker instead of guessing.
5. Print the path written and the list of clarification markers. Stop — do not
   plan or write code. Next step is `/plan`.
