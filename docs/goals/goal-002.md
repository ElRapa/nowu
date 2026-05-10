---
id: goal-002
title: "The workflow becomes AI-led, low-friction, and enjoyable to use"
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

- Linked Horizon: "6 Months — The workflow is yours" where AI carries 90–99% of the cycle and the experience is "genuinely enjoyable" with "low friction, clear feedback, visible progress."
- Desired Change: Humans can enter from vague intent and reliably get meaningful progress while the system orchestrates most execution work with minimal operational burden.
- Non-Goals: One-prompt full automation; human replacement; forcing bureaucratic interaction for its own sake.

## Success Criteria

- [ ] Across representative cycles, AI executes the large majority of workflow steps (target band 90–99%) while humans provide directional checkpoints.
- [ ] A user can start from a vague idea and reach a meaningful artifact/output in a single cycle without process breakdown.
- [ ] Users report the experience as low-friction with clear state/next-step visibility in the majority of sessions.
- [ ] At least two active non-software projects sustain progress through this workflow.
- [ ] This goal can be marked `achieved` when high AI execution share and positive low-friction operation are sustained in real usage, not isolated demos.

## UC Mapping

| UC-ID | Title | Stage | Status | Contribution |
| --- | --- | --- | --- | --- |
| NF-01 | Resume Work After Context Loss | v1-core | ACTIVE | Low-friction AI-led restart; agent carries resumption without human reconstruction (T1) |
| NF-02 | Track and Enforce Architectural Decisions | v1-core | ACTIVE | Decisions enforced automatically by review agent; no human policing required (T3) |
| NF-03 | Scope a Piece of Work Without Scope Creep | v1-core | ACTIVE | Agent scopes autonomously; human approves boundaries not execution details (T3, T8) |
| NF-04 | Self-Assess Quality Without Human Intervention | v1-core | ACTIVE | VBR quality gate runs without requiring human involvement in routine checks (T3) |
| NF-05 | Route Approvals Without Blocking Progress | v1-core | ACTIVE | Tiered routing keeps low-risk work flowing; human reviews only what matters (T3) |
| NF-07 | Bootstrap a New Project Using the Framework | v1-core | ACTIVE | Any domain bootstrapped without manual setup overhead; proves workflow generality (T5) |
| NF-08 | Measure and Visualize Framework Health | v1.1 | ACTIVE | Health metrics make AI execution share and friction points visible (T6) |
| NF-09 | Ensure Every Deliverable Traces Back to a UC | v1-core | ACTIVE | Machine-checkable traceability; no manual audit of what AI built (T3, T6) |
| NF-10 | Maintain the Thread for the Multi-Project Human | v1-core | ACTIVE | Fast re-entry on any surface; orientation delivered by AI with minimal friction (T1, T7) |
| NF-11 | Detect Vision Drift | v1.1 | ACTIVE | Periodic alignment visibility; "clear feedback" on strategic direction (T6) |
| NF-12 | Explore a Vague Idea Without Structure | v1-core | ACTIVE | No-commitment mode; vague intent reaches meaningful output without premature structure (T8) |
| NF-13 | Generate Multiple Options at Decision Point | v1-core | ACTIVE | AI generates options at decision points; human chooses without doing the analysis (T3, T8) |
| NF-14 | Track Human-AI Work Ratio | v1.1 | ACTIVE | Measurable AI execution share; surfaces where human friction and cost are highest (T3, T6) |
| NF-16 | Detect and Surface Strategic Drift | v1 | ACTIVE | Visibility into whether sessions advance the right goals; orientates low-friction restarts (T1) |
| AP-01 | Track Regulatory Requirements as Living Knowledge | v1 | ACTIVE | Non-software project flows through same AI-led pipeline; domain agnosticism validated (T5) |
| AP-02 | Manage Product Formulation as Versioned Knowledge | v1 | ACTIVE | Versioned knowledge management proven for non-software domain via same workflow (T5) |
| AP-03 | Model Supply Chain Relationships and Risks | v1.2 | ACTIVE | Supply chain complexity handled through domain-agnostic AI-led workflow (T5) |
| AP-04 | Capture Market Intelligence Over Time | v1.1 | ACTIVE | Temporal intelligence accumulated through domain-agnostic knowledge pipeline (T5) |
| AP-05 | Plan and Track Business Milestones | v1.2 | ACTIVE | Milestone tracking for non-software through same AI-led workflow (T5) |
| AP-06 | Evaluate a Business Decision With Traceability | v1 | ACTIVE | Business decisions structured and AI-evaluated with full traceability (T5, T8) |
| AP-07 | Onboard a Collaborator Into the Project Context | v1.2 | ACTIVE | AI generates role-scoped briefing; collaborator access on any surface (T5, T6, T7) |
| RE-01 | Inventory Existing Processes Before Digitalization | v1 | ACTIVE | Process documentation handled through AI-led workflow for non-software domain (T5) |
| RE-02 | Track Property Data Across Lifecycle Stages | v1.2 | ACTIVE | Property lifecycle handled through domain-agnostic knowledge workflow (T5) |
| RE-03 | Capture Stakeholder Relationships and Constraints | v1.2 | ACTIVE | Stakeholder mapping structured through same AI-led capture workflow (T5) |
| RE-04 | Prioritize Digitalization by Impact and Feasibility | v1.2 | ACTIVE | AI-assisted prioritisation; human reviews recommendations not raw data (T5) |
| RE-05 | Detect Inconsistencies Across Property Records | v2 | ACTIVE | AI-detected inconsistencies; human reviews flagged items only (T5) |
| RE-06 | Support Long-Term Investment Decision Tracking | v1 | ACTIVE | Investment decisions through same AI-led decision workflow as software ADRs (T5) |
| RE-07 | Generate Reports for Different Audiences | v1.2 | ACTIVE | AI generates audience-appropriate reports from project state; no manual compilation (T5, T6, T7) |
| PK-01 | Capture a Thought Before It's Lost | v1-core | ACTIVE | Minimal-friction capture from any surface; AI enriches asynchronously (T7, T8) |
| PK-03 | Maintain a "Today" View Across All Projects | v1-core | ACTIVE | Cross-project daily view on any surface; visible progress without manual assembly (T1, T7) |
| PK-05 | Build Understanding Incrementally Over a Topic | v1.1 | ACTIVE | Agent synthesises fragments so the human avoids repeated research overhead (T8) |
| PK-08 | Interact with nowu from Any Interface | v1 | ACTIVE | Any-device access; review and light actions from mobile cut friction significantly (T7) |
| XP-06 | Allow Multiple Agents to Work Without Conflicts | v2 | ACTIVE | Concurrent agent execution without conflict enables parallel pipeline throughput (T3) |
| XP-07 | Adapt the Framework to a New Domain Without Rewriting | v2 | ACTIVE | Any domain without code changes; AI workflow generalises across all project types (T5) |
| XP-08 | Export Full Project State in Portable Format | v1.1 | ACTIVE | Inspectable AI-generated artifact chain exportable; "clear feedback" for external review (T6) |
| XP-09 | Onboard a New nowu User | v2 | ACTIVE | Progressive disclosure; new users start from vague intent without process overhead (T8) |
| XP-11 | Query Knowledge Graph in Role-Appropriate Format | v1.1 | ACTIVE | Role-appropriate context delivered to agents without human curation between steps (T6) |

## Phase Coverage

| Phase | Epic | Slice Delivered | Status |
| --- | --- | --- | --- |
| v1-core | epic-v1core-002 | Building Trust: options generation & decision recording, decision enforcement, task scoping, VBR quality gate, tiered approval routing, traceability enforcement, epistemic grade recording | APPROVED |

## UC Completion

- Active UCs: 37/37
- Linked to epics: 6/37 (NF-02, NF-03, NF-04, NF-05, NF-09, NF-13)
- Completed captures: 0/37

## Solution Shape

- Form: A self-managing, product-centric workflow layer that orchestrates agents across discovery-through-capture with explicit human intent checks.
- Key Capabilities: End-to-end workflow orchestration; role-specialized agent execution; low-friction checkpoint UX; progress visibility and feedback loops.
- Main Tradeoffs: Constraining human control surfaces to preserve speed and clarity versus allowing unlimited intervention that increases overhead.
- Sequencing Notes: First secure reliable agent handoffs and cycle completion; then optimize friction, enjoyment, and multimodal accessibility for on-the-go usage.

## Epic Seeds

- Seed 1: AI-led full-cycle orchestration with minimal human overhead
