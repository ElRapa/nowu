---
id: goal-001
title: "Project momentum survives interruptions and compounds over time"
status: proposed
parent_vision_horizon: "6mo"
created: 2026-04-30
linked_epics: []
linked_ucs: []
altitude: PRODUCT
phase: DECISION
retired_reason: ""
---

## Outcome Goal

- Linked Horizon: "6 Months — The workflow is yours" with trust that nowu "hold[s] the thread through real interruptions."
- Desired Change: Work no longer resets between sessions. Across active projects, intent, decisions, and reasoning are reliably preserved so progress resumes from context, not from memory reconstruction.
- Non-Goals: Replacing human direction-setting; prescribing architecture or implementation details; creating manual project-management overhead.

## Success Criteria

- [ ] After at least 8 interruption/restart events across projects, each restart resumes with correct goals, recent decisions, and rationale without manual reconstruction.
- [ ] In at least 90% of resumed sessions, the first meaningful action toward the active outcome is taken within 10 minutes.
- [ ] For every active project, decision history remains inspectable and traceable to prior reasoning and evidence.
- [ ] This goal can be marked `achieved` when continuity is demonstrably reliable across multiple months and real interruption patterns, not just ideal sessions.

## UC Mapping

| UC-ID | Title | Stage | Status | Contribution |
| --- | --- | --- | --- | --- |
| NF-01 | Resume Work After Context Loss | v1-core | ACTIVE | Agent session recovery from persisted checkpoint; AI holds the thread (T1) |
| NF-03 | Scope a Piece of Work Without Scope Creep | v1-core | ACTIVE | Bounded task intent captured in artifacts; scope survives interruptions (T8) |
| NF-10 | Maintain the Thread for the Multi-Project Human | v1-core | ACTIVE | Human orientation on return; thread held across absences of any length (T1) |
| NF-11 | Detect Vision Drift | v1.1 | ACTIVE | Surfaces when accumulated work has drifted from stated goals over time (T4) |
| NF-12 | Explore a Vague Idea Without Structure | v1-core | ACTIVE | Low-fidelity fragments captured without commitment; promoted when ready (T8) |
| NF-13 | Generate Multiple Options at Decision Point | v1-core | ACTIVE | Decision alternatives preserved so past reasoning is revisitable months later (T8) |
| NF-15 | Assign and Surface Epistemic Grades on Workflow Outputs | v1-core | ACTIVE | Confidence level stored with decisions; trustworthy after months have passed (T4) |
| NF-16 | Detect and Surface Strategic Drift | v1 | ACTIVE | Goals with no active progress flagged; momentum stays visible and intentional (T1, T4) |
| AP-01 | Track Regulatory Requirements as Living Knowledge | v1 | ACTIVE | Regulatory state compounds across sessions without rediscovery cost (T2, T4) |
| AP-02 | Manage Product Formulation as Versioned Knowledge | v1 | ACTIVE | Versioned formulation history persists with rationale links across sessions (T2) |
| AP-04 | Capture Market Intelligence Over Time | v1.1 | ACTIVE | Temporal market data accumulates with source grading; no session resets (T2, T4) |
| AP-05 | Plan and Track Business Milestones | v1.2 | ACTIVE | Milestone state survives months-long interruptions without reconstruction (T1) |
| AP-06 | Evaluate a Business Decision With Traceability | v1 | ACTIVE | Business decisions captured with rationale so they outlast any session (T8) |
| RE-02 | Track Property Data Across Lifecycle Stages | v1.2 | ACTIVE | Property lifecycle history persists and remains queryable across months (T2) |
| RE-05 | Detect Inconsistencies Across Property Records | v2 | ACTIVE | Contradiction detection keeps accumulated knowledge coherent over time (T2, T4) |
| RE-06 | Support Long-Term Investment Decision Tracking | v1 | ACTIVE | Investment thesis and actuals persist across years; assumptions compound (T1) |
| PK-01 | Capture a Thought Before It's Lost | v1-core | ACTIVE | Frictionless capture prevents ideas resetting between sessions (T2, T8) |
| PK-02 | Surface Relevant Knowledge Without Being Asked | v1.1 | ACTIVE | Proactive surfacing of past knowledge; continuity without manual reconstruction (T2) |
| PK-03 | Maintain a "Today" View Across All Projects | v1-core | ACTIVE | Daily orientation surface spans all projects; re-entry from any project in seconds (T1) |
| PK-04 | Let Knowledge Decay and Clean Up Gracefully | v1.1 | ACTIVE | Lifecycle management keeps persisted knowledge trustworthy across time (T2, T4) |
| PK-05 | Build Understanding Incrementally Over a Topic | v1.1 | ACTIVE | Fragment-to-synthesis arc; confidence grows as evidence accumulates (T2, T4, T8) |
| PK-06 | Protect Sensitive Personal Knowledge | v1.1 | ACTIVE | Sensitivity controls keep persisted knowledge safe across sessions (T2) |
| PK-07 | Ingest and Integrate External Documents | v1.1 | ACTIVE | External knowledge integrated into durable store; not discarded at session end (T2) |
| PK-08 | Interact with nowu from Any Interface | v1 | ACTIVE | Remote re-entry without losing the thread; continuity from any device (T1) |
| PK-09 | Access Domain Expertise On Demand | v1.1 | ACTIVE | Expertise retained as durable atoms; research compounds across future cycles (T2, T4) |
| XP-01 | Discover Connections Across Projects Automatically | v1-core | ACTIVE | Cross-project semantic links emerge from accumulated knowledge (T2) |
| XP-03 | Transfer Lessons Learned Between Projects | v1.1 | ACTIVE | Compounded lessons applied across projects without requiring recall (T2) |
| XP-04 | Handle Conflicting High-Confidence Knowledge | v1.1 | ACTIVE | Contradiction resolution keeps accumulated knowledge trustworthy (T2, T4) |
| XP-05 | Scale the Knowledge Base Without Degrading Performance | v2 | ACTIVE | Performance at scale keeps the compounding knowledge store usable (T2) |
| XP-09 | Onboard a New nowu User | v2 | ACTIVE | Progressive onboarding; vague input promoted to structured output without overhead (T8) |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format | v1.1 | ACTIVE | Accumulated knowledge rendered for humans and agents without duplication (T2) |

## Phase Coverage

| Phase | Epic | Slice Delivered | Status |
| --- | --- | --- | --- |
| v1-core | epic-v1core-001 | Continuity & Capture: session orientation, agent checkpoint resumption, frictionless capture, cross-project Today view | APPROVED |
| v1-core | epic-v1core-003 | Project Bootstrap & Idea Lifecycle: lightweight idea exploration, single-session project bootstrap for any domain | APPROVED |

## UC Completion

- Active UCs: 31/31
- Linked to epics: 6/31 (NF-01, NF-10, NF-12, NF-16, PK-01, PK-03)
- Completed captures: 0/31

## Solution Shape

- Form: A continuity layer that persists goals, decisions, lessons, and reasoning as durable artifacts used every session.
- Key Capabilities: Persistent context carryover; explicit decision-and-rationale capture; scoped session startup that pulls only relevant prior state; confidence-aware knowledge retention.
- Main Tradeoffs: Higher upfront structure to gain long-term continuity; strict scope boundaries over broad but noisy context loading.
- Sequencing Notes: Establish durable continuity and restart reliability first; then expand to multi-project orchestration and cross-project intelligence.

## Epic Seeds

- Seed 1: Continuity baseline for restart-safe project progression

<!-- Unmapped UCs (not referenced by any SYNTHESIS theme): NF-06 (Learn From Past Mistakes Across Sessions) -->
<!-- Excluded (PENDING status, uncertain horizon): XP-02 (Maintain Consistent Terminology Across Projects) -->
