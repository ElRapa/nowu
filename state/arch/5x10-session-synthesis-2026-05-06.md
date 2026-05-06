---
artifact_type: SYNTHESIS
altitude: ARCHITECTURE
phase: SYNTHESIS
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Decisions validated by 5 Perplexity research evaluations (AFLOW, TOGAF, MVA, Shape Up, multi-agent systems research) plus original concept draft analysis"
created_at: 2026-05-06
session: "5x10 workflow model design + Perplexity evaluation synthesis"
source_artifacts:
  - .sisyphus/drafts/idea-004-2d-altitude-phase-model.md
  - docs/model/MODEL-REFERENCE.md
  - docs/research/2026-05-06_*.md
related_decisions: [D-001, D-002, ADR-0001, ADR-0006]
status: ACTIVE
---

# Session Synthesis: 5×10 Workflow Model Decisions

## What This File Is

Synthesized decisions from the 5×10 altitude-phase model design session (2026-05-06). Each decision has an epistemic grade reflecting confidence level. These decisions should be treated as binding at their stated grade — not reopened without new evidence.

---

## Decided: Model Structure

### D-WF-001: 5 Altitudes × 10 Phases
**Grade: EVIDENCE_BASED** — validated by Anthony 1965, Shape Up, SYSMOD zigzag, Rombaut 2026

- STRATEGIC > PRODUCT > ARCHITECTURE > DELIVERY > EXECUTION
- IDEA > PROBLEM > ANALYSIS > SYNTHESIS > OPTIONS > DECISION > EVALUATION > IMPLEMENTATION > VERIFICATION > LEARN
- The 5×10 matrix is a coordinate system, not a pipeline. Not all 50 cells are active.
- Information flows downward (STRATEGIC→EXECUTION) with LEARN as the upward exception.

### D-WF-002: Phases Are Cognitive Modes, Not Altitude-Locked
**Grade: EVIDENCE_BASED** — validated by AFLOW operators, Rombaut loop primitives

- IMPLEMENTATION works at ARCHITECTURE (writing ADRs), DELIVERY (shaping), EXECUTION (code)
- VERIFICATION works at STRATEGIC, ARCHITECTURE, DELIVERY, EXECUTION
- LEARN works at ALL altitudes
- SYNTHESIS is the ONLY altitude-locked phase (ARCHITECTURE only)
- Agents declare altitude RANGE + phase, not locked coordinates

### D-WF-003: S1-S9 Is a Default Traversal, Not a Rigid Pipeline
**Grade: INFORMED_ESTIMATE** — SYSMOD zigzag validates the pattern; not yet empirically tested in nowu

- S1-S9 zigzag: DELIVERY→ARCHITECTURE→DELIVERY→EXECUTION is the common path for feature intakes
- Alternative traversals are valid: bug fix (pure EXECUTION), spike (pure ARCHITECTURE), strategic pivot
- The model should DESCRIBE observed patterns, not PRESCRIBE mandatory sequences

### D-WF-004: Epistemic Grades with Tiered Thresholds
**Grade: EVIDENCE_BASED** — novel innovation, no comparable mechanism in existing frameworks

| Altitude | Minimum (creation) | Advisory | Aspirational (decision) |
|---|---|---|---|
| STRATEGIC | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| ARCHITECTURE | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED |
| PRODUCT | SPECULATION | HYPOTHESIS | INFORMED_ESTIMATE |
| DELIVERY | SPECULATION | HYPOTHESIS | HYPOTHESIS |
| EXECUTION | SPECULATION | HYPOTHESIS | HYPOTHESIS |

Enforcement: Advisory in v1-core, blocking at decision gates in v1.0+.

---

## Decided: Architecture Approach

### D-WF-005: Architecture Vision Needed Before ADRs
**Grade: INFORMED_ESTIMATE** — TOGAF Phase A validates; not yet produced for nowu

- SYNTHESIS produces themes + ADR recommendations (what problems to solve)
- Architecture Vision is the narrative of what the WHOLE system is (what kind of system solves them)
- Dependency: Architecture Vision → SYNTHESIS → ADRs → S1-S9 intakes
- Architecture Vision is a 1-page artifact: system classification, principles, quality attributes, risks

### D-WF-006: Option C — Architecture Hypothesis + Feedback Loop (MVA)
**Grade: INFORMED_ESTIMATE** — Minimum Viable Architecture literature, GitHub Spec Kit

- Write ADRs at HYPOTHESIS grade (deep enough for AI agents, shallow enough to be wrong)
- Run 1-2 S1-S9 intakes against hypothesis architecture
- Refine: HYPOTHESIS → INFORMED_ESTIMATE (after 2 intakes) → EVIDENCE_BASED (after 5+)
- ADR content minimum: Context, Constraints, Options, Decision, Validation Criteria, Implementation Checklist

### D-WF-007: Soft Enforcement — Advisory in Exploration, Blocking at Gates
**Grade: INFORMED_ESTIMATE** — ADR lifecycle research, ATAM

- Level 0 (v1-core): Syntax check only
- Level 1 (v1.0): Advisory warnings for altitude/grade violations
- Level 2 (v1.1): Blocking at DECISION gates if below aspirational grade
- Level 3 (v2+): Circuit breaker for altitude violations

### D-WF-008: SYNTHESIS Trigger — ≥2 UCs OR Human Override
**Grade: HYPOTHESIS** — logical extension of SYNTHESIS design

- Automatic: ≥2 approved UCs with `architectural_implications: true` and no linked ADRs
- Manual: Human suspects cross-cutting architectural theme (rapid iteration mode)

---

## Decided: Agent Architecture

### D-WF-009: Router-Based Agents (90% Agnostic, 10% Aware)
**Grade: INFORMED_ESTIMATE** — Redis 2026, hierarchical MAS research, AFLOW/MASAI patterns

- S1-S9 agents are altitude-AGNOSTIC executors (they don't know their altitude)
- The orchestrator/router knows altitude and routes agents accordingly
- GAP/reflective agents are altitude-AWARE (they reason about cross-altitude patterns)
- Agent altitude behavior comes from skill files, not self-awareness

### D-WF-010: Triage Is a Missing Primitive
**Grade: HYPOTHESIS** — user-discovered empirical gap

- Neither S1-S9 nor P0-P4 answers "what should we do next?"
- Triage = Intake → Assessment (Impact × Altitude) → Routing
- Implement after SYNTHESIS validates, before S1-S9 scales

---

## Decided: Knowledge & Contract Handling

### D-WF-011: Markdown for Knowledge Management at Current Scale
**Grade: EVIDENCE_BASED** — LLM native format, git-trackable, optimal for <1000 artifacts

- Markdown + YAML frontmatter is correct for nowu's current stage
- Switch to database when: >1000 artifacts, complex relational queries, concurrent editing
- Obsidian optional as human UI layer (graph view, dataview queries)

### D-WF-012: ADR Amendment Process for Contract Evolution
**Grade: INFORMED_ESTIMATE** — API versioning research, fitness functions literature

- Non-breaking changes (add optional field): Amendment to parent ADR
- Breaking changes (remove field, change format): Supersession (new ADR)
- Fitness functions validate architectural characteristics after each change
- Traceability: Amendment → Parent ADR → Source UCs → Goals

### D-WF-013: Traceability Metadata from Day 1
**Grade: INFORMED_ESTIMATE** — stage-gated evolution pattern

- Every artifact includes: `source_goal`, `source_uc`, `source_themes`, `architectural_decisions`
- Forward trace: GOAL → UC → ADR → SESSION
- Backward trace: SESSION → ADR → UC → GOAL
- Implementation stages add automation, not the concept

---

## Open Questions (Not Decided)

### OQ-1: Which of the 50 cells are primary/secondary/rare?
**Status:** Defer until 10+ workflows complete. Perplexity's 13/24/10/3 classification is theoretical — needs empirical validation.

### OQ-2: Exact epistemic threshold calibration
**Status:** Current thresholds are theoretical. Run 5+ intakes with Level 0 (no enforcement), observe actual grades agents assign, calibrate thresholds empirically.

### OQ-3: Triage agent design
**Status:** Concept validated (RICE or Impact×Altitude matrix). Details deferred until after SYNTHESIS + first S1-S9 intakes.

### OQ-4: LangGraph orchestration specifics
**Status:** LangGraph is the right choice (checkpointing, approval gates). Implementation deferred to v1.1+ after S1-S9 agents exist and work.

### OQ-5: AutoResearch integration
**Status:** Valid for Stage 4+ (agent optimization). Not valid for workflow discovery (Stage 0-2).

---

## Key Insight: Where We Are

We are bootstrapping the workflow itself. The current block:

```
Goals     ✅ exist (goal-001 through goal-004)
Use Cases ✅ exist (approved)
                    ↓
          ┌─── BLOCKED HERE ───┐
          │ No Architecture    │
          │ Vision or global   │
          │ synthesis across   │
          │ approved UCs       │
          └────────────────────┘
                    ↓
ADRs      ⚠️ exist (0001-0006) but not connected to UC themes
S1-S9     ❌ not yet run end-to-end
```

**Next action:** Create Architecture Vision + run manual SYNTHESIS → write hypothesis ADRs → unblock S1-S9.
