---
artifact_type: SESSION_LEARNINGS
session: "Orchestrator Layer Implementation"
created_at: 2026-05-09
session_type: "architecture"
source_artifacts:
  - .claude/agents/roadmap-creator.md
  - .claude/agents/roadmap-updater.md
  - .claude/agents/work-scheduler.md
  - docs/ROADMAP-001.md (renamed from docs/STAGED-PLAN.md)
  - docs/model/MODEL-REFERENCE.md (Section 8 added)
  - docs/DECISIONS.md (D-022 added)
  - AGENTS.md (agent count updated)
  - 16 active doc files (STAGED-PLAN → ROADMAP-001 references)
purpose: "Implement orchestrator layer from Perplexity research, with critical evaluation and approved changes"
---

# Session Learnings: Orchestrator Layer Implementation

## What Was Done

- Evaluated Perplexity research package (6 files) proposing an orchestrator layer for the 5×10 model
- Identified 3 divergences from actual codebase state: non-standard frontmatter keys, subdirectory vs flat placement, phantom ROADMAP-001 versioning
- Presented alternatives for each, got human approval on Option C / A / A respectively
- Created 3 meta-agents (roadmap-creator, roadmap-updater, work-scheduler) with hybrid frontmatter
- Renamed STAGED-PLAN.md → ROADMAP-001.md with proper artifact_type and version frontmatter
- Updated MODEL-REFERENCE.md with new Section 8, renumbered subsequent sections
- Added D-022 referencing D-019 and D-020
- Updated 16 active doc files (references), left state/research/archive files untouched as historical records

## Decisions Made

### D-SESS-01: Hybrid frontmatter for orchestrator agents

**Decision:** Use existing frontmatter keys (name, description, model, tools, invoked_at, altitude, phase) plus two new optional keys (output_artifact_type, epistemic_grade_output)
**Context:** Research package proposed 4 non-standard keys (operator, input_scope, output_artifact_type, epistemic_grade_output). Only 2 carry genuinely new info.
**Why it matters:** Sets precedent for extending agent frontmatter. Future agents can use the new keys without breaking tooling that only reads existing keys.

### D-SESS-02: Flat agent directory, no subdirectory

**Decision:** Place orchestrator agents flat in .claude/agents/ alongside all 32 existing agents
**Context:** Research proposed .claude/agents/orchestrator/ subdirectory. No subdirectories exist today.
**Why it matters:** Avoids setting a precedent that forces reorganizing all 32 agents into subdirectories. The description field already signals "meta-agent" purpose.

### D-SESS-03: ROADMAP-001 not ROADMAP-002

**Decision:** Rename STAGED-PLAN.md to ROADMAP-001.md (not 002 with phantom 001)
**Context:** Research proposed ROADMAP-002 with "supersedes: ROADMAP-001 (implicit — never existed)". This creates a phantom artifact that agents would try to find.
**Why it matters:** Clean artifact lineage. Agents and humans searching for ROADMAP-001 will find it. No ghosts in the dependency chain.

---

## Process Insights

### Insight 1: Research package agent count was wrong

**Observation:** Research package repeatedly claimed "19 execution agents" but the repo contains 32 agent files. AGENTS.md also had inconsistent counts.
**Type:** workflow-process
**Implication:** Always validate research claims against actual codebase state before implementing. Explore agents are essential for this — fire them early to ground-truth the research.

### Insight 2: Historical files should not be updated during renames

**Observation:** 27 files referenced STAGED-PLAN. 16 were active docs (updated). 11 were historical records in state/, research/, archive/ (left untouched). This distinction was critical — updating historical records would falsify the project timeline.
**Type:** workflow-process
**Implication:** When renaming artifacts, classify references into "active" (update) and "historical" (preserve). state/ and docs/research/ are always historical.

### Insight 3: Section renumbering is cascade-prone

**Observation:** Inserting Section 8 in MODEL-REFERENCE.md required renumbering 9 subsequent sections (8→9, 9→10, ..., 16→17) plus updating an internal section reference. Easy to miss one.
**Type:** tooling
**Implication:** When inserting numbered sections in large docs, do a grep for all "Section N" cross-references to catch internal links that need updating.

### Insight 4: Parallel delegation + manual work is efficient

**Observation:** Delegating the bulk reference rename (16 files) to a background task while simultaneously editing MODEL-REFERENCE.md and DECISIONS.md saved significant time. The background task completed while structural edits were in progress.
**Type:** workflow-process
**Implication:** For large rename operations, delegate the mechanical find-and-replace to a background agent while doing the creative/structural edits yourself.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Phantom artifact versioning

**Temptation:** Start at version 2 to "acknowledge the implicit mental model that existed before the formal artifact."
**Reality:** Creates a ghost artifact (ROADMAP-001) that agents and humans will search for and never find. Version numbers are for machine consumption — they must resolve to real files.

### Anti-Pattern 2: Research-proposed frontmatter as-is

**Temptation:** Copy research package frontmatter verbatim since it was well-researched.
**Reality:** Research was generated without reading actual agent files. The proposed keys (operator, input_scope) didn't match any existing convention. Always diff research proposals against actual codebase conventions.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| roadmap-creator agent | `.claude/agents/roadmap-creator.md` | NEW | Bootstrap initial roadmap from vision + goals + UCs |
| roadmap-updater agent | `.claude/agents/roadmap-updater.md` | NEW | Integrate milestone evidence into versioned roadmap |
| work-scheduler agent | `.claude/agents/work-scheduler.md` | NEW | Read-only "what's next?" query agent |
| ROADMAP-001 | `docs/ROADMAP-001.md` | ACTIVE | Formalized roadmap (was STAGED-PLAN.md) |
| MODEL-REFERENCE Section 8 | `docs/model/MODEL-REFERENCE.md` | UPDATED | Orchestrator Layer documentation |
| D-022 | `docs/DECISIONS.md` | ACCEPTED | Orchestrator layer decision |
| Agent count fix | `AGENTS.md` | UPDATED | 35 agents (32 execution + 3 orchestrator) |

## What Should Happen Next

1. Run `work-scheduler` to validate it correctly reads ROADMAP-001.md and outputs the current state
2. When W4 (first S1-S9 intake) completes, invoke `roadmap-updater` to produce ROADMAP-002.md
3. Consider adding `output_artifact_type` and `epistemic_grade_output` to existing agents that produce well-defined artifacts (synthesis-agent, architecture-vision-agent, hypothesis-adr-writer)
