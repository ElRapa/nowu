# W6 — 5×10 Model Refactor + Agent-Grid Mapping

## TL;DR

> **Quick Summary**: Fix S7/S8 mapping bugs across 3 model docs, expand Section 13 artifact coverage, formalize artifact_type vocabulary, add altitude/phase to all 35 agent specs, and create a canonical agent grid in AGENTS.md — operationalizing the 5×10 model that W5 validated.
> 
> **Deliverables**:
> - MODEL-REFERENCE.md §7 + §11 corrected (S7/S8 agent swap + phase fix)
> - WORKFLOW-STANDARDS.md §1.1 corrected (S8 VERIFICATION → EVALUATION)
> - MODEL-REFERENCE.md §13 expanded (6+ missing artifact types, consumption-position convention, artifact_type vocabulary)
> - All 35 agent specs carry `altitude` and `phase` in frontmatter
> - Agent grid table in AGENTS.md (canonical source of truth for agent-to-5×10 mapping)
> - S9 curator checklist updated (metadata verification for artifacts)
> - Summary artifact at `state/arch/w6-5x10-refactor-summary.md`
> 
> **Estimated Effort**: Medium (documentation-only, no src/tests changes)
> **Parallel Execution**: YES — 5 waves
> **Critical Path**: T1 → T4 → T7/T8/T9 → T10 → T12 → T13 → F1-F4 → user okay

---

## Context

### Original Request
Execute W6 from ROADMAP-003: "5×10 model refactor with full agent-grid mapping" (v1-core stage, UC: NF-02, NF-03). Uses W5 validation findings as ground truth.

### Interview Summary
**Key Discussions**:
- Perplexity proposal evaluated (~80% correct; missed WORKFLOW-STANDARDS bug, AGENTS.md location, S4/S5 enforcement already exists)
- artifact_type vocabulary: formalize in MODEL-REFERENCE (define canonical list; K1/W20 handles enforcement)
- Agent grid location: root AGENTS.md (all agents load it)
- Agent frontmatter scope: all 31 remaining agents in W6
- Verification: grep-based consistency checks + Oracle review

**Research Findings**:
- S7/S8 bug exists in 3 places: MODEL-REFERENCE §7 (agent swap + phase), WORKFLOW-STANDARDS §1.1 (S8 phase), and possibly MODEL-REFERENCE §11
- WORKFLOW.md and WORKFLOW-DETAILED.md are already correct (no changes needed)
- 35 agent files; 4/35 have altitude/phase; 31 need it
- Section 13 is missing 6+ artifact types (state/changes, state/reviews, state/learnings, etc.)
- 16 artifact_type values already exist in docs/templates; vocabulary must be superset
- S4/S5 decision file enforcement already exists in agent specs — no behavioral changes needed

### Metis Review
**Identified Gaps** (addressed):
- MODEL-REFERENCE §11 (Full Agent Contract Table) may also have S7/S8 bug — added as T3
- Multi-phase agents (nowu-implementer S6+S7) need primary-phase convention — documented
- 4 sources of agent mapping risk — AGENTS.md declared as canonical source
- 16 existing artifact_type values vs. 15 proposed — vocabulary expanded to superset
- S4/S5 decision enforcement already exists — removed from scope
- Health/GAP agents need explicit classification rationale — added to T4

---

## Work Objectives

### Core Objective
Fix model document inconsistencies found in W5, expand artifact coverage, and operationalize the 5×10 model by adding altitude/phase metadata to all 35 agent specifications and creating a canonical agent grid.

### Concrete Deliverables
- `docs/model/MODEL-REFERENCE.md` — §7 S7/S8 fix, §11 verified/fixed, §13 expanded + consumption convention + artifact_type vocabulary
- `docs/model/WORKFLOW-STANDARDS.md` — §1.1 S8 phase corrected
- `.claude/agents/*.md` — all 35 files carry `altitude:` and `phase:` in frontmatter
- `AGENTS.md` — agent grid section added
- `.claude/agents/nowu-curator.md` — S9 checklist item appended
- `state/arch/w6-5x10-refactor-summary.md` — W6 summary artifact

### Definition of Done
- [ ] `grep "^altitude:" .claude/agents/*.md | wc -l` = 35
- [ ] `grep "^phase:" .claude/agents/*.md | wc -l` = 35
- [ ] S7/S8 mapping consistent across MODEL-REFERENCE §7, §11, WORKFLOW-STANDARDS §1.1, WORKFLOW.md
- [ ] No regressions: `git diff docs/WORKFLOW.md docs/WORKFLOW-DETAILED.md` = empty
- [ ] All existing artifact_type values covered by vocabulary
- [ ] Summary artifact exists at `state/arch/w6-5x10-refactor-summary.md`

### Must Have
- S7/S8 bug fixed in all affected locations (MODEL-REFERENCE §7 + §11, WORKFLOW-STANDARDS §1.1)
- All 35 agent specs have valid `altitude` and `phase` values (exact uppercase enum values)
- Agent grid table in AGENTS.md covering all 35 agents
- §13 expanded with missing artifact types
- Consumption-position convention documented in §13
- artifact_type vocabulary formalized in MODEL-REFERENCE
- S9 checklist updated with metadata verification

### Must NOT Have (Guardrails)
- **No agent behavioral changes** — do NOT change tools, model, constraints, or hard rules in any agent spec
- **No frontmatter normalization beyond altitude/phase** — do NOT add/change version, invoked_at, output_artifact_type, or epistemic_grade_output fields
- **No CLAUDE.md modifications** — CLAUDE.md has its own "Agents per Step" section; do NOT touch it
- **No WORKFLOW.md or WORKFLOW-DETAILED.md changes** — they are already correct per W5 validation
- **No PRE-WORKFLOW.md changes** — MODEL-REFERENCE §9 already has the P0-P4 mapping table
- **No template/ changes** — template updates cascade to future artifacts; defer to K1/W20
- **No scripts/ changes** — verify-artifact.py changes require tests; W6 is documentation only
- **No src/ or tests/ changes** — this is a documentation-only refactor
- **No MODEL-REFERENCE restructuring** — do NOT renumber, merge, split, or add new top-level sections
- **No S4/S5 decision enforcement changes** — decision traceability already exists in nowu-decider, nowu-shaper, and nowu-curator

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (pytest, mypy, ruff — but not applicable; W6 is docs-only)
- **Automated tests**: None (no code changes)
- **Framework**: N/A

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Documentation fixes**: Use Bash (grep) — search for patterns, verify consistency across files
- **Frontmatter additions**: Use Bash (grep) — verify fields present with valid enum values
- **Cross-reference checks**: Use Bash (grep + diff) — compare mappings between documents

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — bug fixes, MAX PARALLEL):
├── Task 1: Fix MODEL-REFERENCE §7 S7/S8 mapping [quick]
├── Task 2: Fix WORKFLOW-STANDARDS §1.1 S8 phase [quick]
└── Task 3: Check/fix MODEL-REFERENCE §11 S7/S8 [quick]

Wave 2 (After Wave 1 — classification + model expansion, MAX PARALLEL):
├── Task 4: Create agent classification table (all 35 agents) [deep]
├── Task 5: Expand Section 13 + consumption convention [unspecified-high]
└── Task 6: Add artifact_type vocabulary to MODEL-REFERENCE [unspecified-high]

Wave 3 (After Task 4 — agent frontmatter batches, MAX PARALLEL):
├── Task 7: Agent frontmatter Batch 1 — pre-workflow agents (10 files) [quick]
├── Task 8: Agent frontmatter Batch 2 — S-step + architecture agents (12 files) [quick]
└── Task 9: Agent frontmatter Batch 3 — health/GAP + orchestrator agents (9 files) [quick]

Wave 4 (After Wave 3 — integration, MAX PARALLEL):
├── Task 10: Add agent grid to AGENTS.md [unspecified-high]
└── Task 11: S9 curator checklist append [quick]

Wave 5 (After Wave 4 — verification + summary, SEQUENTIAL):
├── Task 12: Cross-reference consistency verification [deep]
└── Task 13: Write W6 summary artifact [quick]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay

Critical Path: T1 → T4 → T7/T8/T9 → T10 → T12 → T13 → F1-F4 → user okay
Parallel Speedup: ~60% faster than sequential
Max Concurrent: 3 (Waves 1-3)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| T1 | — | T4, T5, T12 | 1 |
| T2 | — | T12 | 1 |
| T3 | — | T12 | 1 |
| T4 | T1 | T7, T8, T9, T10 | 2 |
| T5 | T1 | T12 | 2 |
| T6 | — | T12 | 2 |
| T7 | T4 | T10, T12 | 3 |
| T8 | T4 | T10, T12 | 3 |
| T9 | T4 | T10, T12 | 3 |
| T10 | T7, T8, T9 | T12 | 4 |
| T11 | — | T12 | 4 |
| T12 | T1-T11 | T13 | 5 |
| T13 | T12 | F1-F4 | 5 |
| F1-F4 | T13 | — | FINAL |

### Agent Dispatch Summary

- **Wave 1**: **3** — T1 → `quick`, T2 → `quick`, T3 → `quick`
- **Wave 2**: **3** — T4 → `deep`, T5 → `unspecified-high`, T6 → `unspecified-high`
- **Wave 3**: **3** — T7 → `quick`, T8 → `quick`, T9 → `quick`
- **Wave 4**: **2** — T10 → `unspecified-high`, T11 → `quick`
- **Wave 5**: **2** — T12 → `deep`, T13 → `quick`
- **FINAL**: **4** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

### Agent Classification Reference (MANDATORY — used by T7, T8, T9, T10)

> This table is the CANONICAL altitude/phase assignment for all 35 agents.
> Task 4 will validate and refine this table by reading each agent file.
> Tasks 7-9 MUST use the validated version from T4, not this initial draft.
> Convention: multi-phase agents get their PRIMARY phase (where main work happens).

**S1-S9 Pipeline Agents:**

| Agent | Step | Altitude | Phase | Notes |
|-------|------|----------|-------|-------|
| nowu-intake | S1 | DELIVERY | IDEA | Translates ideas to intake briefs |
| nowu-constraints | S2 | ARCHITECTURE | ANALYSIS | Identifies constraints and risks |
| nowu-options | S3 | ARCHITECTURE | OPTIONS | Proposes 2-3 viable approaches |
| nowu-decider | S4 | ARCHITECTURE | DECISION | Evaluates options, records D-NNN |
| nowu-shaper | S5 | DELIVERY | EVALUATION | Breaks decision into bounded tasks |
| nowu-implementer | S6+S7 | EXECUTION | IMPLEMENTATION | Primary: implements. Also runs VBR. |
| nowu-reviewer | S8 | EXECUTION | EVALUATION | Fresh-context verification + validation |
| nowu-curator | S9 | EXECUTION | LEARN | Updates decisions, roadmap, knowledge |

**Pre-Workflow Agents:**

| Agent | Step | Altitude | Phase | Notes |
|-------|------|----------|-------|-------|
| vision-bootstrap | P0.V | STRATEGIC | DECISION | Creates/refreshes vision.md |
| signal-capture | P0.1 | STRATEGIC | IDEA | Captures raw signals and ideas |
| idea-decomposition | P0.D | PRODUCT | ANALYSIS | Decomposes ideas into components |
| use-case-agent | P0.UC | PRODUCT | PROBLEM | Maintains UC catalog |
| discovery-agent | P1 | PRODUCT | ANALYSIS | Research runs for discovery |
| perspective-interview | P1.2 | PRODUCT | ANALYSIS | Stakeholder perspective capture |
| story-mapper | P2 | DELIVERY | OPTIONS | Epic + story drafting |
| constraint-check | P3.1 | ARCHITECTURE | ANALYSIS | Architecture constraint checking |
| architecture-bootstrap | P3.2 | ARCHITECTURE | OPTIONS | Architecture bootstrap pass |
| readiness-checker | P4.1 | DELIVERY | EVALUATION | Intake readiness verification |

**SYNTHESIS + Architecture Agents:**

| Agent | Step | Altitude | Phase | Notes |
|-------|------|----------|-------|-------|
| synthesis-agent | W1 | ARCHITECTURE | SYNTHESIS | ✅ Already has altitude/phase |
| architecture-vision-agent | W2 | ARCHITECTURE | ANALYSIS | ✅ Already has altitude/phase |
| architecture-design | — | ARCHITECTURE | OPTIONS | General architecture design |
| atam-lite | — | ARCHITECTURE | EVALUATION | Architecture trade-off analysis |
| hypothesis-adr-writer | W3 | ARCHITECTURE | DECISION | Writes hypothesis ADRs |
| fitness-function-writer | W3.5 | ARCHITECTURE | VERIFICATION | Fitness function tests for ADRs |

**Health + GAP Agents:**

| Agent | Step | Altitude | Phase | Notes |
|-------|------|----------|-------|-------|
| health-vision | GAP | STRATEGIC | VERIFICATION | Checks vision health |
| health-goals | GAP | STRATEGIC | VERIFICATION | Checks goals health |
| health-architecture | GAP | ARCHITECTURE | VERIFICATION | Checks architecture health |
| health-use-cases | GAP | PRODUCT | VERIFICATION | Checks UC health |
| gap-analyst | GAP | ARCHITECTURE | ANALYSIS | Analyzes gaps |
| gap-writer | GAP | ARCHITECTURE | LEARN | Writes gap reports |
| gap-detector | GAP | ARCHITECTURE | VERIFICATION | Detects drift/gaps |

**Orchestrator + Meta Agents:**

| Agent | Step | Altitude | Phase | Notes |
|-------|------|----------|-------|-------|
| roadmap-creator | Orch | STRATEGIC | IMPLEMENTATION | ✅ Already has altitude/phase |
| roadmap-updater | Orch | STRATEGIC | LEARN | ✅ Already has altitude/phase |
| work-scheduler | Orch | STRATEGIC | EVALUATION | Read-only scheduling |
| qa-elicitation | P1 | PRODUCT | ANALYSIS | Requirements elicitation |

---

## TODOs

- [x] 1. Fix MODEL-REFERENCE §7 S7/S8 Mapping

  **What to do**:
  - Open `docs/model/MODEL-REFERENCE.md` and find the Section 7 (S1-S9 Pipeline Mapping) table
  - Replace the S7 row: change agent from `nowu-reviewer` to `VBR` (or `nowu-implementer + VBR`), keep phase as `VERIFICATION`, update description to match VBR automated gate behavior
  - Replace the S8 row: change agent from `VBR` to `nowu-reviewer`, change phase from `VERIFICATION` to `EVALUATION`, update description to match review behavior
  - Verify the surrounding prose text doesn't contradict the corrected table
  - Do NOT change any other rows or sections

  **Must NOT do**:
  - Do NOT change any other section of MODEL-REFERENCE.md
  - Do NOT renumber or restructure sections
  - Do NOT modify WORKFLOW.md or WORKFLOW-DETAILED.md (already correct)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 4, 5, 12
  - **Blocked By**: None

  **References**:
  - `docs/model/MODEL-REFERENCE.md` — Section 7, the S1-S9 pipeline mapping table. Current S7/S8 rows are WRONG (agents swapped, S8 phase wrong).
  - `state/arch/w5-5x10-validation.md:182-203` — §5.2 documents the S7/S8 mismatch with evidence from W4 practice.
  - `docs/WORKFLOW.md` — Step Reference table has the CORRECT mapping: S6+S7=nowu-implementer, S8=nowu-reviewer. Use this as ground truth.
  - `docs/WORKFLOW-DETAILED.md` — S7 section ("VBR") and S8 section ("Review") confirm correct mapping.

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: S7/S8 rows corrected in Section 7
    Tool: Bash (grep)
    Preconditions: MODEL-REFERENCE.md has been edited
    Steps:
      1. grep -A1 "| S7 " docs/model/MODEL-REFERENCE.md
      2. Verify S7 row contains "VBR" or "nowu-implementer" as agent and "VERIFICATION" as phase
      3. grep -A1 "| S8 " docs/model/MODEL-REFERENCE.md
      4. Verify S8 row contains "nowu-reviewer" as agent and "EVALUATION" as phase
    Expected Result: S7=VBR/VERIFICATION, S8=nowu-reviewer/EVALUATION
    Failure Indicators: S7 still shows nowu-reviewer, or S8 still shows VERIFICATION
    Evidence: .sisyphus/evidence/task-1-s7s8-section7-fix.txt

  Scenario: No other sections changed
    Tool: Bash (git diff)
    Preconditions: Only Section 7 should be modified
    Steps:
      1. git diff docs/model/MODEL-REFERENCE.md | grep "^@@" | wc -l
      2. Verify only 1-2 diff hunks (Section 7 area only)
    Expected Result: Changes confined to Section 7
    Failure Indicators: Diff hunks in other sections
    Evidence: .sisyphus/evidence/task-1-no-other-changes.txt
  ```

  **Commit**: YES (groups with T2, T3)
  - Message: `fix(model): correct S7/S8 mapping in MODEL-REFERENCE and WORKFLOW-STANDARDS`
  - Files: `docs/model/MODEL-REFERENCE.md`

- [x] 2. Fix WORKFLOW-STANDARDS §1.1 S8 Phase

  **What to do**:
  - Open `docs/model/WORKFLOW-STANDARDS.md` and find Rule 1.1 (S1-S9 Zigzag) table
  - Change the S8 row's phase from `VERIFICATION` to `EVALUATION`
  - Leave all other rows unchanged
  - Check if Rule 1.1 prose text below the table mentions S8 specifically — if so, ensure it says EVALUATION not VERIFICATION

  **Must NOT do**:
  - Do NOT change S7's phase (it IS correctly VERIFICATION)
  - Do NOT change any other rule section
  - Do NOT modify Rule 2.1 (Phase Contracts) — it's descriptive, not a step mapping

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 12
  - **Blocked By**: None

  **References**:
  - `docs/model/WORKFLOW-STANDARDS.md` — Rule 1.1, S1-S9 Zigzag table. Currently maps S8 to VERIFICATION (wrong). Must be EVALUATION.
  - `state/arch/w5-5x10-validation.md:182-203` — W5 §5.2: "S8: nowu-reviewer (EVALUATION)"
  - `docs/WORKFLOW.md` — Step Reference confirms S8 = Review (not VBR/Verification)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: S8 phase corrected in Rule 1.1 table
    Tool: Bash (grep)
    Preconditions: WORKFLOW-STANDARDS.md has been edited
    Steps:
      1. grep "| S8 " docs/model/WORKFLOW-STANDARDS.md
      2. Verify the line contains "EVALUATION" not "VERIFICATION"
      3. grep "| S7 " docs/model/WORKFLOW-STANDARDS.md
      4. Verify S7 still shows "VERIFICATION" (unchanged)
    Expected Result: S7=VERIFICATION, S8=EVALUATION
    Failure Indicators: S8 still shows VERIFICATION, or S7 was accidentally changed
    Evidence: .sisyphus/evidence/task-2-standards-s8-fix.txt

  Scenario: Only the S8 row changed
    Tool: Bash (git diff)
    Preconditions: Only Rule 1.1 S8 row should differ
    Steps:
      1. git diff docs/model/WORKFLOW-STANDARDS.md
      2. Count changed lines — should be 1-3 at most
    Expected Result: Minimal diff, only S8 row
    Evidence: .sisyphus/evidence/task-2-minimal-diff.txt
  ```

  **Commit**: YES (groups with T1, T3)
  - Message: (same commit as T1)
  - Files: `docs/model/WORKFLOW-STANDARDS.md`

- [x] 3. Check/Fix MODEL-REFERENCE §11 S7/S8 Consistency

  **What to do**:
  - Open `docs/model/MODEL-REFERENCE.md` and find Section 11 (Full Agent Contract Table)
  - Check if the S7/S8 agent and phase assignments match the CORRECTED values: S7=VBR/VERIFICATION, S8=nowu-reviewer/EVALUATION
  - If §11 has the same bug as §7 had, fix it to match
  - If §11 is already correct or doesn't contain S7/S8 mapping, document that in evidence

  **Must NOT do**:
  - Do NOT restructure §11
  - Do NOT add new columns or rows beyond the S7/S8 fix

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 12
  - **Blocked By**: None

  **References**:
  - `docs/model/MODEL-REFERENCE.md` — Section 11 (Full Agent Contract Table). Metis flagged this as potentially having the same S7/S8 bug as §7.
  - Task 1 output — the corrected §7 values are the target: S7=VBR/VERIFICATION, S8=nowu-reviewer/EVALUATION

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: §11 S7/S8 mapping consistent with §7
    Tool: Bash (grep)
    Preconditions: §11 has been checked and fixed if needed
    Steps:
      1. grep -A1 "S7\|S8" docs/model/MODEL-REFERENCE.md (look for §11 context)
      2. Verify S7 and S8 entries in §11 match the corrected §7 values
    Expected Result: §7 and §11 agree on S7=VBR/VERIFICATION, S8=nowu-reviewer/EVALUATION
    Failure Indicators: §11 still shows swapped agents or wrong phases
    Evidence: .sisyphus/evidence/task-3-section11-check.txt

  Scenario: No §11 entry exists (acceptable outcome)
    Tool: Bash (grep)
    Steps:
      1. Check if §11 contains S7/S8 step-level entries
      2. If §11 uses different granularity (e.g., agent-level only without step numbers), document this
    Expected Result: Either fixed or documented as N/A
    Evidence: .sisyphus/evidence/task-3-section11-structure.txt
  ```

  **Commit**: YES (groups with T1, T2)
  - Message: (same commit as T1)
  - Files: `docs/model/MODEL-REFERENCE.md` (if changed)

- [x] 4. Create Agent Classification Table (Planning Artifact)

  **What to do**:
  - Read ALL 35 agent files in `.claude/agents/` — read each file's description, step assignment (if any), and existing altitude/phase (if any)
  - Cross-reference with the draft classification in this plan's "Agent Classification Reference" section
  - Validate each assignment against:
    - MODEL-REFERENCE §7 (S1-S9 pipeline mapping — now corrected by T1)
    - MODEL-REFERENCE §9 (Pre-Workflow Mapping)
    - MODEL-REFERENCE §10 (GAP Cycle Mapping)
    - The agent's own description (e.g., "S6+S7" in nowu-implementer)
  - For multi-phase agents: assign the PRIMARY phase (where the main cognitive work happens); note secondary phases
  - For orchestrator agents marked "external to 5×10": still assign altitude/phase but add note "Orchestrator — operates outside 5×10 execution field"
  - Write the validated classification table to `.sisyphus/evidence/task-4-agent-classification.md`
  - This artifact is the INPUT for Tasks 7-9 — they MUST use this, not the draft in the plan

  **Must NOT do**:
  - Do NOT edit any agent files yet (that's Tasks 7-9)
  - Do NOT change agent descriptions, tools, or behavior
  - Do NOT skip any of the 35 agents

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 6)
  - **Blocks**: Tasks 7, 8, 9, 10
  - **Blocked By**: Task 1 (needs corrected §7 for S-step agents)

  **References**:
  - `.claude/agents/*.md` — all 35 agent files. Read EVERY file's full frontmatter and first description paragraph.
  - `docs/model/MODEL-REFERENCE.md` §7 (corrected S1-S9), §9 (P0-P4), §10 (GAP cycle), §11 (agent contracts)
  - This plan's "Agent Classification Reference" section — use as starting draft, validate against actual agent file contents
  - `docs/WORKFLOW.md` — Step Reference table for S-step agent assignments
  - `docs/PRE-WORKFLOW.md` — P0-P4 step sequence and agent assignments

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Classification covers all 35 agents
    Tool: Bash
    Steps:
      1. ls .claude/agents/*.md | wc -l  → expect 35
      2. grep -c "^|" .sisyphus/evidence/task-4-agent-classification.md → expect ≥ 35 data rows
    Expected Result: All 35 agents classified with altitude and phase
    Failure Indicators: Count mismatch or any agent missing from table
    Evidence: .sisyphus/evidence/task-4-classification-complete.txt

  Scenario: All altitude/phase values are valid enums
    Tool: Bash (grep)
    Steps:
      1. Extract altitude column from classification table
      2. Verify all values ∈ {STRATEGIC, PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION}
      3. Extract phase column
      4. Verify all values ∈ {IDEA, PROBLEM, ANALYSIS, SYNTHESIS, OPTIONS, DECISION, EVALUATION, IMPLEMENTATION, VERIFICATION, LEARN}
    Expected Result: No invalid enum values
    Evidence: .sisyphus/evidence/task-4-valid-enums.txt
  ```

  **Commit**: NO (planning artifact, not committed to repo)

- [x] 5. Expand Section 13 + Add Consumption-Position Convention

  **What to do**:
  - Open `docs/model/MODEL-REFERENCE.md` and find Section 13 (Artifact→Position Mapping)
  - Add a brief introductory note after the section heading: "Note: Section 13 maps artifacts to their canonical **consumption position** in the 5×10 grid — the altitude and phase where the artifact is primarily consumed, not necessarily where it was first authored. Example: task specs are authored during S5 (DELIVERY/EVALUATION) but consumed during S6 (EXECUTION/IMPLEMENTATION)."
  - Add the following MISSING entries to the artifact→position table:
    - `state/changes/task-NNN.md` → `EXECUTION` / `IMPLEMENTATION`
    - `state/reviews/review-NNN.md` → `EXECUTION` / `EVALUATION`
    - `state/learnings/*.md` → `(varies)` / `LEARN`
    - `state/arch/*-options.md` → `ARCHITECTURE` / `OPTIONS`
    - `state/arch/*-decision.md` → `ARCHITECTURE` / `DECISION`
    - `state/session-log.md` → `STRATEGIC` / `LEARN`
  - Update the existing `state/analysis/session-review-*.md` entry to also cover `state/analysis/S*-*.md` (step analysis files) — or add a separate entry
  - Update `docs/ROADMAP-001.md` entry to `docs/ROADMAP-NNN.md` (there are now ROADMAP-003)
  - Do NOT change any other section

  **Must NOT do**:
  - Do NOT restructure §13
  - Do NOT remove any existing entries
  - Do NOT add entries for code files (src/, tests/) — those don't carry YAML frontmatter

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 6)
  - **Blocks**: Task 12
  - **Blocked By**: Task 1 (needs corrected §7 to ensure §13 review phase for review artifacts matches)

  **References**:
  - `docs/model/MODEL-REFERENCE.md` — Section 13 (20 existing rows). Full current content retrieved by explore agent.
  - `state/arch/w5-5x10-validation.md:232-254` — §5.5 and §5.6 document the missing entries and propose additions.
  - `state/arch/w5-5x10-validation.md:205-218` — §5.3 documents the consumption-position convention (D-SESS-01).
  - `state/learnings/session-2026-05-14-w5-5x10-validation.md` — D-SESS-01: "artifacts are tagged with the altitude/phase where they are consumed"

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All missing entries added
    Tool: Bash (grep)
    Steps:
      1. grep "state/changes" docs/model/MODEL-REFERENCE.md → expect 1+ match
      2. grep "state/reviews" docs/model/MODEL-REFERENCE.md → expect 1+ match
      3. grep "state/learnings" docs/model/MODEL-REFERENCE.md → expect 1+ match
      4. grep "consumption" docs/model/MODEL-REFERENCE.md → expect 1+ match (convention note)
    Expected Result: All 4 searches return matches
    Failure Indicators: Any search returns 0 matches
    Evidence: .sisyphus/evidence/task-5-section13-expanded.txt

  Scenario: Existing entries preserved
    Tool: Bash (grep)
    Steps:
      1. grep "state/tasks/task" docs/model/MODEL-REFERENCE.md → expect match
      2. grep "state/vbr" docs/model/MODEL-REFERENCE.md → expect match
      3. grep "docs/vision.md" docs/model/MODEL-REFERENCE.md → expect match
    Expected Result: All existing entries still present
    Evidence: .sisyphus/evidence/task-5-no-deletions.txt
  ```

  **Commit**: YES (groups with T6)
  - Message: `docs(model): expand Section 13 coverage and formalize artifact_type vocabulary`
  - Files: `docs/model/MODEL-REFERENCE.md`

- [x] 6. Add artifact_type Vocabulary to MODEL-REFERENCE

  **What to do**:
  - Open `docs/model/MODEL-REFERENCE.md`
  - Add a new subsection within or immediately after Section 13: "### 13.1 Canonical artifact_type Vocabulary" (or "### Artifact Type Vocabulary" as a subsection — do NOT create a new top-level section)
  - First: survey all existing `artifact_type` values currently used in the repo by running: `grep -rh "^artifact_type:" docs/ templates/ state/ | sort -u`
  - Then: create a canonical vocabulary table that is a SUPERSET of all existing values AND the W5 proposed terms
  - The table should have columns: artifact_type | Used By (directory pattern) | Section 13 Position | Example
  - Include at minimum these types (merge overlapping terms):
    - From W5 proposal: INTAKE_BRIEF, CONSTRAINTS_SHEET, OPTIONS_SHEET, DECISION_RECORD, TASK_SPEC, CHANGESET, VBR_REPORT, REVIEW_REPORT, CAPTURE_RECORD, SESSION_ANALYSIS, SESSION_LEARNINGS
    - From existing usage (survey first): ROADMAP, ARCHITECTURE_VISION, SYNTHESIS, GOAL, ADR, EPIC, USE_CASE, PROBLEM, IDEA, LESSON, HANDOFF, RESEARCH_INDEX, SESSION_LOG, LEARNINGS_INDEX (+ any others found)
  - Add a note: "Enforcement: K1/W20 will apply these types to existing artifacts. W6 formalizes the vocabulary only."

  **Must NOT do**:
  - Do NOT apply artifact_type to existing artifacts (that's K1/W20)
  - Do NOT create a new top-level section (keep as §13 subsection)
  - Do NOT remove any currently-used artifact_type value from the vocabulary

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5)
  - **Blocks**: Task 12
  - **Blocked By**: None

  **References**:
  - `state/arch/w5-5x10-validation.md:272-292` — §7: W5 proposed vocabulary (11 terms for S1-S9 pipeline)
  - `templates/artifact-5x10.md` — template has `artifact_type: GOAL | USE_CASE | ADR | SYNTHESIS | LESSON`
  - All `state/`, `docs/`, `templates/` files — survey existing artifact_type values via grep
  - Metis finding: 16 values already exist in the wild; vocabulary must be superset

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Vocabulary table exists in MODEL-REFERENCE
    Tool: Bash (grep)
    Steps:
      1. grep -i "artifact.type vocabulary\|canonical.*artifact" docs/model/MODEL-REFERENCE.md
      2. Verify a vocabulary table with columns exists
    Expected Result: Vocabulary subsection found
    Evidence: .sisyphus/evidence/task-6-vocab-exists.txt

  Scenario: All existing artifact_type values covered
    Tool: Bash
    Steps:
      1. grep -rh "^artifact_type:" docs/ templates/ state/ | sort -u > /tmp/existing_types.txt
      2. For each value in /tmp/existing_types.txt, grep MODEL-REFERENCE for that value
      3. No existing value should be missing from the vocabulary
    Expected Result: Every existing artifact_type value appears in the vocabulary
    Failure Indicators: Any existing value not found in vocabulary table
    Evidence: .sisyphus/evidence/task-6-vocab-coverage.txt
  ```

  **Commit**: YES (groups with T5)
  - Message: (same commit as T5)
  - Files: `docs/model/MODEL-REFERENCE.md`

- [x] 7. Agent Frontmatter Batch 1 — Pre-Workflow Agents (10 files)

  **What to do**:
  - Read the VALIDATED classification table from `.sisyphus/evidence/task-4-agent-classification.md` (Task 4 output)
  - For each of the 10 pre-workflow agents listed below, add `altitude:` and `phase:` lines to the file's frontmatter
  - Placement rule: add `altitude:` and `phase:` AFTER the existing `description:` line (or after `name:` if no description). Do NOT change any other field.
  - Use EXACT uppercase enum values from the classification table. No lowercase, no abbreviations.
  - Files to modify (10):
    1. `.claude/agents/vision-bootstrap.md`
    2. `.claude/agents/signal-capture.md`
    3. `.claude/agents/idea-decomposition.md`
    4. `.claude/agents/use-case-agent.md`
    5. `.claude/agents/discovery-agent.md`
    6. `.claude/agents/perspective-interview.md`
    7. `.claude/agents/story-mapper.md`
    8. `.claude/agents/constraint-check.md`
    9. `.claude/agents/architecture-bootstrap.md`
    10. `.claude/agents/readiness-checker.md`

  **Must NOT do**:
  - Do NOT change agent descriptions, tools, model, memory, or constraints
  - Do NOT add any fields beyond `altitude` and `phase`
  - Do NOT change existing altitude/phase if an agent already has it (none of these 10 do)
  - Do NOT use values not in the Task 4 classification table

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 8, 9)
  - **Blocks**: Tasks 10, 12
  - **Blocked By**: Task 4

  **References**:
  - `.sisyphus/evidence/task-4-agent-classification.md` — MANDATORY: use this validated classification, NOT the draft in the plan
  - `.claude/agents/roadmap-creator.md` — example of an agent that already has altitude/phase frontmatter. Use as format reference.
  - This plan's "Agent Classification Reference" → "Pre-Workflow Agents" table — fallback reference only if T4 matches exactly

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All 10 pre-workflow agents have altitude/phase
    Tool: Bash (grep)
    Steps:
      1. for f in vision-bootstrap signal-capture idea-decomposition use-case-agent discovery-agent perspective-interview story-mapper constraint-check architecture-bootstrap readiness-checker; do echo "==$f=="; grep "^altitude:\|^phase:" .claude/agents/$f.md; done
      2. Verify each file shows exactly 1 altitude: line and 1 phase: line
    Expected Result: 10 agents × 2 fields = 20 lines of output
    Failure Indicators: Any agent missing altitude or phase, or showing 0 or 2+ of either
    Evidence: .sisyphus/evidence/task-7-preworkflow-frontmatter.txt

  Scenario: No other fields changed
    Tool: Bash (git diff)
    Steps:
      1. git diff .claude/agents/vision-bootstrap.md .claude/agents/signal-capture.md .claude/agents/idea-decomposition.md .claude/agents/use-case-agent.md .claude/agents/discovery-agent.md .claude/agents/perspective-interview.md .claude/agents/story-mapper.md .claude/agents/constraint-check.md .claude/agents/architecture-bootstrap.md .claude/agents/readiness-checker.md
      2. Verify each file's diff contains ONLY added altitude/phase lines (no deletions, no modifications to other lines)
    Expected Result: Only "+" lines for altitude: and phase: in each diff
    Failure Indicators: Any "-" lines or changes to existing content
    Evidence: .sisyphus/evidence/task-7-no-other-changes.txt
  ```

  **Commit**: YES (groups with T8, T9)
  - Message: `docs(agents): add altitude/phase frontmatter to all 31 agent specs`
  - Files: 10 files listed above

- [x] 8. Agent Frontmatter Batch 2 — S-Step + Architecture Agents (12 files)

  **What to do**:
  - Read the VALIDATED classification table from `.sisyphus/evidence/task-4-agent-classification.md` (Task 4 output)
  - For each of the 12 agents listed below, add `altitude:` and `phase:` lines to the file's frontmatter
  - Same placement rule as Task 7: after `description:` or `name:`, do NOT change any other field
  - Use EXACT uppercase enum values from the classification table
  - Files to modify (12):
    **S-Step agents (8):**
    1. `.claude/agents/nowu-intake.md`
    2. `.claude/agents/nowu-constraints.md`
    3. `.claude/agents/nowu-options.md`
    4. `.claude/agents/nowu-decider.md`
    5. `.claude/agents/nowu-shaper.md`
    6. `.claude/agents/nowu-implementer.md`
    7. `.claude/agents/nowu-reviewer.md`
    8. `.claude/agents/nowu-curator.md`
    **Architecture agents (4):**
    9. `.claude/agents/architecture-design.md`
    10. `.claude/agents/atam-lite.md`
    11. `.claude/agents/hypothesis-adr-writer.md`
    12. `.claude/agents/fitness-function-writer.md`
  - NOTE: `synthesis-agent.md` and `architecture-vision-agent.md` already have altitude/phase — do NOT touch them

  **Must NOT do**:
  - Do NOT change agent descriptions, tools, model, memory, or constraints
  - Do NOT touch synthesis-agent.md or architecture-vision-agent.md (already have frontmatter)
  - Do NOT add any fields beyond `altitude` and `phase`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 7, 9)
  - **Blocks**: Tasks 10, 12
  - **Blocked By**: Task 4

  **References**:
  - `.sisyphus/evidence/task-4-agent-classification.md` — MANDATORY: use this validated classification
  - `.claude/agents/synthesis-agent.md` — example of existing altitude/phase in an architecture agent
  - This plan's "Agent Classification Reference" → "S1-S9 Pipeline Agents" and "SYNTHESIS + Architecture Agents" tables — fallback

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All 12 S-step + architecture agents have altitude/phase
    Tool: Bash (grep)
    Steps:
      1. for f in nowu-intake nowu-constraints nowu-options nowu-decider nowu-shaper nowu-implementer nowu-reviewer nowu-curator architecture-design atam-lite hypothesis-adr-writer fitness-function-writer; do echo "==$f=="; grep "^altitude:\|^phase:" .claude/agents/$f.md; done
      2. Verify each file shows exactly 1 altitude: line and 1 phase: line
    Expected Result: 12 agents × 2 fields = 24 lines of output
    Failure Indicators: Any agent missing altitude or phase
    Evidence: .sisyphus/evidence/task-8-sstep-arch-frontmatter.txt

  Scenario: synthesis-agent and architecture-vision-agent untouched
    Tool: Bash (git diff)
    Steps:
      1. git diff .claude/agents/synthesis-agent.md .claude/agents/architecture-vision-agent.md
      2. Verify empty diff (no changes)
    Expected Result: No changes to already-correct files
    Evidence: .sisyphus/evidence/task-8-existing-untouched.txt
  ```

  **Commit**: YES (groups with T7, T9)
  - Message: (same commit as T7)
  - Files: 12 files listed above

- [x] 9. Agent Frontmatter Batch 3 — Health/GAP + Orchestrator Agents (9 files)

  **What to do**:
  - Read the VALIDATED classification table from `.sisyphus/evidence/task-4-agent-classification.md` (Task 4 output)
  - For each of the 9 agents listed below, add `altitude:` and `phase:` lines to the file's frontmatter
  - Same placement rule as Tasks 7-8
  - Use EXACT uppercase enum values from the classification table
  - Files to modify (9):
    **Health agents (4):**
    1. `.claude/agents/health-vision.md`
    2. `.claude/agents/health-goals.md`
    3. `.claude/agents/health-architecture.md`
    4. `.claude/agents/health-use-cases.md`
    **GAP agents (3):**
    5. `.claude/agents/gap-analyst.md`
    6. `.claude/agents/gap-writer.md`
    7. `.claude/agents/gap-detector.md`
    **Orchestrator/Meta agents (2):**
    8. `.claude/agents/work-scheduler.md`
    9. `.claude/agents/qa-elicitation.md`
  - NOTE: `roadmap-creator.md` and `roadmap-updater.md` already have altitude/phase — do NOT touch them

  **Must NOT do**:
  - Do NOT change agent descriptions, tools, model, memory, or constraints
  - Do NOT touch roadmap-creator.md or roadmap-updater.md (already have frontmatter)
  - Do NOT add any fields beyond `altitude` and `phase`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 7, 8)
  - **Blocks**: Tasks 10, 12
  - **Blocked By**: Task 4

  **References**:
  - `.sisyphus/evidence/task-4-agent-classification.md` — MANDATORY: use this validated classification
  - `.claude/agents/roadmap-creator.md` — example of existing altitude/phase in an orchestrator agent
  - This plan's "Agent Classification Reference" → "Health + GAP Agents" and "Orchestrator + Meta Agents" tables — fallback

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All 9 health/GAP/orchestrator agents have altitude/phase
    Tool: Bash (grep)
    Steps:
      1. for f in health-vision health-goals health-architecture health-use-cases gap-analyst gap-writer gap-detector work-scheduler qa-elicitation; do echo "==$f=="; grep "^altitude:\|^phase:" .claude/agents/$f.md; done
      2. Verify each file shows exactly 1 altitude: line and 1 phase: line
    Expected Result: 9 agents × 2 fields = 18 lines of output
    Failure Indicators: Any agent missing altitude or phase
    Evidence: .sisyphus/evidence/task-9-health-gap-orch-frontmatter.txt

  Scenario: roadmap-creator and roadmap-updater untouched
    Tool: Bash (git diff)
    Steps:
      1. git diff .claude/agents/roadmap-creator.md .claude/agents/roadmap-updater.md
      2. Verify empty diff (no changes)
    Expected Result: No changes to already-correct files
    Evidence: .sisyphus/evidence/task-9-existing-untouched.txt
  ```

  **Commit**: YES (groups with T7, T8)
  - Message: (same commit as T7)
  - Files: 9 files listed above

- [x] 10. Add Agent Grid to AGENTS.md

  **What to do**:
  - Open `AGENTS.md` (repo root, currently ~245 lines, no agent grid)
  - Add a new section: `## Agent Grid — 5×10 Model Mapping`
  - The section should contain:
    1. A brief intro: "Canonical mapping of all 35 agents to 5×10 altitude/phase positions. This table is the single source of truth for agent-to-grid assignments. Agent frontmatter `altitude:` and `phase:` fields mirror this table."
    2. A table with columns: Agent | File | Step | Altitude | Phase | Notes
    3. All 35 agents in the table, organized by group (S1-S9 Pipeline, Pre-Workflow, SYNTHESIS + Architecture, Health/GAP, Orchestrator)
    4. Group headers as sub-rows or sub-sections within the table
  - Source data: MUST use `.sisyphus/evidence/task-4-agent-classification.md` (validated by T4)
  - Cross-check: verify against the frontmatter actually written by T7-T9 (read a few files to spot-check)
  - Place the new section AFTER the existing "## Structure" section and BEFORE any "## Gotchas" or similar section. If unsure of placement, add at the end before any trailing content.

  **Must NOT do**:
  - Do NOT change any existing section of AGENTS.md
  - Do NOT remove the existing content
  - Do NOT add the grid to docs/AGENTS.md (wrong location — it's at repo root)
  - Do NOT add tool lists, model names, or behavioral descriptions to the grid (keep it position-focused)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Task 11)
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 7, 8, 9 (needs frontmatter written to verify consistency)

  **References**:
  - `AGENTS.md` — repo root file, ~245 lines. Read entire file to find correct insertion point.
  - `.sisyphus/evidence/task-4-agent-classification.md` — MANDATORY: source of truth for grid data
  - `.claude/agents/*.md` — spot-check 3-5 files to verify frontmatter matches classification

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Agent grid exists in AGENTS.md with all 35 agents
    Tool: Bash (grep)
    Steps:
      1. grep -c "Agent Grid" AGENTS.md → expect 1
      2. grep "|" AGENTS.md | grep -E "STRATEGIC|PRODUCT|ARCHITECTURE|DELIVERY|EXECUTION" | wc -l → expect ≥ 35
    Expected Result: Grid section exists with 35+ data rows
    Failure Indicators: Grid missing or fewer than 35 agent rows
    Evidence: .sisyphus/evidence/task-10-grid-exists.txt

  Scenario: Grid matches agent frontmatter (spot check 5 agents)
    Tool: Bash (grep)
    Steps:
      1. Pick 5 agents across different groups: nowu-implementer, vision-bootstrap, health-architecture, gap-analyst, work-scheduler
      2. For each: extract altitude from frontmatter (grep "^altitude:" .claude/agents/{name}.md)
      3. For each: extract altitude from AGENTS.md grid row (grep "{name}" AGENTS.md)
      4. Compare — must match
    Expected Result: All 5 spot-checked agents have matching altitude/phase in frontmatter and grid
    Failure Indicators: Any mismatch between frontmatter and grid
    Evidence: .sisyphus/evidence/task-10-grid-frontmatter-consistency.txt

  Scenario: No existing AGENTS.md content removed
    Tool: Bash (git diff)
    Steps:
      1. git diff AGENTS.md | grep "^-" | grep -v "^---" | wc -l
      2. Expect 0 deleted lines (only additions)
    Expected Result: Zero deletions from existing content
    Evidence: .sisyphus/evidence/task-10-no-deletions.txt
  ```

  **Commit**: YES (groups with T11)
  - Message: `docs(agents): add agent grid to AGENTS.md, update S9 checklist, W6 summary`
  - Files: `AGENTS.md`

- [x] 11. S9 Curator Checklist Append

  **What to do**:
  - Open `.claude/agents/nowu-curator.md`
  - Find the S9 capture/curation checklist (look for a numbered or bulleted list of verification steps)
  - Append ONE new item: "Verify all produced artifacts carry correct `artifact_type`, `altitude`, and `phase` in YAML frontmatter (per MODEL-REFERENCE §13 vocabulary)"
  - This is a small, surgical addition — one line added to an existing checklist

  **Must NOT do**:
  - Do NOT change any existing checklist items
  - Do NOT modify tools, model, memory, or constraints
  - Do NOT restructure the agent file
  - Do NOT add the altitude/phase frontmatter here (that's Task 8)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Task 10)
  - **Blocks**: Task 12
  - **Blocked By**: None (can technically start earlier, but grouped with Wave 4 for commit coherence)

  **References**:
  - `.claude/agents/nowu-curator.md` — S9 curator agent. Look for the checklist/verification section.
  - `state/arch/w5-5x10-validation.md:262-270` — W5 §6 recommended S9 checklist update
  - `docs/model/MODEL-REFERENCE.md` §13 — the vocabulary that the new checklist item references

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: New checklist item added to nowu-curator
    Tool: Bash (grep)
    Steps:
      1. grep -i "artifact_type\|frontmatter" .claude/agents/nowu-curator.md
      2. Verify at least 1 line mentions verifying artifact metadata
    Expected Result: New checklist item found
    Failure Indicators: No mention of artifact_type or frontmatter verification
    Evidence: .sisyphus/evidence/task-11-curator-checklist.txt

  Scenario: Only 1-2 lines added (minimal change)
    Tool: Bash (git diff)
    Steps:
      1. git diff .claude/agents/nowu-curator.md | grep "^+" | grep -v "^+++" | wc -l
      2. Expect 1-3 added lines maximum
    Expected Result: Minimal surgical addition
    Evidence: .sisyphus/evidence/task-11-minimal-diff.txt
  ```

  **Commit**: YES (groups with T10)
  - Message: (same commit as T10)
  - Files: `.claude/agents/nowu-curator.md`

- [x] 12. Cross-Reference Consistency Verification

  **What to do**:
  - This is a VERIFICATION task, not an editing task. Run checks, produce a report.
  - Run ALL verification commands from "Success Criteria" section (AC-1 through AC-7):
    1. S7/S8 consistency: grep S7/S8 across MODEL-REFERENCE, WORKFLOW-STANDARDS, WORKFLOW.md, WORKFLOW-DETAILED.md — all 4 must agree
    2. All 35 agents have altitude/phase: `grep -c "^altitude:" .claude/agents/*.md` = 35 files showing :1
    3. All altitude values valid: no values outside {STRATEGIC, PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION}
    4. All phase values valid: no values outside {IDEA, PROBLEM, ANALYSIS, SYNTHESIS, OPTIONS, DECISION, EVALUATION, IMPLEMENTATION, VERIFICATION, LEARN}
    5. No forbidden file changes: git diff on WORKFLOW.md, WORKFLOW-DETAILED.md, PRE-WORKFLOW.md, CLAUDE.md, src/, tests/, scripts/, templates/
    6. AGENTS.md grid matches agent frontmatter: for ALL 35 agents, compare grid altitude/phase with frontmatter altitude/phase
    7. Section 13 has consumption-position note and all planned entries
    8. artifact_type vocabulary covers all existing values
  - Write a verification report to `.sisyphus/evidence/task-12-consistency-report.md`
  - If ANY check fails: document the failure with file:line, expected vs actual, and severity (BLOCKER / WARNING)
  - If all checks pass: document as PASS with evidence

  **Must NOT do**:
  - Do NOT fix issues found — report them only (fixes require revisiting earlier tasks)
  - Do NOT skip any check

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 5 (sequential, runs first)
  - **Blocks**: Task 13
  - **Blocked By**: Tasks 1-11 (ALL must be complete)

  **References**:
  - This plan's "Success Criteria" section — AC-1 through AC-7 verification commands
  - All modified files from T1-T11 — read and verify each
  - `.sisyphus/evidence/task-4-agent-classification.md` — compare against actual frontmatter

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verification report exists and is comprehensive
    Tool: Bash
    Steps:
      1. test -f .sisyphus/evidence/task-12-consistency-report.md && echo "EXISTS"
      2. grep -c "PASS\|FAIL\|BLOCKER\|WARNING" .sisyphus/evidence/task-12-consistency-report.md → expect ≥ 8 (one per check)
    Expected Result: Report exists with 8+ check results
    Failure Indicators: Report missing or incomplete
    Evidence: .sisyphus/evidence/task-12-report-exists.txt

  Scenario: All checks PASS (ideal outcome)
    Tool: Bash (grep)
    Steps:
      1. grep "BLOCKER" .sisyphus/evidence/task-12-consistency-report.md | wc -l
      2. Expect 0 BLOCKER entries
    Expected Result: Zero blockers
    Failure Indicators: Any BLOCKER found → earlier tasks need revisiting
    Evidence: .sisyphus/evidence/task-12-zero-blockers.txt
  ```

  **Commit**: NO (verification artifact, not committed to repo)

- [x] 13. Write W6 Summary Artifact

  **What to do**:
  - Create `state/arch/w6-5x10-refactor-summary.md` as the W6 completion artifact
  - Use the standard artifact template structure (YAML frontmatter + sections)
  - Frontmatter:
    ```
    ---
    artifact_type: WORK_SUMMARY
    status: COMPLETE
    created_at: [current date]
    workstream: W6
    stage: v1-core
    depends_on: [W4, W5]
    uc_links: [NF-02, NF-03]
    ---
    ```
  - Sections:
    1. **Summary**: 2-3 sentences on what W6 accomplished
    2. **Changes Made**: List ALL files modified with 1-line description each
    3. **Bugs Fixed**: S7/S8 mapping (3 locations)
    4. **New Content**: Section 13 expansion, artifact_type vocabulary, agent grid, agent frontmatter
    5. **Process Updates**: S9 checklist item
    6. **Verification Results**: Reference task-12 report, summarize pass/fail
    7. **Deferred Items**: Explicitly list what was NOT done and why (K1/W20 enforcement, template updates, etc.)
    8. **Impact on Next Work**: How W6 changes affect S1-S9 workflow, GAP cycle, agent invocation
  - Cross-reference the task-12 verification report for accuracy

  **Must NOT do**:
  - Do NOT claim changes that weren't verified by T12
  - Do NOT omit deferred items
  - Do NOT overstate impact

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 5 (sequential, runs after T12)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 12

  **References**:
  - `.sisyphus/evidence/task-12-consistency-report.md` — verification results (MUST read before writing summary)
  - `state/arch/w5-5x10-validation.md` — example of a similar W-step summary artifact (format reference)
  - This plan's "Work Objectives" and "Must Have" sections — checklist of what should be summarized
  - `docs/ROADMAP-003.md` — W6 definition for accurate scope description

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Summary artifact exists with correct frontmatter
    Tool: Bash (grep)
    Steps:
      1. test -f state/arch/w6-5x10-refactor-summary.md && echo "EXISTS"
      2. grep "artifact_type:" state/arch/w6-5x10-refactor-summary.md
      3. grep "status: COMPLETE" state/arch/w6-5x10-refactor-summary.md
      4. grep "workstream: W6" state/arch/w6-5x10-refactor-summary.md
    Expected Result: File exists with correct frontmatter fields
    Failure Indicators: File missing or frontmatter incomplete
    Evidence: .sisyphus/evidence/task-13-summary-exists.txt

  Scenario: All required sections present
    Tool: Bash (grep)
    Steps:
      1. grep -c "^##" state/arch/w6-5x10-refactor-summary.md → expect ≥ 7 sections
      2. grep "Changes Made\|Bugs Fixed\|Deferred" state/arch/w6-5x10-refactor-summary.md
    Expected Result: All 7+ sections present
    Evidence: .sisyphus/evidence/task-13-sections-complete.txt

  Scenario: Deferred items documented
    Tool: Bash (grep)
    Steps:
      1. grep -i "defer\|K1\|W20" state/arch/w6-5x10-refactor-summary.md
      2. Verify explicit mention of deferred K1/W20 enforcement
    Expected Result: Deferred scope explicitly documented
    Evidence: .sisyphus/evidence/task-13-deferred-documented.txt
  ```

  **Commit**: YES (groups with T10, T11)
  - Message: (same commit as T10)
  - Files: `state/arch/w6-5x10-refactor-summary.md`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
>
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (grep, read file). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `grep` consistency checks across all modified docs. Review all changed files for: internal contradictions, broken cross-references, duplicate information, inconsistent terminology. Check that no agent behavioral changes were made (tools, model, constraints unchanged in git diff).
  Output: `Docs [N consistent/N issues] | Agents [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high`
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration: pick 3 random agents and verify their AGENTS.md grid row matches their frontmatter altitude/phase. Test edge cases: check multi-phase agents, orchestrators, health agents.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git diff). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance: no CLAUDE.md changes, no WORKFLOW.md changes, no template changes, no scripts changes, no src/tests changes. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Forbidden [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Commit 1** (after Wave 1): `fix(model): correct S7/S8 mapping in MODEL-REFERENCE and WORKFLOW-STANDARDS`
  - Files: `docs/model/MODEL-REFERENCE.md`, `docs/model/WORKFLOW-STANDARDS.md`
  - Pre-commit: `grep -c "EVALUATION" docs/model/MODEL-REFERENCE.md docs/model/WORKFLOW-STANDARDS.md`

- **Commit 2** (after Wave 2): `docs(model): expand Section 13 coverage and formalize artifact_type vocabulary`
  - Files: `docs/model/MODEL-REFERENCE.md`

- **Commit 3** (after Wave 3): `docs(agents): add altitude/phase frontmatter to all 31 agent specs`
  - Files: `.claude/agents/*.md` (31 files)
  - Pre-commit: `grep -c "^altitude:" .claude/agents/*.md | tail -1` (should show 35 total)

- **Commit 4** (after Wave 4+5): `docs(agents): add agent grid to AGENTS.md, update S9 checklist, W6 summary`
  - Files: `AGENTS.md`, `.claude/agents/nowu-curator.md`, `state/arch/w6-5x10-refactor-summary.md`

---

## Success Criteria

### Verification Commands
```bash
# AC-1: S7/S8 consistency across all model docs
grep -A2 "S7\|S8" docs/model/MODEL-REFERENCE.md docs/model/WORKFLOW-STANDARDS.md
# Expected: S7=VBR/VERIFICATION, S8=nowu-reviewer/EVALUATION in all sources

# AC-2: All 35 agents have altitude/phase
grep -c "^altitude:" .claude/agents/*.md | grep -v ":1$"
# Expected: empty (all files show exactly 1 match)

# AC-3: All altitude values valid
grep "^altitude:" .claude/agents/*.md | grep -vE "(STRATEGIC|PRODUCT|ARCHITECTURE|DELIVERY|EXECUTION)"
# Expected: empty

# AC-4: All phase values valid
grep "^phase:" .claude/agents/*.md | grep -vE "(IDEA|PROBLEM|ANALYSIS|SYNTHESIS|OPTIONS|DECISION|EVALUATION|IMPLEMENTATION|VERIFICATION|LEARN)"
# Expected: empty

# AC-5: No forbidden file changes
git diff --name-only docs/WORKFLOW.md docs/WORKFLOW-DETAILED.md docs/PRE-WORKFLOW.md src/ tests/ scripts/ templates/ CLAUDE.md
# Expected: empty

# AC-6: Summary artifact exists
test -f state/arch/w6-5x10-refactor-summary.md && echo "EXISTS"
# Expected: EXISTS

# AC-7: Agent grid completeness (35 agents in grid)
grep -c "^|" AGENTS.md  # Count grid rows — should be ≥ 35 data rows
```
