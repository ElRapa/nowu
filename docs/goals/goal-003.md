---
id: goal-003
title: "Knowledge compounds within and across projects as durable organizational memory"
status: proposed
parent_vision_horizon: "12mo"
created: 2026-04-30
linked_epics: []
linked_ucs: []
altitude: PRODUCT
phase: DECISION
retired_reason: ""
---

## Outcome Goal

- Linked Horizon: "12 Months — Knowledge compounds across projects" with six-plus active projects and a shared, queryable knowledge base that improves workflow quality each cycle.
- Desired Change: Project work becomes cumulatively smarter: domain knowledge persists, transfers appropriately, and accelerates future decisions without destructive cross-project interference.
- Non-Goals: Collapsing all projects into one context; speculative architecture mandates; enterprise-scale compliance guarantees.

## Success Criteria

- [ ] At least six active projects across software and non-software domains maintain distinct project memory without context pollution.
- [ ] Shared knowledge can be queried to answer cross-project questions with traceable sources and confidence.
- [ ] A new contributor can recover project intent, decisions, and rationale from artifacts alone for any active project.
- [ ] Measurable cycle efficiency improves over time (faster path from vision to shipped outputs with fewer rediscovery steps).
- [ ] This goal can be marked `achieved` when knowledge reuse repeatedly improves outcomes across multiple projects and cycles.

## UC Mapping

| UC-ID | Title | Stage | Status | Contribution |
| --- | --- | --- | --- | --- |
| NF-11 | Detect Vision Drift | v1.1 | ACTIVE | Goal-alignment knowledge accumulates and is queried over time; drift is a knowledge signal (T4) |
| NF-15 | Assign and Surface Epistemic Grades on Workflow Outputs | v1-core | ACTIVE | Every output carries grade; the knowledge base knows how much to trust itself (T4) |
| NF-16 | Detect and Surface Strategic Drift | v1 | ACTIVE | Goal-coverage atoms accumulate; drift signals are derived from the knowledge graph (T4) |
| AP-01 | Track Regulatory Requirements as Living Knowledge | v1 | ACTIVE | Regulatory knowledge with source, confidence, dependencies, and currency — living not static (T2, T4) |
| AP-02 | Manage Product Formulation as Versioned Knowledge | v1 | ACTIVE | Versioned formulation atoms with rationale links; compounding product knowledge (T2) |
| AP-04 | Capture Market Intelligence Over Time | v1.1 | ACTIVE | Source-graded market intelligence accumulates and compounds over multiple cycles (T2, T4) |
| AP-07 | Onboard a Collaborator Into the Project Context | v1.2 | ACTIVE | Knowledge rendered in collaborator-appropriate format from a single underlying graph (T9) |
| RE-02 | Track Property Data Across Lifecycle Stages | v1.2 | ACTIVE | Property data accumulates across lifecycle stages with verification status tracking (T2) |
| RE-05 | Detect Inconsistencies Across Property Records | v2 | ACTIVE | Contradiction detection keeps the knowledge base coherent as it scales (T2, T4) |
| RE-07 | Generate Reports for Different Audiences | v1.2 | ACTIVE | Same knowledge graph rendered for different audiences without maintaining separate copies (T9) |
| PK-01 | Capture a Thought Before It's Lost | v1-core | ACTIVE | Atomic frictionless capture is the entry point for all knowledge that will compound (T2) |
| PK-02 | Surface Relevant Knowledge Without Being Asked | v1.1 | ACTIVE | Proactive surfacing; value compounds as the accumulated base grows (T2) |
| PK-04 | Let Knowledge Decay and Clean Up Gracefully | v1.1 | ACTIVE | Lifecycle management keeps compounding knowledge trustworthy; decay prevents pollution (T2, T4) |
| PK-05 | Build Understanding Incrementally Over a Topic | v1.1 | ACTIVE | Fragment-to-synthesis arc; understanding compounds with each new piece of evidence (T2, T4) |
| PK-06 | Protect Sensitive Personal Knowledge | v1.1 | ACTIVE | Sensitivity scoping allows cross-project sharing without exposing private atoms (T2) |
| PK-07 | Ingest and Integrate External Documents | v1.1 | ACTIVE | External knowledge graded and integrated into the durable base; compounds not discards (T2) |
| PK-08 | Interact with nowu from Any Interface | v1 | ACTIVE | Knowledge capturable from any surface; the base grows regardless of which interface is used (T9) |
| PK-09 | Access Domain Expertise On Demand | v1.1 | ACTIVE | Expertise retained as durable atoms; research compounds so the same question is never started from scratch (T2, T4) |
| XP-01 | Discover Connections Across Projects Automatically | v1-core | ACTIVE | Cross-project connections emerge automatically from the compounding knowledge base (T2) |
| XP-03 | Transfer Lessons Learned Between Projects | v1.1 | ACTIVE | Lessons compound across projects; future decisions accelerated by prior learning (T2) |
| XP-04 | Handle Conflicting High-Confidence Knowledge | v1.1 | ACTIVE | Contradiction resolution keeps high-confidence atoms trustworthy as the base grows (T2, T4) |
| XP-05 | Scale the Knowledge Base Without Degrading Performance | v2 | ACTIVE | Performance at scale is prerequisite for compounding to remain useful at 10K+ atoms (T2) |
| XP-08 | Export Full Project State in Portable Format | v1.1 | ACTIVE | Accumulated knowledge exportable in open formats; not a walled garden (T9) |
| XP-09 | Onboard a New nowu User | v2 | ACTIVE | Knowledge rendered in plain language for new users; accessible without internal vocabulary (T9) |
| XP-10 | Run a Small Company on nowu | v2 | ACTIVE | Company-level knowledge view across projects; compounding benefits extend to teams (T9) |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format | v1.1 | ACTIVE | Same accumulated knowledge rendered for humans and agents alike without duplication (T2, T9) |

## Phase Coverage

| Phase | Epic | Slice Delivered | Status |
| --- | --- | --- | --- |
| v1-core | epic-v1core-004 | Knowledge That Compounds: cross-project connection discovery, AP regulatory & formulation knowledge, AP/RE decision traceability, RE process documentation as structured knowledge | APPROVED |

## UC Completion

- Active UCs: 26/26
- Linked to epics: 3/26 (XP-01, AP-01, AP-02)
- Completed captures: 0/26

## Solution Shape

- Form: A shared but scoped knowledge layer where atomic facts/decisions/lessons are linked, queryable, and rendered for both human and AI use.
- Key Capabilities: Atomic knowledge capture with source/confidence metadata; project-scoped retrieval; controlled cross-project linking; durable artifact traceability.
- Main Tradeoffs: Strong isolation to prevent interference versus selective sharing to maximize reuse and compounding.
- Sequencing Notes: Build per-project durability first; then enable safe cross-project queryability and compounding feedback into each cycle.

## Epic Seeds

- Seed 1: Atomic knowledge graph with scoped cross-project retrieval
