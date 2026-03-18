# nowu Workflow — Detailed Specification

> The standard repeatable process for developing any piece of software.
> Steps are always the same. Depth varies by task size and risk.

## C4 Perspective

Every step operates at a specific C4 level:

- **Above C4**: vision, use cases, requirements (problem space).
- **C4 Level 1 (Context)**: systems and external actors.
- **C4 Level 2 (Containers/Modules)**: major building blocks and their interactions.
- **C4 Level 3 (Components)**: internal structure inside a container/module.
- **C4 Level 4 (Code)**: classes, functions, tests.

Agents and humans only see context from their current level.
Loading context from the wrong level is the main cause of design drift and re‑litigation.

## S0 — Session Bookmark (optional)

Before entering S1–S9, the human or main agent may update
`state/SESSION-STATE.md` with:

- current step (S1–S9)
- current `intake_id` / `decision_id` / `task_id`
- brief summary of focus
- next checkpoint

This is a convenience bookmark for session continuity, not a source of truth.
The canonical state always lives in the S1–S9 artifacts.

At good stopping points in S6–S7, update `SESSION-STATE` so the next session
can resume quickly. After S9 (Capture), you may clear or reset it to indicate
that the current cycle is complete.

---

## The 9 Steps

### S1 — Intake

**C4 position**: Above C4 (problem space: vision, use cases, requirements)  
**Actor**: Human (+ main Claude agent if async)  
**Purpose**: Translate an idea, bug, or need into a structured brief.

**Scope IN**: Vision, use cases, user problems, appetite  
**Scope OUT**: Architecture, code, implementation details

**Requires**:
- `docs/PROGRESS.md` (current phase context)
- `docs/V1_PLAN.md` (plan alignment)
- `docs/USE_CASES.md` (for tagging use case IDs)

**Produces**: `state/intake/intake-NNN.md`  
**Template**: `templates/intake-brief.md`  
**Human gate**: Confirm brief captures the real problem before proceeding.

---

### S2 — Architecture Analysis

**C4 position**: L1–L2 (system context and module boundaries)  
**Actor**: nowu-constraints agent  
**Purpose**: Identify constraints, affected modules, architectural risks.

**Scope IN**: Module map, existing decisions, protocol interfaces  
**Scope OUT**: Source code bodies, test files, task-level details

**Requires**:
- `state/intake/intake-NNN.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `core/contracts/*.py`

**Produces**: `state/arch/intake-NNN-constraints.md`  
**Template**: `templates/constraints-sheet.md`

---

### S3 — Design Options

**C4 position**: L2 (module / container interactions)  
**Actor**: nowu-options agent  
**Purpose**: Propose 2–3 approaches with explicit trade-offs.

**Scope IN**: Constraints, module protocols, module `__init__.py` surfaces  
**Scope OUT**: Implementation internals, test structure

**Requires**:
- `state/arch/intake-NNN-constraints.md`
- `core/contracts/*.py`
- `src/nowu/<module>/__init__.py` (public surface only)

**Produces**: `state/arch/intake-NNN-options.md` (2–3 options, recommendation)  
**Template**: `templates/options-sheet.md`

---

### S4 — Decision 🛑 (VALIDATION GATE)

**C4 position**: L2 (choosing between module-level options)  
**Actor**: nowu-decider (proposes) + Human (approves)  
**Purpose**: Record which option to build AND validate it solves the right problem.

**Two checks**:

1. **Verification**: Is this technically sound? (architect confirms)  
2. **Validation**: Does this actually address the use case? (human confirms)

**Human asks before approving**:

- Does option X address UC-NNN as described in the intake?
- Is the effort within the stated appetite?
- Does this create unacceptable constraints downstream?

**Requires**:
- `state/arch/intake-NNN-options.md`
- `docs/DECISIONS.md`

**Produces**:
- `docs/DECISIONS.md` entry (D-NNN, with `level:` field: product/system/module/component/code)
- `state/arch/intake-NNN-decision.md` (handoff for shaping)  
**Template**: `templates/decision.md`, `templates/decision-handoff.md`

This step is the first validation gate: “Are we planning to build the right thing?”

---

### S5 — Shaping 🛑 (VALIDATION GATE)

**C4 position**: L3 (components: files, classes, internal services)  
**Actor**: nowu-shaper (proposes) + Human (approves)  
**Purpose**: Break decision into bounded, TDD-ready tasks. ≤4h each.

**Scope IN**: Decision D-NNN, file tree, protocol interfaces, test tree  
**Scope OUT**: Architecture docs, vision docs, source code bodies outside scope

**Requires**:
- `state/arch/intake-NNN-decision.md`
- File tree of affected modules
- `core/contracts/*.py`
- `tests/` structure
- `docs/PROGRESS.md`

**Human validates before approving**:

- Does each task’s `validation_trace` connect to the right use cases?
- Is `in_scope_files` tight enough to prevent scope drift?
- Is any task > 4h? If so, split it.

**Produces**: `state/tasks/task-NNN.md` (one per task)  
**Template**: `templates/task-spec.md`

This is the second validation gate: if all acceptance criteria pass, will the original
problem be solved?

---

### S6 — Implementation

**C4 position**: L4 (code: classes, functions, tests)  
**Actor**: nowu-implementer agent (or main Claude session)  
**Purpose**: Write code + tests. TDD. Stay within `in_scope_files`.

**Scope IN**: Task spec + `in_scope_files` ONLY (nothing else)  
**Scope OUT**: Architecture docs, other modules, `DECISIONS.md`, upstream artifacts

**Requires**:
- `state/tasks/task-NNN.md`
- Files listed in `in_scope_files`
- Related test files
- `pyproject.toml`

**TDD cycle** (per acceptance criterion):

1. RED: write a failing test that names the criterion  
2. GREEN: minimal implementation to pass  
3. REFACTOR: clean up while keeping green  

**Produces**: `state/changes/changes-task-NNN.md`  
**Template**: `templates/changeset.md`

At natural stopping points (e.g. after a major AC turns green), optionally update
`state/SESSION-STATE.md` with the current step (S6), `task_id`, and next checkpoint.

---

### S7 — VBR (Verify Before Responding)

**C4 position**: L4 (code, with lightweight structural checks)  
**Actor**: nowu-implementer + automation  
**Purpose**: Mechanically verify code quality and scope compliance.

**Automated gates**:

```bash
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .
# compare changed files vs in_scope_files
git diff --name-only HEAD
```

**Requires**:
- `state/changes/changes-task-NNN.md`
- `state/tasks/task-NNN.md`

**Produces**: `state/vbr/vbr-task-NNN.md`  
**Template**: `templates/vbr-report.md`  

**Rule**: Never proceed to S8 with any FAIL. Fix and re-run.

---

### S8 — Review

**C4 position**: L4 → L3 (zooming out from code to component intent)  
**Actor**: nowu-reviewer agent (fresh context)  
**Purpose**: Human-quality check. Verification + Validation.

**Scope IN**:
- `state/vbr/vbr-task-NNN.md` (VBR evidence)
- `state/changes/changes-task-NNN.md` (what changed)
- `state/tasks/task-NNN.md` (acceptance criteria + validation_trace)
- `git diff` (actual changes)
- `.claude/rules/architecture.md` (boundaries)

**Scope OUT**:
- Full architecture docs, plan, vision (upstream)
- Other tasks’ artifacts

**Verification** (built it right?):

- Every AC has a matching test function  
- VBR gates all PASS  
- Only `in_scope_files` modified  
- Architecture boundaries respected  

**Validation** (built the right thing?):

- Each acceptance criterion is meaningful, not just “makes tests green”  
- Each use case in `validation_trace` is covered by ≥1 passing AC  
- The final behavior matches the original intent in the intake/decision chain  

**Produces**: `state/reviews/review-task-NNN.md`  
**Template**: `templates/review-report.md`

---

### S9 — Capture

**C4 position**: L1–L2 (zooming back out to system/module)  
**Actor**: nowu-curator agent  
**Purpose**: Close the loop. Record decisions, lessons, progress, and commit.

**Scope IN**:
- `state/reviews/review-task-NNN.md`
- `docs/DECISIONS.md`
- `docs/PROGRESS.md`
- `git log`

**Scope OUT**:
- `src/` and `tests/` (implementation details)

**Actions**:

1. Update task status to DONE in `state/tasks/` and/or `docs/PROGRESS.md`  
2. Append new decisions to `docs/DECISIONS.md` if review surfaced any  
3. Write `state/capture/capture-task-NNN.md` with what/why/lessons  
4. Compose or confirm commit message and ensure code is committed  

**Produces**:
- Updated `docs/PROGRESS.md`
- Optional updates in `docs/DECISIONS.md`
- `state/capture/capture-task-NNN.md`
- A commit that reflects the work

After Capture, you may clear or reset `state/SESSION-STATE.md` to indicate
that the current cycle is complete.

---

## Iteration Modes

| Mode            | Steps       | When to use                                        |
|-----------------|-------------|----------------------------------------------------|
| Full Cycle      | S1 → S9     | New feature, cross-module work, anything from idea|
| Implement Loop  | S6 → S9 (×N)| Tasks already shaped; execute in sequence         |
| Single Task     | S6 → S9 (×1)| Bug fix, small refactor, docs update              |
| Architecture Only | S1 → S4   | Planning/research, no implementation yet          |
| One Step        | Any single  | “Just review this” / “Just shape this”            |

## Depth Calibration

The workflow is always the same. The depth varies:

| Task Type            | S1–S4 | S5   | S6–S7 | S8–S9 |
|----------------------|-------|------|-------|-------|
| Framework feature    | Thick | Thick| Thick | Thick |
| Module implementation| Medium| Medium| Thick| Medium|
| Bug fix              | Thin  | Thin | Medium| Thin  |
| Docs/refactor        | Skip  | Thin | Medium| Thin  |

“Thin” means the step still happens, but briefly. A thin S1 might be 2 sentences.
A thick S1 is a full intake brief. The step is never skipped — it may just be a comment.
