---
artifact_type: TASK_SPEC
id: task-008
title: W29 Level 0 epistemic enforcement — grade field existence and validity
created: 2026-05-14
status: DONE
intake_id: none
story_id: none
estimated_hours: 2
primary_module: none
depends_on: []
use_case_ids:
  - NF-15
work_item: W29
altitude: ARCHITECTURE
phase: VERIFICATION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - docs/ROADMAP-003.md
---

# Task Spec: task-008 — W29 Level 0 Epistemic Enforcement

## Purpose

Implement automated Level 0 enforcement: every artifact with `artifact_type` frontmatter
must also have a valid `epistemic_grade` field. This is the syntax check layer from D-015.

## In-Scope Files

- tests/architecture/test_epistemic_enforcement.py (new)

## Out of Scope

- Level 1 semantic checks (W8)
- Modifying existing artifacts
- verify-artifact.py script from VERIFICATION-GUIDE (aspirational design)

## Acceptance Criteria

- id: AC-1
  description: Test scans all .md files in state/ that have `artifact_type` in YAML frontmatter
  test_function_name: test_all_typed_artifacts_have_epistemic_grade

- id: AC-2
  description: Test validates `epistemic_grade` value is one of the 5 valid grades (SPECULATION, HYPOTHESIS, INFORMED_ESTIMATE, EVIDENCE_BASED, VERIFIED_FACT)
  test_function_name: test_epistemic_grades_are_valid_values

- id: AC-3
  description: Test passes on current codebase (all existing artifacts already have valid grades from W5)
  test_function_name: (all tests GREEN)

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-15
    criteria: [AC-1, AC-2, AC-3]
    rationale: "NF-15 requires epistemic grades on all workflow outputs. Level 0 enforces field existence and value validity."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
