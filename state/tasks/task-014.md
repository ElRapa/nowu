---
artifact_type: TASK_SPEC
id: task-014
title: W28 RE evidence artifacts and fit assessment
created: 2026-05-15
status: DONE
decision_id: D-028
intake_id: intake-008
story_id: raw-intake
estimated_hours: 3
primary_module: none
depends_on: []
use_case_ids:
  - RE-01
  - RE-06
work_item: W28
altitude: DELIVERY
phase: EVALUATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - None
---

# Task Spec: task-014 — W28 RE evidence artifacts

## In-Scope Files

- state/arch/intake-008-fit-assessment.md
- state/arch/intake-008-re01-process-inventory.md
- state/arch/intake-008-re06-decision-proof.md

## Out of Scope

- src/nowu/**
- tests/**
- GAP classification artifact (task-015)

## Acceptance Criteria

- id: AC-1
  description: A fit-assessment maps RE-01 and RE-06 evidence needs to existing contracts/schemas (DecisionRecord, TaskSpec, MemoryService) with explicit representability limits.
  test_function_name: test_w28_fit_assessment_maps_re_needs_and_limits

- id: AC-2
  description: RE-01 artifact contains a structured process inventory (steps, actors, handoffs, bottlenecks, digitalization-value notes) using current artifact conventions.
  test_function_name: test_w28_re01_inventory_contains_required_process_fields

- id: AC-3
  description: RE-06 artifact demonstrates one long-term investment decision trace (assumptions, options, chosen path, confidence, retrospective outcome link pattern) with explicit structural limits under current contracts.
  test_function_name: test_w28_re06_decision_proof_contains_long_horizon_trace_pattern

## Test Strategy (TDD order)

1. Draft AC checklists for AC-1/2/3 and confirm RED against empty artifacts.
2. Populate RE-01 and RE-06 artifacts to satisfy AC-2/3.
3. Build fit-assessment synthesis and confirm AC-1.
4. Re-run all checklist assertions to GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: RE-01
    story_ac: AC-001
    criteria: [AC-1, AC-2]
    rationale: "AC-2 proves process inventory representability; AC-1 anchors structural limits and contract fit."
  - use_case: RE-06
    story_ac: AC-001
    criteria: [AC-1, AC-3]
    rationale: "AC-3 proves decision trace representation; AC-1 records constraint fit and capability gaps."
```

---

```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: DONE
```
