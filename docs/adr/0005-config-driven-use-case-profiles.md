# ADR-0005: Config-driven use-case profiles (layered YAML)

- **Status:** Accepted
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, downstream engagement teams
- **Version:** 1

## Context

The accelerator's core promise is that a new use case (a new client, a new
domain) should require configuration, not code changes. We need a single,
predictable mechanism to express per-use-case retrieval params, generation
prompts, and ingestion sources, while keeping deployment secrets separate.

## Decision

We will drive use cases with **layered YAML profiles**: `config/default.yaml`
holds base defaults and `config/<profile>.yaml` overlays use-case overrides,
deep-merged in `config.py`. Environment variables (`RAGONGCP_*`) carry
deployment/runtime settings and secrets. `RAGONGCP_PROFILE` selects the active
use case; `RAGONGCP_BACKEND` may override the backend (e.g. `fake` for offline).

## Consequences

- **Positive:** New use cases = a new YAML file (e.g. `bc_real_estate.yaml`);
  secrets stay out of source; the same image serves many profiles.
- **Negative / trade-offs:** Deep-merge semantics must be understood (lists
  replace, maps merge); validated via Pydantic models and unit tests.
- **Risks & mitigations:** Profile drift from schema — `ProfileConfig` validates
  on load and `test_config.py` covers inheritance/override behavior.
- **Follow-ups:** Per-profile secrets via Secret Manager is a future extension.

## Alternatives considered

- **One config file per environment** — duplicates shared defaults and drifts.
- **Pure environment variables** — unwieldy for nested retrieval/generation/
  ingestion structures and prompts.
