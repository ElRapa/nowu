---
name: full-cycle
version: 2.2
mode: S1–S9
---

# Skill: Full Development Cycle (S1–S9)

## When to use

Use this skill when:

- You already have a **READY_FOR_S1** intake brief (`state/intake/intake-NNN.md`),
- Or you have just completed the pre-workflow (P0–P4) and received `intake-NNN.md`.

This skill does **not** manage vision, use cases, or problem discovery.
Those are handled by pre-workflow skills (P0.VISION, P0.UC, P1–P4).

---

## Orchestration Steps

### 1. Intake — S1 (nowu-intake)

- **Invoke:** `nowu-intake`
- **Input:** human description of the idea/feature **or** `intake-NNN.md` from P4.
- **Output:** `state/intake/intake-NNN.md`
- **Proceed when:** `status: READY_FOR_ARCH`

Notes:

- If the intake references UC-IDs that do **not** exist in `docs/USE_CASES.md`,
  recommend running **P0.UC / use-case-agent** before continuing, but do not
  block automatically.

---

### 2. Constraints Analysis — S2 (nowu-constraints)

- **Invoke:** `nowu-constraints`
- **Input:**
  - `state/intake/intake-NNN.md`
  - `docs/ARCHITECTURE.md`
  - `docs/DECISIONS.md`
  - Any contracts file (e.g., `core/contracts.py`)
- **Output:** `state/arch/intake-NNN-constraints.md`
- **Proceed when:** `status: READY_FOR_OPTIONS`

---

### 3. Options Design — S3 (nowu-options)

- **Invoke:** `nowu-options`
- **Input:**
  - `state/arch/intake-NNN-constraints.md`
  - Contracts / public module surfaces
- **Output:** `state/arch/intake-NNN-options.md`
- **Proceed when:** `status: READY_FOR_DECISION`

---

### 4. Decision — S4 (nowu-decider) — VALIDATION GATE

- **Invoke:** `nowu-decider`
- **Input:**
  - `state/arch/intake-NNN-options.md`
  - `docs/DECISIONS.md`
- **STOP:** agent outputs decision proposal.
- **Human gate:** review and approve.

On approval:

- Append `D-NNN` to `docs/DECISIONS.md`.
- Write `state/arch/intake-NNN-decision.md`.
- **Proceed when:** human approves **and** `status: READY_FOR_SHAPING`.

---

### 5. Shaping — S5 (nowu-shaper) — VALIDATION GATE

- **Invoke:** `nowu-shaper`
- **Input:**
  - `state/arch/intake-NNN-decision.md`
  - File tree of affected modules
  - Test structure
  - `docs/PROGRESS.md`
- **Output:** `state/tasks/task-NNN.md` (1–5 files)
- **STOP:** agent outputs shaped tasks.
- **Human gate:** review and approve shaped tasks.

**Proceed when:** human approves **and** `status: READY_FOR_IMPL`.

---

### 6–7. Implementation + VBR — S6/S7 (nowu-implementer)

For each task spec in dependency order:

- **Invoke:** `nowu-implementer`
- **Input:**
  - `state/tasks/task-NNN.md`
  - Files listed in `in_scope_files`
  - Related tests
  - `pyproject.toml`
- **Loop:**
  - Implement using TDD.
  - Run tests, type checks, lint, VBR.
- **Output:**
  - `state/changes/changes-task-NNN.md`
  - `state/vbr/vbr-task-NNN.md`
- **Proceed when:** `status: READY_FOR_REVIEW` (all gates PASS).
- **On CHANGES_REQUESTED:** fix and retry.

---

### 8. Review — S8 (nowu-reviewer)

- **Invoke:** `nowu-reviewer`
- **Input:**
  - `state/vbr/vbr-task-NNN.md`
  - `state/changes/changes-task-NNN.md`
  - `state/tasks/task-NNN.md`
  - `git diff` output
  - `.claude/rules/architecture.md`
- **Output:** `state/reviews/review-task-NNN.md`
- **Proceed when:** verdict `APPROVED`.
- **On CHANGES_REQUESTED:** return to S6 for that task.

---

### 9. Capture — S9 (nowu-curator)

- **Invoke:** `nowu-curator`
- **Input:**
  - `state/reviews/review-task-NNN.md`
  - `docs/DECISIONS.md`
  - `docs/PROGRESS.md`
  - `git log`
- **Outputs:**
  - Updated `docs/PROGRESS.md`
  - Optional updates to `docs/DECISIONS.md`
  - `state/capture/capture-task-NNN.md`
  - Commit message / commit

`capture-task-NNN.md` includes:

- Summary of what changed and why.
- Lessons learned.
- `next_cycle_trigger`:
  - `CONTINUE | ARCH_PIVOT | PRODUCT_PIVOT | COMPLETE`.

The pre-workflow runner uses `next_cycle_trigger` to decide whether to
re-enter at P0.VISION, P0.UC, P1, or P3 on the next cycle.
