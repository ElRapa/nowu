---
id: story-v1core-001-s004
source_epic: epic-v1core-001
source_problem: problem-006
source_use_cases:
  - PK-03
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-001-s004 — Cross-Project Today View

## Story Statement

As Raphael (the multi-project human),
I want a synthesised view of 3–5 priority items across all my active projects each day,
So that high-importance work is not eclipsed by lower-priority noise and I do not carry the cross-project orientation burden in my own head.

## Appetite

Small — the today view synthesises from existing project state artifacts (tasks, decisions, reminders); it does not require a new data model. The scope is the synthesis and presentation, not the underlying data collection.

## Acceptance Criteria

- **AC-001:** Given at least two active projects each have pending work items or captured reminders, when Raphael requests the today view, then he receives a single synthesised list of 3–5 items ranked by importance across all active projects — not by recency or project order.
- **AC-002:** Given the today view is generated, when Raphael reads it, then every item is traceable to an active project — no synthetic or fabricated items are included — and the source project is visible for each item.
- **AC-003:** Given no new data has been manually entered by Raphael since the last cycle, when the today view is requested, then it is assembled automatically from existing project state records with no manual assembly step required from Raphael.

## Out of Scope (story-level)

1. Proactive push of the today view without Raphael requesting it — that is PK-02, deferred to v1.1.
2. Multi-interface access to the today view from mobile or remote — that is PK-08, deferred to v1.
3. Cross-project connection surfacing — that is story-v1core-004-s001 (XP-01).
4. Personalised ranking model learned from Raphael's past behaviour — manual priority rules are sufficient for v1-core.

## Architecture Signals

- Likely touches: core (cross-project state reader; priority synthesis logic)
- Likely touches: bridge (CLI request handler for today view)
- Likely touches: soul (today view presentation rendering)
- May require: a consistent "pending work" signal across all project state formats so synthesis can operate uniformly
- Unknown whether: priority ranking requires an explicit priority field on each item or can be inferred from item type and recency heuristics

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | PK-03 | Raphael (multi-project human) | Synthesised from existing project state — 3–5 priority items surfaced, ranked by importance not recency |
| AC-002 | PK-03 | Raphael (multi-project human) | No manual assembly required — all items traceable to an active project |
| AC-003 | PK-03 | Raphael (multi-project human) | Generated automatically from existing state — no manual data entry required to produce the view |
