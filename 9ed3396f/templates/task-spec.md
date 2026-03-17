---
# Task Spec
id: task-NNN
title: ...
created: YYYY-MM-DD
status: READY_FOR_IMPL | IN_PROGRESS | DONE | BLOCKED
decision_id: D-NNN
intake_id: intake-<YYYY-MM-DD>-<slug>
estimated_hours: N  # must be ≤4
primary_module: core | flow | bridge | soul | know
depends_on: []  # task IDs
use_case_ids: [UC-NNN]
---

## In-Scope Files
<!-- Explicit paths only — no wildcards -->
- src/nowu/<module>/<file>.py
- tests/unit/<module>/test_<file>.py

## Out-of-Scope
<!-- What must NOT be touched -->
- Everything not listed above

## Acceptance Criteria
- id: AC-1
  description: ...
  test_function_name: test_<unit>_<scenario>_<expected>
- id: AC-2
  description: ...
  test_function_name: test_<unit>_<scenario>_<expected>

## Test Strategy (TDD order)
1. Write `test_<unit>_<scenario>` — confirm RED
2. Implement minimal code — confirm GREEN
3. ...

## Validation Trace
```yaml
validation_trace:
  - use_case: UC-NNN
    criteria: [AC-1, AC-2]
    rationale: "AC-1 tests X, AC-2 tests Y → UC-NNN is covered"
```

## Handoff
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
