# Living Orientation System: Proper Roadmap + Session Dashboard

## TL;DR

> **Quick Summary**: Rewrite the project roadmap as ROADMAP-003.md with full traceability (vision → goals → UCs → SYNTHESIS → work items) and the 7-section structure the work-scheduler expects, then build the supporting orientation artifacts (session-log dashboard, goal backfill, research triage, intake audit).
> 
> **Deliverables**:
> - ROADMAP-003.md — canonical roadmap following roadmap-creator's 7-section contract
> - Enhanced session-log.md — status dashboard section prepended
> - Goal backfill — UC Mapping and Phase Coverage populated in goal-001..004.md
> - Research triage — 5 unprocessed sessions classified in INDEX.md
> - Intake audit report — staleness assessment for intake-002..006
> - ROADMAP-001/002 marked SUPERSEDED
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Task 1 (ROADMAP-003) → Task 3 (Goal Backfill) → Task 4 (Session-Log Dashboard) → Task 5 (Research Triage) → Final Verification

---

## Context

### Original Request
Create a "proper roadmap" that covers all relevant artifacts (SYNTHESIS-001, ARCHITECTURE-VISION, vision.md, USE_CASES.md). Current ROADMAP-001 was created as a side-note and doesn't follow the roadmap-creator's expected structure. Also need a session-log that captures where we are, what we did, and why. Consider unprocessed learnings.

### Interview Summary
**Key Discussions**:
- User wants a "living orientation system" — connected artifacts that answer "where are we, what's next, and why"
- Current ROADMAP-001 lacks UC-to-Stage Mapping, Goal Traceability, and the 7-section structure the work-scheduler expects
- ROADMAP-002 was agent-generated but never finalized (8 pending changes)
- Session-log needs a status dashboard section (human-readable work-scheduler equivalent)
- Goals have empty UC Mapping and Phase Coverage sections
- 5 unprocessed research sessions may affect priorities
- Stale artifact cleanup is explicitly DEFERRED

**Research Findings**:
- D-022 defines 3 orchestrator meta-agents (roadmap-creator, roadmap-updater, work-scheduler)
- work-scheduler reads ROADMAP Section 4 (Dependency Graph), Section 5 (Stage Gates), Section 7 (Current Work Item)
- roadmap-creator expects 7 numbered sections with specific headings
- ROADMAP-002 already has UC Coverage Matrix and Goal Traceability populated (useful reference)
- Intakes 002-006 are at `READY_FOR_ARCH` status
- SYNTHESIS-001 maps all 50 UCs to 9 themes with explicit UC→theme tables

### Metis Review
**Identified Gaps** (addressed):
- ROADMAP-001/002 must be marked SUPERSEDED as correctness requirement for work-scheduler (not cleanup)
- Section numbering is a machine-parseable contract — must match spec exactly
- UC→Goal mapping requires interpretation via SYNTHESIS themes, not mechanical copying
- ROADMAP-002's 8 pending changes need disposition tracking in ROADMAP-003
- Circular dependency: ROADMAP-003 must be written before session-log dashboard
- Goal backfill is additive only — no status changes to `proposed` goals

---

## Work Objectives

### Core Objective
Build a coherent orientation system where the roadmap serves both human readers and the work-scheduler agent, connected to supporting artifacts (session-log, goals) that together answer "where are we, what's next, and why."

### Concrete Deliverables
- `docs/ROADMAP-003.md` — 7-section roadmap with full traceability chain
- `state/session-log.md` — enhanced with Status Dashboard section
- `docs/goals/goal-001.md` through `goal-004.md` — UC Mapping and Phase Coverage populated
- `docs/research/INDEX.md` — all entries marked Processed: Yes
- `state/intake/INTAKE-AUDIT-REPORT.md` — staleness assessment
- `docs/ROADMAP-001.md` and `docs/ROADMAP-002.md` — marked SUPERSEDED

### Definition of Done
- [ ] `grep -c "^## [0-9]\." docs/ROADMAP-003.md` returns exactly `7`
- [ ] ROADMAP-003 YAML frontmatter contains: `artifact_type: ROADMAP`, `version: 3`, `status: ACTIVE`
- [ ] `grep "SUPERSEDED" docs/ROADMAP-001.md` returns a match
- [ ] `grep "SUPERSEDED" docs/ROADMAP-002.md` returns a match
- [ ] Each goal-00N.md UC Mapping table has > 0 data rows
- [ ] `grep "## Status Dashboard" state/session-log.md` returns a match
- [ ] `grep -c "No$" docs/research/INDEX.md` returns `0` (no unprocessed entries)
- [ ] `state/intake/INTAKE-AUDIT-REPORT.md` exists and references intake-002..006

### Must Have
- ROADMAP-003 sections numbered 1-7 matching roadmap-creator spec verbatim
- UC-to-Stage Mapping covering all 50 UCs
- Goal-to-UC linkage via SYNTHESIS themes
- Dependency Graph parseable by work-scheduler
- Stage Gate Criteria with boolean checklists
- Session-log dashboard with: current stage, milestones, blocked items, next action
- All 5 unprocessed research sessions triaged
- Intake audit report with per-intake staleness verdict

### Must NOT Have (Guardrails)
- Do NOT modify any existing session-log entries
- Do NOT change goal `status: proposed` during backfill
- Do NOT create new ADRs, decisions, or epics
- Do NOT modify intake files during audit (report only)
- Do NOT restructure goals to accommodate UC mapping difficulties — use "Unmapped UCs" footnote
- Do NOT invent new work-item IDs that break existing cross-references in intakes/tasks/session-log
- Do NOT act on research findings (classification only — flag priority impacts)
- Do NOT merge session-log entries or restructure the chronological log
- Do NOT modify upstream artifacts (vision.md, USE_CASES.md, SYNTHESIS-001.md, ARCHITECTURE-VISION.md)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (pytest + mypy + ruff)
- **Automated tests**: None — this is documentation-only work, no code changes
- **Framework**: N/A

### QA Policy
Every task includes agent-executed QA scenarios using Bash (grep/read verification).
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Documentation artifacts**: Use Bash (grep/read) — Verify structure, content, frontmatter
- **Cross-references**: Use Bash (grep) — Verify UC IDs, goal IDs, intake IDs present

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — keystone artifact + independent read-only work):
├── Task 1: ROADMAP-003 creation [deep]
├── Task 5: Research triage [quick]
└── Task 6: Intake audit [quick]

Wave 2 (After Task 1 — requires ROADMAP-003 as input):
├── Task 2: Mark ROADMAP-001/002 SUPERSEDED [quick]
├── Task 3: Goal backfill [unspecified-high]
└── Task 4: Session-log dashboard [quick]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay

Critical Path: Task 1 → Task 3 → Task 4 → F1-F4 → user okay
Parallel Speedup: ~50% faster than sequential
Max Concurrent: 3 (Wave 1)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 (ROADMAP-003) | — | 2, 3, 4 | 1 |
| 5 (Research triage) | — | — | 1 |
| 6 (Intake audit) | — | — | 1 |
| 2 (Supersede old roadmaps) | 1 | — | 2 |
| 3 (Goal backfill) | 1 | 4 | 2 |
| 4 (Session-log dashboard) | 1, 3 | — | 2 |

### Agent Dispatch Summary

- **Wave 1**: 3 tasks — T1 → `deep`, T5 → `quick`, T6 → `quick`
- **Wave 2**: 3 tasks — T2 → `quick`, T3 → `unspecified-high`, T4 → `quick`
- **FINAL**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [ ] 1. Create ROADMAP-003.md with 7-Section Structure and Full Traceability

  **What to do**:
  - Read the following source artifacts in order:
    1. `docs/vision.md` — extract success horizons and time-based targets
    2. `docs/goals/goal-001..004.md` — extract goal outcomes and time horizon mappings
    3. `docs/USE_CASES.md` — extract all 50 UCs with their `stage_target` fields
    4. `state/arch/SYNTHESIS-001.md` — extract 9 themes, UC→theme mapping tables, ADR recommendations
    5. `docs/architecture/ARCHITECTURE-VISION.md` — extract 5 principles, quality attributes, key risks, ADR roadmap
    6. `docs/ROADMAP-001.md` — extract existing work items (W1-W6, W-orch, W-log, K1-K2, A1-A2, F1-F3) with their status
    7. `docs/ROADMAP-002.md` — extract UC Coverage Matrix and Goal Traceability sections (reusable content)
    8. `docs/DECISIONS.md` — extract D-001..D-022 for reference
    9. `docs/architecture/adr/ADR-0001..0010.md` — extract status (ACCEPTED vs HYPOTHESIS)
  - Write `docs/ROADMAP-003.md` with exactly 7 numbered sections, headings matching roadmap-creator spec:
    - `## 1. Stage Structure` — table with stages (v1-core, v1, v1.1, v1.2, v2), time horizons (mapped from goals), success criteria, status
    - `## 2. Area × Stage Work Grid` — table mapping areas (Workflow, Knowledge, Agents, Framework) to work items per stage. Reuse existing IDs (W1, K1, etc.) from ROADMAP-001. Add new items where gaps exist (e.g., domain onboarding, NF-15/16 implementation, PK-08 interface). New IDs extend the series (W7, K3, A3, F4 etc.)
    - `## 3. UC-to-Stage Mapping` — table covering ALL 50 UCs with their stage_target. Follow ROADMAP-002's UC Coverage Matrix format. Include which work item addresses each UC.
    - `## 4. Dependency Graph` — explicit `→` notation showing work item dependencies. Must include: completed items (marked ✅), blocked items, and critical path. work-scheduler reads this section to check readiness.
    - `## 5. Stage Gate Criteria` — boolean checklists (`- [ ]` / `- [x]`) for each stage transition (v1-core→v1, v1→v1.1, v1.1→v1.2, v1.2→v2). work-scheduler reads this section.
    - `## 6. Risk Register` — import risks from ARCHITECTURE-VISION Section 4 (R1-R7). Add any new risks from SYNTHESIS themes. Each risk must have: description, source theme, impact, mitigation strategy, status.
    - `## 7. Current Work Item` — identify the next actionable work item with: ID, description, agent to invoke, input artifacts. work-scheduler reads this section to determine what's next.
  - Include YAML frontmatter:
    ```yaml
    artifact_type: ROADMAP
    version: 3
    altitude: STRATEGIC
    phase: IMPLEMENTATION
    epistemic_grade: INFORMED_ESTIMATE
    created_at: [today]
    source_vision: docs/vision.md
    source_goals: [goal-001, goal-002, goal-003, goal-004]
    source_usecases: docs/USE_CASES.md
    source_synthesis: state/arch/SYNTHESIS-001.md
    source_architecture_vision: docs/architecture/ARCHITECTURE-VISION.md
    supersedes: [docs/ROADMAP-001.md, docs/ROADMAP-002.md]
    status: ACTIVE
    ```
  - Include `## Appendix: ROADMAP-002 Change Disposition` documenting which of the 8 recommended changes from `state/learnings/session-2026-05-10-roadmap-global-view.md` were incorporated, deferred, or rejected (with reason)
  - Include `## Appendix: Artifact Landscape` (carry over from ROADMAP-001 v2, updated)

  **Must NOT do**:
  - Do NOT invent new work-item ID prefixes (stick with W, K, A, F)
  - Do NOT modify any source artifacts
  - Do NOT create stage "v1.2" unless USE_CASES.md explicitly defines UCs for it (it does: AP-03, AP-05, AP-07, RE-02, RE-03, RE-04, RE-07)
  - Do NOT include implementation details for work items — keep at strategic altitude

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Requires reading 9+ source artifacts, cross-referencing data across them, and producing a large structured document. Deep autonomous reasoning needed.
  - **Skills**: []
    - No specialized skills needed — this is pure documentation synthesis
  - **Skills Evaluated but Omitted**:
    - `playwright`: No browser interaction needed
    - `git-master`: No git operations needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6)
  - **Parallel Group**: Wave 1 (with Tasks 5, 6)
  - **Blocks**: Tasks 2, 3, 4
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing artifacts to follow):
  - `docs/ROADMAP-001.md` — Current roadmap structure, existing work items with status, Artifact Landscape section format
  - `docs/ROADMAP-002.md` — UC Coverage Matrix format (Section 3), Goal Traceability format (reusable for Section 3)

  **Contract References** (machine-parseable requirements):
  - `.claude/agents/roadmap-creator.md` — Required 7 sections with exact headings: `## 1. Stage Structure`, `## 2. Area × Stage Work Grid`, `## 3. UC-to-Stage Mapping`, `## 4. Dependency Graph`, `## 5. Stage Gate Criteria`, `## 6. Risk Register`, `## 7. Current Work Item`
  - `.claude/agents/work-scheduler.md` — How Section 4, 5, 7 are parsed — readiness checks, stage gate validation, current item identification

  **Content References** (source data):
  - `docs/vision.md` — Success horizons (6mo, 12mo, 24mo) map to stage time horizons
  - `docs/goals/goal-001..004.md` — Goal outcomes and parent_vision_horizon for stage mapping
  - `docs/USE_CASES.md` — All 50 UCs with `stage_target` field (v1-core, v1, v1.1, v1.2, v2)
  - `state/arch/SYNTHESIS-001.md` — 9 themes, UC→theme tables, ADR recommendations with priority ordering
  - `docs/architecture/ARCHITECTURE-VISION.md` — 5 principles, quality attributes, risks R1-R7, ADR roadmap (immediate/near-term/deferred)
  - `docs/DECISIONS.md` — D-001..D-022, all binding
  - `docs/architecture/adr/ADR-0001..0010.md` — ADR-0001..0006 ACCEPTED, ADR-0007..0010 HYPOTHESIS

  **Disposition References** (ROADMAP-002 changes):
  - `state/learnings/session-2026-05-10-roadmap-global-view.md` — Section "What Should Happen Next" contains the 8 recommended changes for ROADMAP-002

  **WHY Each Reference Matters**:
  - roadmap-creator.md: Defines the EXACT section structure that work-scheduler expects — format mismatch breaks automation
  - ROADMAP-002.md: Contains already-built UC Coverage Matrix — saves duplicating the mapping work
  - SYNTHESIS-001.md: UC→theme tables are the KEY for Goal→UC traceability (themes bridge goals to UCs)
  - session-2026-05-10 learnings: Documents the 8 changes that must be dispositioned in the appendix

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ROADMAP-003 has exactly 7 numbered sections
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-003.md exists
    Steps:
      1. Run: grep -c "^## [0-9]\." docs/ROADMAP-003.md
      2. Assert output is "7"
    Expected Result: Exactly 7 section headings matching "## N." pattern
    Failure Indicators: Count != 7, missing sections, unnumbered sections
    Evidence: .sisyphus/evidence/task-1-section-count.txt

  Scenario: ROADMAP-003 frontmatter is valid
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-003.md exists
    Steps:
      1. Run: grep "artifact_type: ROADMAP" docs/ROADMAP-003.md
      2. Run: grep "version: 3" docs/ROADMAP-003.md
      3. Run: grep "status: ACTIVE" docs/ROADMAP-003.md
      4. Run: grep "supersedes:" docs/ROADMAP-003.md
    Expected Result: All 4 grep commands return matches
    Failure Indicators: Any grep returns no match
    Evidence: .sisyphus/evidence/task-1-frontmatter.txt

  Scenario: UC-to-Stage Mapping covers all 50 UCs
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-003.md exists
    Steps:
      1. Run: grep -c "NF-\|AP-\|RE-\|PK-\|XP-" docs/ROADMAP-003.md (count UC references)
      2. Verify NF-01 through NF-16, AP-01..AP-07, RE-01..RE-07, PK-01..PK-09, XP-01..XP-11 are all present
      3. Run: grep "NF-01" docs/ROADMAP-003.md && grep "XP-11" docs/ROADMAP-003.md (spot-check first and last)
    Expected Result: All 50 UC IDs appear at least once in the document
    Failure Indicators: Any UC ID missing from the document
    Evidence: .sisyphus/evidence/task-1-uc-coverage.txt

  Scenario: Dependency Graph uses parseable notation
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-003.md exists
    Steps:
      1. Run: grep -A 50 "^## 4\." docs/ROADMAP-003.md | grep -c "→\|-->"
      2. Assert count > 0 (dependency arrows exist)
    Expected Result: Section 4 contains dependency arrows
    Failure Indicators: No → or --> characters in Section 4
    Evidence: .sisyphus/evidence/task-1-dependency-graph.txt

  Scenario: Stage Gate Criteria have boolean checklists
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-003.md exists
    Steps:
      1. Run: grep -A 100 "^## 5\." docs/ROADMAP-003.md | grep -c "\- \[.\]"
      2. Assert count >= 3 (at least 3 boolean criteria per gate)
    Expected Result: Section 5 contains multiple checkbox items
    Failure Indicators: No checkbox items in Section 5
    Evidence: .sisyphus/evidence/task-1-stage-gates.txt

  Scenario: ROADMAP-002 change disposition is documented
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-003.md exists
    Steps:
      1. Run: grep "ROADMAP-002 Change Disposition" docs/ROADMAP-003.md
      2. Assert match found
    Expected Result: Appendix section documenting disposition of 8 changes exists
    Failure Indicators: No disposition section
    Evidence: .sisyphus/evidence/task-1-disposition.txt
  ```

  **Evidence to Capture:**
  - [ ] task-1-section-count.txt — grep output showing 7 sections
  - [ ] task-1-frontmatter.txt — grep output for all required frontmatter fields
  - [ ] task-1-uc-coverage.txt — UC ID presence verification
  - [ ] task-1-dependency-graph.txt — dependency notation verification
  - [ ] task-1-stage-gates.txt — boolean checklist verification
  - [ ] task-1-disposition.txt — ROADMAP-002 change disposition verification

  **Commit**: YES (groups with Tasks 2, 3, 4, 5, 6)
  - Message: `docs(roadmap): create ROADMAP-003 with full traceability and orientation system`
  - Files: `docs/ROADMAP-003.md`
  - Pre-commit: `uv run ruff check .`

- [ ] 2. Mark ROADMAP-001 and ROADMAP-002 as SUPERSEDED

  **What to do**:
  - In `docs/ROADMAP-001.md`:
    - Change `status: ACTIVE` to `status: SUPERSEDED` in YAML frontmatter
    - Add `superseded_by: docs/ROADMAP-003.md` to frontmatter
    - Add a prominent note at the top of the document body (below frontmatter):
      ```
      > **⚠️ SUPERSEDED** — This roadmap has been superseded by `docs/ROADMAP-003.md` (version 3).
      > Refer to ROADMAP-003 for current project status and work items.
      > This file is retained as historical reference.
      ```
  - In `docs/ROADMAP-002.md`:
    - Same changes: `status: SUPERSEDED`, `superseded_by: docs/ROADMAP-003.md`, prominent note
  - This is a CORRECTNESS REQUIREMENT for the work-scheduler: it reads "latest ROADMAP-NNN.md" and both old versions being ACTIVE creates ambiguity

  **Must NOT do**:
  - Do NOT delete or archive the files — they are historical references
  - Do NOT modify any content below the supersession notice
  - Do NOT change version numbers or other frontmatter fields

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Two simple frontmatter edits + notice additions. Minimal reasoning needed.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 3, 4)
  - **Parallel Group**: Wave 2 (with Tasks 3, 4)
  - **Blocks**: None
  - **Blocked By**: Task 1 (ROADMAP-003 must exist before referencing it)

  **References**:
  - `docs/ROADMAP-001.md` — File to modify (frontmatter + add notice)
  - `docs/ROADMAP-002.md` — File to modify (frontmatter + add notice)
  - `state/PROGRESS.md` — Example of SUPERSEDED notice format (already marked superseded)
  - RP-002 in `state/learnings/INDEX.md` — Recurring pattern: "superseded artifacts must be marked immediately"

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ROADMAP-001 marked SUPERSEDED
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-001.md exists
    Steps:
      1. Run: grep "status: SUPERSEDED" docs/ROADMAP-001.md
      2. Run: grep "superseded_by:" docs/ROADMAP-001.md
      3. Run: grep "SUPERSEDED" docs/ROADMAP-001.md | head -3
    Expected Result: All three greps return matches. status is SUPERSEDED, superseded_by points to ROADMAP-003
    Failure Indicators: status still ACTIVE, no superseded_by field
    Evidence: .sisyphus/evidence/task-2-roadmap-001-superseded.txt

  Scenario: ROADMAP-002 marked SUPERSEDED
    Tool: Bash (grep)
    Preconditions: docs/ROADMAP-002.md exists
    Steps:
      1. Run: grep "status: SUPERSEDED" docs/ROADMAP-002.md
      2. Run: grep "superseded_by:" docs/ROADMAP-002.md
    Expected Result: Both greps return matches
    Failure Indicators: status still ACTIVE
    Evidence: .sisyphus/evidence/task-2-roadmap-002-superseded.txt
  ```

  **Commit**: YES (groups with Tasks 1, 3, 4, 5, 6)
  - Files: `docs/ROADMAP-001.md`, `docs/ROADMAP-002.md`

- [ ] 3. Backfill Goal UC Mappings and Phase Coverage

  **What to do**:
  - For each of the 4 goal files (`docs/goals/goal-001.md` through `goal-004.md`):
    1. Read the goal's `Outcome Goal` and `Solution Shape` to understand what the goal is about
    2. Read `state/arch/SYNTHESIS-001.md` — find which themes align with this goal:
       - goal-001 (Momentum/Continuity) → T1 (Continuity), supported by T2
       - goal-002 (AI-led Workflow) → T3 (Orchestration), T6 (Observability), T8 (Progressive Disclosure)
       - goal-003 (Knowledge Compounds) → T2 (Knowledge), T4 (Epistemic Awareness)
       - goal-004 (Infrastructure) → T5 (Domain Agnostic), T7 (Multi-Surface), T9 (Rendering)
    3. For each aligned theme, read the `Contributing UCs` table in SYNTHESIS-001
    4. Populate the `## UC Mapping` table with all UCs from aligned themes:
       ```
       | UC-ID | Title | Stage | Status | Contribution |
       | NF-01 | Resume Work After Context Loss | v1-core | ACTIVE | Agent session recovery (T1) |
       ```
    5. Populate `## Phase Coverage` table using approved epics from `state/epics/`:
       - Read each epic's `parent_goal` frontmatter to determine which goal it belongs to
       - Fill in: Phase, Epic ID, Slice Delivered, Status
    6. Update `## UC Completion` counters:
       - Active UCs: count of UCs in the mapping table
       - Linked to epics: count of UCs that appear in epic story lists
       - Completed captures: 0/N (none completed yet)
  - If a UC maps to multiple goals via multiple themes, list it in ALL applicable goals (intentional duplication is OK — this is traceability, not ownership)
  - If any UC doesn't map to any goal via themes, add it to an `<!-- Unmapped UCs: UC-ID, UC-ID -->` comment at the bottom

  **Must NOT do**:
  - Do NOT change `status: proposed` on any goal
  - Do NOT modify `Outcome Goal`, `Solution Shape`, `Success Criteria`, or `Epic Seeds` sections
  - Do NOT restructure the goal file format
  - Do NOT create new goals or retire existing ones

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Requires cross-referencing multiple artifacts (4 goals × 9 themes × 50 UCs × 4 epics), systematic mapping, and careful table construction. Not complex reasoning but high volume.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 2, 4)
  - **Parallel Group**: Wave 2 (with Tasks 2, 4)
  - **Blocks**: Task 4 (dashboard references goal completion data)
  - **Blocked By**: Task 1 (uses ROADMAP-003 for work-item-to-UC alignment)

  **References**:
  - `docs/goals/goal-001.md` — Goal file to populate (Outcome: momentum/continuity, Horizon: 6mo)
  - `docs/goals/goal-002.md` — Goal file to populate (check for Outcome: AI-led workflow, Horizon: 6mo)
  - `docs/goals/goal-003.md` — Goal file to populate (check for Outcome: knowledge compounds, Horizon: 12mo)
  - `docs/goals/goal-004.md` — Goal file to populate (check for Outcome: infrastructure, Horizon: 24mo)
  - `state/arch/SYNTHESIS-001.md` — Theme→UC mapping tables (source for UC assignments)
  - `state/arch/SYNTHESIS-001.md` — Goal Alignment sections at end of each theme (maps themes to goals)
  - `state/epics/epic-v1core-001..004.md` — Epic files with `parent_goal` frontmatter (source for Phase Coverage)
  - `docs/USE_CASES.md` — UC titles and stage_targets for the mapping table

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All 4 goals have populated UC Mapping tables
    Tool: Bash (grep)
    Preconditions: docs/goals/goal-001..004.md exist
    Steps:
      1. For each goal file, count table rows: grep -c "^|" docs/goals/goal-001.md (repeat for 002, 003, 004)
      2. Each file should have more table rows than just the header (>2 lines with |)
    Expected Result: Each goal file has at least 3 rows in UC Mapping (header + separator + at least 1 data row)
    Failure Indicators: Any goal file still has 0 data rows in UC Mapping
    Evidence: .sisyphus/evidence/task-3-goal-uc-mapping.txt

  Scenario: UC coverage across goals is comprehensive
    Tool: Bash (grep)
    Preconditions: All goal files updated
    Steps:
      1. Concatenate all goal files and count unique UC IDs: grep -ohE "(NF|AP|RE|PK|XP)-[0-9]+" docs/goals/goal-*.md | sort -u | wc -l
      2. Assert count is close to 50 (some UCs may be unmapped)
    Expected Result: At least 45 unique UC IDs appear across all 4 goal files
    Failure Indicators: Fewer than 40 unique UCs mapped
    Evidence: .sisyphus/evidence/task-3-uc-completeness.txt

  Scenario: Goal status unchanged
    Tool: Bash (grep)
    Preconditions: Goal files updated
    Steps:
      1. For each goal: grep "status:" docs/goals/goal-00N.md
      2. Assert all still say "proposed"
    Expected Result: All 4 goals retain status: proposed
    Failure Indicators: Any goal has a different status
    Evidence: .sisyphus/evidence/task-3-goal-status-unchanged.txt
  ```

  **Commit**: YES (groups with Tasks 1, 2, 4, 5, 6)
  - Files: `docs/goals/goal-001.md`, `docs/goals/goal-002.md`, `docs/goals/goal-003.md`, `docs/goals/goal-004.md`

- [ ] 4. Enhance Session-Log with Status Dashboard

  **What to do**:
  - Read `docs/ROADMAP-003.md` Section 7 (Current Work Item) to determine current state
  - Read `docs/ROADMAP-003.md` Section 1 (Stage Structure) for stage status
  - Read `docs/ROADMAP-003.md` Section 4 (Dependency Graph) for blocked items
  - Read goal files for current completion status
  - In `state/session-log.md`, insert a new section `## Status Dashboard` BETWEEN the existing header/purpose block AND the `## Entries` section. Do NOT modify existing entries.
  - Dashboard content (aim for ~20-30 lines):
    ```markdown
    ## Status Dashboard

    > Last updated: [date]
    > Source: `docs/ROADMAP-003.md` (v3)

    ### Current Position
    - **Stage**: [v1-core / v1 / etc.] — [stage description from Section 1]
    - **Current Work Item**: [ID from Section 7] — [description]
    - **Agent to Invoke**: [from Section 7]

    ### Milestones
    | Milestone | Status | Date |
    |-----------|--------|------|
    | W1: SYNTHESIS | ✅ Done | 2026-05-06 |
    | W2: Architecture Vision | ✅ Done | 2026-05-06 |
    | W3: Hypothesis ADRs | ✅ Done | 2026-05-07 |
    | W3.5: Fitness Functions | ✅ Done | 2026-05-07 |
    | W-orch: Orchestrator Layer | ✅ Done | 2026-05-09 |
    | W-log: Session Log | ✅ Done | 2026-05-10 |
    | W4: First S1-S9 Intake | ⬜ NEXT | — |

    ### Blocked Items
    - [List items from dependency graph that are BLOCKED, with what blocks them]

    ### Goal Progress
    | Goal | Linked UCs | Coverage |
    |------|-----------|----------|
    | goal-001: Momentum | N UCs | [summary] |
    | goal-002: AI-led Workflow | N UCs | [summary] |
    | goal-003: Knowledge Compounds | N UCs | [summary] |
    | goal-004: Infrastructure | N UCs | [summary] |
    ```
  - The dashboard is a SNAPSHOT — it will be updated by the roadmap-updater or manually at session start

  **Must NOT do**:
  - Do NOT modify any existing session-log entries
  - Do NOT restructure the chronological log format
  - Do NOT add entries for this session (that happens at session end)
  - Do NOT make the dashboard longer than ~30 lines

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Read 3 sections of ROADMAP-003, compose a ~25-line dashboard section, insert it into session-log. Straightforward.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Tasks 1 and 3)
  - **Parallel Group**: Wave 2 (after Tasks 1, 3)
  - **Blocks**: None
  - **Blocked By**: Task 1 (ROADMAP-003 data), Task 3 (goal completion counts)

  **References**:
  - `state/session-log.md` — File to modify (insert dashboard section)
  - `docs/ROADMAP-003.md` — Section 1 (stages), Section 4 (blocked items), Section 7 (current work item)
  - `docs/goals/goal-001..004.md` — UC Completion counters (after Task 3 backfill)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Dashboard section exists in session-log
    Tool: Bash (grep)
    Preconditions: state/session-log.md updated
    Steps:
      1. Run: grep "## Status Dashboard" state/session-log.md
      2. Run: grep "Current Work Item" state/session-log.md
      3. Run: grep "Milestones" state/session-log.md
    Expected Result: All 3 greps return matches
    Failure Indicators: Dashboard section missing or incomplete
    Evidence: .sisyphus/evidence/task-4-dashboard-exists.txt

  Scenario: Existing entries are unmodified
    Tool: Bash (grep)
    Preconditions: state/session-log.md updated
    Steps:
      1. Run: grep "### 2026-05-10" state/session-log.md (most recent existing entry)
      2. Run: grep "### 2026-03-04" state/session-log.md (oldest existing entry)
      3. Run: grep -c "^### " state/session-log.md (count entry headings — should still be 10)
    Expected Result: Both date entries exist, entry count unchanged at 10
    Failure Indicators: Missing entries or count changed
    Evidence: .sisyphus/evidence/task-4-entries-unchanged.txt

  Scenario: Dashboard references current stage from ROADMAP-003
    Tool: Bash (grep)
    Preconditions: Both files exist
    Steps:
      1. Extract current stage from ROADMAP-003 Section 7
      2. Check dashboard contains the same stage identifier
    Expected Result: Dashboard's "Stage" matches ROADMAP-003 Section 7
    Failure Indicators: Stage mismatch between dashboard and roadmap
    Evidence: .sisyphus/evidence/task-4-stage-consistency.txt
  ```

  **Commit**: YES (groups with Tasks 1, 2, 3, 5, 6)
  - Files: `state/session-log.md`

- [ ] 5. Triage Unprocessed Research Sessions

  **What to do**:
  - Read `docs/research/INDEX.md` to identify the 5 unprocessed sessions (Processed: No)
  - For each unprocessed session:
    1. Read the research session file from `docs/research/sessions/`
    2. Summarize key findings in 1-2 sentences
    3. Determine what decisions/artifacts the findings informed or should inform
    4. If the findings suggest priority changes or new work items, mark with `⚠️ PRIORITY_IMPACT`
    5. Update the INDEX row: set `Processed: Yes` and fill `Informed Decisions` column
  - The 5 sessions to process:
    1. `2026-06-10_2_perplexity_refactor-5x10-workflow-proposal` — 5×10 model refactoring
    2. `2026-05-10_1_perplexity_workflow_triage_update` — ROADMAP triage for work-scheduler
    3. `2026-05-09_1_perplexity_Research-to-Ship Skillset` — Research artifact schema
    4. `2026-05-08_3_perplexity_Document Maintenance Strategy` — Research doc maintenance
    5. `2026-05-08_2_perplexity_Context Loading Strategy` — Bootstrap context loading

  **Must NOT do**:
  - Do NOT create new decisions, ADRs, or roadmap changes based on findings
  - Do NOT modify the research session files themselves
  - Do NOT act on findings — classification and flag only
  - Do NOT mark sessions as processed without actually reading them

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Read 5 files, update 5 rows in INDEX table. Straightforward classification work.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 6)
  - **Parallel Group**: Wave 1 (with Tasks 1, 6)
  - **Blocks**: None
  - **Blocked By**: None (independent read-only work)

  **References**:
  - `docs/research/INDEX.md` — File to modify (update Processed column and Informed Decisions)
  - `docs/research/sessions/` — Directory containing the 5 research session files to read
  - RP-001 in `state/learnings/INDEX.md` — "Research docs propose more than needed — implement <30%". Apply this filter when classifying.

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All research sessions marked as processed
    Tool: Bash (grep)
    Preconditions: docs/research/INDEX.md updated
    Steps:
      1. Run: grep -c "No$" docs/research/INDEX.md
      2. Assert output is "0"
    Expected Result: Zero unprocessed entries remain
    Failure Indicators: Any "No" in Processed column
    Evidence: .sisyphus/evidence/task-5-all-processed.txt

  Scenario: Informed Decisions column populated
    Tool: Bash (grep)
    Preconditions: docs/research/INDEX.md updated
    Steps:
      1. For each of the 5 sessions, grep for their row and verify non-empty Informed Decisions
      2. Run: grep "refactor-5x10" docs/research/INDEX.md (check it has content after the | delimiter)
    Expected Result: All 5 rows have non-empty Informed Decisions content
    Failure Indicators: Empty cells in Informed Decisions column
    Evidence: .sisyphus/evidence/task-5-informed-decisions.txt

  Scenario: Priority impacts flagged where appropriate
    Tool: Bash (grep)
    Preconditions: docs/research/INDEX.md updated
    Steps:
      1. Run: grep "PRIORITY_IMPACT" docs/research/INDEX.md (may or may not have matches — depends on content)
      2. This is a soft check — the flag should exist IF any findings suggest priority changes
    Expected Result: PRIORITY_IMPACT flag present if warranted by content, absent if not
    Failure Indicators: N/A — this is informational
    Evidence: .sisyphus/evidence/task-5-priority-flags.txt
  ```

  **Commit**: YES (groups with Tasks 1, 2, 3, 4, 6)
  - Files: `docs/research/INDEX.md`

- [ ] 6. Intake Audit Report

  **What to do**:
  - Read each intake file: `state/intake/intake-002.md` through `state/intake/intake-006.md`
  - For each intake, assess staleness against these criteria:
    1. **UC alignment**: Do the `use_case_ids` in frontmatter still match ACTIVE UCs in USE_CASES.md?
    2. **Module accuracy**: Are `affected_modules` still correct given current architecture?
    3. **Workflow status**: Is `READY_FOR_ARCH` the correct status given we're past W3.5? Should they be at `READY_FOR_S1`?
    4. **Roadmap alignment**: Do the intakes reference work items that still exist in ROADMAP-003?
    5. **Content currency**: Does the intake description still match the current vision and goals?
  - Write a report to `state/intake/INTAKE-AUDIT-REPORT.md` with:
    ```yaml
    ---
    artifact_type: AUDIT_REPORT
    created_at: [today]
    scope: intake-002 through intake-006
    status: ACTIVE
    ---
    ```
    - Per-intake section with: Intake ID, UC references, current status, staleness verdict (`CURRENT` / `STALE` / `NEEDS_UPDATE`), specific issues found, recommended action
    - Summary table at top

  **Must NOT do**:
  - Do NOT modify any intake files
  - Do NOT change intake status values
  - Do NOT delete or archive intakes
  - Do NOT create new intakes

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Read 5 files, cross-reference with USE_CASES.md, write a structured report. Bounded scope.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 1, 5)
  - **Parallel Group**: Wave 1 (with Tasks 1, 5)
  - **Blocks**: None
  - **Blocked By**: None (independent read-only assessment)

  **References**:
  - `state/intake/intake-002.md` through `state/intake/intake-006.md` — Files to audit
  - `docs/USE_CASES.md` — UC reference for validating use_case_ids
  - `docs/ROADMAP-003.md` — Work items for roadmap alignment check (if created by Task 1 first; otherwise use ROADMAP-001)
  - `state/PROGRESS.md` — Example of SUPERSEDED artifact format (in case intakes reference it)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Audit report exists and covers all intakes
    Tool: Bash (grep)
    Preconditions: Report written
    Steps:
      1. Run: ls state/intake/INTAKE-AUDIT-REPORT.md (file exists)
      2. Run: grep "intake-002" state/intake/INTAKE-AUDIT-REPORT.md
      3. Run: grep "intake-003" state/intake/INTAKE-AUDIT-REPORT.md
      4. Run: grep "intake-004" state/intake/INTAKE-AUDIT-REPORT.md
      5. Run: grep "intake-005" state/intake/INTAKE-AUDIT-REPORT.md
      6. Run: grep "intake-006" state/intake/INTAKE-AUDIT-REPORT.md
    Expected Result: File exists and all 5 intake IDs are referenced
    Failure Indicators: File missing or any intake ID not mentioned
    Evidence: .sisyphus/evidence/task-6-audit-coverage.txt

  Scenario: Each intake has a staleness verdict
    Tool: Bash (grep)
    Preconditions: Report exists
    Steps:
      1. Run: grep -c "CURRENT\|STALE\|NEEDS_UPDATE" state/intake/INTAKE-AUDIT-REPORT.md
      2. Assert count >= 5 (one verdict per intake)
    Expected Result: At least 5 staleness verdicts in the report
    Failure Indicators: Missing verdicts
    Evidence: .sisyphus/evidence/task-6-verdicts.txt

  Scenario: Intake files are NOT modified
    Tool: Bash (grep)
    Preconditions: Audit complete
    Steps:
      1. Run: git diff --name-only state/intake/intake-*.md
      2. Assert no output (no intake files changed)
    Expected Result: Zero intake files in git diff output
    Failure Indicators: Any intake file shows as modified
    Evidence: .sisyphus/evidence/task-6-no-modifications.txt
  ```

  **Commit**: YES (groups with Tasks 1, 2, 3, 4, 5)
  - Files: `state/intake/INTAKE-AUDIT-REPORT.md`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
>
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, grep). For each "Must NOT Have": search for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Verify YAML frontmatter validity in all modified files. Check markdown structure (heading hierarchy, table formatting). Verify all internal cross-references resolve (file paths, UC IDs, goal IDs). Check for orphaned references.
  Output: `Frontmatter [PASS/FAIL] | Structure [PASS/FAIL] | Cross-refs [N valid/N broken] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Read ROADMAP-003 end-to-end. Verify: Section 7 points to a valid work item. Dependency Graph contains all referenced work items. UC-to-Stage Mapping covers all 50 UCs. Stage Gate Criteria have boolean checklists. Risk Register has mitigations. Read session-log dashboard — verify it references current stage from ROADMAP-003 Section 7. Read goals — verify UC Mapping tables have data. Read research INDEX — verify no "No" in Processed column.
  Output: `ROADMAP [PASS/FAIL] | Dashboard [PASS/FAIL] | Goals [4/4] | Research [PASS/FAIL] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual file changes. Verify 1:1 — everything in spec was done (no missing), nothing beyond spec was done (no creep). Check "Must NOT do" compliance. Detect cross-task contamination. Verify no upstream artifacts (vision.md, USE_CASES.md, SYNTHESIS-001.md) were modified.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- After Wave 2 completion: `docs(roadmap): create ROADMAP-003 with full traceability and orientation system` — all modified files in one commit
- Pre-commit: `uv run ruff check .` (ensure no python issues from accidental changes)

---

## Success Criteria

### Verification Commands
```bash
grep -c "^## [0-9]\." docs/ROADMAP-003.md          # Expected: 7
grep "status: ACTIVE" docs/ROADMAP-003.md           # Expected: match
grep "SUPERSEDED" docs/ROADMAP-001.md               # Expected: match
grep "SUPERSEDED" docs/ROADMAP-002.md               # Expected: match
grep "## Status Dashboard" state/session-log.md     # Expected: match
grep -c "No$" docs/research/INDEX.md                # Expected: 0
ls state/intake/INTAKE-AUDIT-REPORT.md              # Expected: file exists
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] ROADMAP-003 is machine-parseable by work-scheduler
- [ ] UC traceability chain complete: vision → goals → UCs → SYNTHESIS themes → work items
- [ ] Session-log dashboard shows current project state at a glance
