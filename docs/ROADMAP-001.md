---
artifact_type: ROADMAP
version: 1
created_at: 2026-05-06
status: ACTIVE
epistemic_grade: INFORMED_ESTIMATE
supersedes: docs/V1_PLAN.md (directional only — that file is retained as historical reference)
source: state/arch/5x10-session-synthesis-2026-05-06.md
decisions: [D-WF-001 through D-WF-013]
---

# nowu Implementation Roadmap v1

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
| **v2** | Framework Product | Installable, external projects, multi-traversal |

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

**Unblocking chain:** ~~W1~~ → ~~W2~~ → ~~W3~~ → ~~W3.5~~ → **W4** → W5

**Current state:** W1 + W2 + W3 + W3.5 complete. Next: **W4** — first S1-S9 intake end-to-end.

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

## What To Do Right Now

The critical path is **Workflow v1-core**: ~~W1~~ → ~~W2~~ → ~~W3~~ → ~~W3.5~~ → **W4** → W5.

**Next session should execute W4:**
1. Select first intake for S1-S9 end-to-end (recommend NF-01 or a small NF UC)
2. Run full S1-S9 cycle using hypothesis ADRs as architectural context
3. Capture session learnings — validate or refine ADR hypotheses

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
