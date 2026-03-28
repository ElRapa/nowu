---
name: single-step
version: 2.1
mode: C
steps: S6-S7-S8-S9
---

# Skill: Single Step (Mode C — S6→S9)

Use when: making a small change (bugfix, refactor, doc update) where you either
already have a tiny task spec or can write one quickly.

Entry condition:
- Either an existing `task-NNN` OR a new thin task spec you create on the fly

## Orchestration Steps

### 0. Thin Task Spec (optional)

If no task exists:

- Create `state/tasks/task-NNN.md` using `templates/s1-s9/task-spec.md`.
- Keep it minimal but valid (one AC, clear `in_scope_files`).
- Set `status = READY_FOR_IMPL`.

### 1. Implementation + VBR (S6+S7)

Invoke: `nowu-implementer`  
Input:
- `state/tasks/task-NNN.md`

Outputs:
- `state/changes/changes-task-NNN.md`
- `state/vbr/vbr-task-NNN.md`

Loop until:
- `vbr.status = PASS`

### 2. Review (S8)

Invoke: `nowu-reviewer`  
Input:
- `state/vbr/vbr-task-NNN.md`
- `state/changes/changes-task-NNN.md`
- `state/tasks/task-NNN.md`

Output: `state/reviews/review-task-NNN.md`

Lightweight review allowed for docs/refactors, but must still confirm:

- Scope respected (`in_scope_files` only).
- Tests make sense (or are intentionally absent for pure docs, explicitly noted).

### 3. Capture (S9)

Invoke: `nowu-curator`  
Input:
- `state/reviews/review-task-NNN.md`
- `docs/PROGRESS.md`

Output:
- `state/capture/capture-task-NNN.md`
- Updated `docs/PROGRESS.md`
- Commit message suggestion

Done when:
- `capture.status = DONE`
