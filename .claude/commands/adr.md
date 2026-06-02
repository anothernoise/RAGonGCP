---
description: Create a new Architecture Decision Record in Proposed state
argument-hint: <decision title>
allowed-tools: Read, Write, Edit, Bash(ls:*), Glob
---

You are creating a new **Architecture Decision Record** for RAGonGCP.

Decision title: $ARGUMENTS

Steps:
1. Read `docs/adr/README.md` (the process) and `docs/adr/template.md`.
2. Determine the next ADR number by listing `docs/adr/` (zero-padded, monotonic;
   ignore `template.md` and `README.md`).
3. Create `docs/adr/NNNN-kebab-title.md` from the template in **Proposed** state,
   filling Context / Decision / Consequences / Alternatives based on the title and
   what you can learn from the codebase and existing ADRs. Set today's date.
4. Add a row to the index table in `docs/adr/README.md`.
5. Print the path. Remind the user that the ADR is **Proposed** and becomes
   immutable once **Accepted** via review.
