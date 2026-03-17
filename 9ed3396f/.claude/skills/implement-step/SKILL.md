# Skill: Implement Step Loop (Mode B — S5→[S6-S7]×n→S8-S9)

Use when: tasks are already shaped and approved. You are executing known work.
Entry condition: one or more `state/tasks/task-<NNN>.md` files exist with
status = READY_FOR_IMPL.

## Steps

### 1. Read the active task queue
List all tasks in `state/tasks/` with status READY_FOR_IMPL.
Order by `depends_on` field (tasks with no deps first).

### 2. For each task (in order):

**S5 verification** — confirm the task spec is complete:
- `in_scope_files` is explicit (no wildcards)
- `validation_trace` covers all `use_case_ids`
- `estimated_hours` ≤ 4h
If incomplete: stop, invoke `nowu-shaper` to repair, wait for human re-approval.

**S6+S7 — Implement + VBR**:
Invoke `nowu-implementer` with the task spec path.
If VBR status = CHANGES_REQUESTED: fix and re-run VBR (max 3 retries, then escalate).
If VBR status = READY_FOR_REVIEW: proceed.

**S8 — Review**:
Invoke `nowu-reviewer` with VBR + task spec paths.
If verdict = CHANGES_REQUESTED: return to S6 (max 2 retries, then escalate Tier 2).
If verdict = APPROVED: proceed.

**S9 — Capture**:
Invoke `nowu-curator` with review report path.

### 3. After all tasks complete
Report to human:
- Tasks completed (with UC-NNN coverage)
- Decisions recorded (if any)
- Suggested next step (next task, next feature, or ready for phase review)
