---
artifact_type: ROADMAP
version: 3
altitude: STRATEGIC
phase: IMPLEMENTATION
epistemic_grade: INFORMED_ESTIMATE
created_at: 2026-05-10
source_vision: docs/vision.md
source_goals: [goal-001, goal-002, goal-003, goal-004]
source_usecases: docs/USE_CASES.md
source_synthesis: state/arch/SYNTHESIS-001.md
source_architecture_vision: docs/architecture/ARCHITECTURE-VISION.md
supersedes: [docs/ROADMAP-001.md, docs/ROADMAP-002.md]
status: ACTIVE
---

# nowu Canonical Roadmap — ROADMAP-003

## Goal Achievement Horizon

Legend: **F** = first addressed, **A** = target stage where goal is considered achieved.

| Goal | v1-core | v1 | v1.1 | v1.2 | v2 |
|---|---|---|---|---|---|
| goal-001 (continuity, 6mo) | F | A |  |  |  |
| goal-002 (workflow, 6mo) | F | A |  |  |  |
| goal-003 (knowledge, 12mo) | F |  | A |  |  |
| goal-004 (infrastructure, 24mo) |  | F |  |  | A |

## Theme × Stage Matrix

| Theme | v1-core | v1 | v1.1 | v1.2 | v2 |
|---|---|---|---|---|---|
| T1 Continuity | W4, W5, K1 | W28, F4 | W14 | W25 | W18 |
| T2 Knowledge Persistence & Lifecycle | K1, K2, W3/ADR-0008 | K3, K4, W29 | K11, K12, K13, K5, K6 | K9, K10 | K7, K8 |
| T3 Workflow Orchestration | W1, W2, W3, W4 | W7, W8, W10, W32 | W11, W12, W15 | W24, W26 | W16, W17 |
| T4 Epistemic Awareness | W29, W3/ADR-0010 | W32, W9 | W14, W30 | W26 | W16 |
| T5 Domain Agnosticism | W4 baseline validation | W27, W28, W19 | W22 | W24, W25 | W18, F10, F11 |
| T6 Observability & Traceability | K1, W-UCGOAL, W20 | W9 | W12, A7, F9 | W26 | W16 |
| T7 Multi-Surface Access |  | W31, F6 | W22 | F12 | F11 |
| T8 Progressive Disclosure | W4, W21 | W10 | W14, W15 | W25 | W17 |
| T9 Audience-Aware Rendering |  |  | W23 | F13 | F10, F11 |

## 1. Stage Structure

| Stage | Time Horizon | Success Criteria | Status |
|---|---|---|---|
| v1-core | 6 months (foundation for goal-001/002) | First S1-S9 cycle completed, hypothesis ADRs usable in flow, traceability baseline active | IN_PROGRESS |
| v1 | 6 months (goal-001/002 achievement target) | 5+ intakes completed, AP/RE v1 bootstrap running, epistemic Level 0 enforcement active | PLANNED |
| v1.1 | 12 months (goal-003 achievement target) | Knowledge lifecycle and observability loops stable, multi-surface adapter and rendering architecture validated | PLANNED |
| v1.2 | 12 months (domain operational depth) | AP/RE operational domain workflows stable for active use (AP-03/05/07, RE-02/03/04/07) | PLANNED |
| v2 | 24 months (goal-004 achievement target) | Installable, externally adoptable framework with multi-user collaboration and scale envelope | PLANNED |

## 2. Area × Stage Work Grid

| Area | ID | Description | Stage | Depends On | UC(s) | Status |
|---|---|---|---|---|---|---|
| Workflow | W1 | Manual SYNTHESIS on approved UCs | v1-core | none | NF-09, XP-01 | ✅ DONE |
| Workflow | W2 | Architecture Vision from SYNTHESIS themes | v1-core | W1 | NF-02, NF-03 | ✅ DONE |
| Workflow | W3 | Hypothesis ADR pack (ADR-0007..0010) | v1-core | W1, W2 | NF-01, NF-15 | ✅ DONE |
| Workflow | W3.5 | Minimal fitness checks for hypothesis ADRs | v1-core | W3 | NF-04, NF-09 | ✅ DONE |
| Workflow | W4 | First S1-S9 intake (end-to-end cycle) | v1-core | W3.5 | NF-01..NF-13, PK-01, PK-03, XP-01 | ✅ DONE |
| Workflow | W5 | Validate 5×10 coordinates on W4 artifacts | v1-core | W4 | NF-03, NF-09 | READY |
| Workflow | W6 | 5×10 model refactor with full agent-grid mapping | v1-core | W4 | NF-02, NF-03 | READY |
| Workflow | W-orch | Orchestrator layer formalized (roadmap-creator/updater/scheduler) | v1-core | W3 | NF-05, NF-10 | ✅ DONE |
| Workflow | W-log | Session-log + roadmap alignment | v1-core | none | NF-10, NF-06 | ✅ DONE |
| Workflow | W-UCGOAL | Backfill UC↔goal mappings in goal files | v1-core | none | NF-09, NF-11, NF-16 | READY |
| Workflow | W7 | SYNTHESIS trigger automation | v1 | W1 validated | NF-06, NF-11 | PLANNED |
| Workflow | W8 | Level 1 advisory enforcement (altitude/grade violations) | v1 | W32 | NF-15, NF-02 | PLANNED |
| Workflow | W9 | Promote hypothesis ADRs via intake evidence | v1 | 2+ intakes | NF-02, NF-15, AP-06 | PLANNED |
| Workflow | W10 | Triage primitive for path selection | v1 | W4 | NF-03, NF-13 | PLANNED |
| Workflow | W19 | ADR-0011 domain extension model | v1 | ADR-0008, ADR-0009 | XP-07, AP-01, RE-01 | PLANNED |
| Workflow | W20 | ADR-0012 traceability metadata standard | v1 | ADR-0009, K1 | NF-09 | PLANNED |
| Workflow | W21 | ADR-0014 progressive enrichment model | v1 | ADR-0008, ADR-0010 | NF-12, PK-01, PK-05 | PLANNED |
| Workflow | W27 | AP domain project bootstrap (AP-01/AP-02/AP-06) | v1 | W4 | AP-01, AP-02, AP-06 | PLANNED |
| Workflow | W28 | RE domain project bootstrap (RE-01/RE-06) | v1 | W4 | RE-01, RE-06 | PLANNED |
| Workflow | W29 | NF-15 Level 0 epistemic enforcement implementation | v1 | W4, ADR-0010 | NF-15 | PLANNED |
| Workflow | W32 | Epistemic threshold calibration (replaces old v1 W6 naming collision) | v1 | W4, W5 | NF-15, NF-16 | PLANNED |
| Workflow | W11 | Level 2 enforcement (blocking at DECISION gates) | v1.1 | W8 stable | NF-15, NF-11 | PLANNED |
| Workflow | W12 | Architectural fitness function suite | v1.1 | ADRs promoted | NF-04, NF-08 | PLANNED |
| Workflow | W13 | ADR amendment workflow | v1.1 | W12 | NF-02 | PLANNED |
| Workflow | W14 | Grade promotion workflows (H→IE→EB) | v1.1 | W9 | NF-14, PK-04 | PLANNED |
| Workflow | W15 | Alternative traversals (bugfix/spike paths) | v1.1 | 5+ intakes | NF-12, NF-16 | PLANNED |
| Workflow | W22 | ADR-0013 interface adapter architecture | v1.1 | W19, W20, W21 | PK-08, T7 | PLANNED |
| Workflow | W23 | ADR-0015 consumer-aware rendering | v1.1 | W22 | XP-11, RE-07 | PLANNED |
| Workflow | W30 | NF-16 strategic drift detection implementation | v1.1 | W29, W15 | NF-16 | PLANNED |
| Workflow | W24 | AP/RE domain deepening execution plan | v1.2 | W19 | AP-03/05/07, RE-02/03/04/07 | PLANNED |
| Workflow | W25 | Domain milestone/dependency tracking operationalized | v1.2 | W24, K6 | AP-05, RE-04, RE-06 | PLANNED |
| Workflow | W26 | Role-scoped collaborator workflows stabilized | v1.2 | W23, W24 | AP-07, RE-07 | PLANNED |
| Workflow | W16 | Level 3 circuit-breaker enforcement | v2 | W11 | NF-05, XP-10 | PLANNED |
| Workflow | W17 | Multi-traversal auto-selection | v2 | W15 | XP-06 | PLANNED |
| Workflow | W18 | 5×10 grid auto-population from history | v2 | 20+ intakes | NF-08, XP-10 | PLANNED |
| Knowledge | K1 | Traceability metadata in all new artifacts | v1-core | none | NF-09 | ACTIVE |
| Knowledge | K2 | Forward/backward trace validation | v1-core | W4 | NF-09, XP-08 | READY |
| Knowledge | K3 | MemoryService integration for structured recall | v1 | core contracts baseline | NF-01, PK-03 | PLANNED |
| Knowledge | K4 | Session state persistence via know | v1 | K3 | NF-01, NF-10, XP-01 | PLANNED |
| Knowledge | K5 | Cross-project recall | v1.1 | K4 | XP-01, XP-03 | PLANNED |
| Knowledge | K6 | Semantic queries over artifact corpus | v1.1 | K5 | PK-02, PK-09, XP-04 | PLANNED |
| Knowledge | K11 | External document ingestion pipeline | v1.1 | K6 | PK-07 | PLANNED |
| Knowledge | K12 | Knowledge decay and cleanup engine | v1.1 | K6 | PK-04 | PLANNED |
| Knowledge | K13 | Sensitivity classification and enforcement | v1.1 | K6 | PK-06 | PLANNED |
| Knowledge | K9 | Domain atom extension packs (AP/RE) | v1.2 | W19, K6 | AP-03, RE-02 | PLANNED |
| Knowledge | K10 | Cross-domain contradiction/dependency views | v1.2 | K9, W25 | RE-05, AP-04 | PLANNED |
| Knowledge | K7 | Graph-scale knowledge backend (thresholded) | v2 | K6 | XP-05 | PLANNED |
| Knowledge | K8 | Automated knowledge curation at scale | v2 | F8 | XP-05, XP-04 | PLANNED |
| Agents | A1 | Existing 19 execution agents operate as-is | v1-core | none | NF-04, NF-05 | ACTIVE |
| Agents | A2 | Router adds altitude metadata on intake routing | v1-core | W4 | NF-03 | READY |
| Agents | A3 | Orchestrator with altitude routing logic | v1 | W5 | NF-05, NF-09 | PLANNED |
| Agents | A4 | Skill files encode altitude behavior | v1 | A3 | NF-03, NF-12 | PLANNED |
| Agents | A5 | SYNTHESIS agent productionization | v1 | W7 | NF-06, NF-11 | PLANNED |
| Agents | A6 | GAP reflective agent loops | v1.1 | A3 | NF-11, NF-16, XP-03 | PLANNED |
| Agents | A7 | Health monitoring agents (soul integration) | v1.1 | W12 | NF-08, NF-14 | PLANNED |
| Agents | A10 | Domain briefing/onboarding patterns | v1.2 | W26 | AP-07, XP-09 | PLANNED |
| Agents | A11 | Domain risk/operations analyst loops | v1.2 | W25, K10 | AP-03, RE-04 | PLANNED |
| Agents | A8 | LangGraph orchestration | v2 | A3, F5 | XP-06, XP-10 | PLANNED |
| Agents | A9 | Agent optimization from historical traces | v2 | A8 | XP-06, XP-10 | PLANNED |
| Framework | F1 | Contracts baseline | v1-core | none | NF-03 | ✅ DONE |
| Framework | F2 | Import boundary enforcement tests | v1-core | none | NF-02 | ✅ DONE |
| Framework | F3 | Level 0 artifact verification script | v1-core | none | NF-09, NF-15 | PLANNED |
| Framework | F4 | Session runtime + WAL | v1 | K3 | NF-01, NF-10 | PLANNED |
| Framework | F5 | Role sequencer runtime | v1 | F4 | NF-04, NF-05 | PLANNED |
| Framework | F6 | Bridge CLI + approval routing | v1 | F5 | NF-05, PK-08 | PLANNED |
| Framework | F7 | Project bootstrap command | v1.1 | F6 | NF-07 | PLANNED |
| Framework | F8 | Learning + curation loop | v1.1 | K4, A6 | NF-06 | PLANNED |
| Framework | F9 | Health metrics dashboard | v1.1 | A7 | NF-08, NF-14 | PLANNED |
| Framework | W31 | Telegram/remote surface adapter implementation | v1.1 | F6, W22 | PK-08 | PLANNED |
| Framework | F12 | Domain capability matrix surfaced in bridge | v1.2 | W24, W26 | AP-07, RE-07 | PLANNED |
| Framework | F13 | Operational report export presets | v1.2 | W26, W23 | RE-07, XP-08, XP-11 | PLANNED |
| Framework | F10 | Installable package + public docs | v2 | F7, v1.1 gate | XP-09 | PLANNED |
| Framework | F11 | Multi-user/external project support | v2 | F10 | XP-10 | PLANNED |

> **Phase-operator architecture (v1.1+ direction):** v1 and v1.1 should converge on generic phase agents parameterized by `altitude` and `artifact_type`, with P0–P4 and S1–S9 modeled as named traversals of the 5×10 grid, not separate workflows. See MODEL-REFERENCE §5 "Future: Phase Operators" and IMPLEMENTATION-GUIDE Package 2 for design intent.

## 3. UC-to-Stage Mapping

| UC-ID | Title | Stage | Work Items | Theme(s) |
|---|---|---|---|---|
| NF-01 | Resume Work After Context Loss | v1-core | W4, K3, F4 | T1, T2 |
| NF-02 | Track and Enforce Architectural Decisions | v1-core | W4, W9, F2 | T3, T6 |
| NF-03 | Scope a Piece of Work Without Scope Creep | v1-core | W4, W5, A2 | T3, T8 |
| NF-04 | Self-Assess Quality Without Human Intervention | v1-core | W4, W12, A1 | T3, T6 |
| NF-05 | Route Approvals Without Blocking Progress | v1-core | W4, F6, W16 | T3, T6 |
| NF-06 | Learn From Past Mistakes Across Sessions | v1-core | W4, F8, W7 | T3, T6 |
| NF-07 | Bootstrap a New Project Using the Framework | v1-core | W4, F7 | T5, T8 |
| NF-08 | Measure and Visualize Framework Health | v1.1 | W12, A7, F9 | T6 |
| NF-09 | Ensure Every Deliverable Traces Back to a UC | v1-core | K1, K2, W20 | T6 |
| NF-10 | Maintain the Thread for the Multi-Project Human | v1-core | W4, K4, F4 | T1, T7 |
| NF-11 | Detect Vision Drift | v1.1 | A6, W14, W30 | T4, T6 |
| NF-12 | Explore a Vague Idea Without Structure | v1-core | W4, W21 | T8 |
| NF-13 | Generate Multiple Options at Decision Point | v1-core | W4, W10 | T3, T8 |
| NF-14 | Track Human-AI Work Ratio | v1.1 | A7, F9, W14 | T6 |
| NF-15 | Assign and Surface Epistemic Grades on Workflow Outputs | v1-core | W4, W29, W32 | T4 |
| NF-16 | Detect and Surface Strategic Drift | v1 | W30, W15, A6 | T1, T4 |
| AP-01 | Track Regulatory Requirements as Living Knowledge | v1 | W27, K3, K13 | T2, T5 |
| AP-02 | Manage Product Formulation as Versioned Knowledge | v1 | W27, K9 | T2, T5 |
| AP-03 | Model Supply Chain Relationships and Risks | v1.2 | W24, K9, A11 | T5 |
| AP-04 | Capture Market Intelligence Over Time | v1.1 | K11, K12, W14 | T2, T4 |
| AP-05 | Plan and Track Business Milestones | v1.2 | W25, K10 | T1, T5 |
| AP-06 | Evaluate a Business Decision With Traceability | v1 | W27, W9, W20 | T6, T5 |
| AP-07 | Onboard a Collaborator Into the Project Context | v1.2 | W26, A10, F13 | T7, T9 |
| RE-01 | Inventory Existing Processes Before Digitalization | v1 | W28, W19 | T5 |
| RE-02 | Track Property Data Across Lifecycle Stages | v1.2 | W24, K9 | T2, T5 |
| RE-03 | Capture Stakeholder Relationships and Constraints | v1.2 | W24, K10 | T5, T9 |
| RE-04 | Prioritize Digitalization by Impact and Feasibility | v1.2 | W25, A11 | T5, T6 |
| RE-05 | Detect Inconsistencies Across Property Records | v2 | K8, W16 | T2, T4 |
| RE-06 | Support Long-Term Investment Decision Tracking | v1 | W28, W25 | T1, T5 |
| RE-07 | Generate Reports for Different Audiences | v1.2 | W26, W23, F13 | T6, T9 |
| PK-01 | Capture a Thought Before It's Lost | v1-core | W4, W21 | T2, T8 |
| PK-02 | Surface Relevant Knowledge Without Being Asked | v1.1 | K6, A6 | T2 |
| PK-03 | Maintain a "Today" View Across All Projects | v1-core | W4, K4 | T1, T7 |
| PK-04 | Let Knowledge Decay and Clean Up Gracefully | v1.1 | K12, W14 | T2, T4 |
| PK-05 | Build Understanding Incrementally Over a Topic | v1.1 | W21, K6 | T2, T8 |
| PK-06 | Protect Sensitive Personal Knowledge | v1.1 | K13, W23 | T2, T9 |
| PK-07 | Ingest and Integrate External Documents | v1.1 | K11, W23 | T2 |
| PK-08 | Interact with nowu from Any Interface | v1 | F6, W31, W22 | T7 |
| PK-09 | Access Domain Expertise On Demand | v1.1 | K6, K11, W23 | T2, T4 |
| XP-01 | Discover Connections Across Projects Automatically | v1-core | K4, K5, W4 | T2, T6 |
| XP-02 | Maintain Consistent Terminology Across Projects | v2 | K6, K8 | T2 |
| XP-03 | Transfer Lessons Learned Between Projects | v1.1 | A6, F8 | T2, T6 |
| XP-04 | Handle Conflicting High-Confidence Knowledge | v1.1 | K6, K8, W14 | T2, T4 |
| XP-05 | Scale the Knowledge Base Without Degrading Performance | v2 | K7, K8 | T2 |
| XP-06 | Allow Multiple Agents to Work Without Conflicts | v2 | A8, W17, A9 | T3 |
| XP-07 | Adapt the Framework to a New Domain Without Rewriting | v2 | W19, F10, F11 | T5 |
| XP-08 | Export Full Project State in Portable Format | v1.1 | F13, K2 | T6, T9 |
| XP-09 | Onboard a New nowu User | v2 | F10, A10 | T7, T9 |
| XP-10 | Run a Small Company on nowu | v2 | F11, A8, A9 | T3, T9 |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format | v1.1 | W23, F13 | T9 |

## 4. Dependency Graph

**Critical path:** **W1 ✅ → W2 ✅ → W3 ✅ → W3.5 ✅ → W4 ✅ → W5 (READY) → v1-core→v1 gate**

```yaml
dependency_graph:
  # === v1-core (completed + next) ===
  W1: {depends_on: [], status: "✅ complete", evidence: ["state/arch/SYNTHESIS-001.md"]}
  W2: {depends_on: ["W1 ✅ → state/arch/SYNTHESIS-001.md"], status: "✅ complete", evidence: ["docs/architecture/ARCHITECTURE-VISION.md"]}
  W3: {depends_on: ["W1 ✅", "W2 ✅"], status: "✅ complete", evidence: ["docs/architecture/adr/ADR-0007-session-continuity-protocol.md", "docs/architecture/adr/ADR-0008-knowledge-atom-model.md", "docs/architecture/adr/ADR-0009-orchestration-protocol.md", "docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md"]}
  W3.5: {depends_on: ["W3 ✅"], status: "✅ complete", evidence: ["tests/architecture/test_adr_fitness.py"]}
  W-orch: {depends_on: ["W3 ✅"], status: "✅ complete", evidence: [".claude/agents/roadmap-creator.md", ".claude/agents/work-scheduler.md", ".claude/agents/roadmap-updater.md"]}
  W-log: {depends_on: [], status: "✅ complete", evidence: ["state/session-log.md", "docs/research/INDEX.md"]}
  W-UCGOAL: {depends_on: [], status: "✅ complete", evidence: ["docs/goals/goal-001.md", "docs/goals/goal-002.md", "docs/goals/goal-003.md", "docs/goals/goal-004.md"]}

  W4:
    depends_on:
      - "W3.5 ✅ → tests/architecture/test_adr_fitness.py"
      - "ADR-0008 (PROPOSED) → docs/architecture/adr/ADR-0008-knowledge-atom-model.md"
      - "ADR-0009 (PROPOSED) → docs/architecture/adr/ADR-0009-orchestration-protocol.md"
      - "ADR-0010 (PROPOSED) → docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md"
    status: "✅ complete"
    evidence: ["state/intake/intake-001.md", "state/tasks/", "Branch: w4-first-intake"]

  W5: {depends_on: ["W4"], status: "READY"}
  W6: {depends_on: ["W4"], status: "READY"}
  K1: {depends_on: ["W4"], status: "ACTIVE"}
  K2: {depends_on: ["W4"], status: "READY"}
  A1: {depends_on: ["W4"], status: "ACTIVE"}
  A2: {depends_on: ["W4"], status: "READY"}
  F1: {depends_on: [], status: "PLANNED"}
  F2: {depends_on: ["W4"], status: "READY"}
  F3: {depends_on: ["F1"], status: "PLANNED"}
  F4: {depends_on: ["K3"], status: "PLANNED"}
  F5: {depends_on: ["F1"], status: "PLANNED"}

  # === v1 (blocked by W4 or v1-core items) ===
  W7: {depends_on: ["W1"], status: "PLANNED"}
  W8: {depends_on: ["W32"], status: "PLANNED"}
  W9: {depends_on: ["W4"], status: "PLANNED"}
  W10: {depends_on: ["W4"], status: "PLANNED"}
  W19: {depends_on: ["ADR-0008", "ADR-0009"], status: "PLANNED"}
  W20: {depends_on: ["ADR-0009", "K1"], status: "PLANNED"}
  W21: {depends_on: ["ADR-0008", "ADR-0010"], status: "PLANNED"}
  W27: {depends_on: ["W4"], status: "PLANNED"}
  W28: {depends_on: ["W4"], status: "PLANNED"}
  W29: {depends_on: ["W4", "ADR-0010"], status: "PLANNED"}
  W32: {depends_on: ["W4", "W5"], status: "BLOCKED_BY_W5"}
  K3: {depends_on: ["K1"], status: "PLANNED"}
  A3: {depends_on: ["W5"], status: "PLANNED"}
  F6: {depends_on: ["F1"], status: "PLANNED"}
  F7: {depends_on: ["F1", "W4"], status: "PLANNED"}
  F8: {depends_on: ["K3"], status: "PLANNED"}

  # === v1.1 (blocked by v1 prereqs) ===
  W11: {depends_on: ["W8"], status: "PLANNED"}
  W12: {depends_on: ["ADRs promoted"], status: "PLANNED"}
  W13: {depends_on: ["W12"], status: "PLANNED"}
  W14: {depends_on: ["W9"], status: "PLANNED"}
  W15: {depends_on: ["5+ intakes"], status: "PLANNED"}
  W22: {depends_on: ["W19", "W20", "W21"], status: "PLANNED"}
  W23: {depends_on: ["W22"], status: "PLANNED"}
  W30: {depends_on: ["W29", "W15"], status: "BLOCKED_BY_v1.1_prereqs"}
  W31: {depends_on: ["F6", "W22"], status: "BLOCKED_BY_v1+"}
  K4: {depends_on: ["K3"], status: "PLANNED"}
  K5: {depends_on: ["K4"], status: "PLANNED"}
  K6: {depends_on: ["K4"], status: "PLANNED"}
  K11: {depends_on: ["K6"], status: "BLOCKED_BY_v1.1_prereqs"}
  K12: {depends_on: ["K6"], status: "BLOCKED_BY_v1.1_prereqs"}
  K13: {depends_on: ["K6"], status: "BLOCKED_BY_v1.1_prereqs"}
  A6: {depends_on: ["A3"], status: "PLANNED"}
  A7: {depends_on: ["W12"], status: "PLANNED"}
  F9: {depends_on: ["A7"], status: "PLANNED"}
  F13: {depends_on: ["W26", "W23"], status: "PLANNED"}

  # === v1.2 (blocked by v1.1 prereqs) ===
  W24: {depends_on: ["W19"], status: "PLANNED"}
  W25: {depends_on: ["W24", "K6"], status: "PLANNED"}
  W26: {depends_on: ["W23", "W24"], status: "PLANNED"}
  K7: {depends_on: ["K6"], status: "PLANNED"}
  K8: {depends_on: ["K6"], status: "PLANNED"}
  K9: {depends_on: ["W19", "K6"], status: "PLANNED"}
  K10: {depends_on: ["K9", "W25"], status: "PLANNED"}
  A10: {depends_on: ["W26"], status: "PLANNED"}
  A11: {depends_on: ["W25", "K10"], status: "PLANNED"}
  F12: {depends_on: ["W24", "W26"], status: "PLANNED"}

  # === v2 (blocked by v1.2 prereqs) ===
  W16: {depends_on: ["W11"], status: "PLANNED"}
  W17: {depends_on: ["W15"], status: "PLANNED"}
  W18: {depends_on: ["20+ intakes"], status: "PLANNED"}
  A8: {depends_on: ["A3"], status: "PLANNED"}
  A9: {depends_on: ["A8"], status: "PLANNED"}
  F10: {depends_on: ["F7"], status: "PLANNED"}
  F11: {depends_on: ["F10"], status: "PLANNED"}

adr_status_snapshot:
  accepted: [ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006]
  proposed_hypothesis: [ADR-0007, ADR-0008, ADR-0009, ADR-0010]
```

## 5. Stage Gate Criteria

### v1-core → v1

- [x] W1, W2, W3, W3.5 completed and artifacts exist.
- [x] Orchestrator baseline exists (W-orch) and session chronology anchor exists (W-log).
- [x] W4 first S1-S9 intake completed with full artifact chain from intake to capture.
- [ ] K2 traceability validation run and documented.

### v1 → v1.1

- [ ] At least 5 completed intakes with no unresolved Tier-3 blockers.
- [ ] Epistemic Level 0 and calibration path (W29 + W32) operational.
- [ ] AP and RE v1 bootstrap active (W27 + W28), with at least one live intake each.
- [ ] PK-08 first remote surface available (W31 dependency path started).

### v1.1 → v1.2

- [ ] Knowledge lifecycle controls active (K11/K12/K13) with measurable outputs.
- [ ] Strategic drift signal (W30) and health loop (A7/F9) producing regular reports.
- [ ] Interface and rendering ADRs (W22/W23) validated against active usage.
- [ ] Domain deepening plan approved for AP/RE operational UCs.

### v1.2 → v2

- [ ] AP/RE operational UCs in v1.2 are covered by stable workflows (W24/W25/W26).
- [ ] Export + audience rendering quality proven for external handoff scenarios.
- [ ] Scale + concurrency readiness established (K7/K8 + A8/A9 baseline).
- [ ] Installable product path validated (F10), then external/multi-user enablement (F11).

## 6. Risk Register

| ID | Description | Source Theme | Impact Level | Mitigation Strategy | Current Status |
|---|---|---|---|---|---|
| R1 | Knowledge model over-engineering stalls implementation velocity | T2 | HIGH | Keep ADR-0008 minimal, validate via W4/W9 before broad expansion | OPEN |
| R2 | Epistemic grading turns into bureaucracy overhead | T4 | HIGH | Implement Level 0 via W29 + calibrate with W32; restrict human-required grading to higher levels | OPEN |
| R3 | Domain abstraction fails AP/RE real workflows | T5 | HIGH | Validate with W27/W28 and v1.2 execution (W24+) before claiming generality | OPEN |
| R4 | Multi-surface effort fragments delivery | T7 | MEDIUM | Sequence CLI-first then single remote adapter (W31) | OPEN |
| R5 | Orchestration rigidity suppresses exploration | T3/T8 | MEDIUM | Preserve pre-workflow flexibility, keep S1-S9 for committed work | OPEN |
| R6 | Continuity checkpoint overhead reduces usability | T1 | MEDIUM | Checkpoint at step boundaries, not every operation | OPEN |
| R7 | Vision-to-reality overbuild (architecture ahead of proof) | T6 | HIGH | Stage-gated execution; only implement what active UC stage requires | OPEN |
| R8 | Progressive-disclosure maturity protocol remains implicit and inconsistent | T8 | MEDIUM | Formalize via W21 and enforce artifact maturation paths | OPEN |
| R9 | Audience-aware rendering lags knowledge growth, causing poor human/agent UX | T9 | MEDIUM | Prioritize W23 before v1.2 collaboration scaling | OPEN |

## 7. Current Work Item

```yaml
next_work_item: W5
description: Validate 5×10 coordinates on W4 artifacts
current_stage: v1-core
agent_to_invoke: single-step
input_artifacts:
  - state/intake/intake-001.md
  - state/tasks/
  - state/capture/capture-intake-001.md
status_hint: READY (W4 complete; validate the first intake artifact chain)
```

## Appendix A: ROADMAP-002 Change Disposition

| # | ROADMAP-002 Recommendation | Disposition in ROADMAP-003 |
|---|---|---|
| 1 | Domain onboarding work items | INCORPORATED as W27, W28 |
| 2 | NF-15, NF-16, PK-08 implementation tasks | INCORPORATED as W29, W30, W31 |
| 3 | Knowledge subsystem items | INCORPORATED as K11, K12, K13 |
| 4 | Version numbering fix | INCORPORATED (version: 3 canonicalized in frontmatter) |
| 5 | W6 naming collision | INCORPORATED (v1 calibration renamed to W32; v1-core W6 retained) |
| 6 | W-UCGOAL for UC↔goal backfill | INCORPORATED (v1-core immediate work item) |
| 7 | Theme×stage matrix | INCORPORATED (Theme × Stage Matrix preamble) |
| 8 | Goal achievement horizon | INCORPORATED (Goal Achievement Horizon preamble) |
| 9 | 7-section contract alignment | INCORPORATED (exactly sections 1..7, roadmap-creator compliant) |
| 10 | Current Stage/Work Item (Section 7) | INCORPORATED (machine-parseable Section 7 block) |
| 11 | Machine-readable UC mappings | INCORPORATED (Section 3 full 50-UC mapping) |
| 12 | Orientation system hooks | INCORPORATED (Appendix B orientation system statement) |

## Appendix B: Artifact Landscape

### Strategic Inputs

- `docs/vision.md` — success horizons and direction.
- `docs/goals/goal-001.md`..`goal-004.md` — outcome-level targets and horizon mapping.
- `docs/USE_CASES.md` — canonical UC set and stage targets.
- `state/arch/SYNTHESIS-001.md` — themes (T1-T9), UC-theme clustering, ADR recommendations.
- `docs/architecture/ARCHITECTURE-VISION.md` — principles, quality attributes, risks, ADR roadmap.

### Operational Orientation Anchors

- `state/session-log.md` — chronological session history (what happened, when, and why).
- `docs/research/INDEX.md` — research catalog and external evidence trace.
- `state/intake/intake-*.md` — intake frontier / active commitment boundary.

### Orientation System Hook

**ROADMAP + session-log + goals + research INDEX = orientation system**

This canonical roadmap intentionally centralizes stage sequencing and dependency logic while delegating chronology, evidence, and intake frontier to the three companion artifacts above.
