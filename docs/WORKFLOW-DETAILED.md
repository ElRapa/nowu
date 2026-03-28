# nowu Workflow — Detailed Specification

> The standard repeatable process for developing any piece of software.
> Steps are always the same. Depth varies by task size and risk.
> For the quick reference table, see `WORKFLOW.md`.
> For the pre-implementation phases (P0–P4), see `PRE-WORKFLOW.md`.

---

## Connection to Pre-Workflow

The Pre-Workflow (P0–P4) produces `state/intake/intake-NNN.md` with `status: READY_FOR_S1`.
That file is the only valid entry point into S1. Do not start S1 without it.

At S9, the `next_cycle_trigger` field routes back into the pre-workflow:
- `CONTINUE` → P2.1 (next story, same problem already approved)
- `ARCH_PIVOT` → P3.1 (architecture re-check needed)
- `PRODUCT_PIVOT` → P1.1 (new discovery run needed)
- `COMPLETE` → cycle closed, epic done

---

## C4 Perspective

Every step operates at a specific C4 level. Agents load only context from their current level.
Loading context from the wrong level is the primary cause of design drift and re-litigation.

| Level | Scope | Main artifacts |
|-------|-------|----------------|
| Above C4 | Problem space: vision, use cases, requirements | `docs/vision.md`, `state/problems/` |
| L1 — Context | Systems and external actors | `docs/ARCHITECTURE.md` §1 |
| L2 — Containers/Modules | Major building blocks and interactions | `docs/ARCHITECTURE.md` §4 |
| L3 — Components | Internal structure: files, classes, services | contracts, file tree |
| L4 — Code | Classes, functions, tests | `src/`, `tests/` |

---

## S0 — Session Bookmark (optional)

Before entering S1–S9, update `state/SESSION-STATE.md` with:
- Current step (S1–S9)
- Current `intake_id` / `decision_id` / `task_id`
- Brief summary of focus
- Next checkpoint

This is a convenience bookmark for session continuity, **not a source of truth**.
The canonical state always lives in the S1–S9 artifacts.

Consider running `/health-check all` at session start if >7 days since last run.

---

## S1 — Intake

**C4 position:** Above C4 (problem space)
**Actor:** Human + nowu-intake agent
**Purpose:** Confirm the intake brief is complete and understood before architecture work begins.

**Scope IN:** Vision alignment, use case references, appetite, pre-workflow context
**Scope OUT:** Architecture, code, implementation details

**Requires:**
- `state/intake/intake-NNN.md` (READY_FOR_S1 — produced by P4)
- `docs/PROGRESS.md` (current phase context)
- `docs/V1_PLAN.md` (plan alignment)
- `docs/USE_CASES.md` (UC-NNN verification)

**Produces:** `state/intake/intake-NNN.md` status updated to `READY_FOR_ARCH`
**Template:** `templates/intake-brief.md`
**Human gate:** Confirm the brief captures the real problem before architecture begins.

> When the intake is pre-workflow-generated, S1 is thin: confirm fields are correct,
> not re-author. A thin S1 takes 2–5 minutes.

---

## S2 — Architecture Analysis

**C4 position:** L1–L2 (system context and module boundaries)
**Actor:** nowu-constraints agent
**Purpose:** Identify constraints, affected modules, architectural risks.

**Scope IN:** Module map, existing decisions, protocol interfaces, arch-pass from pre-workflow
**Scope OUT:** Source code bodies, test files, task-level details

**Requires:**
- `state/intake/intake-NNN.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `core/contracts/*.py` (or equivalent protocol interfaces)
- `state/arch/arch-pass-NNN.md` (if produced by P3 — use as starting point, document divergences)

**Produces:** `state/arch/intake-NNN-constraints.md`
**Template:** `templates/constraints-sheet.md`

> When an arch-pass exists from the pre-workflow, S2 refines it — not replaces it.
> Any divergence from the arch-pass must be explicitly documented with rationale.
> The S2 Conflict Protocol section in arch-pass-NNN is authoritative.

---

## S3 — Design Options

**C4 position:** L2 (module / container interactions)
**Actor:** nowu-options agent
**Purpose:** Propose 2–3 implementation approaches with explicit trade-offs.

**Scope IN:** Constraints sheet, module protocols, public module surfaces (`__init__.py`)
**Scope OUT:** Implementation internals, test structure, full ARCHITECTURE.md

**Requires:**
- `state/arch/intake-NNN-constraints.md`
- `core/contracts/*.py`
- `src/<module>/__init__.py` (public surface only, not internals)

**Produces:** `state/arch/intake-NNN-options.md` (2–3 options with explicit recommendation)
**Template:** `templates/options-sheet.md`

---

## S4 — Decision 🛑 (VALIDATION GATE)

**C4 position:** L2 (choosing between module-level options)
**Actor:** nowu-decider (proposes) + Human (approves)
**Purpose:** Record which option to build AND validate it solves the right problem.

**Two checks:**
1. **Verification:** Is this technically sound? (agent confirms)
2. **Validation:** Does this actually address the use case? (human confirms)

**Human asks before approving:**
- Does option X address UC-NNN as described in the intake?
- Is the effort within the stated appetite?
- Does this create unacceptable constraints downstream?

**Requires:**
- `state/arch/intake-NNN-options.md`
- `docs/DECISIONS.md`

**Produces:**
- `docs/DECISIONS.md` entry (D-NNN, with `level:` field: product/system/module/component/code)
- `state/arch/intake-NNN-decision.md` (handoff for shaping)

**Template:** `templates/decision.md`

This is the first validation gate: "Are we planning to build the right thing?"

---

## S5 — Shaping 🛑 (VALIDATION GATE)

**C4 position:** L3 (components: files, classes, internal services)
**Actor:** nowu-shaper (proposes) + Human (approves)
**Purpose:** Break decision into bounded, TDD-ready tasks. Each task ≤4h.

**Scope IN:** Decision handoff, file tree, protocol interfaces, test structure, current phase
**Scope OUT:** Architecture docs, vision docs, source code bodies outside in-scope files

**Requires:**
- `state/arch/intake-NNN-decision.md`
- File tree of affected modules (`tree src/<module>`)
- `core/contracts/*.py`
- `tests/` structure (`ls tests/`)
- `docs/PROGRESS.md`

**Human validates before approving:**
- Does each task's `validation_trace` connect to the right use cases?
- Is `in_scope_files` tight enough to prevent scope drift?
- Is any task > 4h? If so, split it.

**Produces:** `state/tasks/task-NNN.md` (one per task)
**Template:** `templates/task-spec.md`

This is the second validation gate: if all acceptance criteria pass, will the original problem be solved?

---

## S6 — Implementation

**C4 position:** L4 (code: classes, functions, tests)
**Actor:** nowu-implementer agent (or main Claude session)
**Purpose:** Write code + tests. TDD. Stay strictly within `in_scope_files`.

**Scope IN:** Task spec + `in_scope_files` ONLY
**Scope OUT:** Architecture docs, other modules, DECISIONS.md, upstream artifacts

**Requires:**
- `state/tasks/task-NNN.md`
- Files listed in `in_scope_files`
- Related test files
- `pyproject.toml`

**TDD cycle per acceptance criterion:**
1. **RED:** Write a failing test that names the criterion
2. **GREEN:** Minimal implementation to pass
3. **REFACTOR:** Clean up while keeping green

**Produces:** `state/changes/changes-task-NNN.md`
**Template:** `templates/changeset.md`

At natural stopping points, optionally update `state/SESSION-STATE.md`.

---

## S7 — VBR (Verify Before Responding)

**C4 position:** L4 (code, with lightweight structural checks)
**Actor:** nowu-implementer + automation
**Purpose:** Mechanically verify code quality and scope compliance before any review.

**Automated gates:**

```bash
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .
git diff --name-only HEAD    # verify against in_scope_files
```

**Requires:**
- `state/changes/changes-task-NNN.md`
- `state/tasks/task-NNN.md`

**Produces:** `state/vbr/vbr-task-NNN.md`
**Template:** `templates/vbr-report.md`

**Rule:** Never proceed to S8 with any FAIL. Fix and re-run.

---

## S8 — Review

**C4 position:** L4 → L3 (zooming out from code to component intent)
**Actor:** nowu-reviewer agent — **always fresh context window**
**Purpose:** Human-quality verification and validation check.

**Scope IN:**
- `state/vbr/vbr-task-NNN.md`
- `state/changes/changes-task-NNN.md`
- `state/tasks/task-NNN.md`
- `git diff` (actual changes)
- `.claude/rules/architecture.md`
- `state/stories/story-NNN-*.md` (via task.story_id — verify story-level coverage)

**Scope OUT:** Full architecture docs, plan, vision (upstream). Other tasks' artifacts.

**Verification (built it right?):**
- Every AC has a matching test function
- VBR gates all PASS
- Only `in_scope_files` modified
- Architecture boundaries respected

**Validation (built the right thing?):**
- Each AC is meaningful, not just "makes tests green"
- Each UC-NNN in `validation_trace` is covered by ≥1 passing AC
- Final behavior matches original intent in the intake/decision chain
- Story-level ACs are fully covered across all tasks

**Produces:** `state/reviews/review-task-NNN.md`
**Template:** `templates/review-report.md`

---

## S9 — Capture

**C4 position:** L1–L2 (zooming back out to system/module)
**Actor:** nowu-curator agent
**Purpose:** Close the loop. Record decisions, lessons, progress. Set the feedback trigger.

**Scope IN:**
- `state/reviews/review-task-NNN.md`
- `docs/DECISIONS.md`
- `docs/PROGRESS.md`
- `state/intake/intake-NNN.md` (to update status and set next_cycle_trigger)
- `git log`

**Scope OUT:** `src/` and `tests/` (implementation details)

**Actions:**
1. Update task status to DONE in `state/tasks/` and `docs/PROGRESS.md`
2. Append new decisions to `docs/DECISIONS.md` if review surfaced any
3. Write `state/capture/capture-task-NNN.md` with what/why/lessons
4. Set `next_cycle_trigger` in `state/intake/intake-NNN.md`:
   - `CONTINUE` → re-enter at P2.1 (next story, same epic)
   - `ARCH_PIVOT` → re-enter at P3.1 (architecture recheck)
   - `PRODUCT_PIVOT` → re-enter at P1.1 (new discovery)
   - `COMPLETE` → cycle closed, epic done
5. Compose commit message and ensure code is committed

**Produces:**
- Updated `docs/PROGRESS.md`
- Optional updates to `docs/DECISIONS.md`
- `state/capture/capture-task-NNN.md`
- `next_cycle_trigger` set in intake record
- A clean commit

After Capture, clear or reset `state/SESSION-STATE.md`.

---

## Iteration Modes

| Mode | Steps | When to use |
|------|-------|-------------|
| Full Cycle | S1 → S9 | New feature, cross-module work, anything from intake |
| Implement Loop | S6 → S9 (×N) | Tasks already shaped; execute in sequence |
| Single Task | S6 → S9 (×1) | Bug fix, small refactor, docs update |
| Architecture Only | S1 → S4 → S9 | Planning/research, no implementation yet |
| One Step | Any single | "Just review this" / "Just shape this" |

---

## Depth Calibration

The workflow structure is always the same. The depth varies:

| Task type | S1–S4 | S5 | S6–S7 | S8–S9 |
|-----------|-------|----|-------|-------|
| Framework feature | Thick | Thick | Thick | Thick |
| Module implementation | Medium | Medium | Thick | Medium |
| Bug fix | Thin | Thin | Medium | Thin |
| Docs / refactor | Skip | Thin | Medium | Thin |

"Thin" means the step still happens but briefly.
A thin S1 for a pre-workflow-generated intake might be a 2-sentence confirmation.
A thick S1 is a full contextual analysis. The step is never silently skipped.
