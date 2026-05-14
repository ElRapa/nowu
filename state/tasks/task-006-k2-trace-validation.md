---
id: task-006
title: K2 Forward/backward trace validation on intake-001
created: 2026-05-14
status: DONE
intake_id: none
story_id: none
estimated_hours: 2
primary_module: none
depends_on: []
use_case_ids:
  - NF-09
  - XP-08
work_item: K2
altitude: ARCHITECTURE
phase: VERIFICATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - docs/ROADMAP-003.md
---

# Task Spec: task-006 — K2 Forward/Backward Trace Validation

## Purpose

Validate end-to-end traceability on the first S1-S9 cycle (intake-001) by walking the
trace chain in both directions:

- **Forward:** GOAL → UC → Story → Intake → Task → Code → Test → VBR → Review → Capture
- **Backward:** Capture → Review → VBR → Task → Story → UC → GOAL

This is the last unchecked v1-core→v1 gate criterion in ROADMAP-003 §5.

## In-Scope Files (read-only — validation only, no edits)

- docs/goals/goal-001.md, goal-002.md
- docs/USE_CASES.md (NF-01, NF-02, NF-09, PK-03, XP-01)
- state/intake/intake-001.md
- state/arch/intake-001-constraints.md
- state/arch/intake-001-options.md
- state/tasks/task-001..005.md
- state/changes/task-001..005.md
- state/vbr/task-001..005.md
- state/reviews/review-intake-001.md
- state/capture/capture-intake-001.md
- src/nowu/core/contracts/types.py
- src/nowu/core/contracts/session.py
- src/nowu/flow/session_store.py
- src/nowu/flow/pipeline.py
- tests/ (relevant test files)

## Out of Scope

- Modifying any code or existing artifact content
- Creating new tests or implementations
- W20 (traceability metadata standard) — future work

## Acceptance Criteria

- id: AC-1
  description: Forward trace from each goal (goal-001..002) through UC(s) to intake-001 to task(s) to code to tests is documented
  test_function_name: N/A (manual validation)

- id: AC-2
  description: Backward trace from capture-intake-001.md back through review → VBR → tasks → intake → UCs → goals is documented
  test_function_name: N/A (manual validation)

- id: AC-3
  description: Every task's validation_trace field correctly maps to UC(s) and story ACs
  test_function_name: N/A (manual validation)

- id: AC-4
  description: Gaps or broken links in the trace chain are identified and documented
  test_function_name: N/A (manual validation)

- id: AC-5
  description: Findings written to state/arch/k2-trace-validation.md
  test_function_name: N/A (artifact existence check)

## Deliverable

`state/arch/k2-trace-validation.md` — structured report with:
1. Forward trace walkthrough (goal → capture)
2. Backward trace walkthrough (capture → goal)
3. Validation matrix (every task ↔ UC ↔ goal mapping)
4. Gap analysis (broken links, missing references)
5. Summary verdict (PASS/FAIL for v1-core→v1 gate)

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-09
    criteria: [AC-1, AC-2, AC-3, AC-4, AC-5]
    rationale: "NF-09 requires every deliverable to trace back to a UC. K2 validates this property on the first intake."
  - use_case: XP-08
    criteria: [AC-1, AC-2]
    rationale: "XP-08 requires portable project state export. Trace validation proves the artifact chain is internally consistent."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
