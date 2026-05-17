---
artifact_type: CONSTRAINTS_SHEET
id: intake-008-constraints
intake_id: intake-008
created_at: 2026-05-15
status: READY_FOR_OPTIONS
altitude: ARCHITECTURE
phase: ANALYSIS
epistemic_grade: HYPOTHESIS
arch_pass_ref: ~
source_work_item: W28
---

# Constraints Sheet: intake-008

## Affected Modules

| Module | Container (C4 L2) | Impact | Confidence |
|---|---|---|---|
| core | Core Contracts | query/fit validation only | HIGH |
| flow | Workflow Orchestrator | domain-agnostic validation target | HIGH |
| know | Knowledge Store (`../know`) | WATCH (no implementation in W28) | MED |

## Fixed Constraints (Binding)

| D-ID / ADR | Constraint |
|---|---|
| D-001 | Evidence must remain explicit, file-based, and inspectable in artifacts. |
| D-002 | Any cross-boundary behavior remains Protocol-mediated; no boundary bypass. |
| D-003 | Scope stays within existing module responsibilities; no new module semantics. |
| D-006 | `know` remains system-of-record target, but W28 is evidence, not integration. |
| D-013 | S1/S2 altitude discipline applies; architecture only after intake framing. |
| D-017 | Hypothesis-grade architecture is validated through intake evidence runs. |
| D-027 | Domain bootstrap evidence can be artifact-only with explicit gap boundaries. |
| ADR-0008 | Knowledge atom model is canonical reference surface for fit checks. |
| ADR-0010 | Epistemic-grade and decay semantics remain policy constraints (including GAP-007 context). |

## Flexible Constraints

- Artifact structure details for RE evidence can be adapted as long as traceability and scope constraints hold.
- RE examples may use narrative + tabular supplemental fields where base contracts are too narrow.
- Task decomposition may be one or multiple tasks (task-014..016) so long as each remains <=4h.

## Binding Contracts

| Contract | Constraint |
|---|---|
| `DecisionRecord` | Baseline for RE-06 decision representation exists, but may be structurally thin for full thesis/evidence chains. |
| `MemoryService` | Current surface remains limited for generic atom/relationship operations; W28 should evaluate, not implement. |
| `TaskSpec` | Scope must remain explicit and artifact-limited; no wildcard expansion into code work. |

## Architectural Risks

| Risk | Severity | Mitigation |
|---|---|---|
| RE evidence over-claims executable capability | HIGH | Keep claim boundary explicit: representability proof only. |
| GAP classification bias from AP anchoring | HIGH | Apply explicit per-gap AP vs RE evidence check before classification. |
| S1 architecture bleed contaminates problem framing | MED | Enforce D-SESS-01 guardrail: no architecture language in intake problem statement. |
| S2 blind spots due to bounded context | MED | Run explicit blindspot check section before finalizing S2 artifact. |

## Assumptions

| Assumption | validated |
|---|---|
| RE-01/RE-06 evidence can be represented without Python changes | false (to be validated in S6/S7 evidence artifacts) |
| W27 gaps are at least partly cross-domain | false (requires W28 comparison evidence) |
| Existing templates are sufficient for comparative gap classification | true |

## Blindspot Check (D-SESS-01 requirement)

1. **No runtime execution evidence:** W28 does not validate runtime behavior, only structural representability.
2. **No direct know integration execution:** cannot claim machine-query path viability beyond contract-level analysis.
3. **AP comparison dependency risk:** Misclassification possible if RE evidence is too shallow; mitigate with explicit per-gap AP/RE matrix in S6/S7 outputs.

## Open Questions for S3

1. Which option best balances RE representability evidence and rigorous GAP classification inside 8h?
2. How should RE-01 process inventory and RE-06 decision tracking artifacts be minimal yet comparable to W27 AP outputs?
3. What explicit evidence threshold defines “equivalent structural impact” for systemic gap classification?

## c4_l1_update_needed

false

## arch_pass_divergences

No pre-workflow arch-pass -- constraints derived cold.

---

```yaml
from_step: S2
to_step: S3
agent: nowu-options
status: READY_FOR_OPTIONS
```
