---
id: task-007
title: W32 Epistemic threshold calibration
created: 2026-05-14
status: DONE
intake_id: none
story_id: none
estimated_hours: 3
primary_module: none
depends_on: []
use_case_ids:
  - NF-15
  - NF-16
work_item: W32
altitude: ARCHITECTURE
phase: DECISION
epistemic_grade: HYPOTHESIS
docs_to_update:
  - docs/model/MODEL-REFERENCE.md
  - docs/ROADMAP-003.md
---

# Task Spec: task-007 — W32 Epistemic Threshold Calibration

## Purpose

Define the canonical threshold table for epistemic grade enforcement at each workflow
step and artifact type. This calibration bridges ADR-0010's default grades (theoretical)
with W4's actual grades (empirical), producing actionable thresholds that W8 will
consume for Level 1 advisory enforcement.

D-015 defines three enforcement levels:
- Level 0 (v1-core): Syntax check — grade field exists ✅ (validated by W5)
- Level 1 (v1): Advisory warnings when grade < minimum threshold ← **W32 defines these thresholds**
- Level 2 (v1.1): Blocking at gates if below aspirational threshold

## In-Scope Files

- docs/model/MODEL-REFERENCE.md (add §12.1 threshold table)
- docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md (read-only reference)
- docs/DECISIONS.md (read-only reference for D-015)
- state/arch/w32-epistemic-calibration.md (new — calibration report)
- All W4 state artifacts (read-only — grade extraction)

## Out of Scope

- Modifying any source code
- Implementing W8 enforcement logic
- Changing existing artifact grades
- W29 (NF-15 Level 0 enforcement implementation)

## Acceptance Criteria

- id: AC-1
  description: Calibration report exists at state/arch/w32-epistemic-calibration.md with actual vs expected grade comparison for all W4 artifacts
  test_function_name: N/A (artifact existence check)

- id: AC-2
  description: MODEL-REFERENCE §12.1 contains canonical threshold table with minimum (Level 1) and aspirational (Level 2) grades per artifact type and workflow step
  test_function_name: N/A (manual validation)

- id: AC-3
  description: Threshold table covers all artifact_types from §13.1 vocabulary that appear in S1-S9 flow
  test_function_name: N/A (manual validation)

- id: AC-4
  description: Propagation rules from ADR-0010 are reflected in threshold expectations for composite artifacts
  test_function_name: N/A (manual validation)

- id: AC-5
  description: Calibration document identifies any deviations between W4 actual grades and ADR-0010 defaults, with rationale for each
  test_function_name: N/A (manual validation)

## Deliverables

1. `state/arch/w32-epistemic-calibration.md` — calibration report:
   - W4 artifact grade inventory (actual vs ADR-0010 default)
   - Deviation analysis
   - Threshold recommendations (minimum + aspirational)
   - W8 input: actionable rules for Level 1 advisory

2. `docs/model/MODEL-REFERENCE.md` §12.1 — canonical threshold table

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-15
    criteria: [AC-1, AC-2, AC-3, AC-4, AC-5]
    rationale: "NF-15 requires epistemic grades on all workflow outputs. W32 calibrates what grades are expected where, enabling W8 enforcement."
  - use_case: NF-16
    criteria: [AC-2, AC-4]
    rationale: "NF-16 requires strategic drift detection. Threshold table enables detecting when artifact grades drift below expectations."
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
