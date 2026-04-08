---
id: story-v1core-001-s001
source_epic: epic-v1core-001
source_problem: problem-001
source_use_cases:
  - NF-01
  - NF-10
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-001-s001 — Human Project Orientation on Return

## Story Statement

As Raphael (the multi-project human),
I want to return to any project after any absence and immediately understand where the thread was left, what decisions were made last, and what the recommended next step is,
So that re-orientation takes less than 3 minutes and I can resume productive work without manually consulting commit history, session logs, or prior artifacts.

## Appetite

Medium — two distinct orientation paths must work together: a structured summary of the last completed work and pending action, plus visible access to recent decisions and their rationale. This requires a defined state artifact schema and a production step at the close of every cycle.

## Acceptance Criteria

- **AC-001:** Given a project where at least one work cycle has been completed, when Raphael opens the project for the first time after 7 or more days of absence, then within a single interaction he receives: what was last completed, the most recent decision with its rationale, and the recommended next step — with no manual search required.
- **AC-002:** Given the orientation summary is presented, when Raphael reads it, then all three elements (last completed, last decision, next step) are present and consistent with the actual recorded state of the project — no fabricated or stale content.
- **AC-003:** Given a work cycle closes on any project, when the closing step executes, then an orientation artifact is produced and persisted automatically — no manual action by Raphael is required to generate it.
- **AC-004:** Given Raphael checks a project he has never opened in the current session, when he requests orientation, then the time from request to complete orientation presentation is under 3 minutes — verified across at least 3 distinct projects.
- **AC-005:** Given the orientation artifact exists for a project, when Raphael opens it, then prior decisions are visible with their rationale — not just their outcome — so Raphael can evaluate whether the original reasoning still applies.

## Out of Scope (story-level)

1. Cross-project orientation (a unified view across all projects at once — that is story-v1core-001-s004).
2. Automatic session start without a human confirmation step.
3. Orientation for collaborators or first-time visitors who did not create the project.
4. Historical session analytics or trend data about past sessions.

## Architecture Signals

- Likely touches: core (state artifact schema and persistence protocol)
- Likely touches: flow (work-cycle close step that produces the orientation artifact)
- May require: a defined orientation artifact format readable by both the human and agents
- Unknown whether: the existing SESSION-STATE.md convention is sufficient as the orientation anchor or whether a separate orientation artifact is warranted

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-10 | Raphael (multi-project human) | Human returns after ≥ 7 days and receives usable orientation (what was done, last decision and rationale, recommended next step) within their first interaction |
| AC-002 | NF-01 | Raphael (multi-project human) | Orientation artifact is consistent with actual recorded state — no fabricated or stale content |
| AC-003 | NF-10 | Raphael (multi-project human) | Orientation artifact produced consistently at close of every work cycle with no manual step required |
| AC-004 | NF-10 | Raphael (multi-project human) | Orientation complete in under 3 minutes — confirmed across at least 3 distinct projects |
| AC-005 | NF-01 | Raphael (multi-project human) | Prior decisions visible with rationale — human can evaluate whether original reasoning still applies |
