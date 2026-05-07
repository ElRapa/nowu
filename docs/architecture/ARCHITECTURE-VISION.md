---
artifact_type: ARCHITECTURE_VISION
altitude: ARCHITECTURE
phase: ANALYSIS
grade: HYPOTHESIS
created_at: 2026-05-06
source_themes: [T1, T2, T3, T4, T5, T6, T7, T8, T9]
source_synthesis: SYNTHESIS-001
source_goals: [goal-001, goal-002, goal-003, goal-004]
status: DRAFT
---

# Architecture Vision: nowu

> **Grade: HYPOTHESIS** — Derived from SYNTHESIS-001 theme analysis. Will be refined
> through S1-S9 feedback cycles. Not binding until promoted to EVIDENCE_BASED via
> successful implementation and review.

---

## 1. System Classification

**nowu is an AI-native project operating environment.**

Not a framework (you don't install it into another project).
Not a runtime (it doesn't execute user code).
Not a platform (others don't yet build apps on it).
Not a tool (it doesn't do one thing).

It is an **operating environment** — analogous to how an OS provides memory management,
process scheduling, filesystem, and I/O to applications. nowu provides:

| OS Concept | nowu Equivalent | Module |
|---|---|---|
| Memory management | Knowledge persistence & lifecycle (T2) | `know` |
| Process scheduling | Workflow orchestration (T3) | `flow` |
| Filesystem | Artifact-based state (D-001) | `core` |
| User interface | Multi-surface access (T7) | `bridge` |
| Security/permissions | Epistemic grades + approval tiers (T4, T3) | `core`/`flow` |
| Device drivers | Domain adapters (T5) | project config |

**Key distinction:** Unlike a traditional OS, nowu's "processes" are not user programs —
they are specialized AI agents with defined cognitive roles. And its "memory" is not
passive storage — it is a managed knowledge graph with active lifecycle (decay,
verification, contradiction detection).

**Open question (for ADR-0011):** The OS analogy is missing a kernel/user space boundary.
Framework modules (`core`, `flow`, `soul`, `know`, `bridge`) are kernel space. But where
does project-specific state live? Initial hypothesis: each project gets an isolated state
directory and knowledge scope — `know` manages memory for both framework and projects, like
an OS kernel manages memory for itself and user processes. This needs to be resolved when
the Domain Extension Model (ADR-0011) is written.

**System identity statement:**

> nowu is the operating environment for AI-native project work. It provides continuity,
> orchestration, knowledge management, and quality assurance to any number of projects
> across any domain — so that ideas become outcomes through a disciplined, compounding
> process rather than a series of disconnected sessions.

---

## 2. Architectural Principles

Five principles derived from SYNTHESIS-001 theme evidence. These are not aspirational —
each is grounded in specific UCs and themes that REQUIRE the principle to be true.

---

### P1: Knowledge is typed, graded, and alive

**Source:** T2 (17+ UCs), T4 (10+ UCs)

Every piece of information in the system has:
- A **type** (what kind of thing it is)
- A **grade** (how much to trust it — 5-level epistemic scale)
- A **lifecycle** (it was born, it may be verified, it will age, it may die)

This is not "add metadata to files." This is the commitment that **there is no raw,
untyped, ungraded data in the system.** A captured thought (PK-01) has type `raw_capture`
and grade `SPECULATION`. A verified ADR has type `decision` and grade `EVIDENCE_BASED`.
Both are first-class atoms.

**Why this must be true:** Without it, PK-04 (decay) cannot know what to clean. NF-15
(epistemic grades) has nothing to assign. XP-04 (conflict resolution) cannot compare
authority. AP-01 (regulatory tracking) cannot distinguish "verified current" from
"probably still valid." The system would accumulate undifferentiated noise.

**Architectural consequence:** The `know` atom schema is THE foundational design decision.
ADR-0008 must be written first.

---

### P2: Artifacts are the interface, state is explicit

**Source:** T1 (7+ UCs), T3 (8+ UCs), Vision Principle #0

Agents communicate through structured, version-controlled files — not conversations,
not in-memory state, not function calls. A broken artifact breaks the pipeline visibly.
A broken conversation fails silently.

**Extension from SYNTHESIS:** This principle, already stated in the vision, gains
architectural weight from T1 (continuity). Continuity IS the consequence of explicit
state. If state is only in memory or conversation, it dies with the session. If state
is an artifact, it survives anything.

**Architectural consequence:** Every workflow step (S1-S9) produces a named, typed,
findable artifact. The orchestrator (flow) routes by reading artifacts, not by
remembering what happened. Session recovery (NF-01) reads artifacts, not transcripts.

---

### P3: Core is domain-neutral and surface-neutral

**Source:** T5 (16+ UCs), T7 (7+ UCs)

The framework core (`core`, `flow`, `soul`) knows nothing about:
- Food regulation, property lifecycles, or software architecture (domain)
- CLI terminals, mobile phones, or voice interfaces (surface)
- Filipino excise tax, real estate valuation, or pili-nut processing (content)

Domain behavior is project configuration. Surface behavior is adapter configuration.
The core provides: orchestration, knowledge management, quality gates, and continuity.
Domains and surfaces plug in.

**Why this must be true:** 14 of 50 UCs are from non-software domains (AP, RE). If the
framework is software-specific, those UCs are architecturally impossible. Similarly, PK-08
requires mobile/voice access — if the framework is CLI-specific, it fails its own vision.

**Architectural consequence:** `bridge` (interface adapters) and project config (domain
customization) are the extension points. Core modules never reference domain-specific
types or surface-specific APIs.

---

### P4: Every action is sequenced, verified, and traceable

**Source:** T3 (8+ UCs), T6 (8+ UCs)

Nothing moves through the system without:
1. Being **sequenced** — it happens at a named workflow step
2. Being **verified** — it passes quality gates before advancing
3. Being **traceable** — it links back to the UC/goal that justifies its existence

**Why this must be true:** NF-04 (VBR) requires verification before "done." NF-09
requires traceability to UCs. NF-05 requires approval routing. Without all three,
the system devolves into unaccountable, unauditable, untraceable activity — and the
human cannot trust that things are actually correct.

**Architectural consequence:** The orchestration protocol (ADR-0009) must define the
handoff contract between steps. Every artifact carries `validation_trace`. VBR is
not optional — it's a pipeline gate.

---

### P5: Uncertainty is first-class

**Source:** T4 (10+ UCs), T8 (7+ UCs)

The system explicitly represents and manages uncertainty:
- "I don't know" (SPECULATION) is a valid state
- Vagueness at entry is normal (NF-12, PK-01)
- Certainty is earned through process (HYPOTHESIS → EVIDENCE_BASED → VERIFIED_FACT)
- The system actively monitors for confidence degradation (drift, staleness, contradiction)

**Why this must be true:** Without explicit uncertainty, every output looks equally
trustworthy. The human acts on HYPOTHESIS as if it were VERIFIED_FACT (NF-15 failure
scenario). Decisions are made on ungraded inputs. Knowledge accumulates without anyone
knowing what to trust.

**Architectural consequence:** Grade is a mandatory field on every significant artifact.
Propagation rules determine how uncertainty compounds. The system prefers "explicitly
uncertain" over "implicitly confident."

---

## 3. Quality Attribute Priorities

Ranked by importance. Explicit tradeoffs stated.

| Rank | Quality Attribute | Trades Off Against | Justification |
|------|------------------|-------------------|---------------|
| 1 | **Continuity** | Performance | "Never lose state" > "respond fast." Session state, decisions, knowledge must survive any failure. XP-05 (performance) is v2; NF-01 (continuity) is v1-core. |
| 2 | **Correctness** | Speed | "Right answer with grade" > "fast answer without context." VBR exists because speed without verification is worse than waiting. NF-04, NF-15. |
| 3 | **Inspectability** | Convenience | Every artifact must be readable by humans without nowu running. Markdown + YAML, not proprietary formats. D-001, XP-08. |
| 4 | **Flexibility** | Optimization | Domain-neutral core > domain-optimized code. Generic orchestration > custom pipelines per domain. NF-07, XP-07. |
| 5 | **Safety** | Throughput | Tiered approvals may slow things, but prevent bad changes. A Tier 3 gate that blocks for 2 hours is better than an unchecked breaking change. NF-05. |
| 6 | **Usability** | Feature richness | "If it feels like bureaucracy, we built it wrong." Fewer features done well > many features that add overhead. Vision "What We Are NOT" #2. |

### Tradeoff Statements (Binding)

- We will sacrifice query performance to preserve knowledge atom integrity.
- We will sacrifice throughput to enforce verification gates.
- We will sacrifice domain-specific optimization to maintain framework generality.
- We will sacrifice feature completeness to maintain low friction for the human.
- We will sacrifice automation coverage to preserve meaningful human checkpoints.

---

## 4. Key Risks

| # | Risk | Source Theme | Impact | Mitigation Strategy |
|---|------|-------------|--------|-------------------|
| R1 | **Knowledge model over-engineering** | T2 | Schema so complex nothing gets built. Analysis paralysis on atom design. | Start with minimal viable schema. ADR-0008 at HYPOTHESIS grade — evolve through implementation feedback. |
| R2 | **Epistemic grade bureaucracy** | T4 | Every artifact needs a grade with justification → system becomes its own overhead. Violates "if it feels like bureaucracy." | Default grades for routine outputs. Human-assigned grades only for EVIDENCE_BASED and above. Agents assign up to INFORMED_ESTIMATE autonomously. |
| R3 | **Domain abstraction gap** | T5 | AP/RE UCs need supply chains, property lifecycles, regulatory tracking — highly specific needs that may not fit a generic model. | Validate abstraction with REAL domain UCs before claiming generality. If AP-03 can't work in the generic model, the model is wrong. |
| R4 | **Multi-surface fragmentation** | T7 | CLI + mobile + voice + web fragments attention. Delivers none well. | Sequence strictly: CLI first (v1-core), then ONE additional surface (v1). Don't attempt all simultaneously. |
| R5 | **Orchestration rigidity** | T3 | S1-S9 as strict sequence forces creative work into bureaucratic pipeline. Kills NF-12 (vague exploration). | Pre-workflow (P0-P4) IS the "flexible" zone. S1-S9 applies only AFTER commitment. Keep exploration explicitly outside the pipeline. |
| R6 | **Continuity overhead** | T1 | Checkpoint writes on every action slow everything down. State persistence becomes the bottleneck. | Checkpoint at step boundaries (S1→S2, S5→S6), not on every operation. Recovery tolerates losing in-step progress (just re-run the step). |
| R7 | **Vision vs. reality gap** | T6, NF-11 | Architecture designed for 50 UCs when only 5-10 will be implemented in v1-core. Over-investment in infrastructure. | Implement themes progressively: only what v1-core UCs REQUIRE gets built now. ADRs are HYPOTHESIS — validated by building, not by theorizing. |

---

## 5. ADR Roadmap

From SYNTHESIS-001, ordered by dependency and v1-core relevance:

### Immediate (Required for first S1-S9 end-to-end — W3/W4)

| ADR | Title | Theme | Why Now |
|-----|-------|-------|---------|
| ADR-0008 | Knowledge Atom Model & Lifecycle | T2 | Foundation — everything else depends on the atom schema |
| ADR-0010 | Epistemic Grade Assignment & Propagation | T4 | Pervasive — every artifact carries grades |
| ADR-0007 | Session Continuity Protocol | T1 | NF-01 is v1-core — first intake needs recovery protocol |
| ADR-0009 | Orchestration Protocol & Agent Handoff Contract | T3 | S1-S9 needs typed interfaces between steps |

### Near-term (Required before v1.1 — after first S1-S9 validates foundation)

| ADR | Title | Theme | Why This Phase |
|-----|-------|-------|---------------|
| ADR-0011 | Domain Extension Model | T5 | AP/RE dogfooding in v1 will reveal extension needs |
| ADR-0012 | Traceability Metadata Standard | T6 | NF-09 (v1-core) needs this, but format can iterate |
| ADR-0014 | Artifact Maturity & Progressive Enrichment | T8 | NF-12 (v1-core) needs vague-mode, but protocol can iterate |

### Deferred (Required for v1.1+ — validate foundation first)

| ADR | Title | Theme | Why Defer |
|-----|-------|-------|-----------|
| ADR-0013 | Interface Adapter Architecture | T7 | PK-08 is v1, not v1-core. CLI-first. |
| ADR-0015 | Consumer-Aware Knowledge Rendering | T9 | XP-11 is v1.1. Rendering layer can wait for atom model. |

---

## 6. Relationship to Existing Architecture

This vision does NOT contradict existing decisions. It EXTENDS them:

| Existing | Relationship to This Vision |
|----------|---------------------------|
| D-001 (File-based memory) | Storage mechanism confirmed. This vision adds: atom schema, lifecycle, grades ON TOP of file-based storage. |
| D-002 (DDD layers) | Confirmed and strengthened. Domain neutrality (P3) IS DDD's domain independence. |
| D-003 (5-module structure) | Confirmed. Module responsibilities align to themes: core=contracts, flow=T3, bridge=T7, soul=identity, know=T2. |
| D-005 (Dedicated agent per step) | Confirmed. P4 (sequenced, verified, traceable) requires this. |
| ADR-0001 (Import boundaries) | Confirmed. P3 (core is neutral) requires strict boundaries. |
| ADR-0006 (soul↔flow via filesystem) | Confirmed. P2 (artifacts are the interface) is the generalization of this. |

---

## Summary

nowu is an AI-native project operating environment. Its architecture is driven by 9
cross-cutting themes extracted from 50 use cases. The 5 architectural principles
(typed/graded knowledge, explicit state, neutral core, verified actions, first-class
uncertainty) determine every structural decision.

The critical path to first implementation:
1. **ADR-0008** (atom model) — unlocks T2, T4, T5, T8, T9
2. **ADR-0010** (epistemic grades) — unlocks T4 pervasively
3. **ADR-0007** (continuity) — unlocks T1, enables NF-01
4. **ADR-0009** (orchestration) — unlocks T3, enables first S1-S9

With these four ADRs at HYPOTHESIS grade, the first end-to-end S1-S9 cycle can run
against real work — and the hypotheses will either validate or fail. That's how this
architecture earns its way from HYPOTHESIS to EVIDENCE_BASED.
