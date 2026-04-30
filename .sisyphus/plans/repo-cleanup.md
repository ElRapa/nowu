# Repo Cleanup — Archive Stale Files & Fix Template Content

## TL;DR

> **Quick Summary**: Clean up orphaned/stale files accumulated across 4 eras of work (March 29 – April 30). Archive superseded ADRs, old state artifacts, and the legacy ARCHITECTURE.md. Strip wrong SaaS template content from 5 architecture files. Flag V1_PLAN.md for future update.
> 
> **Deliverables**:
> - 8 three-digit ADRs archived
> - docs/ARCHITECTURE.md archived
> - CLAUDE.md, BOOTSTRAP.md, BOOTSTRAP_lean.md updated to reference containers.md instead of ARCHITECTURE.md
> - 7 pre-GAP state files archived
> - 5 architecture template files stripped and reset with correct nowu-specific headers
> - V1_PLAN.md marked with update-needed notice
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Task 1 (create archive dirs) → Tasks 2-6 (parallel moves/edits) → Task 7 (verify)

---

## Context

### Original Request
User noticed duplicate ADR files (ADR-0001 vs ADR-001) in `docs/architecture/adr/` and asked for a full audit of what happened since March 29. Analysis revealed multiple categories of stale/orphaned files accumulated across 4 eras of work.

### Interview Summary
**Key Discussions**:
- ADR duplication: 3-digit (PROPOSED, Mar 29 GAP) vs 4-digit (ACCEPTED, Apr 8 P1→P4). User confirmed 4-digit are canonical.
- Template files: User asked for analysis of their purpose. 7 agents reference them — keep as empty templates, strip wrong SaaS content.
- ARCHITECTURE.md: Verified section-by-section that containers.md + context.md fully replace it. User agrees to archive.
- V1_PLAN.md: User wants it kept but updated (not archived, not left as-is). Flagged for future.
- intake-001: User confirmed archive.
- Health reports: User confirmed keep for reference.

### Research Findings
- Full git history analysis completed (March 29 → April 30, all commits mapped)
- Goal-layer v2 commits did NOT touch any ADR or architecture files — duplication predates our work
- Template files contain generic SaaS patterns (JWT, DB bottleneck, 500 concurrent users) completely wrong for nowu (local single-user CLI)
- `containers.md` references exclusively 4-digit ADR format (ADR-0001, etc.)

### Metis Review
**Identified Gaps** (all addressed in plan):
- `CLAUDE.md` lines 101-104 reference `docs/ARCHITECTURE.md` for S1/S2/S5 context scoping. Archiving without updating would break agent workflow. → Merged into Task 3.
- `BOOTSTRAP.md` and `BOOTSTRAP_lean.md` also reference `docs/ARCHITECTURE.md`. → Merged into Task 3.
- `docs/archive/adr/` directory does not yet exist. → Task 1 creates it explicitly.
- Stale docs (`WORKFLOW-DETAILED.md`, `CLAUDE-SETUP.md`, `FILE-STRUCTURE.md`, `GLOBAL-MODEL.md`) also reference `docs/ARCHITECTURE.md` but are themselves stale — updating them is out of scope for this cleanup.

---

## Work Objectives

### Core Objective
Remove stale/orphaned files from active directories and fix misleading template content, so the repository accurately reflects the current state of the project.

### Concrete Deliverables
- All superseded files moved to appropriate archive directories
- Template files contain correct nowu-specific placeholder content
- V1_PLAN.md has an update-needed notice in its header

### Definition of Done
- [ ] No 3-digit ADR files remain in `docs/architecture/adr/`
- [ ] No `docs/ARCHITECTURE.md` exists (archived)
- [ ] No pre-GAP state artifacts remain in active `state/` directories
- [ ] All 5 architecture template files contain nowu-appropriate content (no SaaS patterns)
- [ ] V1_PLAN.md header contains update-needed notice

### Must Have
- All file moves preserve git history (use `git mv`)
- Archive directories clearly separate old from current content
- Template files retain their file structure/headers for agent compatibility

### Must NOT Have (Guardrails)
- Do NOT modify any CURRENT files (containers.md, context.md, 4-digit ADRs, agents, etc.)
- Do NOT delete any files — archive only (moves, not deletes)
- Do NOT update V1_PLAN.md content — only add a notice header
- Do NOT touch `docs/design/`, `state/health/`, `state/stories/`, `state/problems/`, `state/epics/`
- Do NOT modify any `.claude/agents/` files
- Do NOT create new ADRs or modify existing 4-digit ADRs

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: N/A (no code changes)
- **Automated tests**: None
- **Framework**: N/A

### QA Policy
Every task includes agent-executed QA scenarios using Bash commands (ls, git status).
Evidence saved to `.sisyphus/evidence/cleanup/task-{N}-{scenario-slug}.txt`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation — create archive directories):
├── Task 1: Create archive directory structure [quick]

Wave 2 (Parallel moves + edits):
├── Task 2: Archive 3-digit ADRs (depends: 1) [quick]
├── Task 3: Archive ARCHITECTURE.md + update CLAUDE.md references (depends: 1) [quick]
├── Task 4: Archive pre-GAP state files (depends: 1) [quick]
├── Task 5: Strip and reset 5 architecture template files (depends: none) [quick]
├── Task 6: Add update-needed notice to V1_PLAN.md (depends: none) [quick]

Wave 3 (Verification):
├── Task 7: Verify cleanup completeness (depends: 2-6) [quick]

Wave FINAL (after ALL tasks):
├── F1: Plan compliance audit (oracle)
├── F2: Code quality review (deep)
├── F3: Real manual QA (deep)
├── F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|---|---|---|---|
| 1 | — | 2, 3, 4 | 1 |
| 2 | 1 | 7 | 2 |
| 3 | 1 | 7 | 2 | git mv ARCHITECTURE.md + update CLAUDE.md, BOOTSTRAP.md, BOOTSTRAP_lean.md |
| 4 | 1 | 7 | 2 |
| 5 | — | 7 | 2 |
| 6 | — | 7 | 2 |
| 7 | 2, 3, 4, 5, 6 | F1-F4 | 3 |

### Agent Dispatch Summary

- **Wave 1**: 1 task → `quick`
- **Wave 2**: 5 tasks → all `quick`
- **Wave 3**: 1 task → `quick`
- **FINAL**: 4 tasks → `oracle`, `deep`, `deep`, `deep`

---

## TODOs

- [x] 1. Create archive directory structure

  **What to do**:
  - Create `docs/archive/adr/` directory (for 3-digit ADRs)
  - Verify `docs/archive/` exists (it does — contains GLOBAL-MODEL.md etc.)
  - Verify `state/archive/` exists (it does — contains global-pass files etc.)

  **Must NOT do**:
  - Do not move any files yet — directory creation only

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation task)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 2, 3, 4
  - **Blocked By**: None

  **References**:
  - `docs/archive/` — already exists, contains `GLOBAL-MODEL.md`, `WORKFLOW.md`, etc.
  - `state/archive/` — already exists, contains `global-pass-2026-03-29.md`, etc.
  - Only `docs/archive/adr/` is NEW and must be created

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: Archive directories exist
    Tool: Bash
    Steps:
      1. Run `ls -d docs/archive/adr/` — must succeed (exit 0)
      2. Run `ls -d docs/archive/` — must succeed
      3. Run `ls -d state/archive/` — must succeed
    Expected Result: All three directories exist
    Evidence: .sisyphus/evidence/cleanup/task-1-dirs-exist.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 2. Archive 3-digit ADRs

  **What to do**:
  - `git mv` all 8 three-digit ADR files from `docs/architecture/adr/` to `docs/archive/adr/`:
    - `ADR-001-memory-storage-strategy.md`
    - `ADR-002-bridge-layer-architecture.md`
    - `ADR-003-flow-orchestration-pattern.md`
    - `ADR-004-soul-trait-representation.md`
    - `ADR-005-know-package-boundary.md`
    - `ADR-006-cli-presentation-layer.md`
    - `ADR-007-testing-strategy.md`
    - `ADR-008-dash-scope-dependencies-and-activation-trigger.md`
  - After moves, verify only 4-digit ADRs remain in `docs/architecture/adr/`

  **Must NOT do**:
  - Do NOT modify any 4-digit ADR files (ADR-0001 through ADR-0006)
  - Do NOT delete files — use `git mv` only

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `docs/architecture/adr/` — source directory, currently contains both 3-digit and 4-digit ADRs
  - `docs/architecture/containers.md` — references ONLY 4-digit ADRs (confirms 3-digit are orphans)
  - `state/archive/global-pass-2026-03-29.md` — the superseded global pass that created these 3-digit ADRs

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: Only 4-digit ADRs remain in active directory
    Tool: Bash
    Steps:
      1. Run `ls docs/architecture/adr/` — must show ONLY ADR-0001 through ADR-0006
      2. Run `ls docs/architecture/adr/ | grep -c "^ADR-0"` — must output "6"
      3. Run `ls docs/architecture/adr/ | grep -v "^ADR-0"` — must output nothing (empty)
    Expected Result: 6 four-digit ADRs only, zero three-digit ADRs
    Evidence: .sisyphus/evidence/cleanup/task-2-adr-active.txt

  Scenario: All 3-digit ADRs arrived in archive
    Tool: Bash
    Steps:
      1. Run `ls docs/archive/adr/` — must show all 8 three-digit ADR files
      2. Run `ls docs/archive/adr/ | wc -l` — must output "8"
    Expected Result: 8 files in archive
    Evidence: .sisyphus/evidence/cleanup/task-2-adr-archive.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 3. Archive ARCHITECTURE.md and update CLAUDE.md references

  **What to do**:
  - `git mv docs/ARCHITECTURE.md docs/archive/ARCHITECTURE.md`
  - Update `CLAUDE.md` to replace `docs/ARCHITECTURE.md` references with the correct C4 file paths:
    - Line 101 (S1 Never Load): change `docs/ARCHITECTURE.md` → `docs/architecture/containers.md`
    - Line 102 (S2 Load): change `docs/ARCHITECTURE.md` → `docs/architecture/containers.md`
    - Line 104 (S5 Never Load): change `docs/ARCHITECTURE.md` → `docs/architecture/containers.md`
  - Update `BOOTSTRAP.md` line 16: change `docs/ARCHITECTURE.md` → `docs/architecture/containers.md`
  - Update `BOOTSTRAP_lean.md` line 15: change `docs/ARCHITECTURE.md` → `docs/architecture/containers.md`

  **Must NOT do**:
  - Do NOT modify any other lines in CLAUDE.md, BOOTSTRAP.md, or BOOTSTRAP_lean.md
  - Do NOT update stale docs (WORKFLOW-DETAILED.md, CLAUDE-SETUP.md, etc.) — they reference ARCHITECTURE.md but are themselves stale and out of scope
  - Do NOT modify containers.md or context.md

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `docs/ARCHITECTURE.md` — the file being archived. v1.3, last updated Mar 22. Fully superseded by C4 docs.
  - `docs/architecture/containers.md` — C4 L2, the replacement. References `global-pass-2026-04-06`.
  - `docs/architecture/context.md` — C4 L1, the other replacement file.
  - `CLAUDE.md` lines 101-104 — Context Scoping table. S1 lists ARCHITECTURE.md as "Never Load", S2 lists it as "Load", S5 lists it as "Never Load". All must point to containers.md instead.
  - `BOOTSTRAP.md` line 16 — Session bootstrap doc. Lists ARCHITECTURE.md as item 3 to load.
  - `BOOTSTRAP_lean.md` line 15 — Lean bootstrap variant. Same reference.

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: ARCHITECTURE.md archived
    Tool: Bash
    Steps:
      1. Run `ls docs/ARCHITECTURE.md 2>&1` — must fail (file not found)
      2. Run `ls docs/archive/ARCHITECTURE.md` — must succeed
    Expected Result: File moved from docs/ to docs/archive/
    Evidence: .sisyphus/evidence/cleanup/task-3-arch-moved.txt

  Scenario: CLAUDE.md references updated
    Tool: Bash
    Steps:
      1. Run `grep "docs/ARCHITECTURE.md" CLAUDE.md` — must return NO matches (exit 1)
      2. Run `grep "docs/architecture/containers.md" CLAUDE.md` — must return 3 matches
    Expected Result: Zero references to old path, 3 references to new path
    Evidence: .sisyphus/evidence/cleanup/task-3-claude-refs.txt

  Scenario: BOOTSTRAP files updated
    Tool: Bash
    Steps:
      1. Run `grep "docs/ARCHITECTURE.md" BOOTSTRAP.md BOOTSTRAP_lean.md` — must return NO matches
      2. Run `grep "docs/architecture/containers.md" BOOTSTRAP.md BOOTSTRAP_lean.md` — must return matches from both files
    Expected Result: Both bootstrap files reference containers.md
    Evidence: .sisyphus/evidence/cleanup/task-3-bootstrap-refs.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 4. Archive pre-GAP state files

  **What to do**:
  - `git mv` the following 7 files to `state/archive/`:
    - `state/intake/intake-001.md` → `state/archive/intake-001.md`
    - `state/intake/2026-03-22-memory-integration.md` → `state/archive/2026-03-22-memory-integration.md`
    - `state/arch/2026-03-22-memory-integration-constraints.md` → `state/archive/2026-03-22-memory-integration-constraints.md`
    - `state/arch/2026-03-22-memory-integration-options.md` → `state/archive/2026-03-22-memory-integration-options.md`
    - `state/evaluations/s1-intake-evaluation.md` → `state/archive/s1-intake-evaluation.md`
    - `state/evaluations/s2-constraints-evaluation.md` → `state/archive/s2-constraints-evaluation.md`
    - `state/evaluations/s3-options-evaluation.md` → `state/archive/s3-options-evaluation.md`

  **Must NOT do**:
  - Do NOT move intake-002 through intake-006 (those are current)
  - Do NOT move any files from `state/arch/` that belong to intake-003/004/005
  - Do NOT move `state/arch/global-pass-2026-04-06.md` (that is the active global pass)
  - Do NOT touch `state/health/`, `state/stories/`, `state/problems/`, `state/epics/`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `state/intake/intake-001.md` — Status: READY_FOR_ARCH. Pre-GAP artifact from Mar 22-25. Superseded by intake-002..006.
  - `state/intake/2026-03-22-memory-integration.md` — Marked SUPERSEDED within the file itself.
  - `state/arch/2026-03-22-memory-integration-constraints.md` — References old `know/docs/adr/ADR-0005` and `docs/ARCHITECTURE.md §5`. Pre-GAP.
  - `state/arch/2026-03-22-memory-integration-options.md` — Companion to above constraints file. Pre-GAP.
  - `state/evaluations/` — All 3 files reference `intake-2026-03-22-memory-integration`, the superseded intake.
  - `state/archive/` — Destination. Already contains `global-pass-2026-03-29.md`, `001-decomp.md`, etc.

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: Pre-GAP files removed from active directories
    Tool: Bash
    Steps:
      1. Run `ls state/intake/intake-001.md 2>&1` — must fail
      2. Run `ls state/intake/2026-03-22-memory-integration.md 2>&1` — must fail
      3. Run `ls state/arch/2026-03-22-memory-integration-*.md 2>&1` — must fail
      4. Run `ls state/evaluations/s1-intake-evaluation.md 2>&1` — must fail
      5. Run `ls state/evaluations/s2-constraints-evaluation.md 2>&1` — must fail
      6. Run `ls state/evaluations/s3-options-evaluation.md 2>&1` — must fail
    Expected Result: All 7 files no longer in active directories
    Evidence: .sisyphus/evidence/cleanup/task-4-sources-clean.txt

  Scenario: All files arrived in archive
    Tool: Bash
    Steps:
      1. Run `ls state/archive/intake-001.md` — must succeed
      2. Run `ls state/archive/2026-03-22-memory-integration.md` — must succeed
      3. Run `ls state/archive/2026-03-22-memory-integration-constraints.md` — must succeed
      4. Run `ls state/archive/2026-03-22-memory-integration-options.md` — must succeed
      5. Run `ls state/archive/s1-intake-evaluation.md` — must succeed
      6. Run `ls state/archive/s2-constraints-evaluation.md` — must succeed
      7. Run `ls state/archive/s3-options-evaluation.md` — must succeed
    Expected Result: All 7 files present in state/archive/
    Evidence: .sisyphus/evidence/cleanup/task-4-archive-contents.txt

  Scenario: Current state files untouched
    Tool: Bash
    Steps:
      1. Run `ls state/intake/intake-002.md state/intake/intake-003.md state/intake/intake-004.md state/intake/intake-005.md state/intake/intake-006.md` — all must exist
      2. Run `ls state/arch/global-pass-2026-04-06.md` — must exist
      3. Run `ls state/arch/intake-003-constraints.md` — must exist
    Expected Result: Active state files are untouched
    Evidence: .sisyphus/evidence/cleanup/task-4-current-untouched.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 5. Strip and reset 5 architecture template files

  **What to do**:
  - Edit 5 files in `docs/architecture/` to replace wrong SaaS content with empty nowu-appropriate templates
  - For each file, keep ONLY the YAML frontmatter header and a "Not yet populated" notice
  - The replacement content for each file:

  **`crosscutting.md`**:
  ```markdown
  ---
  title: Crosscutting Concerns
  status: placeholder
  last_updated: 2026-04-30
  ---
  # Crosscutting Concerns

  > **Not yet populated.** This file will be filled during a future P3 architecture phase.
  > See `containers.md` for current module architecture.
  ```

  **`deployment.md`**:
  ```markdown
  ---
  title: Deployment View
  status: placeholder
  last_updated: 2026-04-30
  ---
  # Deployment View

  > **Not yet populated.** This file will be filled during a future P3 architecture phase.
  > nowu is a local single-user CLI application — no cloud deployment infrastructure applies.
  ```

  **`quality.md`**:
  ```markdown
  ---
  title: Quality Attributes
  status: placeholder
  last_updated: 2026-04-30
  ---
  # Quality Attributes

  > **Not yet populated.** This file will be filled during a future P3 architecture phase.
  > See `containers.md` for current module boundaries and contracts.
  ```

  **`risks.md`**:
  ```markdown
  ---
  title: Architecture Risks
  status: placeholder
  last_updated: 2026-04-30
  ---
  # Architecture Risks

  > **Not yet populated.** This file will be filled during a future P3 architecture phase.
  > See ADR-0001 through ADR-0006 for current architectural decisions.
  ```

  **`runtime.md`**:
  ```markdown
  ---
  title: Runtime View
  status: placeholder
  last_updated: 2026-04-30
  ---
  # Runtime View

  > **Not yet populated.** This file will be filled during a future P3 architecture phase.
  > nowu runs as a local CLI process — see `context.md` for system context.
  ```

  **Must NOT do**:
  - Do NOT modify `containers.md` or `context.md`
  - Do NOT modify any ADR file
  - Do NOT add new content beyond the placeholder notice — these files get real content during P3

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - `docs/architecture/crosscutting.md` — Currently contains JWT auth, API versioning, test containers. All wrong for nowu.
  - `docs/architecture/quality.md` — References "500 concurrent users", "cross-tenant data exposure". nowu is single-user local.
  - `docs/architecture/risks.md` — References "JWT secret rotation", "DB bottleneck". nowu uses SQLite locally, no JWT.
  - `.claude/agents/nowu-constraints.md`, `.claude/agents/nowu-options.md` (and 5 others) — These agents conditionally load these files. Empty templates are safe; wrong SaaS content is misleading.
  - `docs/architecture/containers.md` — NOT modified, but referenced in placeholder notices for cross-reference.

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: Template files contain placeholder content only
    Tool: Bash
    Steps:
      1. Run `grep -l "JWT\|concurrent users\|cross-tenant\|API versioning\|test containers" docs/architecture/crosscutting.md docs/architecture/deployment.md docs/architecture/quality.md docs/architecture/risks.md docs/architecture/runtime.md` — must return NO matches (exit 1)
      2. Run `grep -l "Not yet populated" docs/architecture/crosscutting.md docs/architecture/deployment.md docs/architecture/quality.md docs/architecture/risks.md docs/architecture/runtime.md` — must return ALL 5 files
    Expected Result: Zero SaaS patterns, all 5 files have placeholder notice
    Evidence: .sisyphus/evidence/cleanup/task-5-templates-clean.txt

  Scenario: Template files have correct frontmatter
    Tool: Bash
    Steps:
      1. Run `grep "status: placeholder" docs/architecture/crosscutting.md docs/architecture/deployment.md docs/architecture/quality.md docs/architecture/risks.md docs/architecture/runtime.md` — must return 5 matches
      2. Run `grep "last_updated: 2026-04-30" docs/architecture/crosscutting.md docs/architecture/deployment.md docs/architecture/quality.md docs/architecture/risks.md docs/architecture/runtime.md` — must return 5 matches
    Expected Result: All 5 have correct status and date
    Evidence: .sisyphus/evidence/cleanup/task-5-templates-frontmatter.txt

  Scenario: containers.md and context.md untouched
    Tool: Bash
    Steps:
      1. Run `git diff docs/architecture/containers.md` — must be empty
      2. Run `git diff docs/architecture/context.md` — must be empty
    Expected Result: No changes to C4 docs
    Evidence: .sisyphus/evidence/cleanup/task-5-c4-untouched.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 6. Add update-needed notice to V1_PLAN.md

  **What to do**:
  - Add a notice block at the top of `docs/V1_PLAN.md` (after any existing frontmatter), containing:
    ```markdown
    > ⚠️ **UPDATE NEEDED** — This plan was written before the P1→P4 pre-workflow run (April 8, 2026)
    > and the goal-layer v2 update (April 30, 2026). It does not reflect the current epic/story
    > structure, 47+ use cases, or goal hierarchy. Treat as directional reference only.
    > See `state/epics/` and `docs/goals/` for current project structure.
    ```
  - Do NOT change any other content in the file

  **Must NOT do**:
  - Do NOT rewrite or update V1_PLAN.md content
  - Do NOT change the body, only prepend the notice

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - `docs/V1_PLAN.md` — Strategic roadmap. Last updated Mar 26-28. References old step structure, 35 use cases (now 47+). Still useful as directional reference but misleading without a notice.
  - `state/epics/epic-v1core-001..004.md` — The epics derived FROM V1_PLAN during P1→P4.
  - `docs/goals/goal-001..004.md` — Goal layer added April 30, not reflected in V1_PLAN.

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: Notice present at top of V1_PLAN.md
    Tool: Bash
    Steps:
      1. Run `head -10 docs/V1_PLAN.md` — must contain "UPDATE NEEDED"
      2. Run `grep "UPDATE NEEDED" docs/V1_PLAN.md` — must return exactly 1 match
    Expected Result: Notice block present at top
    Evidence: .sisyphus/evidence/cleanup/task-6-v1plan-notice.txt

  Scenario: Rest of V1_PLAN.md content unchanged
    Tool: Bash
    Steps:
      1. Run `git diff docs/V1_PLAN.md | grep "^-" | grep -v "^---"` — must show NO deleted lines (only additions)
    Expected Result: Only additions, no deletions or modifications
    Evidence: .sisyphus/evidence/cleanup/task-6-v1plan-diff.txt
  ```

  **Commit**: NO (groups with final commit)

- [x] 7. Verify cleanup completeness

  **What to do**:
  - Run all QA scenarios from Tasks 1-6 as a final cross-check
  - Verify `git status` shows only the expected changes (moved files + edited files)
  - Count total files changed: should be approximately 18-20 (8 ADR moves + 1 ARCHITECTURE.md move + 7 state moves + 5 template edits + 1 V1_PLAN.md edit + 3 reference updates in CLAUDE.md/BOOTSTRAP files)
  - Verify no unexpected files were modified
  - Create a summary evidence file listing all changes

  **Must NOT do**:
  - Do NOT make any changes — verification only
  - Do NOT commit — that happens after F1-F4 approval

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on all previous tasks)
  - **Parallel Group**: Wave 3
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 2, 3, 4, 5, 6

  **References**:
  - All evidence files from Tasks 1-6 in `.sisyphus/evidence/cleanup/`
  - This task is the gate before final verification agents run

  **Acceptance Criteria**:

  **QA Scenarios:**

  ```
  Scenario: Git status shows only expected changes
    Tool: Bash
    Steps:
      1. Run `git status --short` — capture output
      2. Verify all entries are either "R " (renamed/moved) or "M " (modified)
      3. Verify NO "D " (deleted) entries exist
      4. Verify NO "?" (untracked) entries exist outside .sisyphus/evidence/
    Expected Result: Clean git status with only moves and edits
    Evidence: .sisyphus/evidence/cleanup/task-7-git-status.txt

  Scenario: No current files accidentally modified
    Tool: Bash
    Steps:
      1. Run `git diff --name-only docs/architecture/containers.md docs/architecture/context.md` — must be empty
      2. Run `git diff --name-only docs/architecture/adr/ADR-0001.md docs/architecture/adr/ADR-0002.md docs/architecture/adr/ADR-0003.md docs/architecture/adr/ADR-0004.md docs/architecture/adr/ADR-0005.md docs/architecture/adr/ADR-0006.md` — must be empty
    Expected Result: Zero changes to current/canonical files
    Evidence: .sisyphus/evidence/cleanup/task-7-current-untouched.txt

  Scenario: Complete change summary
    Tool: Bash
    Steps:
      1. Run `git status --short | wc -l` — count total changes
      2. Run `git status --short` — list all changes
      3. Write summary to evidence file
    Expected Result: Summary file with full list of all changes
    Evidence: .sisyphus/evidence/cleanup/task-7-change-summary.txt
  ```

  **Commit**: NO (commit happens after F1-F4 user approval)

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists. For each "Must NOT Have": search for violations. Check evidence files exist in .sisyphus/evidence/cleanup/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `deep`
  Verify no files were accidentally deleted (only moved). Check that archive directories contain the expected files. Verify template files have correct content. Check for any broken references in active files that pointed to now-archived files.
  Output: `Moves [N/N correct] | Templates [N/N correct] | References [CLEAN/N broken] | VERDICT`

- [x] F3. **Real Manual QA** — `deep`
  Run `ls` on all archive directories to confirm files arrived. Run `ls` on source directories to confirm files removed. Read each template file to verify content is nowu-appropriate. Check `git status` for clean state.
  Output: `Archives [N/N verified] | Sources [N/N clean] | Templates [N/N correct] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  Verify ONLY the files specified in the plan were touched. No current files modified. No extra files moved. No files deleted. Check git diff against plan scope.
  Output: `Files touched [N expected/N actual] | Scope violations [CLEAN/N issues] | VERDICT`

---

## Commit Strategy

- **Single commit** after all tasks complete:
  - Message: `chore: archive stale files and reset architecture templates`
  - Files: All moved/edited files
  - Pre-commit: `git status` to verify clean state

---

## Success Criteria

### Verification Commands
```bash
ls docs/architecture/adr/          # Expected: only ADR-0001 through ADR-0006
ls docs/archive/                   # Expected: ARCHITECTURE.md + existing archived files
ls state/archive/                  # Expected: intake-001, old evaluations, old constraints/options
grep -l "YYYY-MM-DD" docs/architecture/*.md  # Expected: no matches (all updated)
head -5 docs/V1_PLAN.md            # Expected: update-needed notice in header
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] No broken references in active files
