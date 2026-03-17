---
# Change Set
id: <task-id>-changes
task_id: task-NNN
created: YYYY-MM-DD
status: READY_FOR_VBR
---

## Files Changed
| File | Change Type | Summary |
|------|-------------|---------|
| src/nowu/... | created/modified/deleted | ... |

## Acceptance Criteria Status
| AC | Test Function | Status |
|----|--------------|--------|
| AC-1 | test_... | PASS |

## Implementation Notes
<!-- Anything the reviewer should know about the approach -->

## Handoff
```yaml
from_step: S6
to_step: S7
agent: nowu-implementer (VBR phase)
status: READY_FOR_VBR
```
