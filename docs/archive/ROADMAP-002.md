---
superseded_by: docs/ROADMAP-003.md
artifact_type: ROADMAP
version: 2
altitude: STRATEGIC
phase: IMPLEMENTATION
epistemic_grade: INFORMED_ESTIMATE
created_at: 2026-05-10
updated_at: 2026-05-10
source_synthesis: SYNTHESIS-001
source_vision: ARCHITECTURE-VISION
supersedes: ROADMAP-001
status: SUPERSEDED
decisions: [D-013 through D-022]
---

> **⚠️ SUPERSEDED** — This roadmap has been superseded by `docs/ROADMAP-003.md` (version 3).
> Refer to ROADMAP-003 for current project status and work items.
> This file is retained as historical reference.

# nowu Implementation Roadmap v2

> Areas × Stages. Each cell is independently actionable.
> Dependencies are explicit. No cell assumes another is complete unless stated.

---

## How to Read This Plan

**Areas** = independent workstreams that can progress in parallel (within stage constraints).
**Stages** = maturity gates. A stage is complete when ALL its area-cells are done.
**Dependencies** = explicit blockers. A cell cannot start until its dependencies are met.

### Areas

| Area | Scope | Primary Module |
|---|---|---|
| **Workflow** | 5×10 model, SYNTHESIS, traversals, phases | `flow/` + `docs/` + `state/` |
| **Knowledge** | Memory, traceability, artifact management | `know/` + `core/contracts/` |
| **Agents** | Agent definitions, orchestration, routing | `.claude/agents/` + `flow/` |
| **Framework** | Runtime, contracts, CLI, quality gates | `core/` + `bridge/` + `soul/` |

### Stages

| Stage | Label | Gate |
|---|---|---|
| **v1-core** | Bootstrap | First S1-S9 intake completes end-to-end |
| **v1** | Viable Workflow | 5+ intakes completed, epistemic enforcement active |
| **v1.1** | Reliable | Health metrics, fitness functions, wider dogfooding |
| **v1.2** | Domain Operational | AP/RE domain projects fully operational |
| **v2** | Framework Product | Installable, external projects, multi-traversal |

---

## Evidence Integration (ROADMAP-002 Changelog)

This roadmap version integrates both required milestone artifacts:

- **SYNTHESIS-001** (themes + ADR recommendations + dependency ordering)
  - Source sections: Themes (§32-45), interaction/dependency graph (§530-563), ADR recommendations (§566-600).
- **ARCHITECTURE-VISION** (quality priorities + risk register + ADR phasing)
  - Source sections: quality attributes (§177-197), risks (§200-211), ADR roadmap (§214-241).

### Epistemic Grade Promotion Basis

Roadmap epistemic grade remains/promotes at **INFORMED_ESTIMATE** with stronger evidence basis:
- Cross-UC synthesis complete (all 50 UCs clustered into 9 themes).
- System principles, quality tradeoffs, and risk mitigations explicitly defined.
- ADR roadmap and dependencies specified across immediate/near-term/deferred windows.

---

## Architecture Vision Integration

### Quality Attribute Priorities (Ranked)

Imported from `ARCHITECTURE-VISION.md` §3 and now used for stage-gate interpretation:

| Rank | Quality Attribute | Tradeoff | Stage Gate Impact |
|---|---|---|---|
| 1 | Continuity | Performance | v1-core cannot pass if restart/orientation reliability is weak even if runtime is slower |
| 2 | Correctness | Speed | VBR and epistemic-grade integrity are mandatory before throughput optimization |
| 3 | Inspectability | Convenience | Artifacts must remain human-readable/auditable; no opaque state channels |
| 4 | Flexibility | Optimization | Domain/surface neutrality preferred over short-term domain-specific optimization |
| 5 | Safety | Throughput | Approval tiers can slow flow; unsafe acceleration is disallowed |
| 6 | Usability | Feature richness | Keep workflow low-friction; defer complexity that creates bureaucracy |

### Risk Register (R1-R7) with Mitigation

Imported from `ARCHITECTURE-VISION.md` §4 and tied to roadmap execution:

| Risk | Description | Stage Exposure | Mitigation Strategy | Owner Work Items |
|---|---|---|---|---|
| R1 | Knowledge model over-engineering | v1-core | Keep ADR-0008 minimal at HYPOTHESIS, refine via W4 feedback | W4, W9, K3 |
| R2 | Epistemic grade bureaucracy | v1-core/v1 | Default grades for routine outputs; human grading for high grades only | W6 (v1), W8, W9 |
| R3 | Domain abstraction gap | v1+ | Validate with AP/RE real UCs before claiming generality | W4, W15, W19 |
| R4 | Multi-surface fragmentation | v1 | Sequence CLI-first, then one additional interface | F6, W22 |
| R5 | Orchestration rigidity | v1-core/v1 | Keep P0-P4 as flexible pre-commit zone, S1-S9 after commitment | W4, W10, W15 |
| R6 | Continuity overhead | v1-core | Persist at workflow boundaries, not every operation | W4, F4 |
| R7 | Vision vs reality overbuild | all | Build only what active stage UCs require; treat ADRs as hypotheses | W4, W9, roadmap stage gates |

---

## SYNTHESIS Integration

### Theme Coverage by Roadmap Areas

Mapped from `SYNTHESIS-001.md` §32-45 and theme sections T1..T9:

| Theme | Primary Area | Supporting Areas | Stage Focus |
|---|---|---|---|
| T1 Continuity | Workflow | Knowledge, Framework | v1-core → v1 |
| T2 Knowledge Persistence & Lifecycle | Knowledge | Framework, Agents | v1-core → v1.1 |
| T3 Workflow Orchestration | Workflow | Agents, Framework | v1-core → v1 |
| T4 Epistemic Awareness | Workflow | Knowledge, Agents | v1-core → v1.1 |
| T5 Domain Agnosticism | Framework | Workflow, Knowledge | v1 → v2 |
| T6 Observability & Traceability | Workflow | Knowledge, Agents | v1-core → v1.1 |
| T7 Multi-Surface Access | Framework | Workflow, Agents | v1 → v1.1 |
| T8 Progressive Disclosure | Workflow | Knowledge, Agents | v1-core → v1.1 |
| T9 Audience-Aware Rendering | Framework | Knowledge, Agents | v1.1 → v2 |

### ADR Roadmap (ADR-0007..0015) with Dependency Ordering

Integrated from SYNTHESIS §552-600 + Architecture Vision §214-241.

**Dependency chain (authoritative for planning):**

`ADR-0008 → (ADR-0010 || ADR-0007) → ADR-0009 → ADR-0011 → (ADR-0012 || ADR-0014) → ADR-0013 → ADR-0015`

| ADR | Title | Theme | Phase | Depends On | Roadmap Work Item |
|---|---|---|---|---|---|
| ADR-0008 | Knowledge Atom Model & Lifecycle | T2 | Immediate (done) | — | W3 ✅ |
| ADR-0010 | Epistemic Grade Assignment & Propagation | T4 | Immediate (done) | ADR-0008 | W3 ✅ |
| ADR-0007 | Session Continuity Protocol | T1 | Immediate (done) | ADR-0008 | W3 ✅ |
| ADR-0009 | Orchestration Protocol & Agent Handoff Contract | T3 | Immediate (done) | ADR-0007 + ADR-0010 | W3 ✅ |
| ADR-0011 | Domain Extension Model | T5 | Near-term | ADR-0008 + ADR-0009 | **W19** |
| ADR-0012 | Traceability Metadata Standard | T6 | Near-term | ADR-0009 | **W20** |
| ADR-0014 | Artifact Maturity & Progressive Enrichment | T8 | Near-term | ADR-0008 + ADR-0010 | **W21** |
| ADR-0013 | Interface Adapter Architecture | T7 | Deferred (v1.1+) | ADR-0011 + ADR-0012 + ADR-0014 | **W22** |
| ADR-0015 | Consumer-Aware Knowledge Rendering | T9 | Deferred (v1.1+) | ADR-0013 + ADR-0008 + ADR-0010 | **W23** |

---

## Artifact Landscape

This roadmap is an **implementation task tracker** derived from a larger body of upstream
artifacts. These are the foundational documents that give the roadmap its shape and context.

### Strategic Artifacts (APPROVED / ACCEPTED — stable)

| Artifact | Path | Status | What It Provides |
|---|---|---|---|
| Vision | `docs/vision.md` | APPROVED (v2.0, 2026-03-31) | Product identity, personas, success horizons, principles |
| Goals | `docs/goals/goal-001..004.md` | ACCEPTED (2026-04-30, D-012) | Measurable success criteria per horizon |
| Use Cases | `docs/USE_CASES.md` | ACCEPTED (v2.5, 50 UCs) | Complete UC catalog with stage targets |

### Architecture Artifacts (HYPOTHESIS — evolving)

| Artifact | Path | Status | What It Provides |
|---|---|---|---|
| SYNTHESIS | `state/arch/SYNTHESIS-001.md` | DRAFT (2026-05-06) | 9 cross-cutting themes from 50 UCs |
| Architecture Vision | `docs/architecture/ARCHITECTURE-VISION.md` | DRAFT (2026-05-06) | System identity, 5 principles, quality attributes, ADR roadmap |
| ADR-0007..0010 | `docs/architecture/adr/` | HYPOTHESIS (2026-05-07) | Session continuity, atom model, orchestration, epistemic grades |
| ADR-0001..0006 | `docs/architecture/adr/` | ACCEPTED | Import boundaries, DDD, modules, TDD, know, soul↔flow |
| C4 L1 Context | `docs/architecture/context.md` | DRAFT | System boundary, external systems, stage boundaries |

### Pre-Workflow Artifacts (from P0-P4 run, 2026-04-08)

| Artifact | Path | Count | Status |
|---|---|---|---|
| Problems | `state/problems/problem-001..008.md` | 8 | Completed pre-workflow output |
| Epics | `state/epics/epic-v1core-001..004.md` | 4 | APPROVED |
| Stories | `state/stories/story-v1core-*.md` | 17 (16 APPROVED, 1 DRAFT deferred) | APPROVED |
| Ideas | `state/ideas/idea-001..007.md` | 7 | Mixed status |
| Discovery | `state/discovery/disc-v1core-research.md` | 1 | Completed |

### Operational Artifacts (living)

| Artifact | Path | Status | Notes |
|---|---|---|---|
| Decisions | `docs/DECISIONS.md` | D-001..D-022 | Binding. Updated as new decisions are made. |
| Session Log | `state/session-log.md` | ACTIVE (created 2026-05-10) | Running record of sessions, what happened, and why. |
| Learnings | `state/learnings/INDEX.md` | ACTIVE (7 entries) | Session learnings + recurring patterns. |
| Research | `docs/research/INDEX.md` | ACTIVE (13+ sessions) | Research session catalog with traceability to decisions. |

### Stale / Superseded Artifacts

| Artifact | Path | Superseded By | Action |
|---|---|---|---|
| PROGRESS.md | `state/PROGRESS.md` | This roadmap (D-020) | Marked SUPERSEDED. Refer to ROADMAP-003. |
| SESSION_STATE.md | `state/SESSION_STATE.md` | `state/session-log.md` | Template only — never populated with real data. |
| Health reports (March 2026) | `state/health/*.md` | Need re-run post-architecture rework | Stale — predate 5×10 model, SYNTHESIS, and ADRs. |
| V1_PLAN.md | `docs/archive/V1_PLAN.md` | This roadmap (D-020) | Archived. Framework steps mapped in §Relationship below. |

---

## Stage: v1-core — Bootstrap

**Objective:** Unblock S1-S9 by creating the missing architectural layer.

### Workflow (v1-core) — CRITICAL PATH

| # | Task | Deliverable | Depends On | Status |
|---|---|---|---|---|
| W1 | Manual SYNTHESIS on approved UCs | `state/arch/SYNTHESIS-001.md` — 9 themes + ADR recommendations | Approved UCs exist ✅ | ✅ DONE (2026-05-06) |
| W2 | Architecture Vision | `docs/architecture/ARCHITECTURE-VISION.md` — system identity, principles, quality attributes | W1 | ✅ DONE (2026-05-06) |
| W3 | Hypothesis ADRs from SYNTHESIS themes | ADR-0007, ADR-0008, ADR-0009, ADR-0010 at HYPOTHESIS grade | W1 + W2 | ✅ DONE (2026-05-07) |
| W3.5 | Minimal fitness functions for hypothesis ADRs | Python checks validating ADR-0008 atom schema presence + ADR-0001 import boundaries | W3 | ✅ DONE (2026-05-07) |
| W4 | First S1-S9 intake (end-to-end) | Complete state/intake/ → state/tasks/ → implementation → capture cycle | W3.5 | ⬜ NEXT |
| W5 | Validate 5×10 coordinates on W4 artifacts | Annotate all artifacts from W4 with altitude + phase | W4 | ⬜ BLOCKED (W4) |
| W6 | 5×10 model refactoring: agents into grid | Top-down re-articulation of 5×10 model. Map ALL agents (execution + orchestrator + pre-workflow) into altitude×phase grid. Update MODEL-REFERENCE.md, WORKFLOW.md, PRE-WORKFLOW.md, AGENTS.md. See `docs/research/sessions/2026-06-10_2_perplexity_refactor-5x10-workflow-proposal.md` for analysis. | W4 (need empirical validation first) | ⬜ BLOCKED (W4) |
| W-orch | Orchestrator layer formalized (D-022) | 3 meta-agents (roadmap-creator, roadmap-updater, work-scheduler) + ROADMAP-NNN versioned artifact. Orchestrator sits outside 5×10 grid. | W3 | ✅ DONE (2026-05-09) |
| W-log | Session log + roadmap alignment | Create session-log, update roadmap with artifact landscape, mark stale state files. See `docs/research/sessions/2026-06-10_3_perplexity_roadmap-session-log-proposal.md`. | — | ✅ DONE (2026-05-10) |

**Unblocking chain:** ~~W1~~ → ~~W2~~ → ~~W3~~ → ~~W3.5~~ → **W4** → W5 → W6

**Current state:** W1-W3.5 + W-orch + W-log complete. Next: **W4** — first S1-S9 intake end-to-end. W6 (5×10 refactoring) is blocked on W4 empirical validation.

### Knowledge (v1-core)

| # | Task | Deliverable | Depends On | Grade |
|---|---|---|---|---|
| K1 | Traceability metadata in all new artifacts | `source_goal`, `source_uc`, `source_themes`, `architectural_decisions` in YAML frontmatter | — | EVIDENCE_BASED |
| K2 | Forward/backward trace validation | Manual check: GOAL → UC → ADR → SESSION path works | W4 | HYPOTHESIS |

**Current state:** K1 is immediately actionable — just requires discipline in frontmatter. Already specified in D-WF-013.

### Agents (v1-core)

| # | Task | Deliverable | Depends On | Grade |
|---|---|---|---|---|
| A1 | Existing 19 agents operate as-is | No changes needed — agents are altitude-agnostic executors | — | — |
| A2 | Router assigns altitude metadata to intakes | Intake brief includes `altitude: DELIVERY`, agent prompts receive it | W4 | HYPOTHESIS |

**Current state:** Agents exist. A1 is "do nothing" — just validate they still work during W4.

### Framework (v1-core)

| # | Task | Deliverable | Depends On | Grade |
|---|---|---|---|---|
| F1 | Contracts baseline | ✅ Done (Step 01 complete) | — | EVIDENCE_BASED |
| F2 | Boundary enforcement test | ✅ Done (`tests/architecture/test_import_boundaries.py`) | — | EVIDENCE_BASED |
| F3 | Level 0 artifact verification script | Validate YAML frontmatter syntax on commit | — | HYPOTHESIS |

**Current state:** F1 + F2 are done. F3 exists in the implementation package (`verification/verify-artifact.py`) but not yet integrated into the repo.

---

## Stage: v1 — Viable Workflow

**Objective:** 5+ intakes complete. Epistemic grades enforced at gates. SYNTHESIS triggers automatically.

**Gate:** Cannot enter v1 until v1-core gate passes (first S1-S9 end-to-end).

### Workflow (v1)

| # | Task | Depends On |
|---|---|---|
| W6 | Calibrate epistemic thresholds from v1-core intakes (OQ-2) | W4 + W5 |
| W7 | SYNTHESIS trigger automation (D-WF-008: ≥2 UCs with architectural implications) | W1 manual version validated |
| W8 | Level 1 enforcement: advisory warnings for altitude/grade violations | W6 thresholds calibrated |
| W9 | Promote hypothesis ADRs to INFORMED_ESTIMATE (after 2+ intakes validate them) | 2+ intakes complete |
| W10 | Triage primitive design (D-WF-010) | W4 validates the gap empirically |
| W19 | ADR-0011 (Domain Extension Model) drafted and reviewed at HYPOTHESIS | ADR-0008 + ADR-0009 + AP/RE v1 dogfooding signals |
| W20 | ADR-0012 (Traceability Metadata Standard) drafted and adopted in S5/S8 templates | ADR-0009 + K1 baseline |
| W21 | ADR-0014 (Artifact Maturity & Progressive Enrichment) drafted for vague→structured flow | ADR-0008 + ADR-0010 + NF-12 learning from W4 |

### Knowledge (v1)

| # | Task | Depends On |
|---|---|---|
| K3 | MemoryService integration for structured recall (V1_PLAN Step 02) | core/contracts/memory.py exists ✅ |
| K4 | Session state persistence via know module (V1_PLAN Step 03) | K3 |

### Agents (v1)

| # | Task | Depends On |
|---|---|---|
| A3 | Orchestrator with altitude routing logic | W5 validates coordinate system |
| A4 | Agent skill files encode altitude behavior (not agent self-awareness) | A3 |
| A5 | SYNTHESIS agent (altitude-aware, ARCHITECTURE-locked) | W7 trigger works |

### Framework (v1)

| # | Task | Depends On |
|---|---|---|
| F4 | Session runtime + WAL (V1_PLAN Step 03) | K3 |
| F5 | Role sequencer (V1_PLAN Step 04) | F4 |
| F6 | Bridge CLI + approval routing (V1_PLAN Step 05) | F5 |

---

## Stage: v1.1 — Reliable

**Objective:** Health monitoring, fitness functions, automated quality feedback loops.

### Workflow (v1.1)

| # | Task | Depends On |
|---|---|---|
| W11 | Level 2 enforcement: blocking at DECISION gates below aspirational grade | W8 Level 1 stable |
| W12 | Fitness functions for architectural guardrails (D-WF-012) | ADRs at INFORMED_ESTIMATE+ |
| W13 | ADR amendment workflow (non-breaking contract evolution) | W12 |
| W14 | Grade promotion workflows (HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED) | W9 manual promotion validated |
| W15 | Alternative traversal support (bug fix path, spike path) | 5+ S1-S9 intakes reveal patterns |
| W22 | ADR-0013 (Interface Adapter Architecture) drafted and validated against first non-CLI adapter | W19 + W20 + W21 + PK-08 implementation evidence |
| W23 | ADR-0015 (Consumer-Aware Knowledge Rendering) drafted for role-aware read paths | W22 + XP-11 + PK-09/RE-07 evidence |

### Knowledge (v1.1)

| # | Task | Depends On |
|---|---|---|
| K5 | Cross-project recall via know | K4 + at least 1 non-nowu project |
| K6 | Semantic queries over artifact corpus | K5 |

### Agents (v1.1)

| # | Task | Depends On |
|---|---|---|
| A6 | GAP reflective agent (altitude-aware, cross-altitude pattern detection) | A3 orchestrator stable |
| A7 | Health monitoring agents (soul module integration) | W12 fitness functions exist |

### Framework (v1.1)

| # | Task | Depends On |
|---|---|---|
| F7 | Project bootstrap command (V1_PLAN Step 07) | F6 |
| F8 | Learning + curation loop (V1_PLAN Step 06) | K4 + A6 |
| F9 | Health metrics dashboard (soul → bridge surface) | A7 |

---

## Stage: v1.2 — Domain Operational

**Objective:** AP and RE projects run as operational systems with domain depth and role-aware collaboration outputs.

### Workflow (v1.2)

| # | Task | Depends On |
|---|---|---|
| W24 | AP/RE domain deepening plan execution (AP-03/05/07 + RE-02/03/04/07) | W19 domain extension model |
| W25 | Domain-level milestone/dependency tracking operationalized | W24 + K6 |
| W26 | Role-scoped collaborator onboarding/reporting workflows stabilized | W23 + W24 |

### Knowledge (v1.2)

| # | Task | Depends On |
|---|---|---|
| K9 | Domain-specific atom-type extension packs validated in AP and RE | W19 + K6 |
| K10 | Cross-domain contradiction and dependency views for operational projects | K9 + W25 |

### Agents (v1.2)

| # | Task | Depends On |
|---|---|---|
| A10 | Domain briefing agent patterns for collaborator onboarding | W26 |
| A11 | Domain risk/operations analyst loops (AP/RE) | W25 + K10 |

### Framework (v1.2)

| # | Task | Depends On |
|---|---|---|
| F12 | Domain-capability matrix surfaced in bridge layer | W24 + W26 |
| F13 | Operational report export presets for AP/RE stakeholder types | W26 + W23 |

---

## Stage: v2 — Framework Product

**Objective:** Installable package. External project support. Autonomous workflow selection.

### Workflow (v2)

| # | Task | Depends On |
|---|---|---|
| W16 | Level 3 enforcement: circuit breaker for altitude violations | W11 Level 2 stable |
| W17 | Multi-traversal selection (workflow recommends traversal based on intake type) | W15 patterns catalogued |
| W18 | 5×10 grid auto-population (discover which cells are primary/secondary/rare from data) | 20+ intakes with coordinate annotations |

### Knowledge (v2)

| # | Task | Depends On |
|---|---|---|
| K7 | Graph-based knowledge (if >1000 artifacts) | K6 |
| K8 | Automated knowledge curation | F8 curation loop stable |

### Agents (v2)

| # | Task | Depends On |
|---|---|---|
| A8 | LangGraph orchestration (checkpointing, approval gates) | A3 + F5 stable |
| A9 | Agent optimization (AFLOW-inspired, if applicable) | A8 + 50+ intakes for training data |

### Framework (v2)

| # | Task | Depends On |
|---|---|---|
| F10 | Installable package with public docs | F7 + all v1.1 gates |
| F11 | Multi-user / external project support | F10 |

---

## UC Coverage Matrix (All 50 UCs)

Each UC is mapped to explicit roadmap stage + work item(s).

| UC | Stage | Primary Roadmap Coverage |
|---|---|---|
| NF-01 | v1-core | W4, ADR-0007, F4 |
| NF-02 | v1-core | W4, W9, ADR-0009 |
| NF-03 | v1-core | W4, W10 |
| NF-04 | v1-core | W4, W12 |
| NF-05 | v1-core | W4, F6, W11 |
| NF-06 | v1-core | W4, F8 |
| NF-07 | v1-core | W4, F7 |
| NF-08 | v1.1 | A7, F9, W12 |
| NF-09 | v1-core | K1, K2, W20 |
| NF-10 | v1-core | W4, ADR-0007, K3/K4 |
| NF-11 | v1.1 | A6, F9, W14 |
| NF-12 | v1-core | W4, W21, W15 |
| NF-13 | v1-core | W4, W10 |
| NF-14 | v1.1 | A7, F9, W14 |
| NF-15 | v1-core | W4, W6(v1), W8, W9, ADR-0010 |
| NF-16 | v1 | W6(v1), W15, A6 |
| AP-01 | v1 | W19, K3/K4, W24 |
| AP-02 | v1 | W19, K9, W24 |
| AP-03 | v1.2 | W24, K9/K10, A11 |
| AP-04 | v1.1 | K5/K6, W14, W24 |
| AP-05 | v1.2 | W25, K10 |
| AP-06 | v1 | W9, W19, W20 |
| AP-07 | v1.2 | W26, A10, F13 |
| RE-01 | v1 | W19, W24 |
| RE-02 | v1.2 | W24, K9 |
| RE-03 | v1.2 | W24, K10 |
| RE-04 | v1.2 | W25, A11 |
| RE-05 | v2 | K8, W16, A9 |
| RE-06 | v1 | W19, W25 |
| RE-07 | v1.2 | W26, W23, F13 |
| PK-01 | v1-core | W4, W21 |
| PK-02 | v1.1 | K6, A6 |
| PK-03 | v1-core | W4, K3/K4 |
| PK-04 | v1.1 | K6, K8, W14 |
| PK-05 | v1.1 | W21, K6 |
| PK-06 | v1.1 | W19, W23 |
| PK-07 | v1.1 | K6, W23 |
| PK-08 | v1 | F6, W22 |
| PK-09 | v1.1 | K6, W23 |
| XP-01 | v1-core | K4, K5, W4 |
| XP-03 | v1.1 | A6, F8 |
| XP-04 | v1.1 | K6, K8, W14 |
| XP-05 | v2 | K7, K8 |
| XP-06 | v2 | A8, W17 |
| XP-07 | v2 | W19, F10/F11 |
| XP-08 | v1.1 | F9, F13 |
| XP-09 | v2 | F10, F11 |
| XP-10 | v2 | F11, A8/A9 |
| XP-11 | v1.1 | W23, F13 |

---

## Goal Traceability (All 4 Goals)

Mapped from `docs/goals/goal-001..004.md` plus SYNTHESIS primary-goal mapping.

| Goal | Primary Themes | Roadmap Areas/Items that Advance It |
|---|---|---|
| goal-001 — continuity compounds | T1, T2, T4 | W4, W9, K3/K4, ADR-0007, ADR-0008, W21 |
| goal-002 — AI-led low-friction workflow | T3, T6, T8, T7 | W4→W10, W12/W15, W20, W21, W22, A3/A5/A7, F6/F9 |
| goal-003 — durable compounding knowledge | T2, T4, T6, T9 | K3→K8, W20, W23, ADR-0008/0010/0015, XP-oriented v1.1+ items |
| goal-004 — trusted shippable infrastructure | T5, T7, T9, T3 | W19, W22, W23, F10/F11, A8/A9, v1.2 operationalization |

---

## Theme Coverage by Stage

| Stage | Theme Coverage Focus |
|---|---|
| v1-core | T1 continuity, T2 atom foundation, T3 orchestration, T4 grades baseline, T6 traceability baseline, T8 vague→structured entry |
| v1 | T3 operational orchestration, T4 calibration/promotions, T5 domain extension start, T7 first non-CLI adapter prep |
| v1.1 | T6 observability/fitness loops, T8 maturation protocol, T7 adapter architecture, T9 rendering model |
| v1.2 | T5 domain operational depth (AP/RE), T9 audience-specific reporting, T6 cross-domain operational traceability |
| v2 | T5 full domain agnosticism at scale, T7 multi-surface maturity, T9 multi-consumer rendering/productization |

---

## What To Do Right Now

The critical path is **Workflow v1-core**: ~~W1~~ → ~~W2~~ → ~~W3~~ → ~~W3.5~~ → **W4** → W5 → W6.

**Completed since last update (2026-05-06 → 2026-05-10):**
- W-orch: Orchestrator layer formalized — 3 meta-agents, D-022 accepted (2026-05-09)
- W-log: Session log + roadmap alignment — artifact landscape, stale file cleanup (2026-05-10)
- Multiple research sessions (see `docs/research/INDEX.md`)
- Session learnings captured (see `state/learnings/INDEX.md`)

**Next session should execute W4:**
1. Select first intake for S1-S9 end-to-end (recommend NF-01 or a small NF UC)
2. Run full S1-S9 cycle using hypothesis ADRs as architectural context
3. Capture session learnings — validate or refine ADR hypotheses

**After W4, consider W6 (5×10 refactoring):**
1. Use W4 experience to validate which altitudes/phases are actually used
2. Map all agents (execution, orchestrator, pre-workflow) into the grid
3. Update MODEL-REFERENCE.md as the source of truth for the refined model

---

## Relationship to V1_PLAN.md

The existing `docs/V1_PLAN.md` Steps 01-07 map to Framework cells:
- Step 01 → F1 + F2 (✅ done)
- Step 02 → K3
- Step 03 → F4 + K4
- Step 04 → F5
- Step 05 → F6
- Step 06 → F8
- Step 07 → F7

This plan adds the **Workflow** and **Agents** areas that V1_PLAN didn't cover, and makes the **Knowledge** area explicit. The Framework steps are preserved but now have explicit dependencies on Workflow progress.

---

## Roadmap-Updater Quality Self-Check (Completed)

- [x] Version number incremented correctly (v2 → v3 file as ROADMAP-002)
- [x] `supersedes` points to previous roadmap (`ROADMAP-001`)
- [x] All new work items declare dependencies (W19-W26, K9-K10, A10-A11, F12-F13)
- [x] New risks include mitigation strategies (R1-R7 integrated)
- [x] Grade promotion/justification documented (INFORMED_ESTIMATE evidence basis listed)
- [x] Current Work Item section updated and still points to W4 as next task
