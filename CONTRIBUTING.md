# Contributing to RAGonGCP

Thanks for your interest in improving this project.

## Development setup

```bash
make setup
make lint
make test
```

Run the app locally:

```bash
make run
```

## Branching and pull requests

- Create a feature branch from `main`.
- Keep PRs focused and reviewable.
- Include context in the PR description: what changed and why.
- Add or update tests for behavior changes.
- Ensure `make lint` and `make test` pass before requesting review.

## Coding guidelines

- Prefer small, composable functions and explicit types.
- Keep domain logic independent from concrete backend SDKs.
- Add concise docstrings where behavior or intent is not obvious.
- Keep configuration in `config/*.yaml` or environment variables, not hardcoded.

## Architecture expectations

This repository follows a ports-and-adapters style:

- `domain/` defines contracts (`Retriever`, `Ingestor`, `Generator`)
- `pipeline/` orchestrates use-case flow
- `adapters/` provide backend-specific implementations

New backend implementations should plug into `adapters/factory.py` and satisfy
the relevant domain interfaces. The binding principles live in the
[project constitution](.specify/memory/constitution.md).

## Decision records and specs

- **Significant decisions** (architecture, dependencies, interfaces, security)
  are recorded as [ADRs](docs/adr/README.md). Propose one via `/adr <title>` or
  by copying `docs/adr/template.md`. Accepted ADRs are immutable — supersede them
  rather than editing.
- **Non-trivial features** start from a spec, not code. Follow
  `/specify → /plan → /tasks → /implement` (see [specs/](specs/README.md)).
  Small fixes don't need a spec.
- If a PR introduces or changes a significant decision, include or link the ADR.

## Commit style

Use clear commit messages that explain motivation and scope.

Examples:

- `add cloud run deployment guide`
- `fix web source allowlist validation`
- `improve eval harness summary output`

## Reporting bugs and feature requests

- Open an issue with repro steps, expected behavior, and actual behavior.
- For security-sensitive issues, follow `SECURITY.md` instead of public issues.
