# nowu 5×10 Model Reference

**Version:** 1.1  
**Date:** 2026-05-05  
**Status:** CANONICAL

This document is the single authoritative reference for the nowu 5×10 altitude/phase workflow model.

## 1. Overview

The nowu model organizes work across **5 altitudes** and **10 phases** (including **SYNTHESIS**) to separate strategic intent, product understanding, architectural reasoning, delivery planning, and execution detail into explicit cognitive modes. It exists to prevent category errors (for example, coding during shaping or architecture decisions without evidence), enforce epistemic discipline, and create a coherent, traceable flow from idea to verified implementation and promoted learning. The model enables both humans and AI agents to reason at the right level, use the right language, and transition upward or downward with explicit gates.

## 2. Research Foundation

The nowu 5×10 model is grounded in converging findings from agentic software engineering, management science, and workflow systems. Each source contributes a specific structural insight:

- **Guo et al. 2025 (Agentic Software Engineering survey)**
  - Identifies memory architecture as foundational in agentic SE; nowu’s 3-tier memory aligns with this and maps naturally to the `know` module interface.
  - Highlights weak multi-hypothesis generation in many pipelines; nowu’s **SYNTHESIS** phase explicitly addresses cross-case pattern extraction before narrowing.
  - Notes continuous learning gaps; nowu’s **GAP cycle** operationalizes persistent architecture-level learning and correction.

- **Rombaut 2026 (loop primitives)**
  - Defines five reusable primitives: **ReAct**, **Generate-Test-Repair**, **Plan-Execute**, **Retry**, **Tree Search**.
  - nowu’s S1–S9 maps to a compositional pattern:
    - **S1–S5** ≈ Plan-Execute (problem framing and path selection)
    - **S6–S8** ≈ Generate-Test-Repair (implementation and correction)
    - **S9** ≈ reflective loop (learning abstraction and promotion)

- **AFLOW (ICLR 2025)**
  - Establishes seven universal operators: **Generate, Review, Revise, Ensemble, Test, Format, Program**.
  - nowu alignment:
    - **S3** uses Ensemble logic (alternative construction/combination)
    - **S6** uses Generate + Program
    - **S7** emphasizes Review
    - **S8** emphasizes Test

- **Shape Up (Basecamp)**
  - Distinguishes **Shaping**, **Betting**, **Building**.
  - nowu mapping:
    - **P0–P4** = Shaping
    - **S1–S8** = Building
    - **GAP** = cooldown/learning/correction loop between cycles

- **Anthony 1965 (strategic/tactical/operational management levels)**
  - Provides the canonical three-level management model.
  - nowu extends this to five altitudes to preserve modern software distinctions between product and architecture/delivery concerns.

- **MASAI (modular agentic pipeline work)**
  - Demonstrates modular role decomposition and ranked/fixed candidate evaluation.
  - Supports nowu’s S3/S4 split: **Explore → Decide** with explicit alternative generation and constrained selection.

- **Epistemic AI (Manchingal & Cuzzolin)**
  - Frames boundary quality as epistemic quality.
  - nowu altitude boundaries are epistemic boundaries: each altitude encodes what can be known, argued, or decided at that layer.

- **Context rot research (Anthropic)**
  - Shows degradation under uncontrolled context growth.
  - nowu altitude enforcement is principled context minimization: only altitude-relevant data should be in scope for a phase.

### Operator Mapping Table

| Phase | Research Operator | AFLOW Operator | Rombaut Primitive |
|---|---|---|---|
| IDEA | — (trigger) | — | — |
| PROBLEM | Intake | — | ReAct (sense) |
| ANALYSIS | Explore | Ensemble | Plan-Execute (plan) |
| OPTIONS | Explore | Ensemble | Plan-Execute (plan) |
| DECISION | Decide | — | — |
| EVALUATION | Review | Review | — |
| IMPLEMENTATION | Generate | Generate/Program | Generate-Test-Repair |
| VERIFICATION | Verify | Test | Multi-Attempt Retry |
| LEARN | Curate + Reflect | Revise | — |

## 3. The 5 Altitudes

| Altitude | What It Addresses | Permitted Language | Time Horizon | Reversibility |
|---|---|---|---|---|
| STRATEGIC | Vision, portfolio direction, product thesis, identity | Goals, personas, bets, horizons, principles | Quarterly/permanent | Very hard |
| PRODUCT | Validated user/domain problems, outcome shaping | Problems, pain, outcomes, appetite, desirability | Monthly/per-epoch | Difficult |
| ARCHITECTURE | Constraints, quality attributes, structural options, ADRs | Modules, contracts, tradeoffs, risks, dependencies | Per-cycle (weeks) | Moderate |
| DELIVERY | Epics, intakes, stories, sequencing, shippable slices | Scope, ACs, dependencies, priorities, readiness | Per-cycle (days–weeks) | Moderate |
| EXECUTION | Code, tests, runtime behavior, verification, learning | Files, functions, test cases, errors, metrics | Per-task (hours) | Easy |

### Why 5, Not 3

A 3-level model (strategic/tactical/operational) collapses distinctions that are operationally critical in AI-first software systems:

- Collapsing **STRATEGIC + PRODUCT** into one “high” layer mixes identity-level choices with evidence-backed user/problem discovery.
- Collapsing **ARCHITECTURE + DELIVERY** into one “mid” layer mixes structural/system constraints with sequencing/scope decisions.
- The collapse increases context bleed, weakens accountability boundaries, and obscures failure localization.

The 5-altitude split preserves decision ownership and language discipline where modern product/software work actually diverges.

### Why Not 6

A sixth dedicated **GOVERNANCE** altitude was evaluated but not retained because governance concerns are adequately represented at the top of STRATEGIC (principles, policy constraints, risk posture) without requiring a full additional activity lane. The activity volume and artifact distinctiveness did not justify a permanent sixth altitude.

### Relationship to C4

| C4 Level | nowu Altitude | Phase(s) |
|---|---|---|
| Above C4 | STRATEGIC + PRODUCT | IDEA through DECISION |
| L1 System Context | ARCHITECTURE | ANALYSIS |
| L2 Containers/Modules | ARCHITECTURE | OPTIONS + DECISION |
| L3 Components | DELIVERY + EXECUTION | IMPLEMENTATION |
| L4 Code | EXECUTION | IMPLEMENTATION + VERIFICATION |

## 4. The 10 Phases (Cognitive Modes)

| Phase | What Happens | Cognitive Activity |
|---|---|---|
| IDEA | Raw signal, seed, or emerging concern | Perception, sensing |
| PROBLEM | Validated pain, outcome goal, appetite | Grounding, context reconstruction |
| ANALYSIS | Research, synthesis, tradeoff exploration | Discovery, decomposition |
| SYNTHESIS | Cross-cutting theme detection (ARCHITECTURE only, ≥2 UCs) | Integration, pattern recognition |
| OPTIONS | Alternative paths, candidate shapes | Generation, enumeration |
| DECISION | Chosen path, rationale, rejected alternatives recorded | Commitment, recording |
| EVALUATION | Fitness check — did the decision hold? Does it fit? | Reflection on decision quality |
| IMPLEMENTATION | Execution of the chosen path | Creation, transformation |
| VERIFICATION | Evidence that the implementation satisfies the decision | Testing, validation against criteria |
| LEARN | Captured lessons; may trigger upward promotion | Reflection, knowledge transfer |

### Why EVALUATION and VERIFICATION Are Separate

- **EVALUATION** asks: *Was this the right decision?*  
  It is backward-looking and interrogates decision quality, assumptions, tradeoffs, and fit.
- **VERIFICATION** asks: *Did we build what we said?*  
  It is forward-looking against explicit criteria, checking implementation conformance and correctness.

Conflating the two causes either design-free testing or untestable “evaluation” narratives. Keeping them separate preserves epistemic clarity.

### Multi-Altitude Phase Table

| Phase | Occurs At |
|---|---|
| IDEA | STRATEGIC, PRODUCT, DELIVERY |
| PROBLEM | STRATEGIC, PRODUCT, ARCHITECTURE |
| ANALYSIS | All altitudes |
| SYNTHESIS | ARCHITECTURE only |
| OPTIONS | STRATEGIC, PRODUCT, ARCHITECTURE, DELIVERY |
| DECISION | All altitudes |
| EVALUATION | ARCHITECTURE, DELIVERY, EXECUTION |
| IMPLEMENTATION | ARCHITECTURE, DELIVERY, EXECUTION |
| VERIFICATION | STRATEGIC, ARCHITECTURE, DELIVERY, EXECUTION |
| LEARN | All altitudes |

## 5. The Full 5×10 Matrix

| Altitude | IDEA | PROBLEM | ANALYSIS | SYNTHESIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN |
|---|---|---|---|---|---|---|---|---|---|---|
| STRATEGIC | Vision themes | Strategic tensions | Discovery synthesis | — | Product directions | Vision changes | Coherence review | Roadmap shaping | Goal review | Vision updates |
| PRODUCT | Initiative seed | Problem statement | Discovery research | — | Outcome shapes | Initiative selection | Problem-solution fit | Epic shaping | Outcome validation | Product learning |
| ARCHITECTURE | Arch concern | Constraint | QA scenarios, tradeoffs | Cross-cutting themes | Structural options | ADR choice | ATAM/risk review | Contract/module changes | Fitness checks | Arch corrections |
| DELIVERY | Slice candidate | Delivery obstacle | Readiness analysis | — | Sequencing options | Intake approval | Scope/risk review | Story execution plan | AC review | Cycle retro |
| EXECUTION | Task idea | Bug/defect | Root cause analysis | — | Technical approaches | Local design decision | Review/test eval | Code and tests | CI/runtime checks | Capture/postmortem |

## 6. Epistemic Grades

| Grade | Evidence Required |
|---|---|
| SPECULATION | None |
| HYPOTHESIS | Logical argument OR single anecdote |
| INFORMED_ESTIMATE | ≥2 sources OR expert judgment |
| EVIDENCE_BASED | Empirical data OR research |
| VERIFIED_FACT | Automated verification OR spec |

### Tiered Thresholds

| Altitude | Minimum at Creation | Advisory Threshold | Aspirational at Decision |
|---|---|---|---|
| STRATEGIC | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| ARCHITECTURE | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| PRODUCT | SPECULATION | HYPOTHESIS | INFORMED_ESTIMATE |
| DELIVERY | SPECULATION | HYPOTHESIS | HYPOTHESIS |
| EXECUTION | SPECULATION | HYPOTHESIS | HYPOTHESIS |

### Enforcement Levels

- **Level 0-1 (v1-core):** Advisory — warn if below threshold, do not block.
- **Level 2 (v1.0):** Block if below minimum.
- **Level 3 (v1.1+):** Block at decision gates if below aspirational.

## 7. S1–S9 Pipeline Mapping (The Zigzag)

| Step | Agent | Altitude | Phase | What Happens |
|---|---|---|---|---|
| S1 | nowu-intake | DELIVERY | IDEA | Scopes delivery cycle from user request |
| S2 | nowu-constraints | ARCHITECTURE | ANALYSIS | Identifies architectural boundaries |
| S3 | nowu-options | ARCHITECTURE | OPTIONS | Generates ≥2 architectural alternatives |
| S4 | nowu-decider | ARCHITECTURE | DECISION | Selects architectural path + rationale |
| S5 | nowu-shaper | DELIVERY | EVALUATION | Defines scope, appetite, acceptance criteria |
| S6 | nowu-implementer | EXECUTION | IMPLEMENTATION | Writes code/config/tests |
| S7 | nowu-reviewer | EXECUTION | VERIFICATION | Reviews implementation quality |
| S8 | VBR | EXECUTION | VERIFICATION | Final validation before commit |
| S9 | nowu-curator | EXECUTION→ALL | LEARN | Abstracts lessons, promotes upward |

**S1–S9 is a zigzag across altitudes, not a flat EXECUTION loop.** It starts at DELIVERY, rises to ARCHITECTURE for S2-S4, drops to DELIVERY for S5, drops again to EXECUTION for S6-S8, and the curator zooms back up for S9.

## 8. Orchestrator Layer (External to 5×10)

The orchestrator is a **meta-layer** that sits **outside** the 5×10 execution grid. It decides what work enters the field, when, and in what sequence. The orchestrator is not a phase type — it is a separate system that operates on the field from the outside.

### Why the Orchestrator is External

Every mature workflow system separates:
- **Execution**: The actual work (SENSE, PROBLEM, ANALYSIS, etc. inside the 5×10 field)
- **Orchestration**: Deciding what work happens next (external to the field)

Industry precedent: Shape Up's betting table, SAFe's PI Planning, Temporal's workflow tasks, AFLOW's optimizer, AgentOrchestra's Planning Agent, and HTN's compound tasks all separate execution from orchestration.

### Orchestrator Agents (Meta-Level)

These agents live in `.claude/agents/` alongside execution agents but are **not part of the execution agent roster**. They operate at the orchestrator layer.

| Agent | Trigger | Altitude | Phase | Input | Output |
|---|---|---|---|---|---|
| `roadmap-creator` | P0.V+P0.G complete, 10+ UCs exist | STRATEGIC | IMPLEMENTATION | vision, goals, partial UCs | ROADMAP-001.md |
| `roadmap-updater` | SYNTHESIS complete, Arch Vision complete, stage gates | STRATEGIC | LEARN | current ROADMAP-NNN.md + milestone artifact | ROADMAP-NNN+1.md |
| `work-scheduler` | User asks "what's next?" or agent completes task | N/A (meta) | N/A (query) | current ROADMAP-NNN.md + system state | Next work item decision (console output) |

### Orchestrator Artifacts

| Artifact | Location | Versioned? | Grade Progression |
|---|---|---|---|
| `ROADMAP-NNN.md` | `docs/` | Yes (version in filename + frontmatter) | HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED |

ROADMAP lives in `docs/` (not `state/`) because it is project-level canonical documentation, not session-specific.

### Orchestrator vs. Execution Layer

| Property | 5×10 Execution Layer | Orchestrator Layer |
|---|---|---|
| **What it does** | Executes work (SENSE, PROBLEM, ANALYSIS, etc.) | Decides what work to execute next |
| **Where it lives** | Inside the 5×10 grid (altitude × phase) | Outside the grid (meta-level) |
| **Agents** | Execution agents (nowu-intake, nowu-shaper, etc.) | 3 meta-agents (roadmap-creator, roadmap-updater, work-scheduler) |
| **State location** | `state/` (session artifacts) | `docs/` (versioned roadmap) |
| **Triggered by** | Orchestrator or user | Milestones (SYNTHESIS, Arch Vision, stage gates) or user query |

### Invocation Points

The orchestrator is invoked at **milestone boundaries**, not during execution:

```
P0.V + P0.G complete, 10+ UCs → 🔵 roadmap-creator → ROADMAP-001.md
W1 SYNTHESIS complete           → 🔵 roadmap-updater → ROADMAP-002.md
W3 Hypothesis ADRs complete     → 🔵 roadmap-updater → ROADMAP-003.md
v1-core stage gate passes       → 🔵 roadmap-updater → ROADMAP-004.md
Any time: "what's next?"        → 🔵 work-scheduler  → console output
```

### Hard Constraints

1. Orchestrator agents MUST NOT execute work inside the 5×10 field
2. ROADMAP-NNN.md is the single source of truth for sequencing
3. Orchestrator artifacts MUST be versioned (every update creates a new version)
4. Epistemic grade MUST NOT decrease (can only improve or stay same)
5. work-scheduler is read-only (never modifies the roadmap)

## 9. Pre-Workflow Mapping (P0–P4)

| Step | Agent | Altitude | Phase |
|---|---|---|---|
| P0.V | Vision bootstrap | STRATEGIC | DECISION |
| P0.UC | Use-case agent | PRODUCT | PROBLEM |
| P1 | Discovery/goals | PRODUCT | ANALYSIS |
| P2 | Story mapping | DELIVERY | OPTIONS |
| P3 | Architecture | ARCHITECTURE | OPTIONS → DECISION |
| P4 | Readiness/betting | DELIVERY | EVALUATION → DECISION |

## 10. GAP Cycle Mapping

| Step | Agent | Altitude | Phase |
|---|---|---|---|
| G0 | Gap detector | ARCHITECTURE | IDEA |
| G1 | Gap analyst | ARCHITECTURE | ANALYSIS |
| G2 | Gap writer | ARCHITECTURE | IMPLEMENTATION |

**Note:** GAP is an ARCHITECTURE-altitude loop that runs IDEA → ANALYSIS → IMPLEMENTATION.

## 11. Full Agent Contract Table

| Agent | Altitude | Phase | C4 Scope |
|---|---|---|---|
| Vision bootstrap | STRATEGIC | DECISION | above-C4 |
| Use-case agent | PRODUCT | PROBLEM | above-C4 |
| Discovery agent | PRODUCT | ANALYSIS | — |
| Perspective interview | PRODUCT | PROBLEM | — |
| Story mapper | DELIVERY | OPTIONS | — |
| Signal capture | STRATEGIC/PRODUCT | IDEA | — |
| Idea decomposition | PRODUCT | ANALYSIS | — |
| Health-vision | STRATEGIC | VERIFICATION | — |
| Health-goals | STRATEGIC | VERIFICATION | — |
| Health-architecture | ARCHITECTURE | VERIFICATION | — |
| Health-use-cases | PRODUCT | VERIFICATION | — |
| Gap detector (G0) | ARCHITECTURE | IDEA | — |
| Gap analyst (G1) | ARCHITECTURE | ANALYSIS | C4 L1/L2 |
| Gap writer (G2) | ARCHITECTURE | IMPLEMENTATION | — |
| Architecture bootstrap | ARCHITECTURE | OPTIONS | C4 L1/L2 |
| Architecture design | ARCHITECTURE | OPTIONS | C4 L1/L2 |
| Constraint check | ARCHITECTURE | ANALYSIS | — |
| QA elicitation | ARCHITECTURE | ANALYSIS | — |
| ATAM-lite | ARCHITECTURE | EVALUATION | — |
| Synthesis agent (W1) | ARCHITECTURE | SYNTHESIS | all UCs |
| Architecture vision agent (W2) | ARCHITECTURE | SYNTHESIS→DECISION | C4 L1/L2 |
| Hypothesis ADR writer (W3) | ARCHITECTURE | DECISION | C4 L2 |
| Fitness function writer (W3.5) | ARCHITECTURE | VERIFICATION | C4 L3/L4 |
| Readiness checker | DELIVERY | EVALUATION | — |
| Intake analyst (S1) | DELIVERY | IDEA | C4 L1 |
| Constraints analyst (S2) | ARCHITECTURE | ANALYSIS | C4 L1-2 |
| Options designer (S3) | ARCHITECTURE | OPTIONS | C4 L2 |
| Decision maker (S4) | ARCHITECTURE | DECISION | C4 L2 |
| Task shaper (S5) | DELIVERY | EVALUATION | C4 L3 |
| Implementer (S6-S7) | EXECUTION | IMPLEMENTATION + VERIFICATION | C4 L4 |
| Reviewer (S8) | EXECUTION | EVALUATION | C4 L3-4 |
| Curator (S9) | EXECUTION→STRATEGIC | LEARN | C4 L1-2 |
| **Orchestrator Meta-Agents** | | | |
| Roadmap creator | STRATEGIC | IMPLEMENTATION | above-C4 |
| Roadmap updater | STRATEGIC | LEARN | above-C4 |
| Work scheduler | N/A (meta) | N/A (query) | all |

## 12. Promotion and Transition Rules

### Downward Flow (Normal)

```text
STRATEGIC/DECISION → PRODUCT/PROBLEM
PRODUCT/DECISION → ARCHITECTURE/ANALYSIS
PRODUCT/DECISION → DELIVERY/OPTIONS
ARCHITECTURE/DECISION → DELIVERY/IMPLEMENTATION
DELIVERY/DECISION → EXECUTION/IMPLEMENTATION
```

### Upward Flow (Learning)

```text
EXECUTION/LEARN → DELIVERY/LEARN (CONTINUE)
EXECUTION/LEARN → ARCHITECTURE/PROBLEM (ARCH_PIVOT)
EXECUTION/LEARN → PRODUCT/ANALYSIS (PRODUCT_PIVOT)
EXECUTION/LEARN → STRATEGIC/PROBLEM (rare)
```

### Horizontal Movement

Always valid within altitude and expected to follow loop order. Not every phase must be visited for every artifact.

### Circuit Breaker Triggers

- Agent producing artifact outside its contract
- Artifact containing language from lower altitude
- Skipping >2 altitudes without intermediate gate
- Upward promotion without LEARN phase
- Re-entering higher altitude without trigger

## 13. Artifact→Position Mapping

| Artifact | Altitude | Phase |
|---|---|---|
| docs/vision.md | STRATEGIC | PROBLEM/DECISION |
| docs/goals/goal-NNN.md | STRATEGIC | DECISION |
| docs/USE_CASES.md | PRODUCT | PROBLEM |
| state/ideas/idea-NNN.md | STRATEGIC or PRODUCT | IDEA |
| state/discovery/disc-NNN.md | PRODUCT | ANALYSIS |
| state/problems/problem-NNN.md | PRODUCT | PROBLEM |
| state/epics/epic-NNN.md | DELIVERY | OPTIONS |
| state/stories/story-NNN-*.md | DELIVERY | DECISION |
| state/intake/intake-NNN.md | DELIVERY | DECISION→IMPLEMENTATION |
| state/arch/arch-pass-NNN.md | ARCHITECTURE | OPTIONS |
| state/arch/NNN-constraint-check.md | ARCHITECTURE | ANALYSIS |
| state/arch/NNN-atam-lite.md | ARCHITECTURE | EVALUATION |
| docs/architecture/adr/*.md | ARCHITECTURE | DECISION |
| docs/DECISIONS.md | ARCHITECTURE | DECISION |
| state/tasks/task-NNN.md | EXECUTION | IMPLEMENTATION |
| state/vbr/vbr-task-NNN.md | EXECUTION | VERIFICATION |
| state/capture/capture-task-NNN.md | EXECUTION→DELIVERY | LEARN |
| state/health/arch-*.md | ARCHITECTURE | VERIFICATION |
| state/analysis/session-review-*.md | DELIVERY | LEARN |
| docs/ROADMAP-001.md | STRATEGIC | IMPLEMENTATION |

## 14. SYNTHESIS Phase Details

### Trigger

At least two approved use cases where:

- `architectural_implications: true`
- `linked_adrs: []`

### Process

1. Collect UC inputs.
2. Extract architectural signals (state, contracts, QA, dependencies).
3. Cluster into themes (≥2 UCs per theme).
4. Recommend one ADR per theme.
5. Write `SYNTHESIS-NNN.md` artifact.
6. Update relevant indexes.

### Common Mistakes

- Running SYNTHESIS on a single UC (that is ANALYSIS, not SYNTHESIS).
- Proposing concrete solutions too early instead of naming cross-cutting themes.
- Operating on product-level concerns rather than architectural concerns.

## 15. Security Integration

### Trigger Conditions

Security integration is required when an ADR introduces any of the following:

- Storage changes
- External API integration
- PII handling
- Authentication/authorization changes
- User input pathways

### OWASP Top 10 Coverage Requirement

For ADRs with security implications, the EVALUATION section must explicitly address all applicable OWASP Top 10 categories (A01 through A10), from Broken Access Control through SSRF.

## 16. Concept Draft Reference

**Source:** `.sisyphus/drafts/idea-004-2d-altitude-phase-model.md`

Key design decisions established by the concept draft and preserved in this canonical model:

- 5 altitudes (rejecting both 3-level collapse and 6-level over-segmentation).
- 9 original phases, with **SYNTHESIS** added by the implementation package as the 10th phase.
- Phases are multi-altitude (not single-layer locked).
- Epistemic grades are tiered by altitude and gate.
- Migration is forward-only via explicit transition/promotion rules.

## 17. Routing Vocabulary

Consistent language for describing where you are and where to go. Use these terms in handoffs,
agent prompts, session bookmarks, and capture records.

| Term | Meaning |
|---|---|
| **Altitude** | Which of the 5 layers (STRATEGIC / PRODUCT / ARCHITECTURE / DELIVERY / EXECUTION) |
| **Phase** | Which of the 10 cognitive modes (IDEA / PROBLEM / ANALYSIS / … / LEARN) |
| **Position** | Altitude + Phase (e.g., "ARCHITECTURE / SYNTHESIS") |
| **Artifact** | The file that carries the output of a phase step |
| **Gate** | A human-approval checkpoint between phases or steps |
| **Trigger** | The event that starts a loop at a given altitude (see Section 14 for SYNTHESIS trigger) |
| **Handoff** | The artifact transfer from one altitude or step to the next |
| **Pivot** | A LEARN phase output that routes to a different altitude/phase: `ARCH_PIVOT`, `PRODUCT_PIVOT` |
| **Drift** | Growing gap between what an artifact says and current reality (detected by health agents) |
| **GAP** | An ARCHITECTURE-altitude ANALYSIS loop run specifically for global architecture correction |
| **Pass** | A single run of one altitude loop (e.g., "arch pass", "GAP pass", "synthesis pass") |
| **W-step** | Architecture Foundation steps (W1-W3.5) that run once before the first S1-S9 cycle |

### "Where Are We?" Quick Lookup

At any point, the newest incomplete artifact tells you your current position:

```
Artifact                                         → Position
──────────────────────────────────────────────────────────────────
state/arch/gap-trigger.md OPEN                  → ARCHITECTURE / IDEA
state/arch/global-pass-*.md PROPOSED            → ARCHITECTURE / ANALYSIS
docs/architecture/adr/*.md HYPOTHESIS           → ARCHITECTURE / DECISION (W3)
tests/architecture/test_adr_fitness.py new      → ARCHITECTURE / VERIFICATION (W3.5)
state/health/arch-*.md RED                      → ARCHITECTURE / VERIFICATION
state/ideas/idea-NNN.md                         → STRATEGIC or PRODUCT / IDEA
state/pre-workflow/NNN-mode.md                  → PRODUCT / ANALYSIS
state/discovery/disc-NNN-research.md            → PRODUCT / ANALYSIS
state/problems/problem-NNN.md DRAFT             → PRODUCT / PROBLEM
state/stories/story-NNN-*.md DRAFT              → DELIVERY / OPTIONS
state/arch/arch-pass-NNN.md                     → ARCHITECTURE / OPTIONS
state/intake/intake-NNN.md DRAFT_FOR_REVIEW     → DELIVERY / EVALUATION
state/intake/intake-NNN.md READY_FOR_S1         → DELIVERY / DECISION (handoff to S1)
state/arch/*-constraints.md                     → ARCHITECTURE / ANALYSIS (S2)
state/arch/*-options.md                         → ARCHITECTURE / OPTIONS (S3)
state/arch/*-decision.md                        → ARCHITECTURE / DECISION (S4)
state/tasks/task-NNN.md READY_FOR_IMPL          → EXECUTION / IMPLEMENTATION (S6-S7)
state/vbr/vbr-task-NNN.md                       → EXECUTION / VERIFICATION (S7)
state/reviews/review-task-NNN.md                → EXECUTION / EVALUATION (S8)
state/capture/capture-task-NNN.md               → EXECUTION / LEARN (S9)
```
