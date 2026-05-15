---
artifact_type: TASK_SPEC
id: task-013
title: W27 gap register and claim-boundary synthesis
created: 2026-05-15
status: DONE
decision_id: D-027
intake_id: intake-007
story_id: raw-intake
estimated_hours: 1
primary_module: none
depends_on: [task-011, task-012]
use_case_ids:
  - AP-01
  - AP-02
  - AP-06
work_item: W27
altitude: DELIVERY
phase: EVALUATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - None
---

# Task Spec: task-013 — W27 gap register + claim boundary

## In-Scope Files

- state/arch/intake-007-gap-register.md

## Out of Scope

- src/nowu/**
- tests/**
- Revising already-produced AP-01/AP-02/AP-06 artifacts beyond trace references

## Acceptance Criteria

- id: AC-1
  description: Gap register contains structured entries with required fields (gap_id, affects_uc/ac, missing_capability, workaround, target_work_item, severity) and includes at least one gap each for AP-01, AP-02, and AP-06 evidence limits.
  test_function_name: test_gap_register_has_required_schema_and_uc_coverage

- id: AC-2
  description: A claim-boundary section clearly separates what W27 proved now versus what remains blocked, and maps each blocked claim to owning follow-on work item (K3, K9, K13, W19, W20).
  test_function_name: test_claim_boundary_separates_proven_vs_blocked_and_maps_owners

- id: AC-3
  description: The artifact includes explicit cross-references to AP-06, AP-01, and AP-02 proof artifacts and states that no src/tests changes were required for this evidence run.
  test_function_name: test_gap_register_links_all_w27_evidence_artifacts_and_no_code_change_constraint

## Test Strategy (TDD order)

1. Write `test_gap_register_has_required_schema_and_uc_coverage` checklist and confirm RED.
2. Write `test_claim_boundary_separates_proven_vs_blocked_and_maps_owners` checklist and confirm RED.
3. Populate gap rows and claim-boundary section; run AC-1/AC-2 checks to GREEN.
4. Add cross-references/no-code-change declaration; run `test_gap_register_links_all_w27_evidence_artifacts_and_no_code_change_constraint` to GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: AP-06
    story_ac: AC-001
    criteria: [AC-1, AC-2]
    rationale: "AC-1 captures decision-trace representation limits; AC-2 bounds proven AP-06 traceability versus blocked capabilities."
  - use_case: AP-01
    story_ac: AC-001
    criteria: [AC-1, AC-3]
    rationale: "AC-1 ensures AP-01 gaps are explicitly structured; AC-3 ties AP-01 mini graph evidence into W27 closure."
  - use_case: AP-02
    story_ac: AC-002
    criteria: [AC-1, AC-3]
    rationale: "AC-1 documents AP-02 missing capabilities and workarounds; AC-3 links AP-02 version-chain evidence and no-code constraint."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: DONE
```
