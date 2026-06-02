# ADR-0007: Establish cost tracking and FinOps guardrails

- **Status:** Proposed
- **Date:** 2026-06-02
- **Owner:** dmansh
- **Stakeholders:** Maintainers, platform owners, finance/FinOps stakeholders
- **Version:** 1

## Context

RAGonGCP is intended for real client engagements, where cost predictability and
attribution are non-functional requirements. The current repository defines core
architecture and deployment scaffolding, but does not yet establish a single,
project-wide cost tracking standard for AI usage (Vertex AI/Gemini), API serving
(Cloud Run), and ingestion/storage.

Without a shared cost design:

- cost ownership is unclear across profiles/teams/environments
- spend spikes are detected late
- per-query AI unit economics are hard to measure
- optimization discussions become ad hoc and non-repeatable

Google Cloud and FinOps guidance consistently recommends combining billing-system
truth (Cloud Billing exports) with workload telemetry, budgets/anomaly alerts,
and standardized allocation dimensions.

## Decision

We will adopt a two-layer cost tracking model for RAGonGCP:

1. **Billing truth layer** using Google Cloud Billing exports and native alerts.
2. **Workload attribution layer** using request-level telemetry for RAG flows.

### Recommended cost-tracking design

- **Canonical source of truth**
  - Enable Cloud Billing export to BigQuery (standard, detailed usage/resource,
    and pricing tables).
  - Build cost reporting from exported billing data, not from estimated app-side
    calculations alone.
- **Allocation dimensions**
  - Enforce consistent labels/tags (for example: `env`, `service`, `profile`,
    `team`, `cost_center`) across provisioned resources.
  - Use project/folder boundaries where stronger cost isolation is needed.
- **RAG request telemetry**
  - Record request-level usage signals (for example: model, token counts when
    available, latency, profile/backend, status, request identifier).
  - Store telemetry in BigQuery and join with billing exports for unit economics
    (for example cost per request, cost per 1k requests, cost by profile).
- **Guardrails**
  - Configure billing budgets and threshold alerts (including forecast-based).
  - Enable anomaly detection notifications.
  - Apply service-level spend controls where available (for example Cloud Run
    scaling limits and quota policies).
- **Operating cadence**
  - Review weekly cost KPIs and optimization actions.
  - Treat major changes to cost attribution or control policy as ADR-worthy.

## Consequences

- **Positive:** Cost visibility is standardized across deployments; teams can
  attribute spend and optimize with shared metrics; budget overruns are detected
  earlier.
- **Negative / trade-offs:** Additional operational overhead for labels, data
  pipelines, dashboards, and review routines.
- **Risks & mitigations:** Partial label coverage can reduce attribution quality;
  mitigate via label policy enforcement and periodic audits. Telemetry schema
  drift can reduce comparability; mitigate with versioned event schema.
- **Follow-ups:** Add implementation spec/tasks for telemetry schema, dashboard
  definitions, and Terraform-level budget/anomaly automation.

## Alternatives considered

- **Billing-only tracking (no workload telemetry)** — simpler to start, but
  insufficient for per-request AI economics and shared-resource attribution.
- **Telemetry-only tracking (no billing export truth)** — fast feedback, but not
  invoice-accurate and weak for finance reconciliation.
