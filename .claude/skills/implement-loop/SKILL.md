---
name: implement-loop
version: 2.1
mode: B
steps: S5-S6-S7-S8-S9
---

# Skill: Implement Loop (Mode B — S5→S9)

Use when: tasks are already shaped and approved (READY_FOR_IMPL) and you want to execute them to completion.

Entry condition:
- One or more `state/tasks/task-NNN.md` with `status = READY_FOR_IMPL`

Stop points:
- S8 review may request changes

## Orchestration Steps

### 1. Task Validation (S5 sanity)

For each candidate `task-NNN`:

- Ensure required fields are present:
  - `in_scope_files`
  - `acceptance_criteria`
  - `validation_trace`
- If any are missing or unclear: STOP and fix the task spec before proceeding.

### 2. Implementation + VBR (S6+S7)

For each `task-NNN` with `status = READY_FOR_IMPL` (respecting `depends_on`):

Invoke: `nowu-implementer`  
Input:
- `state/tasks/task-NNN.md`

Agent does:
- TDD implementation
- Runs VBR (tests, types, lint, scope)

Outputs:
- `state/changes/changes-task-NNN.md`
- `state/vbr/vbr-task-NNN.md`

Loop until:
- `vbr.status = PASS`

Proceed when:
- `vbr.status = PASS` for this task

### 3. Review (S8)

Invoke: `nowu-reviewer`  
Input:
- `state/vbr/vbr-task-NNN.md`
- `state/changes/changes-task-NNN.md`
- `state/tasks/task-NNN.md`

Output: `state/reviews/review-task-NNN.md` with `status = APPROVED | CHANGES_REQUESTED | BLOCKED`

If `CHANGES_REQUESTED`:
- Fix as per review comments
- Return to S6 for this task

Proceed when:
- `review.status = APPROVED`

### 4. Capture (S9)

Invoke: `nowu-curator`  
Input:
- `state/reviews/review-task-NNN.md`
- `docs/DECISIONS.md`
- `docs/PROGRESS.md`

Output:
- `state/capture/capture-task-NNN.md`
- Updated `docs/PROGRESS.md`
- Commit message suggestion
- `next_cycle_trigger`

Done when:
- `capture.status = DONE`

## Next Action After Completion

Use `next_cycle_trigger` as guidance:

- `CONTINUE`: pick next `READY_FOR_IMPL` task  
- `ARCH_PIVOT` / `PRODUCT_PIVOT`: hand back to pre-workflow (P3 or P1)  
- `COMPLETE`: no further tasks for this intake
