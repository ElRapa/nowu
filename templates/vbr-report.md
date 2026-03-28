---
id: vbr-task-NNN
task_id: task-NNN
created: YYYY-MM-DD
status: PASS | FAIL
---

# VBR Report: task-NNN

## Gate Results

| Gate | Command | Result | Details |
|---|---|---|---|
| Tests | `pytest --tb=short -q` | PASS/FAIL | [detail if FAIL] |
| Types | `mypy src --strict` | PASS/FAIL | [detail if FAIL] |
| Lint | `ruff check .` | PASS/FAIL | [detail if FAIL] |
| Scope | `git diff --name-only HEAD` | PASS/FAIL | [files outside in_scope if FAIL] |

## Overall: PASS / FAIL

[If FAIL: list specific issues and which AC or file they relate to]

---
```yaml
from_step: S7
to_step: S8
agent: nowu-reviewer
status: READY_FOR_REVIEW
```
