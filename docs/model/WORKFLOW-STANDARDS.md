# nowu Workflow Standards v1.1

**Version:** 1.1 (CORRECTED)  
**Date:** 2026-05-05  
**Status:** RATIFIED  
**Supersedes:** v1.0

---

## Changelog v1.0 → v1.1

### Fixed
1. **S1–S9 zigzag mapping** — Restored correct altitude descent (was flattened to EXECUTION)
2. **Phase restrictions removed** — Phases are cognitive modes, not altitude-locked
3. **Epistemic thresholds relaxed** — Tiered enforcement (advisory→blocking)

---

## 1. Altitude Discipline

### Rule 1.1: S1–S9 Zigzag Is the Model

S1–S9 is a controlled descent through altitudes:

| Step | Altitude | Phase |
|---|---|---|
| S1 | DELIVERY | IDEA |
| S2 | ARCHITECTURE | ANALYSIS |
| S3 | ARCHITECTURE | OPTIONS |
| S4 | ARCHITECTURE | DECISION |
| S5 | DELIVERY | EVALUATION |
| S6 | EXECUTION | IMPLEMENTATION |
| S7 | EXECUTION | VERIFICATION |
| S8 | EXECUTION | EVALUATION |
| S9 | EXECUTION→ALL | LEARN |

### Rule 1.2: Downward Flow (with LEARN Exception)
Information flows downward: STRATEGIC → PRODUCT → ARCHITECTURE → DELIVERY → EXECUTION

Exception: LEARN phase promotes insights upward after abstraction.

---

## 2. Phase Contracts

### Rule 2.1: Phases Are Cognitive Modes

Phases describe WHAT work you're doing, not WHERE you are.

| Phase | Occurs At | Examples |
|---|---|---|
| ANALYSIS | All altitudes | Market analysis, arch research, code review |
| DECISION | All altitudes | Goal approval, ADR approval, scope approval |
| IMPLEMENTATION | ARCH, DELIVERY, EXEC | Writing ADR, writing SHAPE, writing code |
| VERIFICATION | STRATEGIC, ARCH, DELIVERY, EXEC | Goal validation, QA scenarios, AC check, tests |
| LEARN | All altitudes | Capturing lessons anywhere, promoting upward |

SYNTHESIS is the only altitude-locked phase (ARCHITECTURE only).

### Rule 2.2: Required Phases
- DECISION: always required
- VERIFICATION: always required
- LEARN: always required
- SYNTHESIS: only at ARCHITECTURE, only when ≥2 approved UCs

### Rule 2.3: Human Gates
1. STRATEGIC/DECISION (approve goal)
2. PRODUCT/DECISION (approve UC)
3. ARCHITECTURE/DECISION (approve ADR)
4. DELIVERY/DECISION (approve shape)
5. EXECUTION/VERIFICATION (approve code)

---

## 3. Epistemic Grades (Tiered Thresholds)

| Altitude | Minimum at Creation | Advisory Threshold | Aspirational at Decision |
|---|---|---|---|
| STRATEGIC | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| ARCHITECTURE | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| PRODUCT | SPECULATION | HYPOTHESIS | INFORMED_ESTIMATE |
| DELIVERY | SPECULATION | HYPOTHESIS | HYPOTHESIS |
| EXECUTION | SPECULATION | HYPOTHESIS | HYPOTHESIS |

**Enforcement:**
- **Level 0-1 (v1-core):** Warn if below advisory, don't block
- **Level 2 (v1.0):** Block if below minimum
- **Level 3 (v1.1+):** Block at decision gates if below aspirational

---

## 4. SYNTHESIS Phase Rules

### Rule 4.1: Trigger
SYNTHESIS activates when ≥2 approved use cases exist with no linked ADRs.

### Rule 4.2: Scope
Operates on ALL approved UCs pending architectural work.

### Rule 4.3: Output
Groups UCs into themes, recommends ADRs per theme.

---

## 5. Security Integration

### Rule 5.1: Trigger
ARCHITECTURE/EVALUATION must include security review when ADR introduces:
- New data storage
- New external API
- PII/PHI/financial data
- New auth/authz logic

### Rule 5.2: Checklist
Address: Authentication, Authorization, Data at rest, Data in transit, Input validation, Secrets, Audit logging, Dependencies, Least privilege, Fail-secure.

---

## Appendix A: v1.0 → v1.1 Migration

If you applied v1.0:

1. **Re-classify S1-S9 artifacts:**
   - S1: EXECUTION → DELIVERY
   - S2-S4: EXECUTION → ARCHITECTURE
   - S5: EXECUTION → DELIVERY
   - S6-S8: remain EXECUTION

2. **Update agent definitions:**
   - Remove `altitude_applicability` restrictions on IMPLEMENTATION/VERIFICATION/LEARN
   - Add multi-altitude support per Rule 2.1 table

3. **Relax epistemic enforcement:**
   - Change from single threshold to tiered (advisory→blocking)
   - Allow HYPOTHESIS at STRATEGIC/ARCHITECTURE creation

---

**Status:** RATIFIED 2026-05-05 as v1.1, superseding v1.0.
