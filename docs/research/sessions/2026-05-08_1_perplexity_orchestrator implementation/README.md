# Orchestrator Layer for nowu

**Package contents:** 3 meta-agents + 1 MODEL-REFERENCE update section

This package formalizes the **orchestrator layer** — the external meta-workflow that decides what work enters the nowu 5×10 execution field.

---

## What This Solves

**Problem:** STAGED-PLAN.md was created manually during a side-quest and felt like "jumping ahead" because it didn't fit into the 5×10 workflow model.

**Root cause:** The 5×10 model defines **execution phases** (SENSE, PROBLEM, ANALYSIS, etc.) but lacks a formal **orchestration layer** to decide what work happens next.

**Solution:** Introduce an orchestrator layer that sits **outside** the 5×10 grid and manages:
- Roadmap creation (after vision + goals + early UCs)
- Roadmap updates (after SYNTHESIS, Arch Vision, stage gates)
- Work scheduling (deciding "what's next?" based on current roadmap and system state)

**Industry validation:** Shape Up, SAFe, Temporal, AFLOW, AgentOrchestra, and HTN Planning all separate execution (the work) from orchestration (deciding what work happens next). This is not a new pattern — it's the formalization of a gap that every mature workflow system addresses.

---

## Files in This Package

### 1. Agent Definitions (3 files)

#### `roadmap-creator.md`
- **Trigger:** P0.V + P0.G complete, 10+ UCs exist
- **Input:** vision, goals, partial UC catalog
- **Output:** ROADMAP-001.md
- **Grade:** HYPOTHESIS (initial guess based on incomplete evidence)
- **Purpose:** Bootstrap the initial implementation plan with stage structure, area breakdown, dependency graph, stage gates, and risk register

#### `roadmap-updater.md`
- **Trigger:** SYNTHESIS complete, Arch Vision complete, stage gates passed
- **Input:** Current ROADMAP-NNN.md + milestone artifact
- **Output:** ROADMAP-NNN+1.md (versioned)
- **Grade:** INFORMED_ESTIMATE or EVIDENCE_BASED (improves with feedback)
- **Purpose:** Integrate new architectural evidence or execution feedback into the roadmap

#### `work-scheduler.md`
- **Trigger:** User asks "what's next?" or agent completes task
- **Input:** Current ROADMAP-NNN.md + system state (docs/ + state/)
- **Output:** Console decision (READY, BLOCKED, NEEDS_VALIDATION)
- **Grade:** N/A (reports current state, no prediction)
- **Purpose:** Query-only decision logic to determine next work item readiness

### 2. Documentation Update

#### `MODEL-REFERENCE-ORCHESTRATOR-UPDATE.md`
Section to add to `MODEL-REFERENCE.md` explaining:
- Why the orchestrator is external to the 5×10 field
- The three meta-agents and their roles
- Orchestrator vs. execution layer comparison table
- Invocation flow and integration points

---

## How to Integrate

### Step 1: Add Meta-Agents to `.claude/agents/`

```bash
mkdir -p .claude/agents/orchestrator
cp roadmap-creator.md .claude/agents/orchestrator/
cp roadmap-updater.md .claude/agents/orchestrator/
cp work-scheduler.md .claude/agents/orchestrator/
```

**Note:** These are **meta-agents** — they are not part of the 19 execution agents in the standard roster. Keep them in a separate `orchestrator/` subdirectory to signal they operate at a different level.

### Step 2: Update MODEL-REFERENCE.md

Open `docs/model/MODEL-REFERENCE.md` and insert the content from `MODEL-REFERENCE-ORCHESTRATOR-UPDATE.md` after the "Phase Types" section and before "Altitude × Phase Examples".

### Step 3: Retroactively Formalize Existing Roadmap

Rename `STAGED-PLAN.md` → `ROADMAP-002.md` and add frontmatter:

```yaml
---
artifact_type: ROADMAP
version: 2
altitude: STRATEGIC
phase: IMPLEMENTATION
grade: INFORMED_ESTIMATE
created_at: 2026-05-06
source_synthesis: SYNTHESIS-001
source_vision: ARCHITECTURE-VISION
supersedes: ROADMAP-001 (implicit — never existed)
status: ACTIVE
---
```

**Explanation:** STAGED-PLAN.md was the first roadmap created, but it was never formalized with a version number. Retroactively calling it ROADMAP-002 acknowledges there was an implicit ROADMAP-001 (the mental model before it was written down).

### Step 4: Update DECISIONS.md

Add D-022 (see full text in research report):

```markdown
## D-022 — Orchestrator Layer: External Meta-Workflow

**Date**: 2026-05-07 | **Status**: ACCEPTED | **Level**: system

The nowu 5×10 workflow model defines execution phases but lacks a formal mechanism for deciding what work enters the field next. Introduce an orchestrator layer that sits outside the 5×10 execution field and manages roadmap creation, updates, and work scheduling.

Three meta-agents: roadmap-creator, roadmap-updater, work-scheduler.
One versioned artifact: ROADMAP-NNN.md in docs/.

The orchestrator is not part of the 5×10 grid — it decides what work enters the grid.
```

### Step 5: Run W3.9 Validation (Immediate Next Work)

Before proceeding to W4 (First S1-S9 intake), validate readiness:

```markdown
## W3.9: v1-core Readiness Validation

### Module Readiness (Critical Path)
- [ ] core/contracts.py exists with KnowledgeAtom, EpistemicGrade, AdapterProtocol types
- [ ] flow/ module scaffolded
- [ ] know/ module scaffolded
- [ ] bridge/ module scaffolded
- [ ] soul/ module scaffolded

### Agent Readiness
- [ ] 19 agent .md files exist in .claude/agents/
- [ ] Agent frontmatter is parseable (spot-check 5 agents)

### Verification Infrastructure
- [ ] tests/architecture/test_adr_fitness.py passes
- [ ] verify-artifact.py exists and is runnable

### Session State Infrastructure
- [ ] state/intake/ directory exists
- [ ] state/arch/ directory exists
- [ ] state/health/ directory exists

### Dependency Validation (W4 specific)
- [ ] F1+F2 complete: contracts baseline exists
- [ ] K1 complete: traceability metadata in new artifacts
- [ ] A1 complete: existing agents still work

**Result:**
- If all checks pass → W4 is READY
- If any check fails → W4 is BLOCKED, next work item is [fix the blocker]
```

---

## Usage Examples

### Example 1: Bootstrap Initial Roadmap

```bash
# After P0.V, P0.G, and 15 UCs exist
claude --agent roadmap-creator

# Creates docs/ROADMAP-001.md with:
# - Stage structure (v1-core, v1, v1.1, v2)
# - Work grid (Workflow, Knowledge, Agents, Framework × stages)
# - Dependency graph
# - Stage gates
# - Risk register
```

### Example 2: Update Roadmap After SYNTHESIS

```bash
# After SYNTHESIS-001 completes
claude --agent roadmap-updater --input ROADMAP-001.md SYNTHESIS-001.md

# Creates docs/ROADMAP-002.md with:
# - All content from ROADMAP-001
# - ADR roadmap from SYNTHESIS Section 3
# - Updated UC-to-stage mapping based on SYNTHESIS themes
# - New work items for recommended ADRs
```

### Example 3: Query What's Next

```bash
# User asks "what should I work on next?"
claude --agent work-scheduler

# Output:
# status: READY
# next_work_item: W4
# description: First S1-S9 intake end-to-end
# agent_to_invoke: orchestrator (flow module)
# input_artifacts:
#   - docs/USE_CASES.md (select 1 UC)
#   - docs/architecture/ARCHITECTURE-VISION.md
#   - docs/architecture/adr/ADR-0007.md
```

---

## Key Design Principles

### 1. External to Execution

The orchestrator is **not a phase** in the 5×10 grid — it operates on the grid from outside. This matches industry patterns:
- Shape Up: Betting table happens during cooldown, not inside the 6-week cycle
- SAFe: PI Planning is a separate 2-day event, not part of sprints
- Temporal: Workflow tasks coordinate Activity tasks but are separate entities

### 2. Versioned Roadmap

Every roadmap update creates a new version with `supersedes` field. This enables:
- Traceability: What changed and why
- Grade progression: HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED
- Rollback: If a roadmap update was wrong, revert to previous version

### 3. Milestone-Driven Updates

The orchestrator is not invoked during execution — only at milestone boundaries:
- After SYNTHESIS (architectural evidence)
- After Architecture Vision (risks, quality attributes)
- After stage gates (execution feedback)

This prevents constant roadmap churn and ensures updates are based on substantial new evidence.

### 4. Read-Only Scheduler

`work-scheduler` never modifies the roadmap — it only queries current state to decide what's next. This ensures the roadmap is the single source of truth and prevents accidental updates during routine queries.

---

## Relationship to Existing Architecture

| Component | Layer | Altitude | Role |
|---|---|---|---|
| **Orchestrator** (3 meta-agents) | Meta | STRATEGIC (roadmap-creator, roadmap-updater) or N/A (work-scheduler) | Decides what work enters the field |
| **5×10 Field** (19 execution agents) | Execution | STRATEGIC, PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION | Executes the work (SENSE, PROBLEM, ANALYSIS, etc.) |
| **ROADMAP-NNN.md** | Meta-artifact | STRATEGIC/IMPLEMENTATION | System of record for sequencing and dependencies |
| **Session artifacts** (state/) | Execution artifacts | Various altitudes | Work products from execution agents |

**The key distinction:** Orchestrator agents are not phases — they are the **planning system** that feeds work into the **execution system**.

---

## FAQ

### Q: Why is the orchestrator external to the 5×10 grid?

Because orchestration is not a phase type — it's a meta-level activity. The 5×10 grid defines what phases exist (SENSE, PROBLEM, ANALYSIS, etc.), but it doesn't define what sequence to execute them in or when to execute them. That's the orchestrator's job.

### Q: Can execution agents read the roadmap directly?

Yes, but they should use `work-scheduler` as the interface. `work-scheduler` knows how to interpret the roadmap's dependency graph and stage gates — execution agents should just ask "what's next?" rather than parsing the roadmap themselves.

### Q: What if the roadmap becomes out of sync with reality?

`work-scheduler` will detect this and flag it. For example, if ROADMAP-003.md says "Next is W4" but W4's dependencies are missing, `work-scheduler` will output `status: BLOCKED` and recommend invoking `roadmap-updater` to fix the discrepancy.

### Q: Do I need to manually invoke these agents, or can they run automatically?

**Current state:** Manual invocation (user calls `claude --agent roadmap-updater`).

**Future state (v1.1+):** Automatic invocation when milestones complete:
- SYNTHESIS completes → auto-trigger `roadmap-updater`
- Stage gate passes → auto-trigger `roadmap-updater`
- User asks "what's next?" → auto-trigger `work-scheduler`

The agents are designed to be automatable — they have clear trigger conditions and well-defined inputs/outputs.

### Q: How does this relate to P0-P4 pre-workflow phases?

P0-P4 are **execution phases** inside the 5×10 field at STRATEGIC, PRODUCT, and DELIVERY altitudes. The orchestrator decides **when** to run P0-P4 work based on the roadmap. For example:
- Roadmap says "Stage v1-core needs P0.V + P0.G first"
- User invokes P0.V (execution agent)
- P0.V completes
- `work-scheduler` says "Next is P0.G"
- User invokes P0.G (execution agent)
- P0.G completes, 10 UCs exist
- `work-scheduler` says "Next is roadmap-creator" (orchestrator agent)

---

## Credits

This orchestrator design synthesizes patterns from:
- **Shape Up** (Basecamp): Betting table as external orchestration layer
- **SAFe** (Scaled Agile): PI Planning as meta-workflow
- **Temporal** (Workflows): Workflow tasks vs. Activity tasks separation
- **AFLOW** (ICLR 2025): Workflow optimizer as external to workflow nodes
- **AgentOrchestra** (2025): Planning Agent vs. Execution Agents hierarchy
- **HTN Planning** (Classical AI): Compound tasks as orchestration layer

All patterns converge on the same insight: **mature workflow systems separate execution (the work) from orchestration (deciding what work happens next)**.
