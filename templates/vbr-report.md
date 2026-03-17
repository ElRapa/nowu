---
# VBR Report
id: <task-id>-vbr
task_id: task-NNN
created: YYYY-MM-DD
status: READY_FOR_REVIEW | CHANGES_REQUESTED
---

## Checks
| Check | Status | Notes |
|-------|--------|-------|
| pytest | PASS/FAIL | N tests, N failed |
| mypy --strict | PASS/FAIL | N errors |
| ruff check | PASS/FAIL | N violations |
| scope check | PASS/FAIL | files in diff vs .active-scope |

## Raw Output Excerpts
<!-- Paste failure output here if any checks fail -->

## Handoff
```yaml
from_step: S7
to_step: S8
agent: nowu-reviewer
status: READY_FOR_REVIEW | CHANGES_REQUESTED
```
