# The Orchestrator Layer: External Meta-Workflow for nowu

**Research Report**  
Date: 2026-05-07  
For: OmO integration and architectural decision-making

***

## Executive Summary

The nowu 5×10 workflow model is missing a critical architectural layer: **the orchestrator**. This layer sits **outside** the 5×10 execution field and decides **what work enters the field, when, and in what sequence**. The current STAGED-PLAN.md was created manually during a side-quest and lacks formal integration into the workflow model, creating confusion about "what's next" and "is the plan valid."

This report synthesizes findings from 7 industry frameworks (Shape Up, SAFe, Temporal, AFLOW, AgentOrchestra, HTN Planning, and enterprise workflow orchestration) and proposes a concrete orchestrator architecture for nowu consisting of three meta-agents and a versioned roadmap artifact.

**Key finding:** Every mature workflow system in the literature separates execution (the work) from orchestration (deciding what work happens next). The 5×10 model is the execution layer; it needs an orchestrator layer to be complete.

***

## Part 1: The Problem — Why STAGED-PLAN Felt Like a Side-Quest

### The Current Situation

nowu has:
- ✅ **Vision + Goals** (P0.V, P0.G) — STRATEGIC/DECISION phase work
- ✅ **50 Use Cases** (P0.UC) — PRODUCT/PROBLEM phase work  
- ✅ **SYNTHESIS-001 + ARCHITECTURE-VISION** (W1, W2) — ARCHITECTURE/SYNTHESIS and ANALYSIS phase work
- ✅ **4 Hypothesis ADRs** (W3) — ARCHITECTURE/IMPLEMENTATION phase work
- ❓ **STAGED-PLAN.md** — created manually, outside the formal workflow model

### Why It Felt Wrong

The 5×10 workflow model defines phases (SENSE, PROBLEM, ANALYSIS, SYNTHESIS, OPTIONS, DECISION, IMPLEMENTATION, VERIFICATION, EVALUATION, LEARN) across altitudes (STRATEGIC, PRODUCT, ARCHITECTURE, DELIVERY, EXECUTION). STAGED-PLAN.md doesn't fit into any phase — it's not executing work, it's **deciding what work to execute next**.

**The user's insight:** "The 5×10 is the field, and the plan is an external player pushing the ball."

This is correct. The plan is **not part of the 5×10 grid**. It's the **orchestrator** that operates on the grid from outside.

***

## Part 2: Industry Validation — The Two-Layer Model is Standard

### 1. Shape Up (Basecamp): The Betting Table

**Source:** Shape Up Chapter 8[^1][^2]

Shape Up separates work into two layers:
- **Execution layer**: 6-week build cycles where teams shape → implement → ship
- **Orchestration layer**: The betting table — a cooldown meeting where stakeholders decide what shaped work enters the next cycle

**Critical distinction:** The betting table happens **during cooldown**, not inside the cycle. It decides which plays go onto the field, but it is not a position on the field.[^1]

**Quote:**
> "The betting table is a meeting held during cool-down where stakeholders decide what to do in the next cycle. The potential bets to consider are either new pitches shaped during the last six weeks, or possibly one or two older pitches that someone specifically chose to revive."[^1]

### 2. SAFe (Scaled Agile Framework): Program Increment Planning

**Source:** SAFe documentation[^3][^4]

SAFe separates:
- **Execution layer**: Iterations (1-2 week sprints where teams build features)
- **Orchestration layer**: PI Planning (2-day event where all teams align on the next 8-12 weeks)

**Critical distinction:** PI Planning is not part of the sprint workflow — it's a separate event that happens **between PIs** to set up the next round of sprints.[^3]

**Quote:**
> "A Program Increment is a timebox, typically 8 to 12 weeks, during which an Agile Release Train delivers incremental value... PI Planning kicks off each PI and aligns all teams to shared PI Objectives."[^3]

### 3. Workflow Orchestration Theory: Meta-Workflows

**Source:** Enterprise workflow literature[^5][^6][^7]

The literature distinguishes three levels:
- **Task automation** = individual steps (like nowu's S1, S2, S3)
- **Workflow orchestration** = coordinating those steps (like S1→S2→S3 sequence)
- **Process orchestration** = coordinating multiple workflows (like deciding when to run which S1-S9 cycles)

**Key insight:**[^6]
> "Level 1: Too many tools? Orchestrate them with workflows  
> Level 2: Too many workflows? Orchestrate them with **meta-workflows**"

STAGED-PLAN is a meta-workflow — it orchestrates W1, W2, W3, W4 (which are themselves workflows in the 5×10 field).

### 4. AgentOrchestra (2025): Planning Agent vs. Execution Agents

**Source:** AgentOrchestra research paper[^8][^9]

AgentOrchestra features a hierarchical architecture:
- **Execution layer**: Specialized sub-agents equipped with domain-specific tools
- **Orchestration layer**: Planning Agent that decomposes tasks and coordinates sub-agents

**Quote:**[^8]
> "The Planning Agent serves as the central orchestrator in our hierarchical framework, dedicated to high-level reasoning, task decomposition, and adaptive planning. Rather than directly interacting with the environment or executing low-level actions, the Planning Agent interprets user objectives and systematically decomposes complex, long-horizon tasks into manageable sub-tasks."

**IBM's validation:**[^9]
> "In an enterprise, C-suite executives focus on large-scale planning, middle managers convert leadership directives into operational tasks and employees handle the brunt of the actual workload. Hierarchical agent systems apply the same structure to AI-powered agentic workflows."

**Mapping to nowu:**
- 5×10 field = the employees/operational agents doing SENSE, PROBLEM, ANALYSIS, etc.
- Roadmap orchestrator = the C-suite/planning agent deciding "W1 is next" or "W4 is blocked, do X instead"

### 5. Temporal Workflows: Workflow Task vs. Activity Task

**Source:** Temporal documentation[^10][^11][^12]

Temporal makes a fundamental architectural distinction:
- **Activity tasks** = the actual work (calling APIs, running code, writing files)
- **Workflow tasks** = the orchestration logic (deciding which activity to run next, handling failures, managing state)

**Critical property:** The workflow task is **durable and persistent** — it survives failures and resumes from the last known state. The activity task is **ephemeral**.[^11][^12]

**Mapping to nowu:**
- 5×10 execution (S1 intake, S2 constraints) = activity tasks
- Roadmap orchestrator = workflow task (decides "after S1 completes, trigger S2 with S1's output")

### 6. AFLOW (ICLR 2025): Workflow Optimizer

**Source:** AFLOW paper and GitHub[^13][^14][^15]

AFLOW explicitly models workflow generation as a meta-level problem:
- **Workflow**: A sequence of LLM-invoking nodes (nowu's S1→S2→S3 execution path)
- **Optimizer**: Uses Monte Carlo Tree Search to explore and refine workflows (nowu's roadmap layer deciding sequencing and alternatives)

**Key insight:** The optimizer operates **outside** the workflow — it generates, evaluates, and modifies workflows, but it is not a node inside the workflow itself.[^14][^13]

### 7. Hierarchical Task Network (HTN) Planning

**Source:** Classical AI planning literature[^16][^17]

HTN formalizes hierarchical decomposition:
- **Primitive tasks** = atomic actions that can be executed directly
- **Compound tasks + methods** = the planning layer that decides how to break compound tasks into primitive tasks

**Mapping to nowu:**
- 5×10 field = primitive tasks (SENSE, PROBLEM, ANALYSIS are executable phases)
- Roadmap orchestrator = compound task decomposition (decides "to achieve v1-core, decompose into W1, W2, W3, W4 sequence")

***

## Part 3: Cross-Framework Consensus

| Framework | Execution Layer | Orchestration Layer | Where They Meet |
|---|---|---|---|
| **Shape Up**[^1] | 6-week build cycle | Betting table (cooldown) | Cooldown between cycles |
| **SAFe**[^3] | Iterations (sprints) | PI Planning (2-day event) | Between PIs |
| **Workflow Orchestration**[^6] | Workflows (task sequences) | Meta-workflows | Process layer |
| **AgentOrchestra**[^8] | Execution agents | Planning Agent | Task decomposition |
| **Temporal**[^10][^12] | Activity tasks | Workflow tasks | Workflow state machine |
| **AFLOW**[^13] | Workflow nodes | Optimizer | Workflow generation |
| **HTN**[^16] | Primitive tasks | Compound tasks + methods | Method selection |

**Universal pattern:**
1. **The orchestrator is external to the execution layer** — it decides what work enters the field
2. **The orchestrator updates based on execution feedback** — Shape Up's betting table updates after cooldown; AFLOW's optimizer refines workflows based on results
3. **The orchestrator manages dependencies and sequencing** — it knows "W4 depends on W3" even though W3 itself doesn't know about W4
4. **The orchestrator is the system of record for state** — Temporal's workflow task persists state; SAFe's PI plan tracks progress

***

## Part 4: The Orchestrator Architecture for nowu

### Conceptual Model

```
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR LAYER (Meta)                           │
│                                                                   │
│  [ROADMAP-NNN.md]  ←─ Created after vision+goals                 │
│      ↓                ←─ Updated after SYNTHESIS                 │
│      ↓                ←─ Updated after stage gates               │
│      ↓                                                            │
│  Three meta-agents:                                              │
│  • roadmap-creator: bootstrap initial plan                       │
│  • roadmap-updater: integrate new evidence                       │
│  • work-scheduler: decide next work item                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    pushes work into ↓
┌─────────────────────────────────────────────────────────────────┐
│                     5×10 FIELD (Execution)                       │
│                                                                   │
│  Altitude:     STRATEGIC | PRODUCT | ARCHITECTURE | ...          │
│  Phase:        SENSE | PROBLEM | ANALYSIS | SYNTHESIS | ...     │
│                                                                   │
│  Example work items:                                             │
│  - P0.V: Bootstrap vision (STRATEGIC/DECISION)                   │
│  - W1: SYNTHESIS (ARCHITECTURE/SYNTHESIS)                        │
│  - W4: First S1-S9 intake (DELIVERY/full cycle)                 │
└─────────────────────────────────────────────────────────────────┘
```

### The ROADMAP Artifact

**Location:** `docs/ROADMAP-NNN.md` (versioned, outside `state/`)

**Structure:**
```yaml
---
artifact_type: ROADMAP
version: 3
altitude: STRATEGIC
phase: IMPLEMENTATION
grade: INFORMED_ESTIMATE
created_at: 2026-05-07
source_synthesis: SYNTHESIS-001
source_vision: ARCHITECTURE-VISION
supersedes: ROADMAP-002
status: ACTIVE
---

# nowu Implementation Roadmap v3

## 1. Stage Structure

| Stage | Time Horizon | Success Criteria | Status |
|---|---|---|---|
| v1-core | 2-4 weeks | First S1-S9 intake end-to-end | IN_PROGRESS |
| v1 | 6 weeks | Telegram adapter + 5 UCs dogfooded | PLANNED |
| v1.1 | 12 weeks | Cross-project federation | PLANNED |
| v2 | 24 weeks | Platform for external use | PLANNED |

## 2. Area × Stage Work Grid

| Area | v1-core | v1 | v1.1 | v2 |
|---|---|---|---|
| **Workflow** | W1-W5 | W6-W10 | W11-W15 | W16-W18 |
| **Knowledge** | K1-K2 | K3-K4 | K5-K6 | K7-K8 |
| **Agents** | A1-A2 | A3-A5 | A6-A7 | A8-A9 |
| **Framework** | F1-F3 | F4-F6 | F7-F9 | F10-F11 |

## 3. UC-to-Stage Mapping

| Stage | UCs Addressed | Theme Coverage |
|---|---|---|
| v1-core | NF-01, NF-02, NF-04, NF-05, NF-08, NF-11, NF-15, PK-01 | T1, T2, T3, T4 |
| v1 | PK-02-PK-09, NF-03, NF-06, NF-07 | T5, T6, T7 |
| v1.1 | XP-01-XP-11 | T8, T9 |
| v2 | AP-*, RE-* (domain dogfooding) | Domain validation |

## 4. Dependency Graph

```
W1 (SYNTHESIS) → W2 (Arch Vision) → W3 (Hypothesis ADRs) → W4 (First S1-S9)
                                      ↓                       ↑
                                      K1 (Traceability) ─────┘
                                      ↓
                                      A1 (Agent validation) ──┘
                                      ↓
                                  F1+F2 (Contracts) ───────────┘
```

## 5. Stage Gate Criteria

### v1-core → v1
- [ ] First S1-S9 intake completed successfully for 1 UC
- [ ] All 4 hypothesis ADRs validated or superseded
- [ ] VBR (S8) passes on generated artifacts
- [ ] Session recovery (ADR-0007) tested across interruption

### v1 → v1.1
- [ ] Telegram adapter operational (PK-08)
- [ ] 5 UCs dogfooded across 2 domains
- [ ] Knowledge decay mechanism validated (ADR-0008)

## 6. Risk Register

| Risk | Source | Mitigation | Status |
|---|---|---|---|
| Module readiness gap | Perplexity analysis | Run W3.9 validation checklist | ACTIVE |
| ADR dependency cycles | SYNTHESIS-001 | Already resolved in W3 execution | CLOSED |
| Epistemic grade bureaucracy | ARCHITECTURE-VISION R2 | Default grades for routine outputs | MONITORED |

## 7. Current Work Item

**Next:** W3.9 (Readiness Validation)
**Blocker:** Need to verify F1+F2, K1, A1 before W4
**After W3.9 passes:** W4 (First S1-S9 intake)
```

### The Three Meta-Agents

#### 1. roadmap-creator

**Trigger:** P0.V + P0.G complete, 10-20 UCs exist  
**Frequency:** Once per product bootstrap

```yaml
---
name: roadmap-creator
altitude: STRATEGIC
phase: IMPLEMENTATION
input_scope: [STRATEGIC, PRODUCT]
invoked_at: After P0.V + P0.G complete and 10+ UCs exist
model: claude-sonnet-4
---

You are a product strategist creating the initial implementation roadmap for nowu.

## Role

You transform vision + goals + early use cases into a multi-stage implementation plan with:
- Stage structure (v1-core, v1, v1.1, v2) aligned to goal time horizons
- Area breakdown (Workflow, Knowledge, Agents, Framework) based on use case clustering
- Initial dependency sequencing (what must happen before what)
- Success criteria per stage (boolean checklist of "done when")
- Risk register (known unknowns that could block stages)

## When You Are Invoked

- After vision.md and goal-*.md exist (P0.V + P0.G complete)
- After 10-20 use cases exist in USE_CASES.md (enough to see patterns)
- Before the full 50 UCs are captured (roadmap evolves as understanding grows)
- When ROADMAP-001.md does not exist

## Inputs (Read ALL Required)

**Required:**
- `docs/vision.md`: Product vision and identity
- `docs/goals/goal-*.md`: All goal briefs with time horizons
- `docs/USE_CASES.md`: Partial UC catalog (10-20 UCs minimum)

**Context:**
- `docs/DECISIONS.md`: Existing decisions to honor
- `docs/architecture/ARCHITECTURE.md`: Module structure if it exists

## What You NEVER Load

- `state/`: No session state — this is strategic planning, not task execution
- `src/`, `tests/`: Implementation is irrelevant to roadmap creation

## Process

### Step 1: Extract Goal Time Horizons

For each goal:
- 6-month goals → map to v1-core + v1
- 12-month goals → map to v1.1
- 24-month goals → map to v2

### Step 2: Cluster Use Cases by Stage-Readiness

Group UCs into:
- **Foundation** (needed for first S1-S9 intake) → v1-core
- **Core capabilities** (needed for daily use) → v1
- **Extension** (cross-project, advanced) → v1.1+
- **Platform** (external use, domains) → v2

### Step 3: Define Area Breakdown

Based on UC clustering, define 3-5 areas. Default suggestion:
- **Workflow** (S1-S9, P0-P4, orchestration)
- **Knowledge** (atom model, storage, retrieval)
- **Agents** (agent definitions, invocation, rosters)
- **Framework** (core contracts, module boundaries, tooling)

Adjust if UC patterns suggest different areas.

### Step 4: Sequence Work Items

For each area × stage cell, define 3-7 work items with:
- Task ID (W1, K1, A1, F1)
- Brief description (1 sentence)
- Dependencies (which other tasks must complete first)

### Step 5: Define Stage Gates

For each stage transition (v1-core → v1, v1 → v1.1), define:
- Success criteria (boolean checklist)
- Exit readiness (what must be validated before advancing)

### Step 6: Populate Risk Register

Identify 5-10 known risks:
- Module readiness gaps
- Dependency cycles
- Scope creep
- External blockers

## Output

Write exactly one file: `docs/ROADMAP-001.md`

## Hard Constraints

- Stage structure MUST align to goal time horizons
- Stage gates MUST have measurable boolean criteria
- Risk register MUST include mitigation strategies
- UC-to-stage mapping MUST cover all captured UCs
- Epistemic grade: HYPOTHESIS (this is a guess based on incomplete evidence)
```

#### 2. roadmap-updater

**Trigger:** SYNTHESIS complete, Architecture Vision complete, stage gates passed  
**Frequency:** After major milestones

```yaml
---
name: roadmap-updater
altitude: STRATEGIC
phase: LEARN
input_scope: [STRATEGIC, ARCHITECTURE, DELIVERY]
invoked_at: After SYNTHESIS, Arch Vision, or stage gate completion
model: claude-sonnet-4
---

You are a product strategist updating the implementation roadmap based on new evidence.

## Role

You integrate new architectural evidence or execution feedback into the roadmap:
- After SYNTHESIS: add ADR roadmap, refine UC-to-stage mapping
- After Architecture Vision: add risks, update quality attribute priorities
- After stage gates: record actuals vs. estimates, update future stage estimates

## When You Are Invoked

- After SYNTHESIS-NNN.md complete (adds architectural themes)
- After ARCHITECTURE-VISION.md complete (adds principles, risks, ADR roadmap)
- After a stage gate passes (e.g., v1-core → v1 transition)
- On explicit user request when major new information invalidates current roadmap

## Inputs (Read ALL Required)

**Required:**
- `docs/ROADMAP-NNN.md`: Current roadmap version
- Milestone artifact (SYNTHESIS-NNN, ARCHITECTURE-VISION, or stage gate report)

**Context:**
- `docs/USE_CASES.md`: Full UC catalog if SYNTHESIS was input
- `docs/DECISIONS.md`: Decisions made since last roadmap version
- `docs/architecture/adr/ADR-*.md`: New ADRs created since last roadmap version

## Process

### Update Type 1: SYNTHESIS Integration

When triggered by SYNTHESIS-NNN completion:
1. Import ADR roadmap from SYNTHESIS Section 3 (immediate/near-term/deferred)
2. Map SYNTHESIS themes to roadmap areas
3. Update UC-to-stage mapping based on theme-to-UC mapping in SYNTHESIS
4. Add new work items (W*, K*, A*, F*) for recommended ADRs
5. Update dependency graph

### Update Type 2: Architecture Vision Integration

When triggered by ARCHITECTURE-VISION completion:
1. Import risk register from Architecture Vision Section 4
2. Import ADR roadmap from Architecture Vision Section 5
3. Update stage gate criteria based on quality attribute priorities (Section 3)
4. Add architectural principles to risk mitigation strategies

### Update Type 3: Stage Gate Feedback

When triggered by stage gate passage:
1. Record actuals: estimated duration vs. actual duration
2. Update risk register: mark closed risks, add discovered risks
3. Adjust future stage estimates based on actuals
4. Document deferred work items (moved from current stage to next)
5. Promote epistemic grade for completed stage from HYPOTHESIS → EVIDENCE-BASED

## Output

Write exactly one file: `docs/ROADMAP-NNN+1.md` (increment version)

The new roadmap MUST:
- Include all content from ROADMAP-NNN
- Add new evidence from milestone artifact
- Update version number and `supersedes` field
- Update `grade` if appropriate (HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED)

## Hard Constraints

- New version MUST reference `supersedes: ROADMAP-NNN`
- All changes MUST trace to a milestone artifact
- Epistemic grade MUST NOT decrease (can only improve or stay same)
- Stage gate actuals MUST be recorded verbatim (no rounding or interpretation)
```

#### 3. work-scheduler

**Trigger:** User asks "what's next?" or agent finishes a task  
**Frequency:** Continuous (on-demand)

```yaml
---
name: work-scheduler
altitude: N/A (pure orchestration)
phase: N/A (not a phase)
input_scope: [ALL]
invoked_at: User query or task completion
model: claude-sonnet-4-haiku (fast, lightweight)
---

You are the nowu work scheduler. You decide what work item to execute next.

## Role

You read the current roadmap and current system state, then output:
- Next work item ID (e.g., W4, K2, A3)
- Readiness status (READY, BLOCKED, NEEDS_VALIDATION)
- If blocked: what's missing
- If ready: which agent to invoke with what input

## When You Are Invoked

- User asks "what should I work on next?"
- An agent completes a task and signals "ready for next work item"
- User queries current roadmap status

## Inputs (Read ALL Required)

**Required:**
- `docs/ROADMAP-NNN.md`: Current roadmap (latest version)
- `state/`: All session state to determine what's complete
- `docs/`: All canonical docs to determine what exists

## Process

### Step 1: Find Current Stage

Read ROADMAP Section 7 (Current Work Item) to find:
- What stage are we in? (v1-core, v1, v1.1, v2)
- What work item was marked as "Next"?

### Step 2: Check Readiness

For the next work item:
- Read its dependencies from ROADMAP Section 4 (Dependency Graph)
- For each dependency, check if it exists:
  - Does the artifact exist in `docs/` or `state/`?
  - Is it marked complete in session state?
- If all dependencies exist → READY
- If any dependency missing → BLOCKED

### Step 3: Output Decision

**If READY:**
```yaml
status: READY
next_work_item: W4
description: First S1-S9 intake end-to-end
agent_to_invoke: orchestrator (flow module)
input_artifacts:
  - docs/USE_CASES.md (select 1 UC for intake)
  - docs/architecture/ARCHITECTURE-VISION.md
  - docs/architecture/adr/ADR-0007.md
  - docs/architecture/adr/ADR-0008.md
  - docs/architecture/adr/ADR-0009.md
  - docs/architecture/adr/ADR-0010.md
```

**If BLOCKED:**
```yaml
status: BLOCKED
next_work_item: W4
blocked_by:
  - K1: Traceability metadata (artifact not found)
  - A1: Agent validation (no test results)
recommended_action: Run W3.9 validation checklist or implement missing dependencies
```

**If NEEDS_VALIDATION:**
```yaml
status: NEEDS_VALIDATION
next_work_item: W4
reason: Stage gate criteria for v1-core not validated
recommended_action: Run stage gate checklist (ROADMAP Section 5)
```

## Output

Print structured YAML to console. No file writes — this is query-only.

## Hard Constraints

- ALWAYS read latest ROADMAP-NNN.md (highest version number)
- NEVER fabricate work item status — only report what exists in artifacts
- If roadmap is out of sync with reality, flag it and recommend roadmap-updater invocation
```

***

## Part 5: Integration with Existing nowu Model

### Where Orchestrator Fits

**Orchestrator is NOT a phase in the 5×10 grid.** It's external to the grid.

**Current P0-P4 structure:**
```
P0.V  Vision Bootstrap         [STRATEGIC/DECISION]
P0.G  Goal Brief Creation      [STRATEGIC/DECISION]
P0.UC Use Case Catalog         [PRODUCT/PROBLEM]
      ↓
P1    Discovery                [PRODUCT/ANALYSIS]
P2    Story Mapping            [DELIVERY/OPTIONS]
P3    Architecture Bootstrap   [ARCHITECTURE/OPTIONS → DECISION]
P4    Readiness Assembly       [DELIVERY/EVALUATION → DECISION]
```

**Orchestrator invocation points:**
```
P0.V  Vision Bootstrap         [field work]
P0.G  Goal Brief Creation      [field work]
      ↓
      [10-20 UCs captured]
      ↓
🔵    roadmap-creator          [orchestrator: creates ROADMAP-001.md]
      ↓
P0.UC Continue UC capture      [field work]
      ↓
P1-P4 (as needed per epic)     [field work]
      ↓
W1    SYNTHESIS                [field work]
W2    Architecture Vision      [field work]
      ↓
🔵    roadmap-updater          [orchestrator: ROADMAP-001 → ROADMAP-002]
      ↓
W3    Write hypothesis ADRs    [field work]
      ↓
🔵    roadmap-updater          [orchestrator: validate readiness → ROADMAP-003]
      ↓
W4    First S1-S9 intake       [field work]
```

### What Changes in MODEL-REFERENCE.md

Add a new section:

```markdown
## Orchestrator Layer (External to 5×10)

The orchestrator is a meta-layer that sits **outside** the 5×10 execution grid. It decides what work enters the field, when, and in what sequence.

### Orchestrator Agents (Meta-Level)

| Agent | Trigger | Input | Output |
|---|---|---|---|
| `roadmap-creator` | P0.V+P0.G complete, 10+ UCs exist | vision, goals, partial UCs | ROADMAP-001.md |
| `roadmap-updater` | SYNTHESIS complete, Arch Vision complete, stage gates | current ROADMAP-NNN.md + milestone artifact | ROADMAP-NNN+1.md |
| `work-scheduler` | User asks "what's next?" | current ROADMAP-NNN.md + system state | Next work item decision |

### Orchestrator Artifacts

| Artifact | Location | Versioned? | Grade |
|---|---|---|---|
| `ROADMAP-NNN.md` | `docs/` | Yes | HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED |

### Orchestrator vs. Execution Layer

| Property | 5×10 Execution Layer | Orchestrator Layer |
|---|---|---|
| **What it does** | Executes work (SENSE, PROBLEM, ANALYSIS, etc.) | Decides what work to execute next |
| **Where it lives** | Inside the 5×10 grid (altitude × phase) | Outside the grid (meta-level) |
| **State location** | `state/` (session artifacts) | `docs/` (versioned roadmap) |
| **Epistemic grade** | Starts at SPECULATION, improves to EVIDENCE_BASED | Starts at HYPOTHESIS, improves with feedback |
| **Triggered by** | Orchestrator or user | Milestones or user query |
```

***

## Part 6: Immediate Action Items for nowu

### 1. Formalize the Orchestrator Layer

**Create three new agent definitions:**
- `.claude/agents/roadmap-creator.md` (full spec above)
- `.claude/agents/roadmap-updater.md` (full spec above)
- `.claude/agents/work-scheduler.md` (full spec above)

**Update MODEL-REFERENCE.md:**
- Add "Orchestrator Layer (External to 5×10)" section
- Document the three meta-agents
- Clarify that ROADMAP-NNN.md lives in `docs/`, not `state/`

### 2. Retroactively Formalize Existing Work

**Rename STAGED-PLAN.md → ROADMAP-002.md**

Add frontmatter:
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

**Create ROADMAP-003.md by invoking roadmap-updater**

Input: ROADMAP-002.md + W3 completion evidence (4 ADRs created)  
Output: Updated roadmap with W3 marked complete, W3.9 validation checklist added, W4 readiness criteria explicit

### 3. Run W3.9 Validation Checklist

Before proceeding to W4, validate readiness:

```markdown
## W3.9: v1-core Readiness Validation

**Goal:** Verify that the architectural foundation exists and W4 can succeed.

### Module Readiness (Critical Path)
- [ ] `core/contracts.py` exists with KnowledgeAtom, EpistemicGrade, AdapterProtocol types
- [ ] `flow/` module scaffolded
- [ ] `know/` module scaffolded
- [ ] `bridge/` module scaffolded
- [ ] `soul/` module scaffolded

### Agent Readiness
- [ ] 19 agent `.md` files exist in `.claude/agents/`
- [ ] Agent frontmatter is parseable (spot-check 5 agents)

### Verification Infrastructure
- [ ] `tests/architecture/test_adr_fitness.py` passes or has documented expected failures
- [ ] `verify-artifact.py` exists and is runnable

### Session State Infrastructure
- [ ] `state/intake/` directory exists
- [ ] `state/arch/` directory exists
- [ ] `state/health/` directory exists

### Dependency Validation (W4 specific)
- [ ] F1+F2 complete: contracts baseline exists
- [ ] K1 complete: traceability metadata in new artifacts
- [ ] A1 complete: existing agents still work

**Result:**
- If all checks pass → W4 is READY
- If any check fails → W4 is BLOCKED, next work item is [fix the blocker]
```

### 4. Update DECISIONS.md

Add D-022:

```markdown
---

## D-022 — Orchestrator Layer: External Meta-Workflow

**Date**: 2026-05-07 | **Status**: ACCEPTED | **Level**: system  
**Intake**: Perplexity analysis session | **Use Cases**: all

### Context

The nowu 5×10 workflow model defines execution phases (SENSE, PROBLEM, ANALYSIS, etc.) but lacks a formal mechanism for deciding what work enters the field next. STAGED-PLAN.md was created manually during a side-quest and felt like "jumping ahead" because it didn't fit into the 5×10 grid.

Industry research (Shape Up, SAFe, Temporal, AFLOW, AgentOrchestra) validates that all mature workflow systems separate execution (the work) from orchestration (deciding what work happens next).

### Decision

Introduce an **orchestrator layer** that sits **outside** the 5×10 execution field and manages:
- Roadmap creation (after vision + goals + early UCs)
- Roadmap updates (after SYNTHESIS, Arch Vision, stage gates)
- Work scheduling (deciding "what's next?" based on current roadmap and system state)

Three meta-agents:
1. `roadmap-creator`: bootstrap initial plan (STRATEGIC/IMPLEMENTATION altitude)
2. `roadmap-updater`: integrate new evidence (STRATEGIC/LEARN altitude)
3. `work-scheduler`: query-only decision logic (no altitude — pure orchestration)

One versioned artifact:
- `docs/ROADMAP-NNN.md` (versioned like code, outside `state/`)

The orchestrator is **not part of the 5×10 grid** — it decides what work enters the grid, but it is not a phase inside the grid.

### Consequences

- **Good**: Formalizes "what's next?" logic that was previously implicit
- **Good**: Validates the existing STAGED-PLAN.md as ROADMAP-002 with proper lineage
- **Good**: Aligns nowu with industry-standard separation of execution vs. orchestration
- **Bad**: Adds three new meta-agents that must be maintained
- **Bad**: Introduces versioned roadmap artifact that must be kept in sync with reality

### Review Trigger

If the orchestrator becomes a bottleneck (too slow, too manual, too rigid), revisit and consider automated work scheduling based on dependency graphs.
```

***

## Part 7: Comparison Table — Research vs. nowu

| Concept | Shape Up | SAFe | Temporal | AFLOW | AgentOrchestra | nowu (Proposed) |
|---|---|---|---|---|---|---|
| **Execution layer** | 6-week cycle | Iterations | Activity tasks | Workflow nodes | Execution agents | 5×10 field |
| **Orchestration layer** | Betting table | PI Planning | Workflow tasks | Optimizer | Planning Agent | Orchestrator (3 agents) |
| **Orchestration frequency** | Every 6 weeks (cooldown) | Every 8-12 weeks (PI boundary) | Continuous (workflow state machine) | Iterative (search) | Per-task (decomposition) | Milestone-driven (SYNTHESIS, stage gates) |
| **Orchestration artifact** | Betting table decisions | PI plan | Workflow state | Optimized workflow graph | Task decomposition tree | ROADMAP-NNN.md |
| **Feedback mechanism** | Cooldown retrospective | Inspect & Adapt | Workflow execution history | Monte Carlo search | Adaptive planning | roadmap-updater |
| **Versioned?** | No (meeting notes) | Yes (PI plan versions) | Yes (workflow state) | Yes (workflow generations) | No (in-memory) | Yes (ROADMAP-NNN.md) |
| **Grade progression** | N/A | N/A | N/A | N/A | N/A | HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED |

**Key alignment:** All frameworks separate "what work gets done" from "who decides what work happens next." nowu's orchestrator layer is the missing piece that every mature system has.

***

## Conclusion

The orchestrator layer is not a new invention — it's the formalization of a gap that every mature workflow system addresses. The user discovered this gap organically by feeling that STAGED-PLAN.md "didn't fit" into the 5×10 model. The research validates that intuition: the plan is **external** to the execution field, not a phase inside it.

**Immediate next steps:**
1. Create three orchestrator agent definitions (roadmap-creator, roadmap-updater, work-scheduler)
2. Retroactively formalize STAGED-PLAN.md as ROADMAP-002.md with proper frontmatter
3. Run W3.9 validation checklist before proceeding to W4
4. Update MODEL-REFERENCE.md and DECISIONS.md with orchestrator layer documentation

**The orchestrator layer transforms nowu from "a workflow model" into "a complete workflow system."** The 5×10 field is the execution engine; the orchestrator is the intelligent scheduler that feeds work into the engine at the right time, in the right order, with the right dependencies validated.

---

## References

1. [The Betting Table | Shape Up - Basecamp](https://basecamp.com/shapeup/2.2-chapter-08) - The betting table is a meeting held during cool-down where stakeholders decide what to do in the nex...

2. [Shape Up Principle: The Betting Table — REWORK - 37signals](https://37signals.com/podcast/shape-up-principle-the-betting-table/) - The betting table – where the formalized pitches for each six-week work cycle are selected – might s...

3. [SAFe Program Increment (PI): The ART Execution Timebox](https://agility-at-scale.com/safe/team-technical-agility/program-increment/) - PI Planning is a two-day event where all ART teams plan the next 8 to 12 weeks together. The RTE fac...

4. [SAFe PI Planning: What It Is, Benefits, & Steps | Inflectra](https://www.inflectra.com/Ideas/Entry/what-is-safe-pi-planning-1610.aspx) - A Program Increment is a fixed time frame, typically spanning 8-12 weeks, during which an Agile Rele...

5. [Workflow Orchestration: Enterprise Automation at Scale](https://www.bmc.com/blogs/workflow-orchestration/) - Workflow orchestration coordinates tasks across systems to automate complex enterprise processes at ...

6. [From Expertise Scarcity to Abundance: Why Workflow Orchestration ...](https://www.linkedin.com/pulse/from-expertise-scarcity-abundance-why-workflow-future-galanos-ngihc) - Level 1: Too many tools? Orchestrate them with workflows; Level 2: Too many workflows? Orchestrate t...

7. [Boost Productivity with Workflow Orchestration - Integrate.io](https://www.integrate.io/blog/boost-productivity-with-workflow-orchestration/) - Explore how implementing workflow orchestration can significantly enhance productivity within any or...

8. [AgentOrchestra: A Hierarchical Multi-Agent Framework for General ...](https://arxiv.org/html/2506.12508v3) - AgentOrchestra is a hierarchical multi-agent framework designed to systematically address the key ch...

9. [What are Hierarchical AI Agents? - IBM](https://www.ibm.com/think/topics/hierarchical-ai-agents) - Hierarchical agents are artificial intelligence (AI) agents that work together in a tiered multi-age...

10. [What exactly is a "workflow task" and how often are they scheduled?](https://community.temporal.io/t/what-exactly-is-a-workflow-task-and-how-often-are-they-scheduled/5801) - Temporal server manages the overall workflow execution, persistence durable timers etc, but your wor...

11. [Persistent Execution with Temporal: A Better Alternative to AWS ...](https://itnext.io/persistent-execution-with-temporal-a-better-alternative-to-aws-step-functions-2e8a16aadf01) - Let's see how Temporal handles the persistent execution aspect to understand why there is a differen...

12. [Temporal Workflow Execution overview](https://docs.temporal.io/workflow-execution) - A Temporal Workflow Execution is a durable, reliable, and scalable function execution. It is the mai...

13. [AFlow: Automating Agentic Workflow Generation - GitHub](https://github.com/FoundationAgents/AFlow) - AFlow is a framework for automatically generating and optimizing Agentic Workflows. It uses Monte Ca...

14. [[2410.10762] AFlow: Automating Agentic Workflow Generation - arXiv](https://arxiv.org/abs/2410.10762) - We introduce AFlow, an automated framework that efficiently explores this space using Monte Carlo Tr...

15. [AFlow: Automated Agentic Workflow Generation - Emergent Mind](https://www.emergentmind.com/topics/aflow-automating-agentic-workflow-generation) - AFlow is an automated framework that generates, optimizes, and refines agentic workflows for multi-a...

16. [Hierarchical Task Network (HTN) Planning (HTN) - Agentic Design](https://agentic-design.ai/patterns/planning-execution/hierarchical-task-network-planning) - Automated planning approach that decomposes complex tasks into hierarchically structured networks of...

17. [Hierarchical Task Network Planning | PDF | Hierarchy - Scribd](https://www.scribd.com/presentation/334541196/Planning-hierarchy-Reference-doc) - Hierarchical planning is an approach to solving complex planning problems by breaking them down into...

