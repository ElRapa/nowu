---
id: problem-006
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-006

## Core Problem

Valuable thoughts arrive at moments when the human is away from a structured environment — on a commute, at a supplier meeting, mid-dinner — but capturing them requires enough friction (opening the right app, choosing a project, applying structure) that most are lost rather than recorded. Separately, the human has no single view of what actually matters across all their projects today: they assemble priorities manually from multiple disconnected systems, which means high-importance work is routinely eclipsed by low-importance but loud items. Both problems leave the human carrying the orientation burden in their own head.

## Validated Personas

**Primary:** Raphael (the multi-project human) — captures thoughts constantly across non-desk contexts; needs the system to meet him wherever he is rather than requiring him to come to it.

## Confirmed Outcome Goals

1. A thought captured in any context — voice, text, brief message, away from a computer — enters the system without requiring categorisation or project routing at capture time; the system handles enrichment asynchronously.
2. The human starts each day with a single, synthesised view of what genuinely matters across all active projects — sorted by importance, not by recency or project.
3. From any device, in any context, the human can capture a thought, check today's priorities, or respond to a light agent query — without opening a CLI session or being at a desk.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| Low-friction capture will actually happen at the required frequency | Accepted as the primary adoption risk. Mitigation: the capture interface must be genuinely faster than a notes app for raw input; the system must demonstrate enrichment quality early to build the habit. | Highest-risk assumption for this problem; must be monitored post-delivery |
| The "today view" can be generated from structured project state without additional instrumentation | Accepted — PK-03 synthesises from existing project artifacts (tasks, decisions, reminders); it does not require a separate data model. | Confirms design: today view reads from existing state, not a new data source |
| Mobile/remote access can share the same knowledge base as the desktop session | Accepted for v1 — PK-08 is explicitly staged as v1 (after v1-core CLI is stable), recognising the core interface must exist first. | Sequencing implication: PK-08 is this problem's last deliverable, after PK-01 and PK-03 are operational |

## Appetite

- [ ] Tiny (< 2 h)
- [x] Small (< 1 day)
- [ ] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** Two tractable sub-problems: frictionless template-based capture (PK-01) and daily cross-project orientation (PK-03). Multi-interface access (PK-08) is deliberately deferred to v1, and async signal enrichment is deferred to v1.1 — the human can work with a structured template and manual enrichment in v1-core without losing long-term value, provided the architecture is designed for async evaluation from the start.

## Out of Scope (explicit)

1. Multi-interface access including mobile / remote (PK-08 — v1 scope). v1-core capture is desktop CLI + structured template only.
2. Async signal enrichment and evaluation — the system will eventually evaluate and enrich captured signals automatically; this is **v1.1+ scope**.
3. Proactive knowledge surfacing without the human asking (PK-02 — v1.1 scope).
4. Knowledge decay and archival (PK-04 — v1.1 scope).
5. Incremental learning synthesis over a topic (PK-05 — v1.1 scope).
6. Sensitivity controls and access tiering for personal knowledge (PK-06 — v1.1 scope).
7. Ingesting external documents (PDF, web URL — PK-07 — v1.1 scope).
8. Cross-project connection discovery — that is problem-007 (XP-01).

## Architecture Signal (P3 input)

Async signal evaluation is a deliberate future capability, not an afterthought. P3 must confirm that the capture data model and storage layer support:
- Appending enrichment results to an existing capture record without mutation of the original signal.
- A pluggable evaluation trigger (manual in v1-core; scheduled or event-driven in v1.1+).
- Idempotent re-evaluation: running enrichment again on the same signal must be safe.

This must not be designed around in v1-core — the architecture should make async evaluation a configuration change, not a redesign.

## Success Criteria

1. A thought captured via desktop CLI using a structured template takes under 2 minutes of human input; the result is project-linked and findable without any additional action.
2. The human's daily orientation view — synthesised across all active projects — surfaces 3–5 genuinely prioritised focus items and is generated without any manual assembly by the human.
3. (v1.1) From a mobile device, the human can capture a new thought and check today's priorities without opening a laptop.

## Dependencies

Requires: problem-001 to be resolved first. The today view (PK-03) synthesises from project state (last thread, pending decisions, tasks), which requires persisted project state from problem-001 to be reliable. PK-08 (multi-interface access) is v1 scope and is sequenced after the core CLI surface is stable.

## UC Coverage

- PK-01: Capture a Thought Before It's Lost
- PK-03: Maintain a "Today" View Across All Projects
