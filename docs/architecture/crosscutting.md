# Crosscutting Concepts

> This document captures system-wide concerns that apply across many
> containers and features. These decisions are architectural and are
> not re-litigated in individual stories.

last_updated: YYYY-MM-DD  
owner: architecture

> **Human-curated.** Agents (S2, S3, S8) read this file but do not modify it.
> Updates are made at P3.6 when new architectural decisions are recorded,
> or when a binding crosscutting decision changes.

---

## Observability

**Goal:** Make it easy to understand system behavior in production and during development.

- **Logging**
  - Structured JSON logs.
  - Must always include: `timestamp`, `level`, `component`, `trace_id`,
    `span_id`, `tenant_id` (if applicable), and a human-readable message.
  - No sensitive data in logs (passwords, secrets, raw tokens).

- **Tracing**
  - Use a single tracing library (e.g. OpenTelemetry) in all services.
  - Every incoming request gets a `trace_id` propagated across services.

- **Metrics**
  - Export Prometheus-compatible metrics from every container.
  - Standard metrics: request count, error count, latency histograms, queue sizes.

**Relevant ADRs:** ADR-020 (observability stack)

---

## Authentication & Authorization

**Goal:** Ensure only the right actors can access resources, with correct tenant isolation.

- Authentication
  - JWT bearer tokens for external requests.
  - Short-lived access tokens, refresh via dedicated endpoint.
  - Tokens must contain `sub`, `tenant_id`, and relevant roles/claims.

- Authorization
  - All access checks use **role + tenant** information.
  - No direct SQL queries allowed without tenant scoping.

- Multi-tenancy
  - Tenant ID is always required on data reads/writes.
  - All queries must be tenant-filtered by default.

**Relevant ADRs:** ADR-010 (auth strategy), ADR-011 (multi-tenancy model)

---

## Error Handling

**Goal:** Fail gracefully and communicate clearly to both users and operators.

- At domain boundaries:
  - Use explicit result types (e.g. `Ok(value)` / `Err(error)`).

- At API boundaries:
  - Map domain errors to HTTP responses:
    - Validation → 400
    - Auth/authz → 401/403
    - Not found → 404
    - Internal/unexpected → 500 (with correlation IDs)

- Do **not** expose:
  - Stack traces
  - Internal IDs that could leak information
  - Raw database error messages

**Relevant ADRs:** ADR-012 (error handling)

---

## Configuration & Secrets

**Goal:** Keep configuration flexible, secrets safe, deployments reproducible.

- Configuration:
  - Environment variables are the primary config mechanism (12-factor style).
  - No environment-specific logic in code; use env vars or config files.

- Secrets:
  - Never stored in git.
  - Loaded from environment or secret management system at startup.

**Relevant ADRs:** ADR-013 (config and secrets)

---

## Testing Strategy (Architecture Level)

**Goal:** Ensure that the system is verifiable and remains changeable.

- Unit Tests:
  - For pure logic within a single module.
  - No network or file system IO.

- Integration Tests:
  - For interactions with external systems (DB, queues, third-party APIs).
  - Prefer ephemeral resources (e.g. test containers, in-memory DB).

- End-to-End Tests:
  - For a small set of critical flows only.
  - Simulate real user actions through the external API or UI.

**Relevant ADRs:** ADR-014 (testing pyramid)

---

## Other Crosscutting Concerns

Add more sections as they become relevant, e.g.:

- Caching
- API versioning
- Feature flags
- Data retention and GDPR