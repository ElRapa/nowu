# Goal Layer: Add Goal Brief Artifacts Between Vision and Epics

## TL;DR

> **Quick Summary**: Add a "Goal Brief" artifact layer (`docs/goals/goal-NNN.md`) between vision.md and epics, bridging the documented strategy gap at PRODUCT/OPTIONS→DECISION. Each Goal Brief captures an outcome goal (why) + solution shape (what), following the unified approach recommended by Oracle and aligned with Shape Up methodology.
> 
> **Deliverables**:
> - Goal Brief template in `templates/`
> - 3-5 initial Goal Briefs derived from vision.md Success Horizons
> - 4 existing epics backfilled with correct `parent_goal:` references (removing TBD)
> - Workflow doc updates (PRE-WORKFLOW.md, GLOBAL-MODEL.md, ALTITUDES.md, CLAUDE.md)
> - Agent instruction updates (story-mapper, curator, health-goals)
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Template → Initial Goals → Epic Backfill → Doc Updates

---

## Context

### Original Request
User identified a missing layer between vision.md and epics (idea-006). Goals should capture cross-phase outcomes, not just tactical delivery chunks. Research confirmed this as a well-documented "strategy gap" problem.

### Interview Summary
**Key Discussions**:
- UCs = capabilities (what users can do); Goals = outcomes (what change we want)
- Oracle recommended unified Goal Brief (outcome + solution shape in one artifact)
- Location: `docs/goals/` (durable reference, not transient state)
- Creation timing: at vision approval
- Health check: update health-goals agent

**Research Findings**:
- 6/7 frameworks separate goals/solutions, but unified approach suits solo builder (avoids thin goals that agents interpret inconsistently)
- 3-5 artifact layers optimal (Cagan, Torres, Perri, Kniberg); adding goals = 5 layers (upper bound, supported)
- 70% strategy execution failure without intermediate goals (McKinsey 2017)
- Failure modes without this layer: strategy gap, premature convergence, vision drift

### Metis Review
**Identified Gaps** (addressed):
- Goal lifecycle across multiple epics/workflow runs → tracked via status field
- Approval tier → Tier 2 (batch for human review)
- GAP chain interaction → gap-analyst should read docs/goals/ (read-only)
- Retirement process → `retired` status with reason field in template
- Epics MUST have non-TBD parent_goal → enforced as guardrail

---

## Work Objectives

### Core Objective
Fill the PRODUCT/OPTIONS→DECISION gap in the altitude × phase matrix with a lightweight Goal Brief artifact that bridges vision to epics.

### Concrete Deliverables
- `templates/goal-brief.md` — template file
- `docs/goals/goal-001.md` through `goal-00N.md` — initial goals from Success Horizons
- 4 updated epic files with confirmed `parent_goal:` values
- Updated workflow docs: PRE-WORKFLOW.md, GLOBAL-MODEL.md, ALTITUDES.md, CLAUDE.md
- Updated agent instructions for goal-awareness

### Definition of Done
- [ ] `ls docs/goals/` returns 3-5 goal files
- [ ] `grep -r "parent_goal:.*TBD" state/epics/` returns empty
- [ ] `grep "Goal Brief\|goal-brief\|docs/goals" docs/PRE-WORKFLOW.md` returns matches
- [ ] `grep "Goal Brief\|docs/goals" docs/GLOBAL-MODEL.md` returns matches
- [ ] `grep "docs/goals" CLAUDE.md` returns matches in context scoping table
- [ ] Template exists at `templates/goal-brief.md`

### Must Have
- Unified Goal Brief with Outcome Goal section and Solution Shape section
- Frontmatter: status, parent_vision_horizon, created, linked_epics
- Lifecycle: proposed → approved → in_delivery → partially_validated → achieved → retired
- Every Goal Brief references a specific vision.md Success Horizon
- Every epic has a non-TBD parent_goal

### Must NOT Have (Guardrails)
- **NO measurement/metrics tracking infrastructure** — goals updated manually, no dashboards
- **NO dependency mapping between goals** — no `depends_on` fields
- **NO new agent for goal creation** — human or vision-bootstrap creates them
- **NO retroactive story mapping** — only backfill the 4 existing epics, not individual stories
- **NO use-case ↔ goal mapping matrix** — Solution Shape can reference UCs informally
- **NO architecture prescriptions in Goal Briefs** — describe outcome, never prescribe arch (ADRs win if conflict)
- **NO Goal Brief in S6/S7 context** — implementers never load goals (same as vision.md during coding)
- **Goal Brief template under 1 page** — if it needs more, the goal is too broad

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** - ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: N/A (no code changes, only markdown/workflow artifacts)
- **Automated tests**: None (documentation/workflow changes)
- **Framework**: N/A

### QA Policy
Every task includes agent-executed QA scenarios verifying file existence, content correctness, and cross-reference integrity via Bash commands (grep, ls, cat).
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — foundation):
├── Task 1: Create Goal Brief template [quick]
├── Task 2: Create docs/goals/ directory + initial Goal Briefs [unspecified-high]
├── Task 9: Record research synthesis as design document [quick]

Wave 2 (After Wave 1 — cross-references + doc updates):
├── Task 3: Backfill 4 existing epics with parent_goal [quick]
├── Task 4: Update PRE-WORKFLOW.md with goal creation step [quick]
├── Task 5: Update GLOBAL-MODEL.md (fill PRODUCT/OPTIONS & DECISION cells) [quick]
├── Task 6: Update ALTITUDES.md with Goal Brief layer [quick]
├── Task 7: Update CLAUDE.md context scoping table [quick]
├── Task 10: Record decision in docs/DECISIONS.md [quick]

Wave 3 (After Wave 2 — agent instructions):
├── Task 8: Update agent instructions (story-mapper, curator, health-goals) [unspecified-high]

Wave FINAL (After ALL tasks — verification):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
├── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix

| Task | Depends On | Blocks |
|---|---|---|
| 1 | — | 2, 3 |
| 2 | 1 | 3, 4, 5, 6, 8 |
| 3 | 1, 2 | F1-F4 |
| 4 | 2 | F1-F4 |
| 5 | 2 | F1-F4 |
| 6 | 2 | F1-F4 |
| 7 | — | F1-F4 |
| 8 | 2 | F1-F4 |
| 9 | — | F1-F4 |
| 10 | — | F1-F4 |
| F1-F4 | 3-10 | — |

### Agent Dispatch Summary

- **Wave 1**: 3 tasks — T1 `quick`, T2 `unspecified-high`, T9 `quick`
- **Wave 2**: 6 tasks — T3-T7 all `quick`, T10 `quick`
- **Wave 3**: 1 task — T8 `unspecified-high`
- **FINAL**: 4 tasks — F1 `oracle`, F2 `unspecified-high`, F3 `unspecified-high`, F4 `deep`

---

## TODOs

- [x] 1. Create Goal Brief Template

  **What to do**:
  - Create `templates/goal-brief.md` with frontmatter fields: `id`, `title`, `status` (proposed|approved|in_delivery|partially_validated|achieved|retired), `parent_vision_horizon`, `created`, `linked_epics` (list), `retired_reason` (optional)
  - Two sections: **Outcome Goal** (title, linked problem/horizon, desired change, success signals, non-goals) and **Solution Shape** (what form the solution takes, key capabilities, main tradeoffs, sequencing notes, epic seeds)
  - Keep template under 1 page. Follow existing template style from `templates/` directory
  - Add brief inline comments explaining each field's purpose

  **Must NOT do**:
  - No `depends_on` field between goals
  - No metrics tracking fields beyond simple success signals
  - No architecture prescriptions section

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Tasks 2, 3
  - **Blocked By**: None

  **References**:
  - `templates/pre-workflow/problem.md` — existing template style/structure to follow
  - `templates/pre-workflow/epic.md` — frontmatter pattern to match
  - `templates/pre-workflow/intake.md` — how intake templates reference other artifacts
  - Oracle recommendation (in draft): unified Goal Brief with Outcome Goal + Solution Shape sections
  - Shape Up methodology: "Shaped Concept" = combined goal + solution shape

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Template file exists with correct structure
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. cat templates/goal-brief.md
      2. Verify frontmatter contains: id, title, status, parent_vision_horizon, created, linked_epics
      3. Verify "## Outcome Goal" section exists
      4. Verify "## Solution Shape" section exists
      5. Verify no "depends_on" or "metrics" fields in frontmatter
      6. wc -l templates/goal-brief.md — should be under 60 lines
    Expected Result: All fields present, two sections, under 60 lines
    Failure Indicators: Missing frontmatter fields, missing sections, over 60 lines
    Evidence: .sisyphus/evidence/task-1-template-structure.txt

  Scenario: Template does NOT contain forbidden fields
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep -i "depends_on\|architecture\|metrics_tracking\|dashboard" templates/goal-brief.md
    Expected Result: No matches (exit code 1)
    Failure Indicators: Any match found
    Evidence: .sisyphus/evidence/task-1-no-forbidden-fields.txt
  ```

  **Commit**: YES (groups with Task 2 in Commit 1)
  - Message: `feat(goals): add Goal Brief template and initial goal artifacts`
  - Files: `templates/goal-brief.md`

- [x] 2. Create Initial Goal Briefs from Vision Success Horizons

  **What to do**:
  - Create `docs/goals/` directory
  - Analyze vision.md Success Horizons (3 horizons: 6mo, 12mo, 24mo) and the 4 existing epic `parent_goal` references (goal-001 Continuity, goal-002 Building Trust, goal-003 Compounding Knowledge)
  - Create Goal Briefs for at least goal-001, goal-002, goal-003 (already referenced by epics)
  - Derive additional goals from Success Horizons if clearly distinct outcomes exist
  - Each goal: status `proposed`, references specific Success Horizon text, has concrete success signals and epic seeds
  - Use vision.md Success Horizons VERBATIM as source — no reinterpretation or expansion

  **Must NOT do**:
  - No more than 5 Goal Briefs total (keep it tight)
  - No reinterpretation of vision text — use verbatim where possible
  - No architecture prescriptions in Solution Shape
  - No dependency mapping between goals

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1, but conceptually depends on template)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 3, 4, 5, 6, 8
  - **Blocked By**: Task 1 (needs template)

  **References**:
  - `docs/vision.md:59-71` — Success Horizons (6mo, 12mo, 24mo) — source material for goals
  - `state/epics/epic-v1core-001.md:7` — `parent_goal: goal-001  # Continuity`
  - `state/epics/epic-v1core-002.md:7` — `parent_goal: goal-002  # Building Trust`
  - `state/epics/epic-v1core-003.md:7` — `parent_goal: goal-001  # Continuity`
  - `state/epics/epic-v1core-004.md:7` — `parent_goal: goal-003  # Compounding Knowledge`
  - `templates/goal-brief.md` — template created in Task 1
  - `docs/USE_CASES.md` — reference UCs informally in Solution Shape sections

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Goal files exist with correct frontmatter
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. ls docs/goals/ — expect 3-5 files matching goal-NNN.md
      2. For each file: grep "^status:" — expect "proposed"
      3. For each file: grep "^parent_vision_horizon:" — expect non-empty value
      4. For each file: grep "## Outcome Goal" — expect match
      5. For each file: grep "## Solution Shape" — expect match
    Expected Result: 3-5 goal files, all with status proposed, all with both sections
    Failure Indicators: Missing files, wrong status, missing sections
    Evidence: .sisyphus/evidence/task-2-goal-files.txt

  Scenario: Goal-001, 002, 003 exist (referenced by epics)
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. test -f docs/goals/goal-001.md && echo "EXISTS" || echo "MISSING"
      2. test -f docs/goals/goal-002.md && echo "EXISTS" || echo "MISSING"
      3. test -f docs/goals/goal-003.md && echo "EXISTS" || echo "MISSING"
    Expected Result: All three print "EXISTS"
    Failure Indicators: Any prints "MISSING"
    Evidence: .sisyphus/evidence/task-2-required-goals.txt

  Scenario: Goals reference vision.md Success Horizons verbatim
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. For each goal: grep -c "6 Months\|12 Months\|24 Months" docs/goals/goal-NNN.md
    Expected Result: Each goal references at least one horizon
    Failure Indicators: No horizon reference found
    Evidence: .sisyphus/evidence/task-2-horizon-refs.txt
  ```

  **Commit**: YES (Commit 1)
  - Message: `feat(goals): add Goal Brief template and initial goal artifacts`
  - Files: `docs/goals/goal-*.md`

- [x] 3. Backfill Existing Epics with Confirmed parent_goal

  **What to do**:
  - Update all 4 epic files to remove "(TBD: idea-006)" from parent_goal field
  - Verify each epic's parent_goal references an existing goal file in docs/goals/
  - epic-v1core-001 → goal-001, epic-v1core-002 → goal-002, epic-v1core-003 → goal-001, epic-v1core-004 → goal-003

  **Must NOT do**:
  - Do NOT change any other epic content (status, stories, scope, etc.)
  - Do NOT retroactively map stories to goals

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4-7)
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 1, 2

  **References**:
  - `state/epics/epic-v1core-001.md:7` — current: `parent_goal: goal-001  # Continuity — thread survives interruptions (TBD: idea-006)`
  - `state/epics/epic-v1core-002.md:7` — current: `parent_goal: goal-002  # Building Trust — decisions traceable, confidence visible (TBD: idea-006)`
  - `state/epics/epic-v1core-003.md:7` — current: `parent_goal: goal-001  # Continuity — thread survives interruptions (TBD: idea-006)`
  - `state/epics/epic-v1core-004.md:7` — current: `parent_goal: goal-003  # Compounding Knowledge — accumulates within and across projects (TBD: idea-006)`

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: No TBD parent_goal references remain
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep -r "TBD" state/epics/epic-v1core-*.md
    Expected Result: No matches (exit code 1)
    Failure Indicators: Any TBD found
    Evidence: .sisyphus/evidence/task-3-no-tbd.txt

  Scenario: All parent_goal values reference existing goal files
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. For each epic: extract parent_goal value, verify docs/goals/{value}.md exists
    Expected Result: All 4 epics reference existing files
    Failure Indicators: Any referenced goal file missing
    Evidence: .sisyphus/evidence/task-3-valid-refs.txt
  ```

  **Commit**: YES (Commit 2)
  - Message: `docs(workflow): integrate Goal Brief into workflow documentation`
  - Files: `state/epics/epic-v1core-*.md`

- [x] 4. Update PRE-WORKFLOW.md with Goal Creation Step

  **What to do**:
  - Add a goal creation sub-step in the P0 section (after vision approval, before P1)
  - Document: when goals are created (at vision approval), who creates them (human or vision-bootstrap), what artifact is produced (docs/goals/goal-NNN.md)
  - Reference the Goal Brief template
  - Specify approval tier: Tier 2 (batch for human review)
  - Keep the addition concise — a sub-section, not a restructuring of P0

  **Must NOT do**:
  - Do NOT restructure P0-P4 phases
  - Do NOT add a new phase number (keep it as P0 sub-step)
  - Do NOT modify other P1-P4 sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 5-7)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 2

  **References**:
  - `docs/PRE-WORKFLOW.md` — full pre-workflow spec (551 lines), P0 section for insertion point
  - `CLAUDE.md` — approval tiers reference (Tier 1/2/3)
  - `templates/goal-brief.md` — template to reference

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: PRE-WORKFLOW.md mentions Goal Brief in P0
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep -n "Goal Brief\|goal-brief\|docs/goals" docs/PRE-WORKFLOW.md
    Expected Result: At least 2 matches in P0 section area
    Failure Indicators: No matches or matches only outside P0
    Evidence: .sisyphus/evidence/task-4-preworkflow-goals.txt

  Scenario: No other P1-P4 sections modified
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. git diff docs/PRE-WORKFLOW.md — check that changes are confined to P0 area
    Expected Result: Diff shows changes only in P0 section
    Failure Indicators: Changes in P1, P2, P3, or P4 sections
    Evidence: .sisyphus/evidence/task-4-scope-check.txt
  ```

  **Commit**: YES (Commit 2)
  - Files: `docs/PRE-WORKFLOW.md`

- [x] 5. Update GLOBAL-MODEL.md — Fill PRODUCT/OPTIONS and PRODUCT/DECISION

  **What to do**:
  - Fill the currently empty PRODUCT/OPTIONS and PRODUCT/DECISION cells in the altitude × phase matrix
  - PRODUCT/OPTIONS: "Goal Brief explores outcome + solution shape options"
  - PRODUCT/DECISION: "Goal Brief approved — outcome and shape committed"
  - Reference the Goal Brief artifact in the cell descriptions

  **Must NOT do**:
  - Do NOT change other cells in the matrix
  - Do NOT restructure the matrix format

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4, 6, 7)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 2

  **References**:
  - `docs/GLOBAL-MODEL.md` — altitude × phase matrix (171 lines), find the PRODUCT row, OPTIONS and DECISION columns
  - `state/ideas/idea-004.md` — origin of the matrix model, for context on original intent

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: GLOBAL-MODEL.md PRODUCT row has filled OPTIONS and DECISION cells
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep -A2 "PRODUCT.*OPTIONS\|OPTIONS.*PRODUCT" docs/GLOBAL-MODEL.md — or search for Goal Brief in PRODUCT section
      2. grep "Goal Brief" docs/GLOBAL-MODEL.md
    Expected Result: Goal Brief referenced in PRODUCT row
    Failure Indicators: Empty cells or no Goal Brief reference
    Evidence: .sisyphus/evidence/task-5-global-model.txt
  ```

  **Commit**: YES (Commit 2)
  - Files: `docs/GLOBAL-MODEL.md`

- [x] 6. Update ALTITUDES.md with Goal Brief Layer

  **What to do**:
  - Add Goal Brief to the artifact/altitude descriptions where appropriate
  - Show how Goal Brief fits in the fractal loop pattern (HIGH altitude, between vision and epic)
  - Update any diagrams or tables that list artifacts per altitude

  **Must NOT do**:
  - Do NOT restructure the fractal loop model
  - Do NOT change the 3-altitude system (HIGH/MID/LOW)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3-5, 7)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 2

  **References**:
  - `docs/ideas/ALTITUDES.md` — fractal loop pattern (311 lines), HIGH altitude section for insertion
  - `docs/GLOBAL-MODEL.md` — cross-reference for consistency

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ALTITUDES.md references Goal Brief
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep -n "Goal Brief\|goal-brief" docs/ideas/ALTITUDES.md
    Expected Result: At least 1 match in HIGH altitude section
    Failure Indicators: No matches
    Evidence: .sisyphus/evidence/task-6-altitudes.txt
  ```

  **Commit**: YES (Commit 2)
  - Files: `docs/ideas/ALTITUDES.md`

- [x] 7. Update CLAUDE.md Context Scoping Table

  **What to do**:
  - Add `docs/goals/` to the context scoping table in CLAUDE.md
  - Specify which phases load Goal Briefs: P0-P2 (YES), P3 (YES — for constraint context), S1-S2 (YES — intake needs goal reference), S3-S5 (YES — shaping references goals), S6-S7 (NEVER), S8 (YES — reviewer checks goal alignment), S9 (YES — curator updates goal status), Health (YES for health-goals)
  - Also add to the GAP row: gap-analyst should read docs/goals/ (read-only context)

  **Must NOT do**:
  - Do NOT change existing scoping rules for other artifacts
  - Do NOT add docs/goals/ to S6/S7 load scope

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3-6)
  - **Blocks**: F1-F4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `CLAUDE.md` — Context Scoping table, find existing rows and add docs/goals/ entries
  - Goal Brief lifecycle (proposed→approved→in_delivery→achieved→retired) — determines which phases need read access

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: docs/goals/ appears in context scoping table
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep "docs/goals" CLAUDE.md
    Expected Result: At least 3 matches (multiple phase rows reference it)
    Failure Indicators: Fewer than 3 matches
    Evidence: .sisyphus/evidence/task-7-claude-scoping.txt

  Scenario: S6/S7 row does NOT include docs/goals/
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. Inspect S6-S7 row in CLAUDE.md context scoping — verify docs/goals/ is in "Never Load" or not in "Load"
    Expected Result: docs/goals/ not in S6/S7 load scope
    Failure Indicators: docs/goals/ appears in S6/S7 load column
    Evidence: .sisyphus/evidence/task-7-no-s6s7.txt
  ```

  **Commit**: YES (Commit 2)
  - Files: `CLAUDE.md`

- [x] 8. Update Agent Instructions for Goal-Awareness

  **What to do**:
  - **story-mapper** (`.claude/agents/` or relevant location): When creating epics, require `parent_goal` field referencing an existing goal in docs/goals/. If no goal fits, flag for goal creation before proceeding.
  - **curator** (S9 agent): After successful review, check if the completed work changes any goal's status (e.g., move from proposed to in_delivery, or update partially_validated). Update the goal file if appropriate.
  - **health-goals**: Update to check: (a) all goals in docs/goals/ have valid status, (b) all epics have non-TBD parent_goal, (c) all active goals have at least one linked epic, (d) no orphan goals (achieved/retired but still referenced by active epics)
  - Search for agent instruction files to find exact paths

  **Must NOT do**:
  - Do NOT create new agents — only update existing instruction files
  - Do NOT add goal loading to implementer agents (S6/S7)
  - Do NOT build goal decomposition logic

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs Wave 2 docs for consistent references)
  - **Parallel Group**: Wave 3 (solo)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 2

  **References**:
  - `.claude/agents/` — directory containing agent instruction files (search for story-mapper, curator, health-goals)
  - `state/health/health-goals-2026-04-01.md` — existing health-goals report format to understand current checks
  - `docs/goals/goal-*.md` — the artifacts agents need to reference
  - `CLAUDE.md` — agents per step table (story-mapper at P2, curator at S9, health-goals at health checks)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Agent instructions reference docs/goals/
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep -r "docs/goals\|Goal Brief\|parent_goal" .claude/agents/ — find references in updated agents
    Expected Result: At least 3 matches across story-mapper, curator, health-goals agent files
    Failure Indicators: No matches in any agent file
    Evidence: .sisyphus/evidence/task-8-agent-refs.txt

  Scenario: health-goals agent checks goal validity
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. Find health-goals agent file, verify it mentions checking: valid status, non-TBD parent_goal in epics, linked epics exist
    Expected Result: All 3 checks referenced
    Failure Indicators: Missing check types
    Evidence: .sisyphus/evidence/task-8-health-checks.txt
  ```

  **Commit**: YES (Commit 3)
  - Message: `chore(agents): update agent instructions for goal-awareness`
  - Files: `.claude/agents/*.md`

- [x] 9. Record Research Synthesis as Design Document

  **What to do**:
  - Create `docs/design/workflow_design/goal-layer-research.md` — a durable reference document capturing the research that informed the Goal Brief design
  - Include: framework comparison table (OKRs, OST, Shape Up, Dual Track, JTBD, Strategy Maps, North Star), failure modes research, artifact overhead findings, Oracle recommendation, and the synthesis rationale
  - This is a design decision record, not a plan — it explains WHY we chose the unified Goal Brief approach
  - Follow existing design document style in `docs/design/workflow_design/`

  **Must NOT do**:
  - No implementation details — this is pure research synthesis
  - No prescriptive "next steps" — that's the plan's job

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (no dependencies)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `docs/design/workflow_design/nowu-architecture-workflow_v6_analysis_GAP-extension.md` — existing design doc style to follow
  - `.sisyphus/drafts/goal-layer-workflow-redesign.md` — contains all research results to synthesize (Oracle, Librarian #1, Librarian #2 findings)
  - `state/ideas/idea-006.md` — origin idea for context

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Research document exists with key sections
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. test -f docs/design/workflow_design/goal-layer-research.md && echo "EXISTS"
      2. grep "Framework Comparison\|framework comparison" docs/design/workflow_design/goal-layer-research.md
      3. grep "Failure Mode\|failure mode" docs/design/workflow_design/goal-layer-research.md
      4. grep "Oracle\|oracle" docs/design/workflow_design/goal-layer-research.md
    Expected Result: File exists, contains framework comparison, failure modes, and Oracle sections
    Failure Indicators: Missing file or missing sections
    Evidence: .sisyphus/evidence/task-9-research-doc.txt
  ```

  **Commit**: YES (Commit 1)
  - Message: `feat(goals): add Goal Brief template and initial goal artifacts`
  - Files: `docs/design/workflow_design/goal-layer-research.md`

- [x] 10. Record Decision in docs/DECISIONS.md

  **What to do**:
  - Add a new decision entry (D-NNN, using the next available number) to `docs/DECISIONS.md`
  - Decision: "Add Goal Brief artifact layer between vision and epics"
  - Record: what was decided, alternatives considered (separate goals + solutions vs unified Goal Brief vs no change), rationale (research-backed), confidence level, what depends on it
  - Follow existing decision format in DECISIONS.md

  **Must NOT do**:
  - Do NOT modify existing decisions
  - Do NOT add architecture prescriptions — this is a workflow/process decision

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3-7)
  - **Blocks**: F1-F4
  - **Blocked By**: None

  **References**:
  - `docs/DECISIONS.md` — existing decisions format and numbering (find last D-NNN to determine next number)
  - `.sisyphus/drafts/goal-layer-workflow-redesign.md` — research results and rationale
  - `docs/design/workflow_design/goal-layer-research.md` — detailed research to reference (created in Task 9)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: New decision entry exists in DECISIONS.md
    Tool: Bash
    Preconditions: Task completed
    Steps:
      1. grep "Goal Brief" docs/DECISIONS.md
      2. Verify the decision has: title, alternatives, rationale, confidence, dependencies
    Expected Result: Decision entry found with all required fields
    Failure Indicators: No Goal Brief decision found or missing fields
    Evidence: .sisyphus/evidence/task-10-decision-entry.txt
  ```

  **Commit**: YES (Commit 2)
  - Message: `docs(workflow): integrate Goal Brief into workflow documentation`
  - Files: `docs/DECISIONS.md`

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, grep). For each "Must NOT Have": search for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Review all changed/created markdown files for: consistency of frontmatter fields, broken cross-references, template conformance. Check for AI slop: excessive commentary, vague language, placeholder content.
  Output: `Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high`
  Execute EVERY QA scenario from EVERY task. Follow exact verification commands. Test cross-task integration (goal → epic traceability, doc cross-references). Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Commit 1** (after Wave 1): `feat(goals): add Goal Brief template and initial goal artifacts`
  - Files: `templates/goal-brief.md`, `docs/goals/goal-*.md`
- **Commit 2** (after Wave 2): `docs(workflow): integrate Goal Brief into workflow documentation`
  - Files: `state/epics/epic-*.md`, `docs/PRE-WORKFLOW.md`, `docs/GLOBAL-MODEL.md`, `docs/ideas/ALTITUDES.md`, `CLAUDE.md`
- **Commit 3** (after Wave 3): `chore(agents): update agent instructions for goal-awareness`
  - Files: `.claude/agents/*.md` (story-mapper, curator, health-goals)

---

## Success Criteria

### Verification Commands
```bash
ls docs/goals/                                    # Expected: 3-5 goal-NNN.md files
grep -r "parent_goal:.*TBD" state/epics/          # Expected: empty (no TBDs)
grep "Goal Brief" docs/PRE-WORKFLOW.md             # Expected: matches in P0 section
grep "Goal Brief" docs/GLOBAL-MODEL.md             # Expected: matches in PRODUCT row
grep "docs/goals" CLAUDE.md                        # Expected: context scoping entry
cat templates/goal-brief.md                        # Expected: complete template
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All goal files have valid frontmatter
- [ ] All epics reference existing goal files
- [ ] Workflow docs consistently reference Goal Brief
