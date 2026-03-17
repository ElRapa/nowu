# nowu Workflow — Detailed Specification

> The standard repeatable process for developing any piece of software.
> Steps are always the same. Depth varies by task size and risk.

## The Octahedron Principle

Every step maps to a specific layer of the Octahedron (see GLOBAL-MODEL.md).
Agents and humans only see context from their current layer.
Loading context from the wrong layer is the root cause of design drift and re-litigation.

- Upper half (WHY): vision → use cases → requirements.
- Equator: decisions (D-NNN) with `level:` field (product/system/module/component/code).
- Lower half (WHAT): C4 L1–L4 — system context → containers → components → code.

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
**Octahedron layer**: Requirements (upper half)  
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
**Octahedron layer**: Equator (approaching from above) — C4 L1–L2  
**Actor**: nowu-architect agent  
**Purpose**: Identify constraints, affected modules, architectural risks.

**Scope IN**: Module map, existing decisions, protocol interfaces  
**Scope OUT**: Source code, test files, task-level details

**Requires**:
- `state/intake/intake-NNN.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `core/contracts/*.py`

**Produces**: `state/arch/intake-NNN-constraints.md`

---

### S3 — Design Options
**Octahedron layer**: Equator — C4 L2  
**Actor**: nowu-architect agent  
**Purpose**: Propose 2–3 approaches with explicit trade-offs.

**Scope IN**: Constraints, module protocols, integration patterns  
**Scope OUT**: Implementation code, test structure

**Requires**: `state/arch/intake-NNN-constraints.md` + contracts

**Produces**: `state/arch/intake-NNN-options.md` (2–3 options, recommendation)

---

### S4 — Decision 🛑 (VALIDATION GATE)
**Octahedron layer**: Equator  
**Actor**: nowu-architect (proposes) + Human (approves)  
**Purpose**: Record which option to build AND validate it solves the right problem.

**Two checks**:

1. **Verification**: Is this technically sound? (architect confirms)  
2. **Validation**: Does this actually address the use case? (human confirms)

**Human asks before approving**:

- Does option X address UC-NNN as described in the intake?
- Is the effort within the stated appetite?
- Does this create unacceptable constraints downstream?

**Produces**: `docs/DECISIONS.md` entry (D-NNN, with `level:` field set)  
**Template**: `templates/decision.md`

This step is the first validation gate: “Are we planning to build the right thing?”

---

### S5 — Shaping 🛑 (VALIDATION GATE)
**Octahedron layer**: Lower half — C4 L3 (component level)  
**Actor**: nowu-shaper (proposes) + Human (approves)  
**Purpose**: Break decision into bounded, TDD-ready tasks. ≤4h each.

**Scope IN**: Decision D-NNN, file tree, protocol interfaces  
**Scope OUT**: Architecture docs, vision docs, source code bodies

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
**Octahedron layer**: Lower half — C4 L4 (code level)  
**Actor**: Main Claude agent (or future nowu-implementer)  
**Purpose**: Write code + tests. TDD. Stay within `in_scope_files`.

**Scope IN**: Task spec + `in_scope_files` ONLY (nothing else!)  
**Scope OUT**: All architecture docs, other modules, `DECISIONS.md`

**TDD cycle** (per acceptance criterion):

1. RED: write a failing test that names the criterion  
2. GREEN: minimal implementation to pass  
3. REFACTOR: clean up while keeping green  

**Produces**: `state/changes/changes-task-NNN.md`

At natural stopping points (e.g. after a major AC turns green), optionally update
`state/SESSION-STATE.md` with the current step (S6), `task_id`, and next checkpoint.

---

### S7 — VBR (Verify Before Responding)
**Octahedron layer**: Code (AST boundary check = lightweight CPG Layer 1)  
**Actor**: Automated + main agent  
**Purpose**: Mechanically verify code quality and scope compliance.

**Automated gates**:

```bash
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .
git diff --name-only HEAD  # compare vs in_scope_files
```

**Produces**: `state/vbr/vbr-task-NNN.md`  
**Template**: `templates/vbr-report.md`  
**Rule**: Never proceed to S8 with any FAIL. Fix and re-run.

---

### S8 — Review
**Octahedron layer**: Code → Component (zooming out)  
**Actor**: nowu-reviewer agent (fresh context — no inheritance from S6)  
**Purpose**: Human-quality check. Verification + Validation.

**Verification** (built it right?):

- Every AC has a matching test function  
- VBR gates all PASS  
- Only `in_scope_files` modified  
- Architecture boundaries respected  

**Validation** (built the right thing?):

- Tests are meaningful, not just green  
- Each AC provably covers its use case via `validation_trace`  
- If outcome differs from validation intent: `CHANGES_REQUESTED`  

**Produces**: `state/reviews/review-task-NNN.md` + commit message  
**Template**: `templates/review-report.md`

---

### S9 — Capture
**Octahedron layer**: Back to equator (system-level view)  
**Actor**: nowu-curator agent  
**Purpose**: Close the loop. Record decisions, lessons, commit, update progress.

**Actions**:

1. Update task status to DONE in `state/tasks/`  
2. Update `docs/PROGRESS.md`  
3. Append new decisions (if discovered during S6–S8) to `docs/DECISIONS.md`  
4. Write `state/capture/capture-task-NNN.md`  
5. Commit with generated message from review report  

**Produces**: Committed code, updated PROGRESS.md, capture record

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
