---
artifact_type: SYNTHESIS
artifact_id: SYNTHESIS-001
altitude: ARCHITECTURE
phase: SYNTHESIS
grade: HYPOTHESIS
created_at: 2026-05-06
source_goals: [goal-001, goal-002, goal-003, goal-004]
source_ucs: all 50 (NF-01..NF-16, PK-01..PK-09, XP-01..XP-11, AP-01..AP-07, RE-01..RE-07)
status: DRAFT
---

# SYNTHESIS-001: Cross-Cutting Architectural Themes

> **Purpose:** Extract themes that span 3+ use cases and cannot be addressed by any single
> UC in isolation. These themes define the architectural concerns that the system must
> address structurally — not as features, but as systemic capabilities.

---

## Method

1. All 50 approved UCs read and analyzed for: core capability, implicit architectural
   requirement, and cross-UC infrastructure dependencies.
2. Themes identified by clustering UCs that share infrastructure needs that no single UC
   can solve alone.
3. Each theme validated against goals and existing decisions (D-001..D-012, ADR-0001..0006).
4. ADR recommendations derived from unresolved architectural questions per theme.

---

## Themes Identified: 9

| # | Theme | UC Count | Primary Goal | Priority |
|---|-------|----------|--------------|----------|
| T1 | Continuity | 7+ | goal-001 | CRITICAL (v1-core blocker) |
| T2 | Knowledge Persistence & Lifecycle | 17+ | goal-003 | CRITICAL (v1-core blocker) |
| T3 | Workflow Orchestration | 8+ | goal-002 | CRITICAL (v1-core blocker) |
| T4 | Epistemic Awareness | 10+ | goal-003 | HIGH (v1-core: NF-15) |
| T5 | Domain Agnosticism | 16+ | goal-004 | HIGH (validated by AP/RE in v1) |
| T6 | Observability & Traceability | 8+ | goal-002 | HIGH (v1-core: NF-09) |
| T7 | Multi-Surface Access | 7+ | goal-002 | MEDIUM (v1: PK-08, not v1-core) |
| T8 | Progressive Disclosure | 7+ | goal-002 | HIGH (v1-core: NF-12) |
| T9 | Audience-Aware Rendering | 7+ | goal-004 | MEDIUM (v1.1: XP-11) |

---

## T1: Continuity

**Definition:** The system's ability to preserve intent, decisions, and progress across
session boundaries, interruptions, and time gaps — for both AI agents and the human.

**This is not just "save state." It is the ability to answer: "Where are we, what did we
decide, and what should we do next?" — instantly, correctly, without reconstruction.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| NF-01 | Agent session recovery — read checkpoint, propose next action |
| NF-10 | Human orientation — fast re-entry into any project after absence |
| NF-16 | Strategic drift detection — "am I working on the right things?" |
| PK-03 | Today view — unified daily surface across all projects |
| PK-08 | Remote capture/review — continuity doesn't require a desk |
| AP-05 | Long-term milestone tracking — state persists across months |
| RE-06 | Investment thesis tracking — assumptions persist across years |

### Architectural Implication

A **persistent semantic checkpoint system** that:
- Survives crashes (not just clean exits)
- Reconstructs "where we are" for agents (structured state) and humans (narrative orientation)
- Spans multiple projects without cross-contamination
- Tracks not just "what happened" but "what was decided and why"
- Enables both push (automatic orientation) and pull (on-demand catch-up)

### Existing Coverage

- D-001 (file-based memory): Provides storage mechanism but not recovery protocol
- `state/SESSION_STATE.md`: Exists as bookmark, explicitly "not source of truth"
- WORKFLOW.md §S0: Agent reads session state and proposes next action

### What's Missing

- **No defined checkpoint schema** — what must survive a crash?
- **No human orientation protocol** — how is NF-10's "maintain the thread" delivered?
- **No cross-project orientation** — PK-03 "today view" has no architectural home
- **No recovery ordering** — when multiple projects need orientation, what's the priority?

### Goal Alignment

- **goal-001** (primary): "Project momentum survives interruptions and compounds over time"
- **goal-002** (supporting): Low-friction restart is part of the 90-99% AI-handled experience

---

## T2: Knowledge Persistence & Lifecycle

**Definition:** Knowledge as the fundamental managed data type — with explicit confidence,
provenance, temporal awareness, relationships, sensitivity, and active lifecycle management
(creation → enrichment → verification → decay → archival/deletion).

**This is not a database. It is a living system that knows what it knows, how much to trust
each thing, and when to doubt itself.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| PK-01 | Fast capture — minimal friction, deferred categorization |
| PK-02 | Proactive surfacing — semantic relevance across projects |
| PK-04 | Decay — staleness detection, graceful cleanup |
| PK-05 | Incremental understanding — fragment assembly over time |
| PK-06 | Sensitivity — access control per knowledge atom |
| PK-07 | External ingestion — extraction, grading, contradiction detection |
| PK-09 | Domain expertise — research synthesis, durable expertise atoms |
| XP-01 | Cross-project discovery — semantic matching across boundaries |
| XP-03 | Lesson transfer — generalization evaluation |
| XP-04 | Conflict resolution — contradicting high-confidence atoms |
| XP-05 | Scale — performance at 10K+ atoms |
| XP-11 | Role-appropriate rendering — same data, different views |
| AP-01 | Regulatory knowledge with dependencies and currency |
| AP-02 | Versioned formulation knowledge with rationale links |
| AP-04 | Market intelligence with temporal context and source grading |
| RE-02 | Property data across lifecycle stages with verification status |
| RE-05 | Inconsistency detection across records |

### Architectural Implication

A **knowledge atom model** where each atom carries:
- Unique identity and type
- Source provenance (who/what created it, when)
- Epistemic grade (from T4 — canonical 5-level scale)
- Temporal metadata (created, last verified, decay threshold)
- Relationship links (to other atoms, UCs, decisions, projects)
- Sensitivity classification (public, internal, personal, confidential)
- Project scoping (belongs-to, visible-in)

Plus a **lifecycle engine** that:
- Enriches asynchronously after capture (don't block the human)
- Detects contradictions actively
- Proposes decay/archival based on staleness + importance
- Maintains performance at scale (indexing, cold storage)

### Existing Coverage

- D-001 (file-based memory): Storage tiers defined but atom schema is not
- `know` module: External sibling — provides MemoryService Protocol
- `know` ontology.json: Defines the 5-level epistemic scale
- ADR-0001: Import boundaries keep `know` access via Protocol only

### What's Missing

- **No canonical atom schema** — what fields are mandatory on every knowledge unit?
- **No lifecycle state machine** — what are the states and transitions?
- **No decay algorithm** — what makes something "stale" vs. "timeless"?
- **No cross-project access rules** — when can Project A see Project B's atoms?
- **No sensitivity enforcement architecture** — who enforces, where?

### Goal Alignment

- **goal-003** (primary): "Knowledge compounds within and across projects as durable organizational memory"
- **goal-001** (supporting): Persistent knowledge IS continuity

---

## T3: Workflow Orchestration

**Definition:** The coordination of specialized agents through a structured pipeline with
explicit handoffs, quality gates, approval tiers, verification checkpoints, and failure
recovery — while maintaining non-blocking human interaction.

**This is not task management. It is a pipeline protocol that moves ideas to outcomes
through a sequence of specialized cognitive modes.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| NF-02 | Enforce decisions — agents must respect prior architectural choices |
| NF-03 | Scope work — bounded tasks with explicit in/out |
| NF-04 | Self-assess quality — VBR protocol, no human for routine checks |
| NF-05 | Route approvals — tiered gates, non-blocking flow |
| NF-09 | Traceability — machine-checkable chain from code to UC |
| NF-13 | Multiple options — generate 2+ paths before committing |
| NF-14 | Work ratio — measure human vs AI contribution |
| XP-06 | Concurrent agents — coordination without conflict |

### Architectural Implication

An **orchestration engine** (the `flow` module) that:
- Sequences agents by workflow step (S1 → S9)
- Passes structured artifacts (not conversations) between steps
- Classifies actions by approval tier and routes accordingly
- Runs verification (VBR) before any "done" claim reaches the human
- Handles failures: retry, escalation, or human intervention
- Supports parallelism where steps are independent
- Logs every transition for auditability

### Existing Coverage

- D-003 (`flow` module): Designated orchestrator
- D-005 (dedicated agent per step): Agent specialization is decided
- WORKFLOW.md: Full S1-S9 protocol defined
- `.claude/agents/`: 19 agents with step-specific prompts
- Approval tiers: Defined conceptually (T1/T2/T3)

### What's Missing

- **No handoff contract** — what is the typed interface between S5 output and S6 input?
- **No failure recovery protocol** — what happens when S6 fails VBR 3 times?
- **No concurrency model** — when can agents overlap? (XP-06 is v2 but groundwork needed now)
- **No orchestration state machine** — `flow` module has contracts but no implementation

### Goal Alignment

- **goal-002** (primary): "The workflow becomes AI-led, low-friction, and enjoyable to use"
- **goal-004** (supporting): Orchestration must be stable enough to ship as infrastructure

---

## T4: Epistemic Awareness

**Definition:** The system's pervasive ability to represent, assign, propagate, and act on
confidence levels — across knowledge, decisions, options, and recommendations.

**This is not just "add a confidence field." It is a systemic commitment that every piece
of information carries a trust signal, and that trust degrades, propagates, and informs
behavior.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| NF-15 | Assign/surface epistemic grades on all workflow outputs |
| NF-16 | Drift detection — trust in alignment degrades over time |
| NF-11 | Vision drift — gradual disconnection from stated intent |
| PK-04 | Knowledge decay — confidence degrades with staleness |
| PK-05 | Incremental understanding — confidence grows with evidence |
| PK-09 | Domain expertise — graded answers with source provenance |
| XP-04 | Conflicting knowledge — resolution when high-confidence items contradict |
| AP-01 | Regulatory knowledge — "probably still current" vs. "verified current" |
| AP-04 | Market intelligence — anecdotes vs. industry reports |
| RE-05 | Inconsistencies — conflicting records of different authority |

### Architectural Implication

An **epistemic framework** that:
- Adopts the `know` 5-level vocabulary: SPECULATION → HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED → VERIFIED_FACT
- Requires grade assignment on every significant workflow output
- Defines propagation rules (a decision based on HYPOTHESIS inputs inherits their uncertainty)
- Defines decay rules (VERIFIED_FACT about tax law decays faster than VERIFIED_FACT about physics)
- Supports grade promotion (new evidence) and demotion (contradiction, staleness)
- Surfaces grades at human review points and agent consumption points

### Existing Coverage

- NF-15 references `know` ontology.json as canonical vocabulary
- 5×10 model assigns HYPOTHESIS grade to early-phase artifacts
- `grade` field appears in some templates

### What's Missing

- **No propagation rules** — how does uncertainty compound across dependent artifacts?
- **No domain-aware decay** — tax law decays faster than physical constants
- **No grade assignment authority** — who decides: producing agent, reviewer, or human?
- **No composite grading** — what's the grade of an options sheet with mixed-grade options?
- **No behavioral impact** — how should agents weight HYPOTHESIS vs. EVIDENCE_BASED inputs?

### Goal Alignment

- **goal-003** (supporting): Knowledge that compounds must know how much to trust itself
- **goal-001** (supporting): Trusting past reasoning requires knowing confidence at decision time

---

## T5: Domain Agnosticism

**Definition:** The system's ability to support any domain — software, food, real estate,
language learning, event planning — without changes to core code. Domain behavior is
configuration, not implementation.

**This is the architectural commitment that makes nowu a FRAMEWORK, not an APPLICATION.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| NF-07 | Bootstrap any new project — software or non-software |
| XP-07 | Adapt to new domain without rewriting |
| XP-09 | Onboard new users in any domain |
| AP-01..AP-07 | Food/beverage domain (7 UCs proving domain flexibility) |
| RE-01..RE-07 | Real estate domain (7 UCs proving domain flexibility) |

### Architectural Implication

A **domain extension architecture** where:
- Core modules (core, flow, soul) are domain-neutral
- Knowledge types, agent behaviors, and workflow templates are configurable per project
- Domain-specific vocabulary lives in project configuration, not framework code
- The same workflow pipeline works for "build a feature" and "get FDA approval"
- Extension points are explicit and documented (not "just modify the code")

### Existing Coverage

- D-002 (DDD layers): Domain doesn't import infrastructure
- D-003 (5-module structure): Modules are generic
- ADR-0001 (import boundaries): Cross-module calls via Protocol only
- Vision "What We Are NOT" #4: "We orchestrate agents to solve problems, not write code directly"

### What's Missing

- **No domain configuration schema** — what does a project config file look like?
- **No knowledge type extensibility model** — can domains add custom atom types?
- **No workflow customization protocol** — can domains skip/add steps?
- **No template system architecture** — how are domain templates discovered and loaded?

### Goal Alignment

- **goal-004** (primary): "nowu operates as trusted infrastructure and a shippable collaboration layer"
- **goal-002** (supporting): Non-software projects must flow through the same workflow

---

## T6: Observability & Traceability

**Definition:** The system's ability to be inspected at every level — from "why was this
code written?" up to "is the framework healthy?" — with machine-checkable provenance chains
and human-readable health metrics.

**Two distinct sub-concerns:**
1. **Traceability** (bottom-up): code → test → AC → UC → goal. Every artifact can answer "why do I exist?"
2. **Observability** (top-down): health metrics, work ratios, velocity, drift signals. "Is this working?"

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| NF-08 | Framework health metrics — velocity, coverage, loop frequency |
| NF-09 | Deliverable-to-UC traceability — machine-checkable at S8 |
| NF-14 | Human-AI work ratio — measure where friction lives |
| NF-11 | Vision drift — deviation from stated intent over time |
| RE-07 | Generate reports for different audiences from same data |
| AP-07 | Role-appropriate briefings from project state |
| XP-08 | Export full project state — everything is inspectable |
| XP-11 | Role-appropriate rendering — observability for different consumers |

### Architectural Implication

A **traceability + observability layer** that:
- Enforces validation_trace in every task spec (code → test → AC → UC chain)
- Collects metrics passively during normal workflow operation
- Generates periodic health reports (daily/weekly cadence)
- Supports audience-targeted views (developer sees different health than owner)
- Makes the full chain auditable by external parties (for goal-004 "shippable")

### Existing Coverage

- NF-09: Validation trace concept defined
- D-004 (TDD): Tests exist for every implementation
- `.claude/agents/health-*.md`: Health check agents exist
- `health-sweep` skill: Aggregates health checks

### What's Missing

- **No traceability metadata standard** — what fields, where, in what format?
- **No metric collection architecture** — where are metrics stored? Who produces them?
- **No health report schema** — what does a health report contain?
- **No baseline thresholds** — when is "low velocity" actually a problem?

### Goal Alignment

- **goal-002** (supporting): "clear feedback, visible progress" requires observability
- **goal-004** (supporting): External adoption requires inspectable, auditable workflows

---

## T7: Multi-Surface Access

**Definition:** The system's ability to serve the human across multiple interfaces and
contexts — CLI at desk, mobile capture on commute, voice notes mid-dinner, async review
on phone — without degrading core functionality.

**This is not "mobile app." It is the architectural separation between core capabilities
and the surfaces that expose them.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| PK-01 | Capture with minimal friction — anywhere, anytime, any format |
| PK-08 | Three interaction modes: capture, review, light action — from any device |
| NF-10 | Orientation should be available wherever the human is |
| PK-03 | Today view works on any surface |
| AP-07 | Collaborator receives briefing without requiring nowu installation |
| RE-07 | Reports generated for external consumption |
| XP-09 | New users onboard without learning internal vocabulary |

### Architectural Implication

An **adapter architecture** where:
- Core operations are exposed via a stable internal API
- `bridge` module is the adapter layer between core and multiple surfaces
- Each surface implements a subset of operations appropriate to its context
- Capture is the minimum viable surface (voice, text, any device)
- Enrichment happens async after capture (don't block the input moment)
- Review surfaces render the same data in context-appropriate formats

### Existing Coverage

- D-003: `bridge` module designated for human-AI translation
- ADR-0001: Bridge can import core and flow (it's the outermost layer)
- Vision: "nowu must meet him wherever he is"

### What's Missing

- **No internal API specification** — what operations does bridge expose?
- **No adapter contract** — what must a new surface implement?
- **No async enrichment protocol** — how does raw capture become structured knowledge?
- **No surface capability matrix** — what can you do from mobile vs. desktop?

### Goal Alignment

- **goal-002** (supporting): Low-friction requires meeting the user where they are
- **goal-004** (supporting): Multi-user adoption requires multiple access paths

---

## T8: Progressive Disclosure

**Definition:** The system's ability to accept input at ANY level of fidelity — from a raw
half-thought to a fully structured decision — and resolve ambiguity progressively through
structured doing, not by demanding premature structure.

**This is Guiding Principle #3 ("Clarity is earned, not imposed") made architectural.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| NF-12 | Explore vague idea without structure — no-commitment mode |
| NF-13 | Options at decisions — structure only at decision points |
| NF-03 | Scope comes AFTER idea has been explored, not before |
| PK-01 | Capture raw thought — categorization happens later |
| PK-05 | Build understanding incrementally — fragments become synthesis |
| XP-09 | Onboard without exposing internal vocabulary |
| AP-06 | Decision can be lightweight or structured — context-dependent |

### Architectural Implication

An **artifact maturity model** where:
- Entities evolve through stages: raw capture → enriched fragment → linked atom → structured artifact
- The system never rejects input for being "too vague"
- Promotion from one stage to the next is triggered by evidence or action, not time
- Async enrichment resolves what can be resolved without human input
- The system invites structure at the right moment — not before
- Pre-workflow P0 IS the architectural expression of this: vague → structured progressively

### Existing Coverage

- 5×10 model: Altitude layers ARE progressive disclosure (product → system → module → component → code)
- Guiding Principle #3: "Clarity is earned, not imposed"
- P0-P4 pre-workflow: Progressively structures ideas before S1
- NF-12 explicitly requires "no-commitment exploration mode"

### What's Missing

- **No artifact maturity state machine** — what are the formal stages?
- **No promotion triggers** — when does a raw capture become a linked atom?
- **No enrichment protocol** — what does async enrichment DO, specifically?
- **No "vague mode" architecture** — how does NF-12 differ from P0 structurally?

### Goal Alignment

- **goal-002** (primary): "start from a vague idea and get meaningful output" = progressive disclosure
- **goal-001** (supporting): Captured fragments must persist even when vague

---

## T9: Audience-Aware Rendering

**Definition:** The system's ability to render the SAME underlying data in formats
optimized for different consumers — human narrative, agent-structured context, collaborator
briefings, portable exports — without maintaining separate copies.

**This is the architectural commitment: STORAGE is separated from PRESENTATION. One graph,
many views.**

### Contributing UCs

| UC | Contribution to Theme |
|---|---|
| XP-11 | Same knowledge subgraph → human summary vs. agent context block |
| AP-07 | Role-scoped project briefings for collaborators |
| RE-07 | Audience-appropriate reports (bank, accountant, tenant, buyer) |
| PK-08 | Mobile review surface renders context differently than CLI |
| XP-08 | Export in open formats — rendering for portability |
| XP-09 | New user sees plain language, not internal vocabulary |
| XP-10 | Company-level view aggregates across project views |

### Architectural Implication

A **rendering layer** separated from storage that:
- Determines consumer type (human, agent, role, external)
- Selects appropriate renderer per consumer
- Applies access control (sensitivity from T2) during rendering
- Produces different formats from same underlying graph query
- Supports: narrative prose, structured context blocks, filtered briefings, portable exports

### Existing Coverage

- Vision "Our Solution": "rendered differently depending on who is reading it"
- Vision: "condensed and visual for the human, structured and scoped for the AI agent"
- D-002 (DDD layers): Presentation is a separate layer concern

### What's Missing

- **No renderer architecture** — is rendering a core concern or a bridge concern?
- **No consumer type taxonomy** — what consumer types exist?
- **No rendering format registry** — what output formats are supported?
- **No query-to-render pipeline** — how does "show me X" become the right format?

### Goal Alignment

- **goal-004** (primary): Shippable infrastructure must serve multiple consumer types
- **goal-003** (supporting): Knowledge that compounds must be usable by both humans and agents

---

## Theme Interaction Map

Themes are not independent. Key interactions:

```
T1 (Continuity) ←→ T2 (Knowledge): Continuity IS persistent knowledge about project state
T2 (Knowledge) ←→ T4 (Epistemic): Every atom carries an epistemic grade
T3 (Orchestration) ←→ T4 (Epistemic): Agents must respect confidence when making decisions
T3 (Orchestration) ←→ T6 (Observability): Every orchestration step is observable
T5 (Domain Agnostic) ←→ T2 (Knowledge): Atom types must be extensible per domain
T7 (Multi-Surface) ←→ T9 (Rendering): Surfaces consume rendered output, not raw data
T8 (Progressive) ←→ T2 (Knowledge): Knowledge atoms have maturity stages
T6 (Observability) ←→ T4 (Epistemic): Health reports carry confidence grades
```

**Critical dependency chain:**
```
T2 (Knowledge Model) must be decided FIRST — T1, T4, T5, T8, T9 all depend on it.
T3 (Orchestration) is independent but touches everything at handoff boundaries.
T4 (Epistemic) is pervasive — it infects every other theme's metadata model.
```

**Refined ADR dependency graph** (from Perplexity review, 2026-05-07):
```
ADR-0008 (atom schema) ← foundational, everything depends on this
    ↓
ADR-0010 (grades) + ADR-0007 (continuity) — PARALLEL, both depend on atom schema
    ↓                                         (T1: "session state IS knowledge atoms")
ADR-0009 (orchestration) — depends on having continuity protocol + graded artifacts to route
```
Note: ADR-0007 depends on ADR-0008 because continuity state uses the atom model
(session checkpoints ARE knowledge atoms about project state). This was implicit in
the original dependency description but the graph now makes it explicit.

---

## ADR Recommendations

Based on the gaps identified above, the following hypothesis ADRs should be written.
Ordered by dependency (foundational first):

| Priority | Recommended ADR | Theme | Architectural Question | Existing Partial Coverage |
|----------|----------------|-------|----------------------|--------------------------|
| 1 | ADR-0008: Knowledge Atom Model & Lifecycle | T2 | What is the canonical atom schema? What are lifecycle states? | D-001 (storage), `know` ontology |
| 2 | ADR-0010: Epistemic Grade Assignment & Propagation | T4 | Who assigns grades? How do they propagate? When do they decay? | NF-15, `know` ontology.json |
| 3 | ADR-0007: Session Continuity Protocol | T1 | What checkpoint schema survives crashes? How does orientation work? | D-001, SESSION_STATE.md |
| 4 | ADR-0009: Orchestration Protocol & Agent Handoff Contract | T3 | What's the typed interface between workflow steps? | D-005, WORKFLOW.md |
| 5 | ADR-0011: Domain Extension Model | T5 | What's configurable per domain? What extension points exist? | D-002, D-003, ADR-0001 |
| 6 | ADR-0012: Traceability Metadata Standard | T6 | What fields, where, in what format for the UC→code chain? | NF-09, D-004 |
| 7 | ADR-0014: Artifact Maturity & Progressive Enrichment | T8 | What stages exist? What triggers promotion? | 5×10 model, Principle #3 |
| 8 | ADR-0013: Interface Adapter Architecture | T7 | What's the internal API surface? What must adapters implement? | D-003 (bridge), ADR-0001 |
| 9 | ADR-0015: Consumer-Aware Knowledge Rendering | T9 | How is storage separated from presentation? Consumer types? | Vision, D-002 |

### Why This Order

1. **ADR-0008 first**: The knowledge atom model is the foundational data type. T1 (continuity
   state IS knowledge), T4 (grades live ON atoms), T5 (domains extend atom types), T8
   (atoms have maturity stages), and T9 (atoms are what gets rendered) all depend on it.

2. **ADR-0010 second**: Epistemic grades are pervasive metadata on atoms and artifacts. Once
   the atom model exists, grades must be defined before anything produces graded output.

3. **ADR-0007 third**: Continuity protocol builds ON the knowledge model (session state IS
   knowledge atoms about project state). Must be resolved before first S1-S9 intake.

4. **ADR-0009 fourth**: Orchestration defines how agents MOVE artifacts through the pipeline.
   Independent of knowledge model but needs to reference it for handoff payloads.

5. **ADR-0011..0015**: Build on the foundation. Deferrable to later stages without blocking
   v1-core, but should be at least HYPOTHESIS-grade before v1.1.

---

## Validation Against Expected Themes

The handoff document predicted 6 themes. Result:

| Expected Theme | Confirmed? | Notes |
|---|---|---|
| Continuity | YES (T1) | Confirmed with strong evidence |
| Knowledge persistence | YES (T2) | Much broader than expected — 17+ UCs, lifecycle is key |
| Workflow orchestration | YES (T3) | Confirmed as expected |
| Epistemic awareness | YES (T4) | More pervasive than expected — crosses ALL other themes |
| Domain agnosticism | YES (T5) | Confirmed; AP/RE groups ARE the evidence |
| Observability | YES (T6) | Extended to include traceability as sub-concern |

**3 additional themes discovered:**

| New Theme | Why It's Distinct | Why It Matters |
|---|---|---|
| T7: Multi-Surface Access | Not "domain agnostic" (T5) — that's WHAT the system does. This is WHERE/HOW the human accesses it. | PK-08 + vision "meet him wherever he is" — affects bridge architecture fundamentally |
| T8: Progressive Disclosure | Not "workflow" (T3) — that's agent sequencing. This is the HUMAN's journey from vague to structured. | Principle #3 made architectural — without this, NF-12 is impossible |
| T9: Audience-Aware Rendering | Not "observability" (T6) — that's "is it healthy?" This is "render the SAME data for DIFFERENT consumers." | XP-11 + vision "same data, different lenses" — drives storage/presentation separation |

---

## Next Steps

1. **Produce Architecture Vision** (`docs/architecture/ARCHITECTURE-VISION.md`) — system
   classification, principles, quality attributes, and ADR roadmap derived from these themes.
2. **Write hypothesis ADRs** (W3 from STAGED-PLAN) starting with ADR-0008, following the
   priority order above.
3. **Map themes to goals** — populate `linked_ucs` fields in goal-001..004.md with theme
   evidence.
4. **First S1-S9 intake** (W4) — use SYNTHESIS themes as architectural context for the
   first end-to-end workflow run.
