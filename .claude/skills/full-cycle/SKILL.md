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

### 0. Session Context — Load Before Starting

Read these files to orient before any agent invocation:

- `docs/DECISIONS.md` — binding decisions (D-001 through D-020)
- `docs/ROADMAP-004.md` — current roadmap and "What To Do Right Now"
- `docs/WORKFLOW.md` — S1-S9 reference table and context scoping rules
- `state/intake/intake-NNN.md` — the intake you're working on

Do NOT load architecture docs, `src/`, `tests/`, or health reports upfront.
Each step below specifies exactly what additional files its agent needs.

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
  - `docs/architecture/ARCHITECTURE-VISION.md`
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
  - `docs/ROADMAP-004.md`
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
  - `docs/ROADMAP-004.md`
  - `state/session-log.md`
  - `git log`
- **Outputs:**
  - `state/capture/capture-task-NNN.md`
  - Updated `docs/ROADMAP-004.md`: work grid + dep graph + Section 7 + dependency cascade
  - Updated `state/session-log.md`: entry + dashboard (milestones, blocked items, current work)
  - Optional updates to `docs/DECISIONS.md`
  - Commit (not just message) on feature branch `feat/{work-item-id}` (D-025)

**Branch strategy (Mode A — full-cycle):**
- Work on branch `feat/{work-item-id}` (e.g., `feat/W8`).
- Curator commits capture artifacts + roadmap/session-log updates to the branch.
- Merge to main is Tier 3 (human-gated).

**Session-learning (D-026):**
- After capture completes, curator evaluates whether to auto-invoke session-learning.
- Auto-invoke if: 5+ files changed, 3+ tasks completed, new D-NNN decisions,
  or `next_cycle_trigger` is ARCH_PIVOT/PRODUCT_PIVOT.
- Produces `state/learnings/session-*.md` + updates `state/learnings/INDEX.md`.

`capture-task-NNN.md` includes:

- Summary of what changed and why.
- Lessons learned.
- `next_cycle_trigger`:
  - `CONTINUE | ARCH_PIVOT | PRODUCT_PIVOT | COMPLETE`.

The pre-workflow runner uses `next_cycle_trigger` to decide whether to
re-enter at P0.VISION, P0.UC, P1, or P3 on the next cycle.
