# Quality Attribute Scenarios Registry

## Registry Metadata

version: 1.0  
last_updated: YYYY-MM-DD  
owner: architecture

> **Human-curated.** Agents write QA scenarios to `state/arch/NNN-qa-scenarios.md`.
> Scenarios are promoted here by a human at P3.6 only.
> Automated agents must not edit this file.

## Scenario Index

| ID      | QA Axis          | Summary                                       | Priority | Status   |
|---------|------------------|-----------------------------------------------|----------|----------|
| QAS-001 | Performance      | p95 search latency < 300ms at 500 concurrent  | HIGH     | ACTIVE   |
| QAS-002 | Security         | No cross-tenant data exposure                 | HIGH     | ACTIVE   |
| QAS-003 | Maintainability  | Add new module by changing ≤ 3 existing files | MEDIUM   | ACTIVE   |

> Status: ACTIVE | DEPRECATED | SUPERSEDED

---

## Scenario Details

### QAS-001 — Search latency under load

**QA Axis:** Performance efficiency  
**Stimulus:** User submits a search query  
**Source:** Authenticated end user  
**Environment:** Peak load, 500 concurrent sessions, normal network conditions  
**Artifact:** API gateway + search service + data store  
**Response:** Results are returned without error  
**Measure:**  
- p95 latency ≤ 300ms  
- p99 latency ≤ 1s  
- error rate ≤ 0.1% during peak

**Addressed By:** ADR-00X (caching), ADR-00Y (DB indexing)  
**Validated In:** S8 for story-XXX-YYY (load test)

---

### QAS-002 — Tenant isolation

**QA Axis:** Security  
**Stimulus:** Any user request with a tenant identifier  
**Source:** Authenticated end user (or system integration)  
**Environment:** Normal and high load, including background jobs  
**Artifact:** All components that read or write tenant data  
**Response:** Only data for the tenant in the request is ever read or returned  
**Measure:**  
- 0 cross-tenant rows returned in any query  
- 0 cross-tenant rows written in any write operation  
- verified by periodic automated tests over anonymized logs

**Addressed By:** ADR-00A (multi-tenant strategy)  
**Validated In:** S8 for stories that touch data access

---

### QAS-003 — Ease of extension

**QA Axis:** Maintainability / Modifiability  
**Stimulus:** Need to add a new user-facing capability in an existing bounded context  
**Source:** Developer  
**Environment:** Normal development process  
**Artifact:** Codebase + architecture boundaries  
**Response:** New capability is added with minimal changes to existing code  
**Measure:**  
- ≤ 3 existing files modified (excluding configuration and tests)  
- ≤ 1 architectural boundary crossed  
- tests added or updated in the same context

**Addressed By:** ADR-00B (modularization strategy)  
**Validated In:** S9 review of recent change sets

---

## Notes

- New scenarios should be added here **only** after they are first drafted in
  `state/arch/NNN-qa-scenarios.md` and reviewed.
- Deprecated or superseded scenarios should be clearly marked and referenced
  from ADRs that changed them.