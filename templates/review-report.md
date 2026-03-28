***
id: review-task-NNN
task_id: task-NNN
story_id: story-NNN-001
created: YYYY-MM-DD
status: APPROVED | CHANGES_REQUESTED | BLOCKED
***

# Review Report: task-NNN

## Verification (built it right?)

| Check | Result | Notes |
|---|---|---|
| Every AC has matching test function | PASS/FAIL | |
| All VBR gates PASS | PASS/FAIL | |
| Only in_scope_files modified | PASS/FAIL | |
| Architecture rules respected | PASS/FAIL | |
| Type annotations present | PASS/FAIL | |

## Validation (built the right thing?)

| Check | Result | Notes |
|---|---|---|
| Each AC tests observable behavior (not just “code runs”) | PASS/FAIL | |
| Each UC-NNN in validation_trace is covered by ≥1 AC | PASS/FAIL | |
| Story-level ACs covered across all tasks in this epic | PASS/FAIL | |
| Behavior matches original intake intent | PASS/FAIL | |
| No hidden scope additions | PASS/FAIL | |

## Status: APPROVED / CHANGES_REQUESTED / BLOCKED

[If CHANGES_REQUESTED: specific numbered list of required changes with file + line references]  
[If BLOCKED: what human decision is required before proceeding]

***
```yaml
from_step: S8
to_step: S9
agent: nowu-curator
status: APPROVED