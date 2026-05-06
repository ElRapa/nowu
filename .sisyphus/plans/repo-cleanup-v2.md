# Repo Cleanup & Organization v2

## TL;DR

> **Quick Summary**: Fix stale references to archived `docs/ARCHITECTURE.md`, consolidate scattered ideas, archive superseded workflow docs, promote ALTITUDES.md to canonical docs, resolve KIS.md inbox, delete orphaned directories, and update FILE-STRUCTURE.md to reflect current state.
> 
> **Deliverables**:
> - Zero stale `docs/ARCHITECTURE.md` references in active files
> - `docs/ideas/` dissolved — superseded items archived, future items in `docs/design/`, ALTITUDES promoted
> - `docs/GLOBAL-MODEL.md` and `docs/ARCH-WORKFLOW.md` archived
> - `docs/PRE-WORKFLOW-P0-UC-spec.md` merged into `docs/PRE-WORKFLOW.md`
> - `soul/`, `agents/`, `archive/` root dirs deleted
> - `docs/inbox/KIS.md` resolved → idea-007 created, inbox deleted
> - `FILE-STRUCTURE.md` updated to current state
> 
> **Estimated Effort**: Medium (2-3 days)
> **Parallel Execution**: YES — 4 waves
> **Critical Path**: Task 1 (audit) → Tasks 2-8 (moves/edits) → Task 9 (deletions) → Task 10 (FILE-STRUCTURE update)

---

## Context

### Original Request
Thorough repo-wide analysis for cleanup and optimization. User specifically mentioned: doc content streamlining, ideas consolidation (docs/ vs state/), workflow doc proliferation, and overall organization.

### Interview Summary
**Key Discussions**:
- Superseded ideas in `docs/ideas/`: Archive to `docs/archive/ideas/`
- Future ideas (cpg, learning-loop): Move to `docs/design/concepts/`
- Paperclip Analysis: Move to `docs/design/research/`
- KIS.md inbox: Resolve (6/7 items already captured, create idea-007 for remaining)
- Orphaned dirs (soul/, agents/, archive/): Delete all three
- Workflow docs: Archive GLOBAL-MODEL, ARCH-WORKFLOW; merge PRE-WORKFLOW-P0-UC-spec into PRE-WORKFLOW; promote ALTITUDES
- Agent/skill renaming: DEFERRED to altitude implementation (idea-004)

**Research Findings**:
- 15 files reference archived `docs/ARCHITECTURE.md` — 4 active docs need fixing, rest are archived/design files
- `docs/GLOBAL-MODEL.md` has unique CPG content (§5-6) not in ALTITUDES.md but marked as "future (v2+)" — safe to archive as-is
- `ARCH-WORKFLOW.md` referenced only by one archived health report
- KIS.md analysis: "failing is a valid outcome" is the only uncaptured idea

### Metis Review
**Identified Gaps** (addressed):
- Grep before every move/rename: Included as Task 1 (full audit)
- Separate content edits from structural moves: Tasks split accordingly
- Verify before deleting dirs: Task 9 includes verification
- Skill naming unresolved: DEFERRED per user decision
- KIS.md item validation: All 7 items mapped with specific references
- GLOBAL-MODEL.md unique content check: Verified, CPG sections are "future" content that can live in archive

---

## Work Objectives

### Core Objective
Clean up stale references, consolidate scattered ideas, archive superseded docs, and delete orphaned directories to create a tidy, accurate repo structure.

### Concrete Deliverables
- Updated `WORKFLOW-DETAILED.md`, `GLOBAL-MODEL.md` (before archive), `CLAUDE-SETUP.md`, `FILE-STRUCTURE.md`
- `docs/ALTITUDES.md` (promoted from `docs/ideas/`)
- `docs/archive/ideas/` with 3 superseded idea docs + evaluation transcript
- `docs/design/concepts/` with 2 future idea docs
- `docs/design/research/paperclip-analysis/` with 14 research files
- `state/ideas/idea-007.md` (new)
- Updated `docs/PRE-WORKFLOW.md` with P0.UC spec content merged in

### Definition of Done
- [ ] `grep -r "docs/ARCHITECTURE.md" --include="*.md" . | grep -v archive | grep -v design | grep -v ".git"` returns 0 results
- [ ] `ls docs/ideas/ 2>&1` returns "No such file or directory"
- [ ] `ls docs/ALTITUDES.md` exists with 311 lines
- [ ] `ls soul/ agents/ archive/ docs/inbox/ 2>&1` all return "No such file or directory"
- [ ] `state/ideas/idea-007.md` exists with required frontmatter
- [ ] `FILE-STRUCTURE.md` reflects current directory structure

### Must Have
- All stale `docs/ARCHITECTURE.md` references fixed in active docs
- ALTITUDES.md promoted to `docs/`
- Superseded ideas archived
- Orphaned directories deleted

### Must NOT Have (Guardrails)
- DO NOT edit agent file content (only move/rename — deferred to altitude implementation)
- DO NOT edit skill content (only potential future rename — deferred)
- DO NOT restructure CLAUDE.md beyond fixing stale references
- DO NOT edit content of files being moved (git mv only for moves)
- DO NOT touch `src/` or `tests/`
- DO NOT edit archived files to fix stale references (they're archived — stale is expected)
- DO NOT edit `docs/design/` files to fix references (historical docs — stale is expected)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: N/A — no code changes
- **Automated tests**: None — docs-only cleanup
- **Framework**: N/A

### QA Policy
Every task includes agent-executed QA scenarios using Bash (grep, ls, wc).
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — audit):
└── Task 1: Full reference audit [quick]

Wave 2 (After Wave 1 — structural moves, MAX PARALLEL):
├── Task 2: Fix stale ARCHITECTURE.md refs in active docs (depends: 1) [quick]
├── Task 3: Archive superseded ideas + evaluation transcript (depends: 1) [quick]
├── Task 4: Move future ideas to docs/design/ (depends: 1) [quick]
├── Task 5: Promote ALTITUDES.md to docs/ (depends: 1) [quick]
├── Task 6: Archive GLOBAL-MODEL + ARCH-WORKFLOW (depends: 1) [quick]
├── Task 7: Merge PRE-WORKFLOW-P0-UC-spec into PRE-WORKFLOW (depends: 1) [quick]
├── Task 8: Resolve KIS.md → create idea-007 (depends: 1) [quick]

Wave 3 (After Wave 2 — deletions):
└── Task 9: Delete orphaned dirs + empty docs/ideas/ + docs/inbox/ (depends: 2-8) [quick]

Wave 4 (After Wave 3 — final update):
└── Task 10: Update FILE-STRUCTURE.md (depends: 9) [quick]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (deep)
├── Task F3: Real manual QA (deep)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | — | 2-8 | 1 |
| 2 | 1 | 9 | 2 |
| 3 | 1 | 9 | 2 |
| 4 | 1 | 9 | 2 |
| 5 | 1 | 9 | 2 |
| 6 | 1 | 9 | 2 |
| 7 | 1 | 9 | 2 |
| 8 | 1 | 9 | 2 |
| 9 | 2-8 | 10 | 3 |
| 10 | 9 | F1-F4 | 4 |
| F1-F4 | 10 | user okay | FINAL |

### Agent Dispatch Summary

- **Wave 1**: 1 task → `quick`
- **Wave 2**: 7 tasks → all `quick`
- **Wave 3**: 1 task → `quick`
- **Wave 4**: 1 task → `quick`
- **FINAL**: 4 tasks → F1 `oracle`, F2-F4 `deep`

---

## TODOs

- [x] 1. Full Reference Audit

  **What to do**:
  - Run `grep -r "docs/ARCHITECTURE.md" --include="*.md" .` and categorize results as: active (must fix), archived (skip), design-history (skip)
  - Run `grep -r "GLOBAL-MODEL" --include="*.md" .` and list all references
  - Run `grep -r "ARCH-WORKFLOW" --include="*.md" .` and list all references
  - Run `grep -r "docs/ideas/" --include="*.md" .` and list all references
  - Run `grep -r "PRE-WORKFLOW-P0-UC" --include="*.md" .` and list all references
  - Run `grep -r "soul/SESSION-STATE" --include="*.md" .` and list all references
  - Save results as structured audit report

  **Must NOT do**:
  - Do NOT edit any files — audit only
  - Do NOT grep in `.git/`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (solo)
  - **Blocks**: Tasks 2-8
  - **Blocked By**: None

  **References**:
  - Previous cleanup commit `de09472` — established which files were archived
  - `.sisyphus/plans/repo-cleanup-v2.md` — this plan, for full list of expected moves

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Audit produces complete reference map
    Tool: Bash
    Preconditions: Working directory is repo root
    Steps:
      1. Run all grep commands listed above
      2. Categorize each result as active/archived/design-history
      3. Write results to stdout
    Expected Result: Each grep returns results; categorization is complete
    Failure Indicators: Any grep fails; results not categorized
    Evidence: .sisyphus/evidence/task-1-reference-audit.md
  ```

  **Commit**: NO (groups with final commit)

- [x] 2. Fix Stale ARCHITECTURE.md References in Active Docs

  **What to do**:
  - In `docs/WORKFLOW-DETAILED.md`: Replace `docs/ARCHITECTURE.md` with `docs/architecture/containers.md` (lines 31-32, 88, 109). Also update `state/SESSION-STATE.md` reference to `state/SESSION_STATE.md` (line 201, 297)
  - In `docs/CLAUDE-SETUP.md`: Replace `docs/ARCHITECTURE.md` references with `docs/architecture/containers.md`
  - In `docs/WORKFLOW.md`: Fix `ARCHITECTURE.md` references in context scoping table (lines 55-57)
  - In `state/arch/intake-003-constraints.md`: Fix `docs/ARCHITECTURE.md` reference
  - In `BOOTSTRAP.md` and `BOOTSTRAP_lean.md`: Verify refs are already fixed (from v1 cleanup), fix any remaining

  **Must NOT do**:
  - Do NOT edit archived files (`docs/archive/`, `state/archive/`)
  - Do NOT edit design-history files (`docs/design/`)
  - Do NOT restructure the documents — only fix the specific references

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3-8)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/WORKFLOW-DETAILED.md:31-32` — C4 level table referencing `docs/ARCHITECTURE.md §1` and `§4`
  - `docs/WORKFLOW-DETAILED.md:88` — S2 Requires section
  - `docs/WORKFLOW-DETAILED.md:109` — S3 Scope OUT
  - `docs/WORKFLOW-DETAILED.md:201,297` — S6/S9 reference to `state/SESSION-STATE.md`
  - `docs/CLAUDE-SETUP.md` — multiple ARCHITECTURE.md references
  - `docs/WORKFLOW.md:55-57` — context scoping table
  - `state/arch/intake-003-constraints.md` — constraint sheet from previous cycle
  - `docs/architecture/containers.md` — canonical replacement target
  - `docs/architecture/context.md` — for L1 references specifically

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Zero stale ARCHITECTURE.md refs in active docs
    Tool: Bash
    Preconditions: Task 1 audit complete
    Steps:
      1. Edit each file listed above, replacing stale refs
      2. Run: grep -r "docs/ARCHITECTURE.md" --include="*.md" . | grep -v archive | grep -v design | grep -v ".git"
      3. Assert 0 results
    Expected Result: Command returns empty (exit code 1 from grep = no matches)
    Failure Indicators: Any matches remain in non-archived files
    Evidence: .sisyphus/evidence/task-2-stale-refs-fixed.txt

  Scenario: SESSION-STATE.md refs updated
    Tool: Bash
    Steps:
      1. Run: grep -n "SESSION-STATE" docs/WORKFLOW-DETAILED.md
      2. Assert all refs point to state/SESSION_STATE.md (underscore, not hyphen)
    Expected Result: Only `state/SESSION_STATE.md` references found
    Evidence: .sisyphus/evidence/task-2-session-state-refs.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 3. Archive Superseded Ideas + Evaluation Transcript

  **What to do**:
  - Create `docs/archive/ideas/` directory
  - `git mv docs/ideas/atam-for-options-evaluation.md docs/archive/ideas/`
  - `git mv docs/ideas/octahedron-model.md docs/archive/ideas/`
  - `git mv docs/ideas/workflow-standardisation.md docs/archive/ideas/`
  - `git mv "docs/ideas/Evaluation on two new ideas that are not.md" docs/archive/ideas/`

  **Must NOT do**:
  - Do NOT edit file content
  - Do NOT move files that are NOT marked INCORPORATED/FORMALISED (cpg, learning-loop, ALTITUDES, Paperclip stay for other tasks)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4-8)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/ideas/atam-for-options-evaluation.md` — status: INCORPORATED into nowu-options.md and nowu-decider.md
  - `docs/ideas/octahedron-model.md` — status: FORMALISED in docs/GLOBAL-MODEL.md
  - `docs/ideas/workflow-standardisation.md` — status: INCORPORATED into docs/WORKFLOW.md
  - `docs/ideas/Evaluation on two new ideas...md` — chat transcript, not a proper idea doc

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Superseded ideas archived
    Tool: Bash
    Steps:
      1. Run: ls docs/archive/ideas/
      2. Assert 4 files present: atam-for-options-evaluation.md, octahedron-model.md, workflow-standardisation.md, "Evaluation on two new ideas..."
      3. Run: ls docs/ideas/ — assert these 4 files are NOT present
    Expected Result: All 4 files in archive, none in original location
    Evidence: .sisyphus/evidence/task-3-ideas-archived.txt

  Scenario: No broken references to moved files
    Tool: Bash
    Steps:
      1. Run: grep -r "atam-for-options-evaluation\|octahedron-model\|workflow-standardisation" --include="*.md" . | grep -v archive | grep -v ".git"
      2. Assert 0 results (or only self-references within archived files)
    Expected Result: No active files reference these archived docs
    Evidence: .sisyphus/evidence/task-3-no-broken-refs.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 4. Move Future Ideas to docs/design/

  **What to do**:
  - Create `docs/design/concepts/` directory
  - Create `docs/design/research/` directory
  - `git mv docs/ideas/cpg-as-know-graph.md docs/design/concepts/`
  - `git mv docs/ideas/workflow-learning-loop.md docs/design/concepts/`
  - `git mv "docs/ideas/Paperclip Analysis" "docs/design/research/paperclip-analysis"`
  - Update the one reference: in `docs/design/concepts/workflow-learning-loop.md`, line 154 references `docs/ideas/workflow-learning-loop.md` — update to `docs/design/concepts/workflow-learning-loop.md`

  **Must NOT do**:
  - Do NOT edit file content beyond the self-reference fix
  - Do NOT rename individual files within Paperclip Analysis

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2-3, 5-8)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/ideas/cpg-as-know-graph.md` — status: FUTURE v2+
  - `docs/ideas/workflow-learning-loop.md` — status: CONCEPT, ready for pre-workflow
  - `docs/ideas/Paperclip Analysis/` — 14 files: research reports + artifacts from external analysis
  - `docs/design/` — already exists with `flow/`, `framework_design/`, `workflow_design/`

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Future ideas in docs/design/concepts/
    Tool: Bash
    Steps:
      1. Run: ls docs/design/concepts/
      2. Assert: cpg-as-know-graph.md and workflow-learning-loop.md present
    Expected Result: Both files exist at new location
    Evidence: .sisyphus/evidence/task-4-concepts-moved.txt

  Scenario: Paperclip Analysis in docs/design/research/
    Tool: Bash
    Steps:
      1. Run: ls docs/design/research/paperclip-analysis/
      2. Assert: 14 files present (7 .md + 7 .pdf files)
    Expected Result: All 14 files exist at new location
    Evidence: .sisyphus/evidence/task-4-paperclip-moved.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 5. Promote ALTITUDES.md to docs/

  **What to do**:
  - `git mv docs/ideas/ALTITUDES.md docs/ALTITUDES.md`

  **Must NOT do**:
  - Do NOT edit the file content
  - Do NOT change its status (already ACTIVE)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2-4, 6-8)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/ideas/ALTITUDES.md` — 311 lines, status: ACTIVE, type: framework-pattern
  - This is the canonical document describing the altitude model that unifies the workflow

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ALTITUDES.md exists at docs/ root
    Tool: Bash
    Steps:
      1. Run: wc -l docs/ALTITUDES.md
      2. Assert: 311 lines
      3. Run: grep "status: ACTIVE" docs/ALTITUDES.md
      4. Assert: match found
    Expected Result: File exists at docs/ALTITUDES.md with correct content
    Evidence: .sisyphus/evidence/task-5-altitudes-promoted.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 6. Archive GLOBAL-MODEL.md + ARCH-WORKFLOW.md

  **What to do**:
  - `git mv docs/GLOBAL-MODEL.md docs/archive/GLOBAL-MODEL.md`
    Note: `docs/archive/GLOBAL-MODEL.md` already exists from a previous archive. Check if it's the same file or different. If different, rename the existing one with a date suffix first.
  - `git mv docs/ARCH-WORKFLOW.md docs/archive/ARCH-WORKFLOW.md`
  - Update references in active files:
    - `BOOTSTRAP.md` and `BOOTSTRAP_lean.md`: Remove or update GLOBAL-MODEL references
    - `FILE-STRUCTURE.md`: Will be handled in Task 10
    - `state/PROGRESS.md`: Update if it references GLOBAL-MODEL

  **Must NOT do**:
  - Do NOT edit the file content of the archived files
  - Do NOT update references in design-history or already-archived files

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2-5, 7-8)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/GLOBAL-MODEL.md` — 128 lines, overlaps with ALTITUDES.md, has stale refs to ARCHITECTURE.md
  - `docs/ARCH-WORKFLOW.md` — 53 lines, implementation notes for P3 extension, partially done
  - `docs/archive/GLOBAL-MODEL.md` — may already exist (check first!)
  - `BOOTSTRAP.md` — references GLOBAL-MODEL.md
  - `BOOTSTRAP_lean.md` — references GLOBAL-MODEL.md
  - `state/PROGRESS.md` — may reference GLOBAL-MODEL.md

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Both docs archived
    Tool: Bash
    Steps:
      1. Run: ls docs/GLOBAL-MODEL.md docs/ARCH-WORKFLOW.md 2>&1
      2. Assert: both "No such file or directory"
      3. Run: ls docs/archive/GLOBAL-MODEL.md docs/archive/ARCH-WORKFLOW.md
      4. Assert: both exist
    Expected Result: Files moved from docs/ to docs/archive/
    Evidence: .sisyphus/evidence/task-6-docs-archived.txt

  Scenario: No broken active references
    Tool: Bash
    Steps:
      1. Run: grep -r "GLOBAL-MODEL" BOOTSTRAP.md BOOTSTRAP_lean.md state/PROGRESS.md 2>/dev/null
      2. Assert: 0 results (references updated or removed)
    Expected Result: No active files point to archived GLOBAL-MODEL.md
    Evidence: .sisyphus/evidence/task-6-refs-updated.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 7. Merge PRE-WORKFLOW-P0-UC-spec.md into PRE-WORKFLOW.md

  **What to do**:
  - Read `docs/PRE-WORKFLOW-P0-UC-spec.md` (73 lines — P0.UC step specification)
  - Find the P0.UC section in `docs/PRE-WORKFLOW.md` (search for "P0.UC" or "use-case-agent")
  - Insert the spec content into the appropriate P0.UC section of PRE-WORKFLOW.md
  - If PRE-WORKFLOW.md already has a P0.UC section, merge the content (spec is more detailed)
  - `git rm docs/PRE-WORKFLOW-P0-UC-spec.md`
  - Check if any file references `PRE-WORKFLOW-P0-UC-spec.md` and update

  **Must NOT do**:
  - Do NOT restructure PRE-WORKFLOW.md beyond inserting the merged content
  - Do NOT change the substance of either document

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2-6, 8)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/PRE-WORKFLOW-P0-UC-spec.md` — 73 lines, standalone P0.UC step spec
  - `docs/PRE-WORKFLOW.md` — 560 lines, full P0-P4 specification (search for P0.UC section)
  - The spec has frontmatter, Purpose, When to run, Inputs sections — these should integrate into the existing P0.UC subsection of PRE-WORKFLOW.md

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: P0-UC-spec merged and original deleted
    Tool: Bash
    Steps:
      1. Run: ls docs/PRE-WORKFLOW-P0-UC-spec.md 2>&1
      2. Assert: "No such file or directory"
      3. Run: grep "P0.UC" docs/PRE-WORKFLOW.md
      4. Assert: P0.UC content present
      5. Run: grep -c "use-case-agent" docs/PRE-WORKFLOW.md
      6. Assert: count > 0
    Expected Result: Spec deleted, content merged into PRE-WORKFLOW.md
    Evidence: .sisyphus/evidence/task-7-p0uc-merged.txt

  Scenario: No broken references
    Tool: Bash
    Steps:
      1. Run: grep -r "PRE-WORKFLOW-P0-UC" --include="*.md" . | grep -v ".git"
      2. Assert: 0 results
    Expected Result: No files reference the deleted spec
    Evidence: .sisyphus/evidence/task-7-no-broken-refs.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 8. Resolve KIS.md Inbox — Create idea-007

  **What to do**:
  - Create `state/ideas/idea-007.md` using `templates/pre-workflow/idea.md` template
  - Content: "Failing is a Valid Outcome" — the concept that failure should be explicitly captured as a workflow outcome with failure mode and reason, not forced into success
  - Frontmatter: `id: idea-007`, `created: 2026-04-30`, `status: DRAFT`, `size: Story`
  - Source: Dogfooding
  - Related UCs: NF-06 (learn from past mistakes)
  - After creating idea-007, `git rm docs/inbox/KIS.md`

  KIS.md item resolution (for reference — do NOT create ideas for these):
  - "add status of last session" → Already in WORKFLOW-DETAILED.md S0 + state/SESSION_STATE.md
  - "requirements scope sensitive" → Covered by context scoping rules (CLAUDE.md) and idea-004
  - "requirements inheritance" → Covered by altitude model (HIGH constrains MID constrains LOW)
  - "place requirements in CPG/C4" → Covered in GLOBAL-MODEL.md/ALTITUDES.md
  - "add level of decision" → Already implemented: D-NNN has `level:` field (WORKFLOW-DETAILED.md:141)
  - "Diamond on pyramid model" → Covered in octahedron-model.md (FORMALISED)

  **Must NOT do**:
  - Do NOT create ideas for the 6 already-captured items
  - Do NOT expand idea-007 beyond stub quality — use template as-is

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2-7)
  - **Blocks**: Task 9
  - **Blocked By**: Task 1

  **References**:
  - `docs/inbox/KIS.md` — 22 lines of raw brainstorm from 2026-03-10/11
  - `templates/pre-workflow/idea.md` — idea note template with required fields
  - `state/ideas/idea-006.md` — latest idea, for ID sequencing reference
  - NF-06 in `docs/USE_CASES.md` — "learn from past mistakes" use case

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: idea-007 exists with correct frontmatter
    Tool: Bash
    Steps:
      1. Run: grep "^id: idea-007" state/ideas/idea-007.md
      2. Assert: match found
      3. Run: grep "^status: DRAFT" state/ideas/idea-007.md
      4. Assert: match found
      5. Run: grep "failing\|failure\|valid outcome" state/ideas/idea-007.md (case-insensitive)
      6. Assert: match found
    Expected Result: idea-007 exists with correct ID, status, and content about failure as valid outcome
    Evidence: .sisyphus/evidence/task-8-idea-007-created.txt

  Scenario: KIS.md deleted
    Tool: Bash
    Steps:
      1. Run: ls docs/inbox/KIS.md 2>&1
      2. Assert: "No such file or directory"
    Expected Result: KIS.md removed
    Evidence: .sisyphus/evidence/task-8-kis-deleted.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 9. Delete Orphaned Directories

  **What to do**:
  - Verify no remaining references to files in these dirs
  - `git rm -r soul/`
  - `git rm -r agents/` (root — NOT .claude/agents/)
  - `git rm -r archive/` (root — NOT docs/archive/)
  - `git rm -r docs/inbox/` (should be empty after KIS.md deletion, or `rmdir`)
  - `rm -rf docs/ideas/` (should be empty after Tasks 3-5 moved everything — use `rmdir` to verify empty first)
  - Remove `docs/PRE-WORKFLOW-P0-UC-spec.md` if not already removed in Task 7

  **Must NOT do**:
  - Do NOT delete `.claude/agents/` (those are the active agents!)
  - Do NOT delete `docs/archive/` (that's the destination, not a source)
  - Do NOT delete any directory without first verifying it's empty or all contents are orphaned

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (solo)
  - **Blocks**: Task 10
  - **Blocked By**: Tasks 2-8

  **References**:
  - `soul/SESSION-STATE.md` — only referenced by archived files
  - `agents/archive/` — 6 old step-NNN files, all superseded by `.claude/agents/`
  - `archive/prompts/general/` and `archive/skills/` — old versions
  - Previous grep audit (Task 1) confirms no active references

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All orphaned directories deleted
    Tool: Bash
    Steps:
      1. Run: ls -d soul/ agents/ archive/ docs/inbox/ docs/ideas/ 2>&1
      2. Assert: ALL return "No such file or directory"
      3. Run: ls .claude/agents/ | head -5
      4. Assert: .claude/agents/ still exists with agent files (NOT deleted)
      5. Run: ls docs/archive/ | head -5
      6. Assert: docs/archive/ still exists (NOT deleted)
    Expected Result: Orphaned dirs deleted; active dirs preserved
    Evidence: .sisyphus/evidence/task-9-dirs-deleted.txt

  Scenario: No references to deleted dirs
    Tool: Bash
    Steps:
      1. Run: grep -r "soul/SESSION-STATE\|agents/archive\|^archive/" --include="*.md" . | grep -v ".git" | grep -v "docs/archive"
      2. Assert: 0 results in active files
    Expected Result: No active files reference deleted directories
    Evidence: .sisyphus/evidence/task-9-no-orphan-refs.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 10. Update FILE-STRUCTURE.md

  **What to do**:
  - Read current `FILE-STRUCTURE.md` (233 lines, version 2.2 from 2026-03-26)
  - Update to reflect all changes made in this cleanup:
    - Remove `docs/ARCHITECTURE.md` entry (archived)
    - Remove `docs/GLOBAL-MODEL.md` entry (archived)
    - Remove `docs/ARCH-WORKFLOW.md` entry (archived)
    - Remove `docs/PRE-WORKFLOW-P0-UC-spec.md` entry (merged)
    - Remove `docs/ideas/` section (dissolved)
    - Remove `docs/inbox/` section (deleted)
    - Remove `soul/` entry (deleted)
    - Remove `state/ideas/parked/` entry (never existed)
    - Add `docs/ALTITUDES.md` entry
    - Add `docs/goals/` entry with goal-NNN.md pattern
    - Add `docs/design/concepts/` entry
    - Add `docs/design/research/` entry
    - Update `docs/architecture/` description to reflect it's the canonical C4 docs location
    - Update version number and date
  - Do NOT rewrite from scratch — edit the existing structure

  **Must NOT do**:
  - Do NOT add entries for things that didn't change in this cleanup (don't do a full audit)
  - Do NOT restructure the document format

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (solo, after all moves complete)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 9

  **References**:
  - `FILE-STRUCTURE.md` — current version 2.2, 233 lines
  - This plan — for complete list of all moves/deletions/additions

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: FILE-STRUCTURE.md reflects current state
    Tool: Bash
    Steps:
      1. Run: grep "ARCHITECTURE.md" FILE-STRUCTURE.md
      2. Assert: no reference to docs/ARCHITECTURE.md as [LANDMARK] (may reference docs/archive/)
      3. Run: grep "ALTITUDES.md" FILE-STRUCTURE.md
      4. Assert: present
      5. Run: grep "containers.md" FILE-STRUCTURE.md
      6. Assert: present as [LANDMARK]
      7. Run: grep "ideas/parked" FILE-STRUCTURE.md
      8. Assert: not present
      9. Run: grep "docs/goals/" FILE-STRUCTURE.md
      10. Assert: present
    Expected Result: All updated entries reflect actual repo state
    Evidence: .sisyphus/evidence/task-10-file-structure-updated.txt

  Scenario: No references to deleted items
    Tool: Bash
    Steps:
      1. Run: grep -E "soul/|docs/inbox/|docs/GLOBAL-MODEL|ARCH-WORKFLOW|PRE-WORKFLOW-P0-UC" FILE-STRUCTURE.md
      2. Assert: 0 results (or only in archive context)
    Expected Result: FILE-STRUCTURE.md doesn't reference deleted/archived items
    Evidence: .sisyphus/evidence/task-10-no-stale-entries.txt
  ```

  **Commit**: YES
  - Message: `chore(docs): repo cleanup v2 — fix stale refs, consolidate ideas, archive superseded docs, delete orphaned dirs`
  - Files: all modified/moved/created/deleted files across Tasks 1-10
  - Pre-commit: `grep -r "docs/ARCHITECTURE.md" --include="*.md" . | grep -v archive | grep -v design | grep -v ".git" | wc -l` → expected: 0

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (grep, ls). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [4/4] | Must NOT Have [5/5] | Tasks [10/10] | VERDICT: APPROVE`

- [x] F2. **Code Quality Review** — `deep`
  Since this is docs-only: verify all moved files exist at new locations. Verify no broken internal links in updated docs. Check for orphaned references to deleted files.
  Output: `Moves [14/14 verified] | Links [0 broken] | Orphans [0 found] | VERDICT: APPROVE`

- [x] F3. **Real Manual QA** — `deep`
  Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration: do the BOOTSTRAP files still reference the right things? Does CLAUDE.md's context scoping table match reality?
  Output: `Scenarios [10/10 pass] | Integration [6/6] | VERDICT: APPROVE`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Flag unaccounted changes.
  Output: `Tasks [10/10 compliant] | Unaccounted [CLEAN] | VERDICT: APPROVE` (architecture stub files pre-existed from commit de09472 — not caused by this plan)

---

## Commit Strategy

- Single commit after all tasks complete: `chore(docs): repo cleanup v2 — fix stale refs, consolidate ideas, archive superseded docs, delete orphaned dirs`
- Files: all moved/edited/created/deleted files

---

## Success Criteria

### Verification Commands
```bash
# Zero stale ARCHITECTURE.md refs in active files
grep -r "docs/ARCHITECTURE.md" --include="*.md" . | grep -v archive | grep -v design | grep -v ".git"
# Expected: 0 results

# docs/ideas/ deleted
ls docs/ideas/ 2>&1
# Expected: No such file or directory

# ALTITUDES.md promoted
wc -l docs/ALTITUDES.md
# Expected: 311

# Orphaned dirs deleted
ls soul/ agents/ archive/ docs/inbox/ 2>&1
# Expected: all "No such file or directory"

# idea-007 exists
grep "^id:" state/ideas/idea-007.md
# Expected: "id: idea-007"

# FILE-STRUCTURE.md updated (check for containers.md reference)
grep "containers.md" FILE-STRUCTURE.md
# Expected: 1+ matches
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] FILE-STRUCTURE.md reflects reality
