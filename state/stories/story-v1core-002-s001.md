---
id: story-v1core-002-s001
source_epic: epic-v1core-002
source_problem: problem-002
source_use_cases:
  - NF-02
  - NF-13
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s001 — Options Generation and Decision Recording

## Story Statement

As Raphael (the multi-project human),
I want the system to generate at least two well-reasoned options with explicit tradeoffs at every identified decision point, and record the chosen option and rejected alternatives with full rationale,
So that six months later I can retrieve any significant decision and understand what was chosen, why, what was considered but rejected, and what conditions existed at the time — without replaying the original analysis.

## Appetite

Small — options generation and decision recording are two sequential steps at a single decision point. The cross-domain application (AP-06, RE-06) is addressed in epic-004; this story delivers the core decision mechanism for the framework itself.

## Acceptance Criteria

- **AC-001:** Given a decision point is identified during any workflow step, when the decision agent runs, then at least two distinct options are presented to Raphael with explicit tradeoffs stated for each — before any option is committed.
- **AC-002:** Given Raphael selects an option, when the decision is recorded, then the decision record contains: the chosen option with its rationale, all rejected alternatives with their reasons for rejection, and the conditions known at the time of the decision.
- **AC-003:** Given a decision record exists for any project, when Raphael retrieves it 6 months later (simulated by retrieval without any session context), then he can read the chosen path, rationale, rejected alternatives, and original conditions — without consulting git history, session logs, or any external notes.

## Out of Scope (story-level)

1. Domain-specific decision templates for AP or RE — those are applied in story-v1core-004-s003.
2. Automatic detection of when conditions have changed and a prior decision should be revisited — that is NF-11, deferred to v1.1.
3. Conflict resolution across decision records (XP-04 — v1.1 scope).
4. Retrospective analytics across multiple decision records.

## Architecture Signals

- Likely touches: flow (decision step — options generation and recording protocol)
- Likely touches: core (decision record schema; storage and retrieval)
- Likely touches: soul (options presentation rendering)
- May require: a structured decision record format with required fields for options, rationale, conditions, and timestamp
- Unknown whether: decision records should share the same storage layer as ADRs or occupy a separate namespace

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-13 | Raphael (multi-project human) | At any decision point, at least two distinct well-reasoned options with explicit tradeoffs are generated before a choice is committed |
| AC-002 | NF-02 | Raphael (multi-project human) | Chosen path, rejected alternatives, rationale, and conditions recorded in a single decision record |
| AC-003 | NF-02 | Raphael (multi-project human) | Decision retrievable 6 months later without context prompting — options, rationale, rejected alternatives, and conditions all present |
