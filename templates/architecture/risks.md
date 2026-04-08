# Architecture Risk Register

> This document tracks known architectural risks, their impact,
> and how they are mitigated or accepted.

last_updated: YYYY-MM-DD  
owner: architecture

---

## Risk Table

| ID    | Description                                      | Affected QAs                | Prob. | Impact | Mitigation                         | Status     |
|-------|--------------------------------------------------|-----------------------------|-------|--------|-------------------------------------|-----------|
| R-001 | Single primary DB may become a bottleneck        | QAS-001 (perf), QAS-004     | MED   | HIGH   | Add read replica, caching, sharding | MITIGATED |
| R-002 | JWT secret rotation could log out all users      | QAS-002 (security, usability)| LOW | HIGH   | Key rotation strategy, versioned JWT| ACCEPTED  |
| R-003 | External API rate limit during batch operations  | QAS-001 (perf)             | HIGH  | MED    | Rate limiting, backoff queue        | OPEN      |

> Status: OPEN | MITIGATED | ACCEPTED | DEPRECATED

---

## Risk Details

### R-001 — DB bottleneck

**Description:** A single primary DB might not handle future load.

**Affected QA Scenarios:** QAS-001, QAS-004  
**Probability:** MEDIUM  
**Impact:** HIGH  

**Mitigation:**

- Add a read replica for heavy read workloads.
- Introduce a caching layer for hot paths.

**Status:** MITIGATED  
**Related ADRs:** ADR-00X (DB strategy), ADR-00Y (caching)

---

### R-002 — JWT secret rotation side effects

**Description:** Rotating JWT secrets could invalidate all sessions.

**Affected QA Scenarios:** QAS-002 (Security), QAS-XXX (Usability)  
**Probability:** LOW  
**Impact:** HIGH  

**Mitigation:**

- Versioned signing keys in tokens.
- Graceful rotation window.

**Status:** ACCEPTED (with documented mitigation)  
**Related ADRs:** ADR-010 (auth strategy)

---

## Notes

- New risks should be added here when:
  - Identified in ATAM-lite evaluation (`state/arch/NNN-atam-lite.md`), or
  - Arise from incidents or surprising behavior in S9 captures.
- When a risk is mitigated or accepted, update the table and details section.
- **Who updates this file:**
  - S9 (curator) promotes HIGH-probability or HIGH-impact OPEN risks from
    `NNN-atam-lite.md` after each implementation cycle.
  - Humans promote risks at P3.6 or after incidents.
  - `atam-lite`, `qa-elicitation`, and other automated agents do **not** write
    to this file — they write findings to `state/arch/` only.