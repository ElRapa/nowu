---
artifact_type: REPORT
status: DRAFT
created_at: 2026-05-10
altitude: STRATEGIC
phase: REVIEW
subject: roadmap-creator.md, roadmap-updater.md, work-scheduler.md
references:
  - docs/ROADMAP-003.md
  - docs/DECISIONS.md (D-022)
  - .claude/agents/roadmap-creator.md
  - .claude/agents/roadmap-updater.md
  - .claude/agents/work-scheduler.md
---

# T8 Agent Spec Review: Roadmap Orchestrator Agents

**Purpose:** Identify concrete gaps between the three orchestrator agent specs and the canonical
7-section roadmap contract exemplified by ROADMAP-003.md. Propose targeted, specific changes.
No agent specs are modified by this report — all changes are recommendations.

---

## Table of Contents

1. [Shared Format Contract](#1-shared-format-contract)
2. [Frontmatter Convention](#2-frontmatter-convention)
3. [roadmap-creator.md — Assessment](#3-roadmap-creatormd--assessment)
4. [roadmap-updater.md — Assessment](#4-roadmap-updatermd--assessment)
5. [work-scheduler.md — Assessment](#5-work-schedulermd--assessment)
6. [Summary: Gap Severity Matrix](#6-summary-gap-severity-matrix)

---

## 1. Shared Format Contract

All three agents must agree on an exact format for machine-parseable sections. This contract is
derived from ROADMAP-003.md, which was manually created with the correct structure.

### 1.1 Section Heading Format

Every section must use numbered heading format:

```markdown
## N. Section Name
```

Exact required heading sequence:
```
## 1. Stage Structure
## 2. Area × Stage Work Grid
## 3. UC-to-Stage Mapping
## 4. Dependency Graph
## 5. Stage Gate Criteria
## 6. Risk Register
## 7. Current Work Item
```

No agent may add sections between 1–7 or rename these headings. Optional `Appendix N:` sections
may follow Section 7.

### 1.2 Preamble Tables (before Section 1)

Two optional but strongly recommended preamble tables appear before `## 1. Stage Structure`:

**Goal Achievement Horizon** — maps goals to their first-addressed (F) and achievement (A) stages:
```markdown
## Goal Achievement Horizon

| Goal | v1-core | v1 | v1.1 | v1.2 | v2 |
|---|---|---|---|---|---|
| goal-NNN (label, horizon) | F | A |  |  |  |
```

**Theme × Stage Matrix** — maps SYNTHESIS themes to work item IDs per stage:
```markdown
## Theme × Stage Matrix

| Theme | v1-core | v1 | v1.1 | v1.2 | v2 |
|---|---|---|---|---|---|
| T1 Theme Name | W4, K1 | W28 | W14 | W25 | W18 |
```

These are produced by creator and preserved/updated by updater.

### 1.3 Section 2 Table Schema (Area × Stage Work Grid)

The table MUST have exactly these columns in this order:

```markdown
| Area | ID | Description | Stage | Depends On | UC(s) | Status |
|---|---|---|---|---|---|---|
```

- **Area**: One of `Workflow`, `Knowledge`, `Agents`, `Framework`
- **ID**: Area-prefixed code: `W*` (Workflow), `K*` (Knowledge), `A*` (Agents), `F*` (Framework)
- **Description**: 1-sentence description (no period required)
- **Stage**: One of `v1-core`, `v1`, `v1.1`, `v1.2`, `v2`
- **Depends On**: Comma-separated IDs or `none`
- **UC(s)**: Comma-separated UC IDs or empty
- **Status**: One of: `✅ DONE`, `NEXT`, `READY`, `ACTIVE`, `BLOCKED`, `PLANNED`

### 1.4 Section 3 Table Schema (UC-to-Stage Mapping)

```markdown
| UC-ID | Title | Stage | Work Items | Theme(s) |
|---|---|---|---|---|
```

All UCs in USE_CASES.md must appear here. No UC may be omitted.

### 1.5 Section 4 Format (Dependency Graph)

Section 4 MUST contain:
1. A critical-path summary line in bold:
   ```markdown
   **Critical path:** **W1 ✅ → W2 ✅ → ... → WN (NEXT) → ... → stage-gate**
   ```
2. A labeled YAML block using the dependency_graph key:

```yaml
dependency_graph:
  WN: {depends_on: [], status: "✅ complete", evidence: ["path/to/artifact.md"]}
  WM: {depends_on: ["WN"], status: "NEXT"}
  WP: {depends_on: ["WM"], status: "BLOCKED_BY_WM"}
```

Required fields per entry:
- `depends_on`: list of IDs (empty list if none)
- `status`: one of `"✅ complete"`, `"NEXT"`, `"READY"`, `"BLOCKED_BY_XN"`, `"BLOCKED_BY_stage_prereqs"`, `"ACTIVE"`
- `evidence`: list of file paths (only for completed items)

### 1.6 Section 7 Format (Current Work Item)

Section 7 MUST be a labeled YAML block with exactly these fields:

```yaml
next_work_item: WN
description: <1-sentence description matching Section 2>
current_stage: <v1-core|v1|v1.1|v1.2|v2>
agent_to_invoke: <agent-name or "none if no execution agent">
input_artifacts:
  - path/to/artifact.md
status_hint: <READY|BLOCKED|NEEDS_VALIDATION> (<reason>)
```

work-scheduler reads ALL six fields. If any are absent, work-scheduler MUST flag the roadmap as
malformed rather than guessing.

### 1.7 Status Value Vocabulary

Canonical status values for work items (Section 2, Section 4):

| Value | Meaning |
|---|---|
| `✅ DONE` | Complete; evidence artifact exists |
| `NEXT` | First item to execute; no blockers |
| `READY` | Dependencies met; can be started after NEXT |
| `ACTIVE` | In progress across multiple sessions |
| `BLOCKED` | Explicit dependency not yet met |
| `PLANNED` | Future stage; not yet sequenced |

---

## 2. Frontmatter Convention

### 2.1 Agent Spec Frontmatter (the `.claude/agents/*.md` file header)

Standard keys apply to all agents. Orchestrator-specific keys apply to these three agents only.

**Standard keys (all agents):**
```yaml
name: <agent-name>
description: >
  <multi-line description>
model: claude-sonnet-4-6  # or claude-haiku-4-5 for lightweight agents
tools: [Tool1, Tool2]
invoked_at: "<condition>"
altitude: <STRATEGIC|PRODUCT|ARCHITECTURE|DELIVERY|EXECUTION>
phase: <IMPLEMENTATION|LEARN|SYNTHESIS|ANALYSIS|...>
```

**Orchestrator-specific keys (roadmap-creator and roadmap-updater only):**
```yaml
output_artifact_type: ROADMAP
epistemic_grade_output: <HYPOTHESIS|INFORMED_ESTIMATE|EVIDENCE_BASED>
```

**Explicitly excluded keys** (do NOT add these):
- `operator`: Redundant with `name`; rejected per session convention
- `input_scope`: Too rigid for orchestrator agents that read variable inputs

**work-scheduler exception:** Uses `output_artifact_type: none` and `epistemic_grade_output: N/A`
because it produces no file artifacts.

### 2.2 Document Frontmatter (produced inside ROADMAP-NNN.md)

The roadmap document itself carries this frontmatter:

```yaml
---
artifact_type: ROADMAP
version: <N>
altitude: STRATEGIC
phase: IMPLEMENTATION
epistemic_grade: <HYPOTHESIS|INFORMED_ESTIMATE|EVIDENCE_BASED>
created_at: <YYYY-MM-DD>
source_vision: docs/vision.md
source_goals: [goal-001, goal-002, ...]   # list of goal file basenames
source_usecases: docs/USE_CASES.md
source_synthesis: state/arch/SYNTHESIS-NNN.md   # if applicable
source_architecture_vision: docs/architecture/ARCHITECTURE-VISION.md  # if applicable
source_stagegate: <description>   # if triggered by stage gate
supersedes: [docs/ROADMAP-NNN.md, ...]  # list with full paths; empty list for v1
status: ACTIVE
---
```

Key rules:
- `supersedes` is a YAML list of full doc paths (not bare names), even for a single predecessor
- `phase` is always `IMPLEMENTATION` regardless of update trigger
- `version` is a monotone integer (never decrement, never skip)
- `epistemic_grade` only increases or stays same across versions

---

## 3. roadmap-creator.md — Assessment

### 3.1 Current State

The spec is well-structured at a high level: invocation conditions, inputs, 6-step process,
and output are all present. The 7 section names are listed correctly. However the spec lacks
precision at the FORMAT level — it describes WHAT sections to create but not HOW they must
be formatted for machine parseability.

### 3.2 Gaps Found

| # | Gap | Severity | Impact |
|---|---|---|---|
| G1 | Section heading format not specified | HIGH | Producer can use `### Section Name` instead of `## N. Section Name` |
| G2 | Section 2 table columns not specified | HIGH | work-scheduler reads Section 2 with implicit column expectations |
| G3 | Section 4 format (YAML + critical path) not specified | HIGH | work-scheduler reads dependency_graph YAML keys; mismatch breaks parsing |
| G4 | Section 7 YAML schema not specified | CRITICAL | work-scheduler reads 6 specific keys from Section 7 |
| G5 | Preamble tables (Goal Horizon, Theme×Stage) not mentioned | MEDIUM | Orientation tables lost; updater won't know to preserve them |
| G6 | Status vocabulary not enumerated | MEDIUM | Inconsistent status values break work-scheduler status checks |
| G7 | Area ID prefix convention not defined | MEDIUM | W*, K*, A*, F* prefix scheme implied but not stated |
| G8 | Document frontmatter missing `supersedes` and list-form sources | LOW | Not needed for v1, but transition to updater is ambiguous |

### 3.3 Proposed Changes

**Change C1: Add format contract reference and section heading spec**

*Location:* In `## Output`, after "Required sections:" list

*Current text:*
```markdown
**Required sections:**
1. Stage Structure (table with time horizons, success criteria, status)
2. Area × Stage Work Grid (table mapping areas to work items per stage)
3. UC-to-Stage Mapping (which UCs are addressed by each stage)
4. Dependency Graph (visual or list showing W1 → W2 → W3 sequencing)
5. Stage Gate Criteria (boolean checklists for each transition)
6. Risk Register (risks, sources, mitigations, status)
7. Current Work Item (what's next right now)
```

*Proposed replacement:*
```markdown
**Required sections (EXACT heading format — do not deviate):**

Use numbered `## N. Name` headings verbatim:
```
## 1. Stage Structure
## 2. Area × Stage Work Grid
## 3. UC-to-Stage Mapping
## 4. Dependency Graph
## 5. Stage Gate Criteria
## 6. Risk Register
## 7. Current Work Item
```

Before Section 1, add two preamble tables:
- **Goal Achievement Horizon**: maps each goal to the stage where it's first addressed (F)
  and achieved (A). Columns: `Goal | v1-core | v1 | v1.1 | v1.2 | v2`
- **Theme × Stage Matrix**: maps SYNTHESIS themes (T1..TN) to work item IDs per stage.
  Columns: `Theme | v1-core | v1 | v1.1 | v1.2 | v2`
```

*Justification:* ROADMAP-003 shows that preamble tables are needed for orientation. Exact
heading format prevents heading level or numbering drift.

---

**Change C2: Specify Section 2 table schema**

*Location:* In `## Process → Step 4: Sequence Work Items`

*Current text:*
```markdown
For each area × stage cell, define 3-7 work items with:
- Task ID (W1, K1, A1, F1)
- Brief description (1 sentence)
- Dependencies (which other tasks must complete first)
```

*Proposed replacement:*
```markdown
For each area × stage cell, define 3-7 work items. Render Section 2 as a table with
EXACTLY these columns in this order:

```markdown
| Area | ID | Description | Stage | Depends On | UC(s) | Status |
```

- **Area**: `Workflow`, `Knowledge`, `Agents`, or `Framework`
- **ID**: Area-prefixed — `W*` (Workflow), `K*` (Knowledge), `A*` (Agents), `F*` (Framework).
  Numbering within an area is sequential but may have gaps for historical reasons.
- **Description**: 1-sentence, no period
- **Stage**: one of `v1-core`, `v1`, `v1.1`, `v1.2`, `v2`
- **Depends On**: comma-separated IDs or `none`
- **UC(s)**: comma-separated UC IDs (from USE_CASES.md) or empty
- **Status**: `✅ DONE`, `NEXT`, `READY`, `ACTIVE`, `BLOCKED`, or `PLANNED`

Sort within each area block by stage, then by dependency order.
```

*Justification:* work-scheduler reads "work item description from ROADMAP Section 2" — it
needs stable column positions. Without exact schema, column interpretation differs between runs.

---

**Change C3: Specify Section 4 dependency graph format**

*Location:* In `## Process → Step 4: Sequence Work Items` (after the Section 2 schema)
or as a new step entry for Section 4.

*Current text:*
```markdown
### Step 4: Sequence Work Items

For each area × stage cell, define 3-7 work items with:
...
```

*Proposed: add after the step body:*
```markdown
**Section 4 format (Dependency Graph):**

Section 4 MUST contain two parts:
1. A critical-path summary line:
   `**Critical path:** **WN ✅ → WM ✅ → WP (NEXT) → ... → stage-gate-name**`
2. A labeled YAML block:

```yaml
dependency_graph:
  WN: {depends_on: [], status: "✅ complete", evidence: ["docs/path/artifact.md"]}
  WM: {depends_on: ["WN"], status: "NEXT"}
  WP: {depends_on: ["WM"], status: "BLOCKED_BY_WM"}
```

Fields per entry: `depends_on` (list), `status` (string), `evidence` (list, only for completed).
```

*Justification:* work-scheduler Step 2 says "Read its dependencies from ROADMAP Section 4
(Dependency Graph)" but specifies no format. The labeled YAML block with `dependency_graph`
key is what ROADMAP-003 established as canonical.

---

**Change C4: Specify Section 7 YAML schema**

*Location:* In `## Process → Step 4` or as part of `## Output`

*Current text (in Output section):*
```markdown
7. Current Work Item (what's next right now)
```

*Proposed: append Section 7 schema after the section list:*
```markdown
**Section 7 format (machine-parseable YAML block — no prose, no tables):**

```yaml
next_work_item: WN
description: <1-sentence matching Section 2 description>
current_stage: <v1-core|v1|v1.1|v1.2|v2>
agent_to_invoke: <agent-name or skill-name>
input_artifacts:
  - path/to/artifact.md
status_hint: <READY|BLOCKED|NEEDS_VALIDATION> (<brief reason>)
```

All 6 fields are required. work-scheduler reads all 6 fields directly. Prose explanations
go in the field values, not as additional Markdown paragraphs in this section.
```

*Justification:* This is the CRITICAL gap. work-scheduler's entire Step 1 depends on reading
Section 7. Without a schema, the agent could write prose (as ROADMAP-002 apparently did)
and work-scheduler would fail to parse it.

---

**Change C5: Update document frontmatter template**

*Location:* `## Output → Required frontmatter:`

*Current text:*
```yaml
---
artifact_type: ROADMAP
version: 1
altitude: STRATEGIC
phase: IMPLEMENTATION
epistemic_grade: HYPOTHESIS
created_at: [timestamp]
source_vision: vision.md
source_goals: [list of goal files]
source_usecases: USE_CASES.md
status: ACTIVE
---
```

*Proposed replacement:*
```yaml
---
artifact_type: ROADMAP
version: 1
altitude: STRATEGIC
phase: IMPLEMENTATION
epistemic_grade: HYPOTHESIS
created_at: YYYY-MM-DD
source_vision: docs/vision.md
source_goals: [goal-001, goal-002]   # list of goal file basenames
source_usecases: docs/USE_CASES.md
supersedes: []                        # empty list for initial creation
status: ACTIVE
---
```

*Justification:* (a) `source_*` paths should use full relative paths from repo root, not
bare filenames. (b) `supersedes` field should be declared as empty list on creation so
updater has a consistent field to append to. (c) `created_at` format standardized to ISO date.

---

**Change C6: Add Quality Self-Check item for Section 7**

*Location:* `## Quality Self-Check`

*Current text:*
```markdown
- [ ] "Current Work Item" section points to a specific work item ID
```

*Proposed replacement:*
```markdown
- [ ] Section 7 is a fenced YAML block with all 6 required fields: `next_work_item`,
      `description`, `current_stage`, `agent_to_invoke`, `input_artifacts`, `status_hint`
- [ ] Section 7 `next_work_item` ID appears in Section 2 with status `NEXT`
- [ ] Section 4 contains a `dependency_graph:` YAML key and a bold critical-path line
```

*Justification:* The old self-check only tested for ID presence; new checks test format
compliance — the actual failure mode that caused ROADMAP-002 to break work-scheduler.

---

## 4. roadmap-updater.md — Assessment

### 4.1 Current State

The spec correctly identifies three update types (SYNTHESIS, Architecture Vision, Stage Gate)
and has a `supersedes` field in its frontmatter template. However, it is critically vague
about structure preservation — the root cause of ROADMAP-002's format divergence.
The spec instructs the agent on WHAT to update but never says WHERE in the document, and never
mandates that the 7-section structure must be preserved verbatim.

### 4.2 Gaps Found

| # | Gap | Severity | Impact |
|---|---|---|---|
| G1 | No explicit section preservation mandate | CRITICAL | Caused ROADMAP-002 to abandon 7-section format |
| G2 | No per-section update routing | HIGH | Agent doesn't know which section each update type modifies |
| G3 | `supersedes` format is bare name; should be full-path list | HIGH | Lineage breaks; ROADMAP-003 used list of full paths |
| G4 | `phase: LEARN` in agent spec vs `phase: IMPLEMENTATION` in document template | MEDIUM | Inconsistency confuses agent about document-level phase |
| G5 | Preamble tables (Goal Horizon, Theme×Stage) not mentioned | MEDIUM | Updater may drop preamble tables when rewriting |
| G6 | Appendix A (Change Disposition) pattern not documented | MEDIUM | No audit trail of what changed between versions |
| G7 | Section 7 update format not specified | HIGH | Updater must know exact YAML schema to update Section 7 correctly |
| G8 | Status upgrade logic for work items not specified | MEDIUM | When updating post-stage-gate, how to change PLANNED → BLOCKED, etc. |

### 4.3 Proposed Changes

**Change C7: Add explicit structure preservation mandate**

*Location:* In `## Output`, before "The new roadmap MUST:"

*Current text:*
```markdown
## Output

Write exactly one file: `docs/ROADMAP-NNN+1.md` (increment version)

The new roadmap MUST:
- Include all content from ROADMAP-NNN
- Add new evidence from milestone artifact
- Update version number and `supersedes` field
- Update `epistemic_grade` if appropriate (HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED)
```

*Proposed replacement:*
```markdown
## Output

Write exactly one file: `docs/ROADMAP-NNN+1.md` (increment version)

**CRITICAL: Structure Preservation Rule**

The 7-section structure is a machine-readable contract. You MUST NOT:
- Add, remove, or rename sections 1–7
- Change the heading level or numbering of `## N. Section Name` headings
- Restructure or combine existing sections
- Remove the preamble tables (Goal Achievement Horizon, Theme × Stage Matrix)

You MUST only:
- Add rows to existing tables
- Update existing rows (change status, description, etc.)
- Add entries to existing YAML blocks
- Append `Appendix N:` sections after Section 7

The new roadmap MUST:
- Preserve EVERY section heading verbatim (`## 1. Stage Structure` through `## 7. Current Work Item`)
- Include all existing rows from every table in ROADMAP-NNN (no row deletions)
- Add new evidence from milestone artifact within the appropriate existing sections
- Update version number and `supersedes` field
- Update `epistemic_grade` only if appropriate (HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED)
```

*Justification:* ROADMAP-002 was produced by roadmap-updater without the 7-section structure,
proving this mandate was missing. The CRITICAL label ensures agents prioritize this over their
natural instinct to "improve" document structure.

---

**Change C8: Add per-update-type section routing**

*Location:* In each Update Type section (Update Type 1, 2, 3)

*Current text for Update Type 1:*
```markdown
### Update Type 1: SYNTHESIS Integration

When triggered by SYNTHESIS-NNN completion:
1. Import ADR roadmap from SYNTHESIS Section 3 (immediate/near-term/deferred)
2. Map SYNTHESIS themes to roadmap areas
3. Update UC-to-stage mapping based on theme-to-UC mapping in SYNTHESIS
4. Add new work items (W*, K*, A*, F*) for recommended ADRs
5. Update dependency graph
```

*Proposed replacement:*
```markdown
### Update Type 1: SYNTHESIS Integration

When triggered by SYNTHESIS-NNN completion:
1. **Preamble tables**: Add `Theme × Stage Matrix` table if not present; populate from SYNTHESIS themes
2. **Section 2** (Area × Stage Work Grid): Add new work item rows for ADRs recommended in SYNTHESIS Section 3
3. **Section 3** (UC-to-Stage Mapping): Update stage assignments based on theme-to-UC mapping; add any new UCs
4. **Section 4** (Dependency Graph): Add new entries for new work items; update critical-path line
5. **Section 6** (Risk Register): Add risks identified from SYNTHESIS theme interaction analysis
6. **Section 7** (Current Work Item): Update if next work item has changed

Do NOT restructure existing sections. Add rows and entries only.
```

*Justification:* Without knowing WHICH section to update, agents either update everything
in free-form narrative or ignore correct section placement. This routing is what ROADMAP-002 lacked.

*Apply equivalent routing to Update Type 2 and Update Type 3 in the same pattern.*

---

**Change C9: Fix `supersedes` format in document frontmatter template**

*Location:* `## Output → Required frontmatter (updated):`

*Current text:*
```yaml
supersedes: ROADMAP-NNN
```

*Proposed replacement:*
```yaml
supersedes: [docs/ROADMAP-001.md, docs/ROADMAP-NNN.md]  # full-path list of ALL predecessors
```

*Justification:* ROADMAP-003 correctly uses `supersedes: [docs/ROADMAP-001.md, docs/ROADMAP-002.md]`
as a list of all predecessors with full paths. The spec shows bare name (single value), which:
(a) loses path context for tools that need to find the file; (b) doesn't accumulate the full chain.
The convention is: the new version lists ALL previous versions, not just the immediate predecessor.

---

**Change C10: Fix phase inconsistency**

*Location:* Agent spec frontmatter (YAML header at top of file)

*Current text:*
```yaml
phase: LEARN
```

*Proposed replacement:*
```yaml
phase: IMPLEMENTATION
```

*Justification:* The document frontmatter template correctly says `phase: IMPLEMENTATION`.
The agent spec frontmatter (which describes WHAT the agent does) says `phase: LEARN`, creating
contradictory signals. The roadmap artifact is always IMPLEMENTATION-phase — the update trigger
may come from LEARN phase artifacts, but the roadmap itself is IMPLEMENTATION. Consistent with
roadmap-creator's `phase: IMPLEMENTATION`.

---

**Change C11: Document the Appendix A (Change Disposition) pattern**

*Location:* In `## Output`, after the "The new roadmap MUST:" list

*Proposed addition:*
```markdown
**Required: Add Appendix A (Change Disposition)**

Every updated roadmap MUST append an `Appendix A: ROADMAP-NNN Change Disposition` section
after Section 7 with a table showing what was incorporated from the trigger artifact:

```markdown
## Appendix A: ROADMAP-NNN Change Disposition

| # | ROADMAP-NNN Recommendation / Evidence | Disposition in ROADMAP-NNN+1 |
|---|---|---|
| 1 | <what was in trigger artifact> | INCORPORATED as WN / DEFERRED to vX / REJECTED because... |
```

This creates an audit trail that makes it possible to trace every roadmap change back to
its evidence source without reading the full trigger artifact.
```

*Justification:* ROADMAP-003's Appendix A is invaluable for understanding the change lineage.
Without mandating this, future runs will omit it. Explicitly DEFERRED and REJECTED entries
prevent evidence loss.

---

**Change C12: Specify Section 7 update procedure**

*Location:* In each Update Type section, as part of the "Section 7" routing step

*Proposed text (to include in each Update Type's routing):*
```markdown
**Section 7** (Current Work Item): Update the YAML block to reflect the new next work item.
Preserve exact schema:
```yaml
next_work_item: WN
description: <1-sentence>
current_stage: <v1-core|v1|...>
agent_to_invoke: <agent-name>
input_artifacts:
  - path/to/artifact.md
status_hint: <READY|BLOCKED|NEEDS_VALIDATION> (<reason>)
```
All 6 fields required. Do not add prose text in Section 7 — YAML block only.
```

*Justification:* work-scheduler depends on exact YAML parsing. If roadmap-updater adds prose
or changes field names, work-scheduler silently fails to parse the correct work item.

---

## 5. work-scheduler.md — Assessment

### 5.1 Current State

The spec is the leanest of the three — it describes what the agent outputs well (three YAML
statuses), and the role is read-only which limits its complexity. However, it documents HOW
it reads the roadmap only at a high level ("Read ROADMAP Section 4") without specifying which
YAML keys to read or which table columns to parse. This makes it impossible for roadmap-creator
and roadmap-updater to know what exact format work-scheduler needs.

### 5.2 Gaps Found

| # | Gap | Severity | Impact |
|---|---|---|---|
| G1 | No format contract for Section 7 (which YAML fields are read) | CRITICAL | Producer agents can't know what format work-scheduler expects |
| G2 | No format contract for Section 4 (which YAML keys are read) | HIGH | Dependency parsing logic undocumented |
| G3 | No format contract for Section 2 (which table columns are used) | MEDIUM | Work item lookup logic undocumented |
| G4 | Roadmap discovery procedure not specified | LOW | "Read latest ROADMAP-NNN.md (highest version number)" — HOW to find it? |
| G5 | Malformed roadmap handling undefined | MEDIUM | If Section 7 is prose not YAML, agent should detect and flag this |

### 5.3 Proposed Changes

**Change C13: Specify Section 7 parsing contract**

*Location:* In `## Process → Step 1: Find Current Stage`

*Current text:*
```markdown
### Step 1: Find Current Stage

Read ROADMAP Section 7 (Current Work Item) to find:
- What stage are we in? (v1-core, v1, v1.1, v2)
- What work item was marked as "Next"?
```

*Proposed replacement:*
```markdown
### Step 1: Find Current Stage

Read the fenced YAML block in ROADMAP `## 7. Current Work Item`. Parse these fields:
- `next_work_item`: The work item ID to evaluate (e.g., `W4`)
- `current_stage`: The current execution stage (e.g., `v1-core`)
- `agent_to_invoke`: Agent to invoke when READY
- `input_artifacts`: List of required input files
- `status_hint`: Pre-computed status from last roadmap update (advisory only — verify below)

**If Section 7 is missing, is prose (no YAML block), or is missing any required field**:
Output `status: MALFORMED_ROADMAP` and recommend invoking `roadmap-updater` to fix it.
```

*Justification:* Producer agents need to know what work-scheduler reads. Documenting exact
field names closes the format contract loop. The MALFORMED_ROADMAP detection prevents silent
failures when roadmap-updater produces incorrectly formatted output.

---

**Change C14: Specify Section 4 parsing contract**

*Location:* In `## Process → Step 2: Check Readiness`

*Current text:*
```markdown
### Step 2: Check Readiness

For the next work item:
- Read its dependencies from ROADMAP Section 4 (Dependency Graph)
- For each dependency, check if it exists:
  - Does the artifact exist in `docs/` or `state/`?
  - Is it marked complete in session state?
- If all dependencies exist → READY
- If any dependency missing → BLOCKED
```

*Proposed replacement:*
```markdown
### Step 2: Check Readiness

For the next work item (ID from Step 1's `next_work_item`):

1. Find the entry in the `dependency_graph:` YAML block in `## 4. Dependency Graph`.
   Look up the work item ID as a top-level key.
2. Read the `depends_on` field (list of prerequisite IDs).
3. For each prerequisite ID:
   a. Look up its entry in `dependency_graph` — check `status` field for `"✅ complete"`
   b. If status is `"✅ complete"`, check `evidence` list — verify each path actually exists
      using `docs/` and `state/` filesystem checks.
   c. If status is not `"✅ complete"` → dependency not met → BLOCKED
4. If `depends_on` is empty list → no dependencies → proceed to Step 3
5. If all dependencies met → READY (proceed to Step 3)
6. If any dependency unmet → BLOCKED (output BLOCKED status with details)

**If the work item ID is not found in `dependency_graph`:**
Flag as `status: MALFORMED_ROADMAP` — the dependency graph is out of sync with Section 2.
```

*Justification:* "Read its dependencies from ROADMAP Section 4" is too vague for an agent
to implement reliably. The YAML key `dependency_graph` and field `depends_on` are the specific
parsing targets. Documented here, they create a binding format contract with the producer agents.

---

**Change C15: Specify Section 2 lookup contract**

*Location:* In `## Hard Constraints`

*Current text (last constraint):*
```markdown
- If user asks for work item details, read the work item description from ROADMAP Section 2
```

*Proposed replacement:*
```markdown
- If user asks for work item details, look up the work item ID in `## 2. Area × Stage Work Grid`.
  The table has columns: `Area | ID | Description | Stage | Depends On | UC(s) | Status`.
  Read `Description` column for the human-readable summary, `UC(s)` for traceability,
  and `Status` for current state. The `ID` column is the lookup key.
```

*Justification:* Specifying exact column names allows the agent to parse reliably and
enables roadmap-creator/updater to know that the column order and names are load-bearing.

---

**Change C16: Add roadmap discovery procedure**

*Location:* In `## Inputs (Read ALL Required)` or `## Process → before Step 1`

*Current text:*
```markdown
**Required:**
- `docs/ROADMAP-NNN.md`: Current roadmap (latest version by number)
```

*Proposed replacement:*
```markdown
**Required:**
- `docs/ROADMAP-NNN.md`: Current roadmap — find by globbing `docs/ROADMAP-*.md`,
  parsing the `version:` frontmatter field from each match, and selecting the highest
  version number. Log the resolved file path and version before proceeding (required
  by Quality Self-Check).
```

*Justification:* "Read latest ROADMAP-NNN.md (highest version number)" is stated as a
constraint but the discovery procedure (glob + frontmatter parse) is not specified. An agent
could naively sort filenames lexicographically, which would fail for ROADMAP-010 vs ROADMAP-009.

---

**Change C17: Add MALFORMED_ROADMAP output type**

*Location:* In `## Process → Step 4: Output Decision`, add a fourth output case

*Current text ends after NEEDS_VALIDATION block*

*Proposed addition:*
```markdown
**If MALFORMED_ROADMAP:**
```yaml
status: MALFORMED_ROADMAP
detected_issue: <description of what's wrong>
section: <7|4|2|frontmatter>
recommended_action: |
  Invoke roadmap-updater to correct the roadmap structure.
  Specific issue: <issue description>
  Do not attempt to infer work items from a malformed roadmap.
```
```

*Justification:* Without this exit path, work-scheduler will either hallucinate work item
status or fail silently when roadmap structure is wrong. An explicit MALFORMED_ROADMAP
status creates a clean feedback loop: work-scheduler detects → signals roadmap-updater to fix.

---

## 6. Summary: Gap Severity Matrix

| # | Agent | Gap | Severity | Change |
|---|---|---|---|---|
| G1 | creator | Section heading format not specified | HIGH | C1 |
| G2 | creator | Section 2 table columns not specified | HIGH | C2 |
| G3 | creator | Section 4 YAML format not specified | HIGH | C3 |
| G4 | creator | Section 7 YAML schema missing | CRITICAL | C4 |
| G5 | creator | Preamble tables not mentioned | MEDIUM | C1 |
| G6 | creator | Status vocabulary not enumerated | MEDIUM | C2 |
| G7 | creator | Area ID prefixes not defined | MEDIUM | C2 |
| G8 | creator | `supersedes` not in template | LOW | C5 |
| G1 | updater | No structure preservation mandate | CRITICAL | C7 |
| G2 | updater | No per-section update routing | HIGH | C8 |
| G3 | updater | `supersedes` format: bare name not list | HIGH | C9 |
| G4 | updater | `phase: LEARN` in agent spec | MEDIUM | C10 |
| G5 | updater | Preamble tables not mentioned | MEDIUM | C8 |
| G6 | updater | Appendix A pattern not documented | MEDIUM | C11 |
| G7 | updater | Section 7 update format not specified | HIGH | C12 |
| G1 | scheduler | No format contract for Section 7 | CRITICAL | C13 |
| G2 | scheduler | No format contract for Section 4 | HIGH | C14 |
| G3 | scheduler | No format contract for Section 2 | MEDIUM | C15 |
| G4 | scheduler | Roadmap discovery not specified | LOW | C16 |
| G5 | scheduler | MALFORMED_ROADMAP case not handled | MEDIUM | C17 |

### Root Cause of ROADMAP-002 Failure

The ROADMAP-002 failure (produced by roadmap-updater, does not follow 7-section format) can
be traced to three concurrent missing pieces:
1. **G1/updater**: No structure preservation mandate — agent "improved" document structure
2. **G2/updater**: No per-section routing — agent added content in free-form narrative
3. **G4/creator**: Section 7 schema absent — no YAML format to preserve

Applying changes **C7** (mandate) + **C8** (routing) + **C12** (Section 7 schema) in roadmap-updater.md
and **C4** (Section 7 schema) in roadmap-creator.md is the minimum fix to prevent recurrence.

### Recommended Application Order

1. **First**: Apply C4 + C13 (Section 7 schema) — closes the CRITICAL format contract gap
2. **Second**: Apply C7 + C8 (updater structure preservation) — prevents ROADMAP-002 recurrence
3. **Third**: Apply C2 + C14 + C15 (Section 2/4 schemas) — closes remaining parsing gaps
4. **Fourth**: Apply remaining changes (C1, C3, C5, C6, C9, C10, C11, C12, C16, C17) for completeness

---

*Report completed: 2026-05-10 | All 17 proposed changes are targeted edits; no full spec rewrites.*
