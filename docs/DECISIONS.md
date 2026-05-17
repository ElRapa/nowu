# nowu Architectural Decisions

<!-- Template for new entries: templates/decision.md -->
<!-- Template for new entries: templates/decision.md
     Level values (decision zoom): product | system | module | component | code -->

---

## D-001 — File-Based Memory Architecture

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Context
AI agents and humans both lose context. A persistent, readable, recoverable
memory system is required before any other feature can work reliably.

### Decision
Use file-based memory (Markdown + YAML frontmatter) with three tiers:
1. Active working state (`state/`) — per-artifact files
2. Architecture decisions (`docs/DECISIONS.md`) — this file
3. Long-term knowledge (`know` module) — future semantic graph

### Consequences
- **Good**: version-controllable, human-readable, no external deps
- **Bad**: files grow; need compaction strategy later (know handles this)

### Review Trigger
When `know` MemoryService is operational.

---

## D-002 — DDD Layer Architecture

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Context
Without enforced layer boundaries, infrastructure concerns leak into domain
logic, making testing difficult and coupling inevitable.

### Decision
Four-layer DDD: Domain (pure logic) → Application (use cases) →
Infrastructure (I/O, AI) → Interface (CLI, API).  
Domain must not import from any other layer.  
All cross-module dependencies go through `core/contracts/*.py` Protocols.

### Consequences
- **Good**: domain is testable in isolation, layers are swappable
- **Bad**: more boilerplate (mitigated by Protocol pattern)

### Review Trigger
Never — this is a foundational constraint.

---

## D-003 — 5-Module Structure

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: module  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Decision
Five modules: `core` (shared contracts+services) · `flow` (orchestration) ·
`bridge` (human-AI translation) · `soul` (identity+config) · `know` (knowledge).

### Tradeoff Points
Simplicity vs. granularity. Five modules is lean — avoids over-engineering at v1.
May need splitting when `bridge` grows complex.

### Review Trigger
When any module exceeds 2000 LOC.

---

## D-004 — TDD as Non-Negotiable Constraint

**Date**: 2026-02-25 | **Status**: ACCEPTED | **Level**: component  
**Intake**: — (bootstrap decision) | **Use Cases**: all

### Decision
Tests written BEFORE implementation. 90%+ coverage enforced in CI.
VBR hook prevents commits when tests fail.

### Consequences
- **Good**: code quality, safe refactoring, verified acceptance criteria
- **Bad**: slower initial velocity (worthwhile tradeoff for a self-developing system)

### Review Trigger
When coverage or quality targets need adjustment.

---

## D-005 — Dedicated Agent Per Workflow Step

**Date**: 2026-03-15 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (architecture decision) | **Use Cases**: all

### Context
Previous versions used 4 shared agents (architect used for S2, S3, S4).
Research shows context scope and cognitive mode differ per step, and a single
“architect” agent carries stale context between steps.

### Decision
8 dedicated agents, one per step (S1: nowu-intake, S2: nowu-constraints,
S3: nowu-options, S4: nowu-decider, S5: nowu-shaper, S6+S7: nowu-implementer,
S8: nowu-reviewer, S9: nowu-curator). Each agent is concise (≤60 lines) and
scoped to exactly the context its step needs.

### Tradeoff Points
More agent files vs. cleaner context isolation and specialised prompting.
The benefits (no context bleed, step-appropriate decision methods) outweigh
the maintenance cost of 8 small files over 4 large ones.

### Review Trigger
When agents need to collaborate across steps (future team features).

---

## D-006 — Treat `know` as the external memory system of record

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: system  
**Intake**: V1 planning | **Use Cases**: all

### Context
The original nowu draft planned to implement a local `know` module from scratch.

### Decision
Reuse the existing sibling project `know` (v0.4.0) through `KnowledgeBase` class API and `KnowAdapter(kb)`.
No internal reimplementation in nowu.

### Consequences
- Faster delivery, lower risk, and tighter contract boundaries.
- nowu modules must not bypass `know`.
- `know.init()` and flat module functions are gone; use `KnowledgeBase` instance methods.
- `today()` removed; use `kb.query_atoms(type=KnowledgeType.TASK, ...)` + date filtering.

---

## D-007 — Choose integration-first modular monolith for v1

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: system  
**Intake**: V1 architecture | **Use Cases**: all

### Context
Evaluated three options: modular monolith, event-driven internal bus,
and early microservices.

### Decision
Use an integration-first modular monolith for v1, with explicit interfaces
to allow future event-driven evolution.

### Consequences
- Best speed/reliability tradeoff for solo + AI development.
- Scale/distribution concerns deferred beyond v1.

---

## D-008 — Rebase v1 planning around integration slices, not component reinvention

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: product  
**Intake**: V1 planning | **Use Cases**: all

### Context
Prior `V1_PLAN.md` did not reflect current repository reality and lacked
architecture decision gates per step.

### Decision
Replace with seven incremental steps: contracts, memory integration,
session/WAL, role pipeline, bridge/approvals, learning/curation,
bootstrap/cross-project context.

### Consequences
Each step now includes architecture analysis, design options, evaluation,
detailed plan, and implementation verification.

---

## D-009 — Standardize role-driven workflow with VBR and approval tiers

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: system  
**Intake**: Workflow design | **Use Cases**: all

### Context
Existing workflow text was tied to a tool-specific issue pattern and did not
define strict AI handoffs.

### Decision
Adopt a role loop (Architect, Shaper, Implementer, Reviewer, Curator) with
Verify Before Reporting, Tier 1/2/3 approvals, and clear escalation.

### Consequences
Reduced scope drift, higher review quality, and clearer escalation behavior.

---

## D-010 — Prioritize NF core use cases for v1 and treat full set as direction

**Date:** 2026-03-04 | **Status**: ACCEPTED | **Level**: product  
**Intake**: V1 scope | **Use Cases**: NF-01..NF-07, PK-01, PK-03, XP-01

### Context
`USE_CASES.md` contains 35 use cases across NF/AP/RE/PK/XP and is intentionally broad.

### Decision
Focus v1 on NF-01..NF-07 plus PK-01/PK-03 and XP-01 as enabling coverage.

### Consequences
Keeps v1 achievable while preserving expansion path for domain-specific capabilities.

---

## D-012 — Goal Brief v2: Agent-created goals with measurement infrastructure

**Date:** 2026-04-30 | **Status**: ACCEPTED | **Level**: product  
**Supersedes**: D-011 (reverted)  

### Context
D-011 proposed a minimal goal-layer approach, which was reverted due to lack of
measurement infrastructure and bidirectional UC↔goal mapping. This decision
revisits the goal layer with a more comprehensive approach.

### Decision
Adopt Goal Brief v2 with the following key elements:
- Agent-created goals (not human-created) to align with the 90-99% AI work vision.
- Bidirectional UC↔goal mapping for traceability.
- Measurement infrastructure to track success criteria, phase coverage, and UC completion %.
- Capability maps in Solution Shape to provide agents with "bigger picture" context.
- Altitude/phase frontmatter for forward-compatible groundwork (idea-004).

### Alternatives Considered
1. **V1 Minimal Approach (D-011):**
   - Pros: Faster to implement.
   - Cons: Lacked measurement infrastructure and traceability.
2. **V2 Full Approach (adopted):**
   - Pros: Comprehensive, forward-compatible, aligns with AI-first vision.
   - Cons: Higher initial complexity.
3. **No Goals:**
   - Pros: Simplifies architecture.
   - Cons: No progress tracking, misaligned AI work.

### Rationale
- Agent-created goals ensure alignment with the AI-first vision.
- Measurement infrastructure enables progress tracking and accountability.
- Capability maps and altitude/phase frontmatter future-proof the system.

### Dependencies
- UC backfill of existing 50 UCs is deferred.
- Measurement infrastructure requires updates to `state/` and `docs/USE_CASES.md`.

---

## D-013 — 5×10 Altitude-Phase Workflow Model

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: EVIDENCE_BASED  
**Evidence**: Anthony 1965, Shape Up, SYSMOD zigzag, Rombaut 2026, AFLOW (ICLR 2025)

### Context
The original workflow (S1-S9 with C4 levels) lacked explicit altitude coordination,
had no mechanism for cross-cutting synthesis, and didn't prevent altitude drift
(jumping from PRODUCT to DELIVERY without ARCHITECTURE).

### Decision
Adopt a 5×10 model: 5 altitudes (STRATEGIC > PRODUCT > ARCHITECTURE > DELIVERY > EXECUTION)
× 10 phases (IDEA > PROBLEM > ANALYSIS > SYNTHESIS > OPTIONS > DECISION > EVALUATION >
IMPLEMENTATION > VERIFICATION > LEARN). The matrix is a coordinate system (cognitive GPS),
not a pipeline. S1-S9 is a default traversal within this space.

### Consequences
- **Good**: Explicit altitude tracking, SYNTHESIS forces global view, epistemic grades possible
- **Bad**: More conceptual overhead; requires model documentation (→ `docs/model/`)

### Review Trigger
After 10+ intakes complete — validate the model reflects observed patterns.

---

## D-014 — SYNTHESIS as Altitude-Locked Phase at ARCHITECTURE

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: INFORMED_ESTIMATE  
**Evidence**: TOGAF Phase A, cross-cutting concern analysis

### Context
Approved UCs accumulate without global architectural view. Each S1-S9 intake
starts from scratch. Result: patchwork architecture with misaligned features.

### Decision
SYNTHESIS is the 10th phase, locked to ARCHITECTURE altitude. It reads approved
UCs, finds cross-cutting themes, and recommends ADRs. Triggered when ≥2 approved
UCs have `architectural_implications: true` and no linked ADRs, or by human override.

### Consequences
- **Good**: Forces global view before individual intakes; prevents premature decomposition
- **Bad**: Adds a blocking step before S1-S9 can run (intentional — that's the point)

### Review Trigger
After first manual SYNTHESIS run validates the process.

---

## D-015 — Epistemic Grades with Tiered Enforcement

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (workflow architecture session) | **Use Cases**: NF-15  
**Epistemic Grade**: INFORMED_ESTIMATE  
**Evidence**: Novel mechanism; validated by Perplexity research (no comparable framework)

### Context
Agent outputs (options, decisions, ADRs) carry no explicit confidence level.
Downstream consumers can't distinguish "first guess" from "battle-tested decision."

### Decision
Every artifact carries an epistemic grade: SPECULATION, HYPOTHESIS, INFORMED_ESTIMATE,
EVIDENCE_BASED, VERIFIED_FACT. Enforcement is tiered:
- Level 0 (v1-core): Syntax check only (grade field exists)
- Level 1 (v1): Advisory warnings for altitude/grade violations
- Level 2 (v1.1): Blocking at DECISION gates if below aspirational grade

### Consequences
- **Good**: Trust calibration; safe "write first, validate later" workflow
- **Bad**: Requires discipline in grading; needs calibration from real usage

### Review Trigger
After 5+ intakes — calibrate thresholds empirically.

---

## D-016 — Architecture Vision Required Before Hypothesis ADRs

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: product  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: INFORMED_ESTIMATE  
**Evidence**: TOGAF Phase A (Architecture Vision distinct from ADRs)

### Context
SYNTHESIS produces themes and ADR recommendations. But themes alone don't establish
"what kind of system is this?" — the narrative identity that makes ADRs coherent.

### Decision
SYNTHESIS → Architecture Vision → Hypothesis ADRs. Architecture Vision is a 1-page
artifact: system classification, principles, quality attributes, risks. It answers
"what kind of system solves these themes?" before ADRs answer "how?"

### Consequences
- **Good**: ADRs become coherent (share a vision); prevents contradictory decisions
- **Bad**: One more artifact before implementation starts (short — 1 page)

### Review Trigger
When Architecture Vision is produced and validated through first intakes.

---

## D-017 — Minimum Viable Architecture (Hypothesis ADRs + Feedback Loop)

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: INFORMED_ESTIMATE  
**Evidence**: MVA literature, GitHub Spec Kit methodology

### Context
Two extremes: Big Design Upfront (slow, often wrong) vs. No Design (chaotic).
Need a middle path that allows architecture to emerge through validated iteration.

### Decision
Write ADRs at HYPOTHESIS grade (deep enough for AI agents to follow, shallow enough
to be wrong). Run 1-2 S1-S9 intakes against hypothesis. Refine based on friction.
Promote grades: HYPOTHESIS → INFORMED_ESTIMATE (after 2 intakes) → EVIDENCE_BASED (after 5+).

### Consequences
- **Good**: Architecture evolves with evidence; no Big Design Upfront paralysis
- **Bad**: Early intakes may hit friction from hypothesis ADRs (expected, that's learning)

### Review Trigger
After 2 intakes validate/invalidate hypothesis ADRs.

---

## D-018 — Phases Are Cognitive Modes (Not Altitude-Locked)

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: EVIDENCE_BASED  
**Evidence**: AFLOW operators, Rombaut loop primitives

### Context
Initial model assumed phases were locked to altitudes (e.g., IMPLEMENTATION = EXECUTION only).
This doesn't match reality: writing an ADR is IMPLEMENTATION at ARCHITECTURE altitude.

### Decision
Phases are cognitive modes that can occur at multiple altitudes. IMPLEMENTATION works at
ARCHITECTURE (writing ADRs), DELIVERY (creating task specs), and EXECUTION (code).
Exception: SYNTHESIS is the ONLY altitude-locked phase (ARCHITECTURE only).

### Consequences
- **Good**: Model matches reality; agents can implement/verify at any altitude
- **Bad**: The 5×10 grid isn't fully populated — many cells are rare/empty (that's fine)

### Review Trigger
Never — this is definitional to the model.

---

## D-019 — Router-Based Agent Architecture (Altitude-Agnostic Executors)

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: system  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: INFORMED_ESTIMATE  
**Evidence**: Hierarchical MAS research, Redis 2026 multi-agent patterns

### Context
Should S1-S9 agents know their altitude and behave differently, or should
routing be centralized with agents remaining simple executors?

### Decision
90% of agents are altitude-AGNOSTIC (they execute their phase without knowing altitude).
The orchestrator/router knows altitude and routes accordingly.
10% are altitude-AWARE: only GAP/reflective agents that reason about cross-altitude patterns.

### Consequences
- **Good**: Agents stay simple; routing logic is centralized and testable
- **Bad**: Router becomes a critical single point; must be well-tested

### Review Trigger
When orchestrator is implemented (v1, task A3 in ROADMAP-001).

---

## D-020 — Staged Plan: Areas × Stages

**Date**: 2026-05-06 | **Status**: ACCEPTED | **Level**: product  
**Intake**: — (workflow architecture session) | **Use Cases**: all  
**Epistemic Grade**: HYPOTHESIS  
**Supersedes**: V1_PLAN.md 7-step linear approach

### Context
V1_PLAN.md was a linear 7-step plan focused only on Framework implementation.
It didn't account for Workflow, Knowledge, or Agent areas as independent workstreams.

### Decision
Replace with 4 areas (Workflow, Knowledge, Agents, Framework) × 4 stages
(v1-core, v1, v1.1, v2). Each cell is independently actionable with explicit dependencies.
See `docs/ROADMAP.md` for full detail.

### Consequences
- **Good**: Parallel progress possible; clear dependencies; no monolithic sequencing
- **Bad**: More complex to track than linear steps (mitigated by ROADMAP-001 structure)

### Review Trigger
After v1-core gate passes (first S1-S9 intake end-to-end).

---

<!-- Add new decisions below this line using templates/decision.md -->

## D-021 — Hypothesis ADRs Written in Dependency Order (W3 Complete)

**Date**: 2026-05-07 | **Status**: ACCEPTED | **Level**: system  
**Intake**: W3 (ROADMAP-001) | **Use Cases**: all  
**Epistemic Grade**: INFORMED_ESTIMATE

### Context
SYNTHESIS-001 (W1) and Architecture Vision (W2) produced 9 architectural themes and a
dependency-ordered ADR roadmap. W3 required writing the first 4 hypothesis ADRs to unblock
the first S1-S9 intake (W4).

### Decision
Write 4 hypothesis ADRs in dependency order:
1. **ADR-0008** (Knowledge Atom Model) — foundational; adopts `know` module's `KnowledgeAtom`
2. **ADR-0010** (Epistemic Grades) — assignment rules, propagation, decay
3. **ADR-0007** (Session Continuity) — two-layer checkpoint (machine + human bookmark)
4. **ADR-0009** (Orchestration Protocol) — typed handoff contract, state machine, failure recovery

All at HYPOTHESIS grade per D-017 (Minimum Viable Architecture).

Perplexity review (2026-05-07) validated the synthesis and vision work, identified 3 refinements:
refined ADR dependency graph (ADR-0007 depends on ADR-0008), user space boundary gap (deferred
to ADR-0011), and W3.5 fitness functions (added to ROADMAP-001).

### Consequences
- W3 is complete; critical path advances to W3.5 → W4
- 4 new ADRs provide architectural context for first S1-S9 intake
- ADRs are HYPOTHESIS — expected to be refined through implementation feedback

---

## D-022 — Orchestrator Layer: External Meta-Workflow

**Date**: 2026-05-09 | **Status**: ACCEPTED | **Level**: system  
**Intake**: Perplexity research session (2026-05-08) | **Use Cases**: all  
**Epistemic Grade**: INFORMED_ESTIMATE  
**Builds on**: D-019 (Router-Based Agent Architecture), D-020 (Staged Plan: Areas × Stages)

### Context

The nowu 5×10 workflow model defines execution phases (SENSE, PROBLEM, ANALYSIS, etc.)
but lacks a formal mechanism for deciding what work enters the field next. ROADMAP-001.md
(formerly STAGED-PLAN.md) was created manually outside the formal workflow model, revealing
the gap between execution (the work) and orchestration (deciding what work happens next).

Industry research validates this separation as universal: Shape Up's betting table, SAFe's
PI Planning, Temporal's workflow tasks, AFLOW's optimizer, AgentOrchestra's Planning Agent,
and HTN's compound tasks all distinguish execution from orchestration.

D-019 established that the orchestrator/router is the centralized routing authority. This
decision formalizes the orchestrator as a layer with dedicated agents and artifacts.

### Decision

Introduce an **orchestrator layer** that sits **outside** the 5×10 execution field:

Three meta-agents (not part of the execution agent roster):
1. `roadmap-creator`: Bootstraps initial roadmap from vision + goals + early UCs (STRATEGIC/IMPLEMENTATION)
2. `roadmap-updater`: Integrates new evidence at milestone boundaries (STRATEGIC/LEARN)
3. `work-scheduler`: Read-only query agent that decides next work item (no altitude — pure orchestration)

One versioned artifact:
- `docs/ROADMAP-NNN.md` with epistemic grade progression (HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED)

The orchestrator is **not part of the 5×10 grid** — it decides what work enters the grid.
ROADMAP-001.md (formerly STAGED-PLAN.md) is retroactively formalized as the first roadmap artifact.

### Consequences

- **Good**: Formalizes "what's next?" logic that was previously implicit
- **Good**: Validates existing ROADMAP-001.md with proper lineage and versioning
- **Good**: Aligns nowu with industry-standard separation of execution vs. orchestration
- **Bad**: Adds three new meta-agents that must be maintained
- **Bad**: Introduces versioned roadmap artifact that must be kept in sync with reality

### Review Trigger

If the orchestrator becomes a bottleneck (too slow, too manual, too rigid),
revisit and consider automated work scheduling based on dependency graphs.

---

## D-023 — Use Cases Must Not Reference Implementation Artifacts

**Date**: 2026-05-11 | **Status**: ACCEPTED | **Level**: product  
**Intake**: Validity audit of USE_CASES.md (2026-05-11) | **Use Cases**: NF-09  
**Epistemic Grade**: EVIDENCE_BASED  
**Builds on**: D-013 (Altitude Discipline), D-020 (Staged Plan)

### Context

Use cases in `docs/USE_CASES.md` accumulated inline references to implementation
artifacts — specific filenames (`state/SESSION-STATE.md`, `V1_PLAN Step 05`),
directory paths (`state/goals/goal-NNN.md`), and resolved implementation details
(`in_scope_files` in Task Spec). These references broke repeatedly as the codebase
evolved: filenames changed (SESSION_STATE vs SESSION-STATE), files were archived
(V1_PLAN → docs/archive/), directories moved (goals from state/ to docs/), and
the session-state methodology was replaced entirely (session-log.md).

Use cases are written *before* implementation and describe *what* the system must
do, not *how* it does it. Embedding implementation references couples a stable
strategic document to an unstable implementation surface, violating altitude
discipline (D-013 Principle 4).

### Decision

**Strategic and product altitude documents (vision, goals, use cases) must not
reference implementation artifacts by filepath or filename.** Specifically:

1. **Reference stable IDs, not files.** Use decision IDs (D-NNN), ADR IDs
   (ADR-NNNN), and UC IDs (NF-01) — never filenames or directory paths.

2. **Resolved open questions reference the decision, not the artifact.** Instead
   of `*(Resolved: agent reads state/SESSION-STATE.md...)*`, write
   `*(Resolved: see ADR-0007 for session continuity protocol.)*`

3. **UC-to-implementation traceability lives in the ROADMAP.** ROADMAP-NNN
   Section 3 (UC-to-Stage Mapping) is the canonical place for linking UCs to
   work items and implementation details. It is expected to change frequently.

4. **No V1_PLAN-era traceability sections in USE_CASES.md.** Stage mapping is
   now owned by the roadmap artifact per D-020.

### Consequences

- **Good**: USE_CASES.md stops breaking when filenames change
- **Good**: Enforces altitude discipline — UCs stay at product altitude
- **Good**: Reduces maintenance burden on strategic documents
- **Good**: Traceability is centralized in the roadmap where it belongs
- **Bad**: Existing resolved open questions need a cleanup pass (one-time cost)

### Review Trigger

Never — this is a documentation hygiene constraint that follows directly from
altitude discipline (D-013).---

## D-024 — Versioned Session Checkpoint Schema

**Date**: 2026-05-12 | **Status**: ACCEPTED | **Level**: module  
**Intake**: intake-001 (Resume Work After Context Loss) | **Use Cases**: NF-01  
**Epistemic Grade**: HYPOTHESIS (tested via intake-001 implementation)  
**Builds on**: D-002 (DDD), D-004 (TDD), D-017 (Hypothesis ADRs)

### Context

Intake-001 requires agents to read persisted session state and propose the next action (NF-01 AC-1). ADR-0007 specifies `SessionCheckpoint` with 10 fields. Current `SessionSnapshot` has 5 fields, is frozen.

### Decision

Implement Option C: Versioned Schema.

1. New `SessionCheckpoint` dataclass in `core/contracts/types.py` with all 10 fields required
2. Update `SessionStore` protocol: `save(checkpoint: SessionCheckpoint)`, `load() -> SessionCheckpoint | None`
3. Migration logic in `FileSessionStore` to read old format, upgrade to new
4. Write `state/SESSION_STATE.md` YAML projection atomically with JSON checkpoint

### Consequences

- **Good**: Eliminates Optional-field ambiguity, direct ADR-0007 test
- **Bad**: Tier 3 breaking change to SessionStore API (low blast radius — flow is stub)

### Effort: 7h (tight vs 8h appetite)

### Review Trigger

After S6-S7: verify migration complete, schema translation tested, atomicity proven.

---

## D-025 — Branch Strategy: Mode-Dependent Git Workflow

**Date**: 2026-05-14 | **Status**: ACCEPTED | **Level**: system
**Intake**: — (workflow optimization) | **Use Cases**: NF-01, NF-09

### Context

Commit behavior was inconsistent across workflow skills: full-cycle said "Commit message / commit",
implement-loop and single-step said "Commit message suggestion". No branching strategy existed.
Tier 3 rules require human-gated merges to main, but nothing enforced working on branches.

### Decision

Branch strategy is mode-dependent:
- **Mode A/B** (full-cycle, implement-loop): Work on feature branch `feat/{work-item-id}`.
  Commit per task within the branch. Merge to main is Tier 3 (human-gated).
- **Mode C** (single-step): Commit directly to main. No branch overhead for small fixes.

Curator executes the commit (not just suggests a message). Staged paths are restricted to
`state/`, `docs/`, and `state/learnings/` — never `src/` or `tests/` (those are S6/S7 territory).

### Consequences

- **Good**: Consistent git workflow; heavy work is isolated on branches; small fixes stay fast
- **Bad**: Mode A/B requires branch creation/switching overhead; merge conflicts possible

---

## D-026 — Conditional Auto-Invocation of Session-Learning

**Date**: 2026-05-14 | **Status**: ACCEPTED | **Level**: system
**Intake**: — (workflow optimization) | **Use Cases**: NF-06

### Context

Session-learning was documented as "run after S9" but never auto-invoked. In 3 of 5 recent
sessions it was forgotten, losing process insights. Always auto-invoking would generate noise
for trivial single-file fixes.

### Decision

Session-learning auto-invokes after S9 capture when ANY condition is met:
1. Session modified 5+ files
2. 3+ tasks were completed
3. Session introduced new decisions (D-NNN)
4. `next_cycle_trigger` is ARCH_PIVOT or PRODUCT_PIVOT

Skip if the session was Mode C with ≤4 files changed and no new decisions.

### Consequences

- **Good**: Process insights captured consistently; recurring patterns detected earlier
- **Bad**: Adds ~2 minutes to S9 for qualifying sessions; learnings files accumulate

---

## D-027 — AP Domain Bootstrap as Artifact-Only Evidence Run

**Date**: 2026-05-15 | **Status**: ACCEPTED | **Level**: system
**Intake**: intake-007 (W27) | **Use Cases**: AP-01, AP-02, AP-06
**Epistemic Grade**: HYPOTHESIS
**Builds on**: D-006 (know as external memory), D-017 (Hypothesis ADRs), D-020 (Staged Plan)

### Context

W27 is the first domain-specific intake — validating that nowu can manage non-software
domain knowledge (aperitif business). Three options were evaluated: (A) artifact-only
validation, (B) artifact + thin schema proposal, (C) artifact + minimal contract extension.
The current MemoryService Protocol exposes only 4 task/decision-skewed methods; `know`
supports generic atom CRUD but nowu's contracts don't expose it. Full integration requires
K3/W19 work not budgeted in this 8h intake.

### Decision

Use Option A: Artifact-Only Validation (Pre-Integration Proof). Represent AP knowledge
using existing workflow artifact structures. Document gaps with traceability to follow-on
work items (K3, K9, K13, W19, W20). No protocol changes, no source code changes.

### Consequences

- **Good**: Strongest T5 evidence — proves flow is domain-agnostic at artifact level
- **Good**: Lowest scope risk; 6h effort within 8h appetite
- **Good**: Gap register provides honest roadmap input for K3/W19/K9
- **Bad**: AP-01 dependency traversal and AP-02 version comparisons remain conceptual
- **Bad**: No executable integration proof against know atom APIs in this cycle

### Tradeoff Accepted

Simplicity and migration safety over near-term query/performance realism. AP knowledge
representability is proven; executable integration deferred to K3/W19.

### Review Trigger

After K3 implementation — verify that gap register items are addressed.

---

## D-028 — RE Domain Comparative Bootstrap and Gap Classification

**Date**: 2026-05-15 | **Status**: ACCEPTED | **Level**: system
**Intake**: intake-008 (W28) | **Use Cases**: RE-01, RE-06
**Epistemic Grade**: HYPOTHESIS
**Builds on**: D-027

### Context

W27 delivered AP-domain evidence and documented GAP-001..007 but did not establish whether
those gaps are AP-specific or cross-domain systemic. ROADMAP-004 positions W28 as the second
domain validation (RE-01/RE-06) to classify each gap using comparative evidence.

### Decision

Execute W28 as an artifact-only comparative validation run:
1. Produce RE-01 process inventory evidence and RE-06 decision-tracking evidence.
2. Classify GAP-001..007 using the rule: **systemic** if equivalent structural impact appears
   in ≥2 domains (AP and RE), otherwise **domain-specific**.
3. Do not change `src/` or `tests/`; all outputs remain in `state/` and roadmap/session artifacts.

### Consequences

- **Good**: Produces an explicit cross-domain confidence signal for K3/W19/W20/K9 prioritization.
- **Good**: Preserves scope discipline and comparability with W27.
- **Bad**: Still no executable integration proof for contract/runtime surfaces.

### Tradeoff Accepted

Classification rigor and traceability over implementation breadth in this cycle.

### Review Trigger

After K3 and W19 implementation work begins, re-evaluate this classification against runtime evidence.
