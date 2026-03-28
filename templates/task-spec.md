---
id: task-NNN
title: [title]
created: YYYY-MM-DD
status: READY_FOR_IMPL | IN_PROGRESS | DONE | BLOCKED
decision_id: D-NNN
intake_id: intake-NNN
story_id: story-NNN-001
estimated_hours: N  # must be <= 4
primary_module: core | flow | bridge | soul | know
depends_on: []  # other task IDs, if any
use_case_ids:
  - UC-NNN
---

# Task Spec: task-NNN

## In-Scope Files

<!-- Explicit paths only — no wildcards, no directories -->

- src/nowu/module/file.py
- tests/unit/module/test_file.py

## Out of Scope

<!-- What must NOT be touched — be explicit -->

- Everything not listed above
- [any specific file that might seem related but is excluded]

## Acceptance Criteria

- id: AC-1  
  description: [what must be true — behavior, not implementation]  
  test_function_name: test_unit_scenario_expected

- id: AC-2  
  description: [what must be true]  
  test_function_name: test_unit_scenario_expected

## Test Strategy (TDD order)

1. Write `test_unit_scenario_expected` — confirm RED
2. Implement minimal code — confirm GREEN
3. Refactor — confirm still GREEN

## Validation Trace

```yaml
validation_trace:
  - use_case: UC-NNN
    criteria: [AC-1, AC-2]
    rationale: "AC-1 tests X, AC-2 tests Y — UC-NNN is fully covered"
```


---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```