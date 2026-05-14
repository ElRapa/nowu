---
artifact_type: TASK_SPEC
id: task-009
title: W8 Level 1 advisory enforcement — grade minimum threshold checks
created: 2026-05-14
status: DONE
intake_id: none
story_id: none
estimated_hours: 3
primary_module: none
depends_on: [task-008]
use_case_ids:
  - NF-15
  - NF-02
work_item: W8
altitude: ARCHITECTURE
phase: VERIFICATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - docs/ROADMAP-003.md
---

# Task Spec: task-009 — W8 Level 1 Advisory Enforcement

## Purpose

Implement Level 1 advisory enforcement: check that each artifact's epistemic grade
meets the minimum threshold for its artifact_type, per W32 calibration table
(MODEL-REFERENCE §6 "Per-Artifact-Type Thresholds"). Advisory = test warns but does
not block (xfail or separate reporting).

## In-Scope Files

- tests/architecture/test_epistemic_enforcement.py (extend from W29)

## Out of Scope

- Level 2 blocking enforcement (W11, v1.1)
- Modifying existing artifact grades
- Runtime enforcement in pipeline code

## Acceptance Criteria

- id: AC-1
  description: Test checks each artifact's grade against W32 minimum threshold for its artifact_type
  test_function_name: test_artifact_grades_meet_minimum_threshold

- id: AC-2
  description: Test checks capture records inherit review grade (capture.grade >= review.grade)
  test_function_name: test_capture_inherits_review_grade

- id: AC-3
  description: Threshold table is defined as data in the test (matching MODEL-REFERENCE §6), not hardcoded per-file
  test_function_name: (structural requirement)

- id: AC-4
  description: All tests pass on current codebase (existing artifacts meet or exceed minimum thresholds)
  test_function_name: (all tests GREEN)

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-15
    criteria: [AC-1, AC-2, AC-3, AC-4]
    rationale: "NF-15 requires epistemic grades assigned and surfaced. Level 1 enforces minimum thresholds via advisory checks."
  - use_case: NF-02
    criteria: [AC-1, AC-3]
    rationale: "NF-02 requires structured architecture decisions. Grade threshold enforcement ensures decisions carry adequate confidence."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
