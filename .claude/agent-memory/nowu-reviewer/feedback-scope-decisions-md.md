---
name: out-of-scope-decisions-md
description: DECISIONS.md updates land outside all task scopes in multi-task intakes; this is expected workflow behavior, not scope creep
metadata:
  type: feedback
---

In intake-001, D-024 was added to `docs/DECISIONS.md` as part of the implementation
work. However, none of the 5 tasks declared `docs/DECISIONS.md` in `in_scope_files` or
`docs_to_update` (all tasks have `docs_to_update: None`).

**Why:** D-024 was authored at S4 (nowu-decider) and committed as part of the S4→S5
workflow transition. The decision record must exist before task specs reference it. By
the time S6-S7 runs, DECISIONS.md already has D-024. The diff at S8 review time shows
it as a modification because the prior commit added it.

**How to apply:** When `docs/DECISIONS.md` appears in the diff but is not in any task's
scope, check if:
1. The change adds a DECISION record referenced by task specs → expected, not scope creep
2. The change modifies an existing decision → flag as potential scope concern
3. The change is unrelated formatting → flag as W-2 (minor)

Do not fail the scope check for DECISIONS.md additions that are the decision records
authorizing the implementation. They are workflow artifacts from S4, not S6-S7.

Related: [[vbr-dependency-gap]], [[tdd-commit-order]]
