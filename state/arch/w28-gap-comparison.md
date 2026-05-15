---
artifact_type: GAP_COMPARISON
id: w28-gap-comparison
status: ACCEPTED
created_at: 2026-05-15
intake_id: intake-008
decision_id: D-028
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: INFORMED_ESTIMATE
---

# W28 Gap Comparison — AP (intake-007) vs RE (intake-008)

## Classification Rule (binding)

A gap is **systemic** if it manifests in >=2 domains with equivalent structural impact.
Otherwise, classify as **domain-specific**.

## Comparison Matrix (GAP-001..007)

| gap_id | AP evidence (intake-007) | RE evidence (intake-008) | Equivalent structural impact in both domains? | Classification |
|---|---|---|---|---|
| GAP-001 | AP artifacts cannot cross into machine-queryable atom CRUD/query via current contract boundary. | RE process/decision artifacts also remain markdown-only without contract-level atom CRUD/query. | YES | **systemic** |
| GAP-002 | AP dependency graphs are representable but non-traversable programmatically. | RE process handoffs are representable but non-traversable programmatically. | YES | **systemic** |
| GAP-003 | AP-06 evidence chain exceeds DecisionRecord first-class shape. | RE-06 long-horizon thesis/evidence/outcome chain exceeds DecisionRecord first-class shape. | YES | **systemic** |
| GAP-004 | AP formulation version chains are narrative; no first-class lineage traversal. | RE investment thesis evolution similarly relies on narrative supersession without lineage traversal. | YES | **systemic** |
| GAP-005 | AP-specific atoms lack formal extension typing model. | RE process/investment entities also lack formal extension typing model. | YES | **systemic** |
| GAP-006 | AP regulatory freshness lacks automated staleness monitoring. | RE evidence run did not require a comparable regulatory-currency freshness loop for RE-01/RE-06 core proof. | NO | **domain-specific** (AP-oriented in current scope) |
| GAP-007 | ADR-0010 MEDIUM decay mismatch affects AP confidence semantics. | Same policy/runtime mismatch would apply to RE medium-confidence longitudinal claims. | YES | **systemic** |

## Per-Gap Evidence Notes

### GAP-001 — systemic

- AP source: `state/arch/intake-007-gap-register.md` (GAP-001 card)
- RE source: `state/arch/intake-008-fit-assessment.md` (machine-query limit rows)

### GAP-002 — systemic

- AP source: `state/arch/intake-007-ap01-mini-graph.md` + gap register
- RE source: `state/arch/intake-008-re01-process-inventory.md` (handoff limits)

### GAP-003 — systemic

- AP source: `state/arch/intake-007-ap06-proof.md` + gap register
- RE source: `state/arch/intake-008-re06-decision-proof.md` (data richness limit)

### GAP-004 — systemic

- AP source: `state/arch/intake-007-ap02-mini-version-chain.md`
- RE source: `state/arch/intake-008-re06-decision-proof.md` (thesis evolution limit)

### GAP-005 — systemic

- AP source: `state/arch/intake-007-fit-assessment.md`
- RE source: `state/arch/intake-008-fit-assessment.md` + RE-01/RE-06 entity conventions

### GAP-006 — domain-specific (current evidence)

- AP source: explicit regulatory freshness need in AP-01 evidence
- RE source: W28 anchors (RE-01 process inventory, RE-06 decision tracking) did not surface an equivalent automated freshness requirement with the same structural urgency in this cycle.

### GAP-007 — systemic

- AP source: gap register mismatch note (MEDIUM 90d vs 180d baseline)
- RE source: RE-06 medium-confidence projection semantics would inherit same mismatch.

## Classification Outcome Summary

- **Systemic:** GAP-001, GAP-002, GAP-003, GAP-004, GAP-005, GAP-007 (6/7)
- **Domain-specific:** GAP-006 (1/7, AP-oriented in current W28 scope)

## Prioritization Implications

1. **Priority increase (cross-domain pressure):** K3, W19, W20, K9a/K9, ADR-0010 maintenance.
2. **Keep as scoped domain/feature precursor:** GAP-006 remains tied to freshness monitoring tracks (K12/PK-04 area per roadmap note).
3. **Roadmap interpretation:** W28 materially strengthens R10/R11/R12 risk urgency as systemic rather than AP-isolated.
