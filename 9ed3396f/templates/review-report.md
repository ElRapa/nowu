---
# Review Report
id: <task-id>-review
task_id: task-NNN
reviewed: YYYY-MM-DD
verdict: APPROVED | CHANGES_REQUESTED
---

## Verification Checklist ("built it right")
- [ ] No architecture boundary violations
- [ ] Only in_scope_files modified
- [ ] Tests written before implementation (git log)
- [ ] Every AC-N has a passing named test
- [ ] mypy clean (from VBR)
- [ ] ruff clean (from VBR)
- [ ] Changes follow D-NNN constraints

## Validation Checklist ("built the right thing")
- [ ] task.decision_id → D-NNN exists + ACCEPTED
- [ ] D-NNN.intake_id → intake file exists
- [ ] intake.use_case_ids → all UC-NNN exist
- [ ] Every UC-NNN in validation_trace has ≥1 passing AC-N
- [ ] No orphan work (nothing outside trace chain)
- [ ] Passing tests actually prove the use case is solved

## Critical Issues (must fix)
<!-- Empty = none -->

## Warnings (should fix)
<!-- Empty = none -->

## Lessons (for S9 capture)
<!-- Patterns to remember, things that went well, things to avoid -->

## Handoff
```yaml
from_step: S8
to_step: S9
agent: nowu-curator
verdict: APPROVED | CHANGES_REQUESTED
status: READY_FOR_CAPTURE | CHANGES_REQUESTED
```
