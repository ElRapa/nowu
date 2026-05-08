# Concept Design: 2D Altitude × Phase Workflow Model (idea-004)

> **Status**: DRAFT v2 — concept design, not implementation plan
> **Source**: state/ideas/idea-004.md (Epic, DRAFT)
> **Date**: 2026-05-04
> **Supersedes**: v1 draft (2026-04-30) which proposed 3×8 — revised to 5×9

---

## 1. Problem Statement

Altitude confusion is the primary workflow failure mode in nowu. Observed symptoms:

- **Altitude drift**: appetite rationale at PRODUCT level contained EXECUTION-level implementation language (problem-005, caught at human gate)
- **Wrong-altitude artifacts**: epic artifacts containing solution-level detail ("how / solution — wrong altitude" — session-review-2026-04-08)
- **No machine enforcement**: context scoping in CLAUDE.md is advisory, not validated; agents can silently produce artifacts at the wrong altitude
- **Vocabulary collision**: "phase" previously meant both "product delivery stage" (v1-core, v1.1) AND "workflow position" — this is resolved in this design (see §4.1)

The system has implicit altitude enforcement (C4 scope headers in agent prompts, context scoping tables in CLAUDE.md) but no explicit, machine-readable, validatable altitude × phase coordinates on artifacts or agent contracts.

### Why This Matters Beyond Software

nowu is not just a software development workflow. It covers the entire journey from "what should exist in the world?" to "does it work?" — including vision, product thinking, architectural decisions, delivery planning, and execution. Non-software projects (AP food business, RE real estate, PK personal knowledge) use the same loop structure with different artifact content. The altitude model must cover all of this, not just the code-level activities.

---

## 2. Research Foundation

This design synthesizes inputs from multiple sources. Each is cited where it influenced a decision.

### 2.1 Internal Sources

| Document | Key Contribution |
|---|---|
| `docs/ALTITUDES.md` (v1.0, ACTIVE) | 3-altitude model (HIGH/MID/LOW), 8-step generic loop, routing vocabulary, position tracker concept, helicopter metaphor. **Superseded by this design** in altitude/phase counts; philosophy and vocabulary retained. |
| GLOBAL-MODEL v2.0 (`docs/design/flow/2026-04-08_3_...`) | Complete 5×9 matrix, 15 agent altitude contracts, artifact mapping, promotion rules, C4 relationship. **Primary structural input.** |
| Research & Generalization Analysis (`docs/design/flow/2026-04-07_...`) | Academic backing for 5 altitudes (Anthony's strategic/tactical/operational), operator vocabulary, loop primitives, Shape Up validation. **Primary theoretical input.** |
| Workflow-update & output-graph evaluation (`docs/design/flow/2026-04-08_4_...`) | ARCHITECTURE should NOT be split into sub-altitudes; CPG/knowledge-graph direction; `relationships: []` schema recommendation. |
| Paperclip analysis (`docs/design/research/paperclip-analysis/`) | Goal Ancestry → `promoted_from`; Circuit Breakers → altitude violation detection; Heartbeat → gate validation. |
| `state/ideas/idea-004.md` | Original idea with 5-altitude × 9-phase proposal, open questions, routing guidance. |

### 2.2 External Research

| Source | Key Contribution |
|---|---|
| Anthony's three-level model (strategic/tactical/operational) | Validates altitude stratification by time horizon and reversibility |
| AFLOW (ICLR 2025) | 7 universal operator types derived from cross-domain workflow clustering |
| Rombaut 2026 | 5 composable loop primitives (ReAct, Generate-Test-Repair, Plan-Execute, Retry, Tree Search) |
| MASAI modular pipeline | Fixer+Ranker separation validates S3/S4 Explore→Decide |
| Shape Up (Basecamp) | Shaping/Betting/Building tracks map to PRODUCT→DELIVERY→EXECUTION |
| Guo et al. 2025 (Agentic SE Survey) | Hierarchical cognitive architecture, multi-hypothesis generation, continuous learning |
| Epistemic AI (Manchingal & Cuzzolin) | Altitude boundaries = epistemic boundaries defining what an agent can/should reason about |
| Structured Knowledge Protocol (Stetsenko) | Frontmatter metadata enables better agent reasoning |
| Context rot research (Anthropic) | Minimal relevant context outperforms full context; altitude enforcement = principled context minimization |

---

## 3. Design Decisions

### 3.1 Five Altitudes

The model uses 5 altitudes from the GLOBAL-MODEL v2.0, enriched with time horizon and reversibility from the research analysis.

| Altitude | What It Addresses | Permitted Language | Time Horizon | Reversibility |
|---|---|---|---|---|
| **STRATEGIC** | Vision, portfolio direction, product thesis, identity | Goals, personas, bets, horizons, principles | Quarterly / permanent | Very hard |
| **PRODUCT** | Validated user/domain problems, outcome shaping | Problems, pain, outcomes, appetite, desirability | Monthly / per-epoch | Difficult |
| **ARCHITECTURE** | Constraints, quality attributes, structural options, ADRs | Modules, contracts, tradeoffs, risks, dependencies | Per-cycle (weeks) | Moderate |
| **DELIVERY** | Epics, intakes, stories, sequencing, shippable slices | Scope, ACs, dependencies, priorities, readiness | Per-cycle (days–weeks) | Moderate |
| **EXECUTION** | Code, tests, runtime behavior, verification, learning | Files, functions, test cases, errors, metrics | Per-task (hours) | Easy |

**Altitude discipline rule**: No artifact at one altitude should contain language that belongs to a lower altitude. A problem statement must not name commands. A story must not name files unless the schema is already decided. An idea note must not name modules.

#### Why 5, Not 3

The previous ALTITUDES.md used 3 (HIGH/MID/LOW). This was a valid simplification for the scope it covered, but it collapsed three fundamentally different concerns:

- **STRATEGIC vs PRODUCT**: Vision/identity decisions (permanent, very hard to reverse) are different from product-problem decisions (monthly, difficult to reverse). Collapsing them into "HIGH" means a vision change and a problem statement get the same altitude treatment, which erases the distinction between "what should exist?" and "what pain does it solve?"
- **ARCHITECTURE vs DELIVERY**: Structural decisions (ADRs, module boundaries) and delivery decisions (intake approval, story sequencing) have different stakeholders, different time horizons, and different failure modes. ALTITUDES.md handled this by putting both in "MID", but agents operating at ARCHITECTURE need constraint/tradeoff reasoning while DELIVERY agents need scope/sequencing reasoning.
- **C4 only covers software architecture**: C4 levels (L1–L4) have no concept of vision, goals, product problems, or delivery planning. Using C4 as the altitude backbone compresses the entire pre-software lifecycle into one bucket.

The research analysis independently arrived at 5 altitudes (GOVERNANCE / STRATEGIC / TACTICAL / OPERATIONAL / RETROSPECTIVE) using Anthony's model. The GLOBAL-MODEL's naming (STRATEGIC / PRODUCT / ARCHITECTURE / DELIVERY / EXECUTION) is more concrete and directly maps to nowu's existing artifact types.

#### Why Not 6 (Adding GOVERNANCE)

The research analysis proposed GOVERNANCE as a separate altitude above STRATEGIC for permanent identity/principles. This design keeps 5 by treating vision and principles as STRATEGIC/DECISION artifacts — they sit at the top of STRATEGIC altitude, not a separate altitude. The reasoning: nowu doesn't have enough governance-level activity to justify a separate altitude. Vision changes are rare (quarterly at most), and principles are established once and rarely revised. If governance activity increases in v2+, splitting STRATEGIC into GOVERNANCE + STRATEGIC can be reconsidered.

#### Relationship to C4

C4 does not disappear — it becomes a **view** over the altitude model, not the model's backbone:

| C4 Level | nowu Altitude | Phase(s) |
|---|---|---|
| Above C4 (vision, problems) | STRATEGIC + PRODUCT | IDEA through DECISION |
| L1 — System Context | ARCHITECTURE | ANALYSIS |
| L2 — Containers / Modules | ARCHITECTURE | OPTIONS + DECISION |
| L3 — Components | DELIVERY + EXECUTION | IMPLEMENTATION |
| L4 — Code | EXECUTION | IMPLEMENTATION + VERIFICATION |

C4 diagrams (`docs/architecture/context.md`, `docs/architecture/containers.md`) are ARCHITECTURE/DECISION artifacts produced by the Global Architecture Pass (GAP) and refined by per-epic architecture bootstrap passes.

### 3.2 Nine Phases

Each altitude runs its own loop through 9 phases:

| Phase | What Happens | Cognitive Activity |
|---|---|---|
| **IDEA** | Raw signal, seed, or emerging concern | Perception, sensing |
| **PROBLEM** | Validated pain, outcome goal, appetite | Grounding, context reconstruction |
| **ANALYSIS** | Research, synthesis, tradeoff exploration | Discovery, decomposition |
| **OPTIONS** | Alternative paths, candidate shapes | Generation, enumeration |
| **DECISION** | Chosen path, rationale, rejected alternatives recorded | Commitment, recording |
| **EVALUATION** | Fitness check — did the decision hold? Does it fit? | Reflection on decision quality |
| **IMPLEMENTATION** | Execution of the chosen path | Creation, transformation |
| **VERIFICATION** | Evidence that the implementation satisfies the decision | Testing, validation against criteria |
| **LEARN** | Captured lessons; may trigger upward promotion | Reflection, knowledge transfer |

#### Why EVALUATION and VERIFICATION Are Separate

EVALUATION asks: "Was this the right decision? Does it hold under new information? What's the impact?" — it's backward-looking at decision quality. At ARCHITECTURE altitude, this is ATAM-lite (risk review of the chosen architecture). At DELIVERY altitude, this is scope/risk review of the delivery plan.

VERIFICATION asks: "Did we build what we said we'd build? Does it meet acceptance criteria?" — it's forward-looking at implementation quality. At EXECUTION altitude, this is CI/runtime checks. At DELIVERY altitude, this is AC review and completion check.

The previous ALTITUDES.md collapsed these into a single VERIFY step. The GLOBAL-MODEL correctly separates them because they involve different agents, different inputs, and different outputs.

#### Mapping to Research Operator Vocabulary

The 9 phases map to the research analysis's generalizable operators as a reference layer (not a replacement):

| Phase | Research Operator | AFLOW Operator | Rombaut Primitive |
|---|---|---|---|
| IDEA | — (trigger, not operator) | — | — |
| PROBLEM | Intake | — | ReAct (sense) |
| ANALYSIS | Explore | Ensemble | Plan-Execute (plan) |
| OPTIONS | Explore | Ensemble | Plan-Execute (plan) |
| DECISION | Decide | — | — |
| EVALUATION | Review | Review | — |
| IMPLEMENTATION | Generate | Generate / Program | Generate-Test-Repair |
| VERIFICATION | Verify | Test | Multi-Attempt Retry |
| LEARN | Curate + Reflect | Revise | — |

This mapping is informational — it confirms that the 9 phases cover all identified operator types from the literature. The phase names are used in practice; the operator names appear in documentation for cross-referencing with academic sources.

### 3.3 The Full Matrix

| Altitude | IDEA | PROBLEM | ANALYSIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN |
|---|---|---|---|---|---|---|---|---|---|
| **STRATEGIC** | Vision themes, opportunity seeds | Strategic tensions, portfolio pains | Discovery synthesis, trend synthesis | Product directions, horizon options | Vision changes, scope bets | Coherence, viability, strategic fit | Roadmap shaping | Goal review, progress against vision | Vision updates, strategic lessons |
| **PRODUCT** | Initiative seed | Problem statement | Discovery research, persona validation | Outcome shapes, candidate capabilities | Initiative selection, appetite | Problem-solution fit, desirability review | Epic shaping | Outcome validation | Product learning, new assumptions |
| **ARCHITECTURE** | Architectural concern | Constraint / problem statement | QA scenarios, tradeoff analysis | Structural options | ADR / architecture choice | ATAM / risk review | Contract / module changes | Fitness checks, integration tests | Architecture corrections |
| **DELIVERY** | Slice candidate | Delivery obstacle | Readiness, dependency analysis | Sequencing and shaping options | Intake approval, story approval | Scope / risk review | Story execution plan | AC review, completion check | Cycle retrospective |
| **EXECUTION** | Task / code change idea | Bug, defect, mismatch | Root cause analysis | Technical approach options | Local design / code decision | Review / test evaluation | Code and tests | CI, runtime, behavior checks | Capture, postmortem, refactor lesson |

### 3.4 Same Topic Across Altitudes

The same topic appears at multiple altitudes without confusion. Each is a legitimate artifact at its level — they are not duplicates:

**Example: cross-project knowledge**

| Position | Artifact |
|---|---|
| STRATEGIC / PROBLEM | Vision-level continuity story ("projects compound") |
| PRODUCT / PROBLEM | problem-007 (knowledge invisible across projects) |
| ARCHITECTURE / DECISION | intake-003, ADR-0004 (per-project SQLite + federation) |
| DELIVERY / IMPLEMENTATION | Stories for know module integration |
| EXECUTION / LEARN | Retrospective after first real cross-project use |

---

## 4. Artifact Metadata Schema

### 4.1 Vocabulary Resolution

**Problem**: "phase" was previously overloaded — it meant both "product delivery stage" (v1-core, v1.1, v2) and "workflow position" (DECISION, ANALYSIS).

**Resolution**: This design adopts the following terms:
- **`altitude`** — vertical axis: abstraction level of the work
- **`phase`** — horizontal axis: position in the workflow loop (as in GLOBAL-MODEL v2.0)
- **`stage_target`** — product delivery stage (v1-core, v1.1, v2) — used only in story-mapper and health-goals context, not part of the 2D model

The term "phase" belongs to the 2D model. Product delivery stages are always referred to as `stage_target`. The existing `phase` field on `goal-brief.md` (currently set to `DECISION`) becomes the workflow-phase field — no rename needed, just semantic clarification.

The term "step" (from ALTITUDES.md routing vocabulary and S1–S9 naming) remains as an ordering label for the S1–S9 session pipeline. Steps are a traversal sequence that crosses multiple altitudes (DELIVERY→ARCHITECTURE→EXECUTION); phases are the universal horizontal axis.

### 4.2 Frontmatter Fields

Every workflow artifact gets these fields in its YAML frontmatter:

```yaml
# Altitude × Phase coordinates (REQUIRED on all new artifacts)
altitude: STRATEGIC | PRODUCT | ARCHITECTURE | DELIVERY | EXECUTION
phase: IDEA | PROBLEM | ANALYSIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN

# Lineage tracking (set when known)
promoted_from: <artifact-id>    # what artifact at same/lower altitude originated this
promotes_to: <artifact-id>      # set retroactively when this artifact produces a higher-altitude output

# Graph-readiness (for v1.1+ knowledge graph integration)
relationships: []               # list of {edge_type, target_id, target_altitude, target_phase}
```

**Field rules**:
- `altitude` + `phase` are REQUIRED on all new artifacts going forward
- `promoted_from` is set at creation time when the parent artifact is known
- `promotes_to` is set retroactively by the curator (LEARN phase) when an artifact produces a child at a higher altitude
- `relationships` starts as an empty list; populated when the knowledge graph layer (v1.1+) is operational
- Existing fields (id, status, created, etc.) are unchanged — these are additions

### 4.3 Artifact → Position Mapping

Complete mapping of all current artifact types to their (altitude, phase) coordinate:

| Artifact | Altitude | Phase |
|---|---|---|
| `docs/vision.md` | STRATEGIC | PROBLEM / DECISION |
| `docs/goals/goal-NNN.md` | STRATEGIC | DECISION | ¹ |
| `docs/USE_CASES.md` | PRODUCT | PROBLEM |
| `state/ideas/idea-NNN.md` | STRATEGIC or PRODUCT | IDEA |
| `state/discovery/disc-NNN.md` | PRODUCT | ANALYSIS |
| `state/problems/problem-NNN.md` | PRODUCT | PROBLEM |
| `state/epics/epic-NNN.md` | DELIVERY | OPTIONS |
| `state/stories/story-NNN-*.md` | DELIVERY | DECISION |
| `state/intake/intake-NNN.md` | DELIVERY | DECISION → IMPLEMENTATION |
| `state/arch/arch-pass-NNN.md` | ARCHITECTURE | OPTIONS |
| `state/arch/NNN-constraint-check.md` | ARCHITECTURE | ANALYSIS |
| `state/arch/NNN-atam-lite.md` | ARCHITECTURE | EVALUATION |
| `docs/architecture/adr/*.md` | ARCHITECTURE | DECISION |
| `docs/DECISIONS.md` | ARCHITECTURE | DECISION |
| `state/tasks/task-NNN.md` | EXECUTION | IMPLEMENTATION |
| `state/vbr/vbr-task-NNN.md` | EXECUTION | VERIFICATION |
| `state/capture/capture-task-NNN.md` | EXECUTION → DELIVERY | LEARN |
| `state/health/arch-*.md` | ARCHITECTURE | VERIFICATION |
| `state/analysis/session-review-*.md` | DELIVERY | LEARN |
| `V1_PLAN.md` | STRATEGIC | IMPLEMENTATION |

¹ **Deviation from current template**: `templates/goal-brief.md` currently has `altitude: PRODUCT`. This concept places goals at STRATEGIC because they represent strategic commitments derived from vision horizons — they answer "what outcome are we pursuing?" at the portfolio level. Problems (PRODUCT altitude) answer "what pain does it solve?" If goals are better understood as product-level, this can be changed to PRODUCT/DECISION without affecting the rest of the model.

---

## 5. Agent Altitude Contracts

Every agent operates at a declared (altitude, phase) pair. The contract is a one-line addition to each agent's existing `## Your Scope` section.

### 5.1 Contract Format

```markdown
## Your Scope: C4 Level 2 (Module Interactions)
**Position**: ARCHITECTURE / OPTIONS — output artifacts must be altitude=ARCHITECTURE, phase=OPTIONS
```

The existing C4 level declaration stays as complementary detail. The altitude contract is the machine-readable summary.

### 5.2 Full Agent Contract Table

| Agent | Altitude | Phase | Current C4 Scope |
|---|---|---|---|
| Vision bootstrap | STRATEGIC | DECISION | above-C4 |
| Use-case agent | PRODUCT | PROBLEM | above-C4 |
| Discovery agent | PRODUCT | ANALYSIS | — |
| Perspective interview | PRODUCT | PROBLEM | — |
| Story mapper | DELIVERY | OPTIONS | — |
| Health-goals | STRATEGIC | VERIFICATION | — |
| Gap detector (G0) | ARCHITECTURE | IDEA | — |
| Gap analyst (G1) | ARCHITECTURE | ANALYSIS | C4 L1/L2 global |
| Gap writer (G2) | ARCHITECTURE | IMPLEMENTATION | — |
| Architecture bootstrap | ARCHITECTURE | OPTIONS | C4 L1/L2 |
| Constraint check | ARCHITECTURE | ANALYSIS | — |
| QA elicitation | ARCHITECTURE | ANALYSIS | — |
| ATAM-lite | ARCHITECTURE | EVALUATION | — |
| Readiness checker | DELIVERY | EVALUATION | — |
| Intake analyst (S1) | DELIVERY | PROBLEM | C4 L1 |
| Constraints analyst (S2) | ARCHITECTURE | ANALYSIS | C4 L1-2 |
| Options designer (S3) | ARCHITECTURE | OPTIONS | C4 L2 |
| Decision maker (S4) | ARCHITECTURE | DECISION | C4 L2 |
| Task shaper (S5) | DELIVERY | IMPLEMENTATION | C4 L3 |
| Implementer (S6–S7) | EXECUTION | IMPLEMENTATION + VERIFICATION | C4 L4 |
| Reviewer (S8) | EXECUTION | EVALUATION | C4 L3-4 |
| Curator (S9) | EXECUTION → STRATEGIC | LEARN | C4 L1-2 |

**Notable observations**:
- S1–S9 is NOT a single-altitude traversal. It crosses DELIVERY (S1, S5), ARCHITECTURE (S2–S4), and EXECUTION (S6–S9). This is correct — the "session" pipeline operates at the altitude appropriate to each step's cognitive task.
- S9 (Curator) uniquely spans EXECUTION → STRATEGIC during LEARN — it can trigger upward promotion to any altitude via `next_cycle_trigger`.
- Pre-workflow agents (P0–P4) operate at STRATEGIC, PRODUCT, and DELIVERY altitudes — they are not "above" the model, they are within it.
- GAP agents (G0–G2) operate at ARCHITECTURE altitude — GAP is an ARCHITECTURE-altitude loop, not a separate system.

### 5.3 The S1–S9 Pipeline Mapped to the Grid

```
S1 (intake)       = DELIVERY / PROBLEM         receives intake, grounds it
S2 (constraints)  = ARCHITECTURE / ANALYSIS     analyzes constraints at arch level
S3 (options)      = ARCHITECTURE / OPTIONS      generates structural options
S4 (decider)      = ARCHITECTURE / DECISION     commits to an approach
S5 (shaper)       = DELIVERY / IMPLEMENTATION   shapes tasks for execution
S6-S7 (impl)      = EXECUTION / IMPLEMENTATION  builds code and tests
S8 (reviewer)     = EXECUTION / EVALUATION      evaluates build quality
S9 (curator)      = EXECUTION→STRATEGIC / LEARN captures and routes upward
```

This reveals that S1–S9 is a **zigzag across altitudes**, not a linear descent. S1 starts at DELIVERY, rises to ARCHITECTURE for S2–S4, drops to DELIVERY for S5, drops again to EXECUTION for S6–S8, and the curator zooms back up for S9.

### 5.4 Pre-Workflow Mapped to the Grid

```
P0.V  (vision bootstrap)     = STRATEGIC / DECISION
P0.UC (use-case agent)       = PRODUCT / PROBLEM
P1    (discovery/goals)       = PRODUCT / ANALYSIS
P2    (story mapping)         = DELIVERY / OPTIONS
P3    (architecture)          = ARCHITECTURE / OPTIONS → DECISION
P4    (readiness/betting)     = DELIVERY / EVALUATION → DECISION
```

### 5.5 GAP Cycle Mapped to the Grid

```
G0 (gap-detector)  = ARCHITECTURE / IDEA        detects architectural concern
G1 (gap-analyst)   = ARCHITECTURE / ANALYSIS     analyzes global architecture
G2 (gap-writer)    = ARCHITECTURE / IMPLEMENTATION  updates arch artifacts
```

GAP is an ARCHITECTURE-altitude loop that runs IDEA → ANALYSIS → IMPLEMENTATION. It is a **Retrospective Cycle** (per research analysis) — the industry-standard term for this phase type.

---

## 6. Promotion and Transition Rules

### 6.1 Downward Flow (Normal)

Work flows downward through explicit gates:

```
STRATEGIC / DECISION  →  PRODUCT / PROBLEM      (vision shapes product problems)
PRODUCT / DECISION    →  ARCHITECTURE / ANALYSIS (product decisions trigger constraint analysis)
PRODUCT / DECISION    →  DELIVERY / OPTIONS      (product decisions shape delivery)
ARCHITECTURE / DECISION →  DELIVERY / IMPLEMENTATION (ADRs constrain delivery shaping)
DELIVERY / DECISION   →  EXECUTION / IMPLEMENTATION  (delivery approval triggers execution)
```

Each downward transition requires the source artifact to be in an approved/accepted state. The receiving altitude picks up at its own PROBLEM or IDEA phase.

**Note**: The downward flow is not strictly linear. ARCHITECTURE is entered both during pre-workflow (P3 architecture bootstrap) and during the session pipeline (S2–S4). It functions as a lateral excursion from the DELIVERY→EXECUTION path — the S1–S9 pipeline zigzags through DELIVERY, ARCHITECTURE, and EXECUTION rather than descending linearly.

### 6.2 Upward Flow (Learning and Escalation)

Upward movement is triggered by the LEARN phase via `next_cycle_trigger`:

```
EXECUTION / LEARN     →  DELIVERY / LEARN        (CONTINUE — normal cycle)
EXECUTION / LEARN     →  ARCHITECTURE / PROBLEM   (ARCH_PIVOT — architecture issue found)
EXECUTION / LEARN     →  PRODUCT / ANALYSIS       (PRODUCT_PIVOT — product rethink needed)
EXECUTION / LEARN     →  STRATEGIC / PROBLEM      (rare — fundamental direction issue)
```

The S9 curator's `next_cycle_trigger` values map to altitude re-entry points:
- **CONTINUE**: stay at EXECUTION, next task
- **ARCH_PIVOT**: re-enter at ARCHITECTURE / PROBLEM
- **PRODUCT_PIVOT**: re-enter at PRODUCT / ANALYSIS
- **COMPLETE**: close the cycle, update DELIVERY / LEARN

### 6.3 Horizontal Movement (Within Altitude)

Movement through phases within a single altitude is always valid and follows the loop order: IDEA → PROBLEM → ANALYSIS → OPTIONS → DECISION → EVALUATION → IMPLEMENTATION → VERIFICATION → LEARN.

Not every phase must be visited. A simple bug fix at EXECUTION altitude may go PROBLEM → IMPLEMENTATION → VERIFICATION → LEARN, skipping ANALYSIS/OPTIONS/DECISION. The phases are waypoints, not mandatory gates. However, skipping DECISION at any altitude should be deliberate and documented.

### 6.4 Invalid Transitions (Circuit Breaker Triggers)

These transitions should trigger a circuit breaker warning:

- Any agent producing an artifact at an altitude outside its contract (§5.2)
- Any artifact containing language from a lower altitude (altitude discipline violation)
- Skipping more than 2 altitudes in a single downward transition without an intermediate gate
- Upward promotion without passing through the LEARN phase first
- Re-entering a higher altitude without a `next_cycle_trigger` or gap-detector trigger

---

## 7. Enforcement Strategy

### 7.1 Three Enforcement Levels

| Level | What It Does | When to Implement |
|---|---|---|
| **Level 1 — Advisory** | Frontmatter fields on all templates; agent contract lines in scope headers; ALTITUDES.md updated with the 5×9 grid; runner/skill prompts include "validate altitude+phase before proceeding" | **First** — implement with this concept |
| **Level 2 — Validated** | Runner checks artifact frontmatter at each handoff gate; mismatches logged as warnings; circuit breaker pattern triggers after >2 violations in a traversal | **Second** — implement after 2-3 full workflow traversals confirm Level 1 is insufficient |
| **Level 3 — Enforced** | PydanticAI validators reject output with wrong-altitude language; context scoping derived from altitude contracts (not manually maintained); gates refuse invalid transitions | **Third** — implement when/if programmatic orchestration (LangGraph) is adopted in v1.1+ |

**Recommendation**: Implement Level 1 now. Assess after 2-3 complete workflow cycles whether Level 2 is needed. Level 3 is coupled to the framework runtime adoption and should not be planned independently.

### 7.2 Level 1 Implementation Scope

**Templates** (~27 files): Add `altitude`, `phase`, `promoted_from`, `promotes_to`, `relationships` fields to YAML frontmatter with correct defaults per template.

**Agent prompts** (~22 agents): Add one-line `**Position**: ALTITUDE / PHASE` contract to each agent's `## Your Scope` section. Keep existing C4 level declarations unchanged.

**ALTITUDES.md**: Rewrite to reflect 5×9 model. Retain: philosophy, helicopter metaphor (adapted), routing vocabulary, position tracker concept, cross-domain applicability. Replace: 3 altitudes → 5, 8 steps → 9 phases, per-altitude tables → full matrix.

**CLAUDE.md**: Add note linking context scoping rules to altitude contracts. Context scoping table stays as-is (it's the operational enforcement); altitude coordinates are the conceptual framework it implements.

**Runner/skill prompts**: Add altitude validation instruction at gate points: "Before proceeding, verify that the output artifact's altitude and phase match your declared contract."

---

## 8. What Changes in ALTITUDES.md

ALTITUDES.md (currently v1.0, 311 lines, status: ACTIVE) is rewritten to v2.0. Here is what survives, what changes, and what's added:

### Survives (retained content)

- **§1 Why This Exists** — philosophy of "same loop at different scales". Updated to reference 5 altitudes and 9 phases.
- **§2 Reference Models** — academic backing table. Extended with Anthony's model, AFLOW, Rombaut, Shape Up.
- **Helicopter metaphor** — adapted: "At STRATEGIC altitude you see the product landscape and horizons. At PRODUCT altitude you see the problems and outcomes. At ARCHITECTURE altitude you see modules and contracts. At DELIVERY altitude you see epics, stories, and schedules. At EXECUTION altitude you see files, functions, and test cases."
- **§7 Loop Interactions** — constrains-down, signals-up principle. Updated with 5 altitudes.
- **§8 Project-Level Mapping** — cross-domain applicability (AP, RE, PK). Expanded to 5 altitudes.
- **§9 Routing Vocabulary** — all terms retained (Altitude, Phase, Position, Gate, Trigger, Handoff, Pivot, Drift, GAP, Pass). "Step" definition updated.
- **§10 Evaluation / What to watch out for** — retained and expanded.
- **§11 Quick Reference** — retained, updated for 5 altitudes.

### Changes (replaced content)

- **§3 Generic Loop**: 8 steps → 9 phases (IDEA through LEARN)
- **§4 The Three Altitudes**: → **Five Altitudes** (STRATEGIC/PRODUCT/ARCHITECTURE/DELIVERY/EXECUTION)
- **§5 Loop Mapping per Altitude**: 3 per-altitude tables → full 5×9 matrix + per-altitude detail tables
- **§6 Position Tracker**: Updated with 5-altitude artifact→position mapping

### Added (new content)

- **Altitude properties table**: time horizon, reversibility, permitted language per altitude
- **Agent altitude contracts**: full table from §5.2 above
- **Promotion and transition rules**: downward flow, upward flow, circuit breaker triggers
- **C4 relationship mapping**: how C4 levels map onto the altitude model
- **Frontmatter schema**: the `altitude`, `phase`, `promoted_from`, `promotes_to`, `relationships` fields

---

## 9. Relationship to Research Input Documents

Assessment of whether each design input document's insights are captured in this concept:

| Document | Status | Action |
|---|---|---|
| `docs/design/flow/2026-04-07_Research & Generalization Analysis` | **ABSORBED** — 5-altitude model, academic backing, operator vocabulary, loop primitives all integrated | Mark as `status: input-consumed` |
| `docs/design/flow/2026-04-08_1_AI Coding Agent Systems Guide` | **TANGENTIAL** — framework comparison (LangGraph, PydanticAI, etc.) relevant to runtime implementation, not altitude model | Keep as reference for runtime phase |
| `docs/design/flow/2026-04-08_2_Architecture Plan — Roadmap` | **PARTIALLY ABSORBED** — strangler-fig strategy and phased adoption referenced in §7.1 enforcement levels | Keep; migration phases inform implementation order |
| `docs/design/flow/2026-04-08_3_Evaluation in global-model workflow` | **ABSORBED** — GLOBAL-MODEL v2.0 (5×9 matrix, agent contracts, artifact mapping, promotion rules) is the primary structural input | Mark as `status: input-consumed` |
| `docs/design/flow/2026-04-08_4_Workflow-update & output-graph evaluation` | **ABSORBED** — ARCHITECTURE sub-altitude rejection, CPG direction, `relationships: []` schema recommendation | Mark as `status: input-consumed` |
| `docs/design/framework_design/2026-04-06_Global Architecture Analysis` | **TANGENTIAL** — architecture options A/B/C and 4 know improvements relevant to runtime, not model design | Keep as reference |
| `docs/design/framework_design/nowu_palantir_guo_et_al_comparison` | **TANGENTIAL** — Palantir ontology and Guo survey mapping relevant to know module design | Keep as reference |

**Recommended marking**: Add `consumed_by: idea-004-concept` to the frontmatter of documents marked `input-consumed`, so future agents know these documents' insights are captured in the concept.

---

## 10. Open Questions Resolved

From idea-004.md's original open questions:

| Question | Resolution |
|---|---|
| How many altitude levels — 5 or 3? | **5** (STRATEGIC / PRODUCT / ARCHITECTURE / DELIVERY / EXECUTION). See §3.1 for rationale. |
| Does `promotes_to` need to be set at write time or retroactively? | **Retroactively**, by the curator during the LEARN phase. `promoted_from` is set at creation time. |
| Does the phase axis need all 9 steps or simplified? | **9 phases** (IDEA through LEARN). EVALUATION and VERIFICATION are separate — see §3.2. |
| How does migration work for existing artifacts? | **Forward-only**. New artifacts get the fields. Existing artifacts are updated opportunistically when edited for other reasons. No backfill campaign. |

---

## 11. What This Does NOT Cover (Explicit Exclusions)

- **Agent/skill renaming**: Deferred per user decision — altitude implementation is separate from naming conventions
- **Runtime enforcement tooling**: No scripts, no CI checks, no PydanticAI validators — those come with Level 3 enforcement and LangGraph adoption
- **Retroactive artifact migration**: No backfill campaign for existing artifacts
- **Product delivery stages**: "v1-core", "v1.1", "v2" remain as `stage_target`, orthogonal to the 2D model
- **C4 level replacement**: C4 levels stay in agent prompts as complementary detail
- **Pre-workflow restructuring**: P0–P4 steps map onto the grid but their workflow mechanics don't change
- **Knowledge graph implementation**: `relationships: []` is schema preparation only; graph traversal and query infrastructure are v1.1+ work
- **Code Property Graph (CPG)**: Future v2+ feature at EXECUTION/(VERIFICATION, LEARN) — mentioned for completeness but not designed here
- **S3/S4 Explore-Decide protocol formalization**: The research analysis recommended minimum 2 options with explicit tradeoffs for S3, and traceable rationale for S4. This is a valid improvement to the workflow step contracts but is separate from the altitude model — it can be addressed independently as a workflow refinement

---

## 12. Self-Review: Issues and Deviations

Cross-referencing this concept against its source documents surfaced the following:

| # | Finding | Resolution |
|---|---|---|
| 1 | `goal-NNN.md` altitude: concept says STRATEGIC, template currently says PRODUCT | Flagged in §4.3 footnote ¹ — deliberate change with rationale; user decides |
| 2 | §6.1 downward flow originally skipped ARCHITECTURE | Fixed — ARCHITECTURE now included in downward flow with note about lateral excursion pattern |
| 3 | §4.1 incorrectly said steps are "at EXECUTION altitude" | Fixed — steps are an ordering label for the session pipeline that crosses multiple altitudes |
| 4 | Research recommended S3/S4 Explore-Decide formalization | Added to §11 exclusions — separate from altitude model |
| 5 | Concept adds 6 agents not in GLOBAL-MODEL v2.0 table (Vision bootstrap, Use-case agent, Health-goals, G0/G1/G2) | Intentional expansion — these agents exist in the codebase but weren't listed in the GLOBAL-MODEL's Section 8 |
| 6 | Concept adds 4 artifact types not in GLOBAL-MODEL v2.0 mapping (goals, health, session-reviews, V1_PLAN) | Intentional expansion — more complete inventory of existing artifacts |
| 7 | Promotion rules (§6) are consistent with existing `next_cycle_trigger` mechanism | Verified — CONTINUE/ARCH_PIVOT/PRODUCT_PIVOT/COMPLETE map to the altitude re-entry points exactly |
| 8 | Phase skip rules (§6.3) are new — not in GLOBAL-MODEL or ALTITUDES.md | Acknowledged — practical addition based on the reality that not every workflow traversal visits all 9 phases |

---

## 13. Implementation Summary

| What | Change | Files Affected | Effort |
|---|---|---|---|
| ALTITUDES.md rewrite | 3→5 altitudes, 8→9 phases, full matrix, contracts, promotion rules, C4 mapping | `docs/ALTITUDES.md` | Significant (rewrite, keeping philosophy) |
| Artifact frontmatter | Add `altitude`, `phase`, `promoted_from`, `promotes_to`, `relationships` | ~27 templates | Mechanical (correct defaults per template) |
| Agent contracts | Add `**Position**: ALTITUDE / PHASE` line to `## Your Scope` | ~22 agent .md files | Mechanical (one line each) |
| CLAUDE.md update | Link context scoping to altitude contracts | `CLAUDE.md` | Small (add note) |
| Runner/skill prompts | Add altitude validation instruction at gates | Runner skill .md files | Small |
| Input document marking | Add `consumed_by: idea-004-concept` to absorbed docs | 3 design docs | Trivial |
| goal-brief.md update | Change `altitude: PRODUCT` to correct value, clarify `phase` semantics | `templates/goal-brief.md` + 4 goal files | Trivial |

**Total**: ~55 file edits (mostly mechanical frontmatter), 1 significant doc rewrite (ALTITUDES.md), no code changes.

---

## 14. Design Input Sources (Full Bibliography)

### Internal

1. `docs/ALTITUDES.md` v1.0 — 3-altitude model, 8-step generic loop
2. `state/ideas/idea-004.md` — original idea (5×9 proposal)
3. `docs/design/flow/2026-04-07_Research & Generalization Analysis` — academic backing, 5-altitude spine, operator vocabulary
4. `docs/design/flow/2026-04-08_3_Evaluation in global-model workflow` — GLOBAL-MODEL v2.0 (5×9 matrix, agent contracts)
5. `docs/design/flow/2026-04-08_4_Workflow-update & output-graph evaluation` — CPG direction, `relationships: []`, no ARCHITECTURE sub-levels
6. `docs/design/research/paperclip-analysis/REPORT-paperclip-analysis.md` — Goal Ancestry, Circuit Breakers, Heartbeat
7. `docs/design/workflow_design/nowu Workflow v4 — Final Unified Specification.md` — S1–S9, V-Model gap
8. `docs/design/workflow_design/nowu Workflow Artifact Specification v3.md` — handoff headers, artifact schemas
9. `docs/design/workflow_design/flow_vs_sdlc-context_scoping_guide.md` — per-step context loading rules
10. `docs/design/workflow_design/flow_vs_sldc-key_takes.md` — context rot research, minimal context

### External

11. Anthony's three-level model (strategic/tactical/operational) — altitude time horizons
12. AFLOW (ICLR 2025) — universal operator types
13. Rombaut 2026 — 5 composable loop primitives
14. MASAI — Fixer+Ranker separation for Explore→Decide
15. Shape Up (Basecamp) — Shaping/Betting/Building track validation
16. Guo et al. 2025 — agentic SE survey, hierarchical cognitive architecture
17. Manchingal & Cuzzolin — epistemic AI, reasoning about knowledge boundaries
18. Stetsenko 2026 — structured knowledge protocols for AI agents
19. Context rot research (Anthropic) — minimal relevant context principle
