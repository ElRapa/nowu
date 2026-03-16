---
name: full-cycle
description: Run the complete nowu workflow (S1–S9) for a feature or V1 plan step, delegating to the nowu-architect, nowu-shaper, nowu-reviewer, and nowu-curator agents.
---

# Full nowu Workflow Cycle (S1–S9)

You will run the full 9-step nowu workflow for the given work item:

S1 Intake →  
S2 Architecture analysis →  
S3 Design options →  
S4 Decision →  
S5 Task shaping →  
S6 Implementation (TDD) →  
S7 VBR (Verify Before Reporting) →  
S8 Review →  
S9 Capture & close

Always respect context boundaries and delegate to subagents where specified.

---

## 0. Before You Start

1. Identify the **work item**:
   - Either a free-form feature/bug description, or
   - A specific step from `docs/V1_PLAN.md` (for example, "Step 02 – Memory Integration Layer").
2. Confirm which **modules** are affected (core, flow, bridge, soul, know).

If the work item is unclear, ask the user 2–3 focused clarification questions, then continue.

---

## 1. S1–S4: Architecture Phase (Delegate to `nowu-architect`)

**Goal**: Understand the problem at system/module level and decide on an approach.

1. **Load context**:
   - `docs/ARCHITECTURE.md`
   - `docs/DECISIONS.md`
   - `docs/V1_PLAN.md` (if the work item is a V1 step)

2. **Delegate to `nowu-architect`** with a prompt like:

   > Use the nowu-architect agent to:
   > 1) Analyze this work item,
   > 2) List constraints, module boundaries, and risks,
   > 3) Propose 2–3 design options with tradeoffs,
   > 4) Recommend one option.

3. When `nowu-architect` returns:
   - Treat the design options + recommendation as S2–S3.
   - If a **new architecture decision** is needed, create a D-NNN entry in `docs/DECISIONS.md` as S4.
   - If the decision is high-impact, **STOP** and present it to the user for approval before continuing.

**Output of this phase**:
- A chosen design option with rationale, recorded as D-NNN if non-trivial.

---

## 2. S5: Task Shaping (Delegate to `nowu-shaper`)

**Goal**: Turn the chosen design into bounded implementation tasks (≤4h each).

1. **Load context**:
   - The chosen option from S4 (and its D-NNN number if created).
   - `docs/V1_PLAN.md`
   - `docs/PROGRESS.md`
   - `core/contracts/` and file tree of affected modules.

2. **Delegate to `nowu-shaper`** with a prompt like:

   > Use the nowu-shaper agent to:
   > - Read the chosen design option and relevant contracts,
   > - Produce 1–5 tasks (≤4h each) with:
   >   - title, use-case IDs,
   >   - in-scope files,
   >   - out-of-scope boundaries,
   >   - dependencies,
   >   - acceptance criteria,
   >   - test strategy.

3. When `nowu-shaper` returns:
   - Review that each task is realistically completable and has clear acceptance criteria.
   - **STOP** and present the task list to the user for scope approval before implementation.

**Output of this phase**:
- A small set of shaped tasks with explicit scope and acceptance criteria.

---

## 3. S6–S7: Implementation + VBR (Main Session)

**Goal**: For each approved task, implement using TDD and verify with VBR.

For **each task** in dependency order:

1. **Limit context** to this task only:
   - The task spec (scope, acceptance criteria, test strategy).
   - Only the files listed in the task’s scope.
   - Relevant test files.
   - `pyproject.toml` for tooling.

2. **Implement with TDD**:
   - Write a failing test first.
   - Implement minimal code to make it pass.
   - Refactor while keeping tests green.

3. **Run VBR** (Verify Before Reporting):

   ```bash
   uv run pytest --tb=short -q
   uv run mypy src/ --strict
   uv run ruff check .
   ```

   - If checks fail: fix issues and repeat.
   - If checks pass: proceed to review.

**Output per task**:
- Updated code + tests, both passing, all checks green.

---

## 4. S8: Review (Delegate to `nowu-reviewer`)

**Goal**: Ensure the implementation respects architecture, scope, and quality standards.

For the group of completed tasks:

1. **Load context**:
   - Git diff (what changed).
   - Task specs (scope + acceptance criteria).
   - `.claude/rules/architecture.md`
   - Test/VBR results.

2. **Delegate to `nowu-reviewer`** with:

   > Use the nowu-reviewer agent to:
   > - Review the diff against:
   >   - architecture rules,
   >   - task scope,
   >   - acceptance criteria,
   >   - testing and type-checking standards.
   > - Produce:
   >   - Critical issues (must fix),
   >   - Warnings,
   >   - Suggestions,
   >   - Summary of VBR evidence.

3. If there are **critical issues**:
   - Return to S6 for fixes, then re-run S7 and S8.
4. If only warnings/suggestions:
   - Optionally address them, then proceed.

**Output of this phase**:
- A review report and either approval or a list of issues to fix.

---

## 5. S9: Capture & Close (Delegate to `nowu-curator`)

**Goal**: Make the work durable in memory and progress tracking.

1. **Load context**:
   - `docs/DECISIONS.md`
   - `docs/PROGRESS.md`
   - Git log / description of the work just done.
   - Any new patterns or lessons discovered.

2. **Delegate to `nowu-curator`** with:

   > Use the nowu-curator agent to:
   > - Update DECISIONS.md if new decisions were made,
   > - Update PROGRESS.md for the relevant v1 step,
   > - Capture any lessons learned that should influence future work.

3. After curator finishes:
   - Commit the changes with a conventional commit including use-case IDs, for example:
     - `feat(flow): add session WAL recovery [NF-01, NF-04]`

**Output of this phase**:
- Decisions and progress durably recorded, clean commit ready.

---

## 6. When to Stop

After S9, ask:

- Is there a **next shaped task** in this scope?  
  - If yes: loop back to S5 or S6 as appropriate.
- Is there a **next V1 plan step**?  
  - If yes: start a new full cycle from S1.
- If not: report a concise summary:
  - What was done,
  - What decisions were made,
  - What remains open.

---

## 7. Context Discipline Rules

Throughout the full-cycle:

- During S1–S4 (architecture): **never** load source code or tests.
- During S5 (shaping): load contracts, file tree, test structure, but **not** full architecture docs.
- During S6–S7 (implementation + VBR): **only** load in-scope files, tests, and tooling config.
- During S8 (review): load diff, rules summary, and criteria — **not** full vision/plan docs.
- During S9 (capture): load decisions + progress, **never** source code.

If you are unsure which step you are in, ask the user:  
> “Are we currently at architecture (S1–S4), shaping (S5), implementation (S6–S7), review (S8), or capture (S9)?”

Then adjust your context accordingly.