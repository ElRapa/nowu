---
id: story-v1core-002-s006
source_epic: epic-v1core-002
source_problem: problem-004
source_use_cases:
  - NF-09
  - NF-06
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s006 — Traceability Enforcement and Cross-Session Learning

## Story Statement

As Raphael (the multi-project human),
I want every acceptance criterion in a delivered task to carry an unbroken link to a use case ID — with missing traces blocking review — and for recurring failure patterns across sessions to be surfaced automatically so the framework can improve,
So that no untraced work reaches completion and the framework demonstrably improves over time rather than repeating the same mistakes.

## Appetite

Small — traceability enforcement is a check at the existing review step (S8); pattern detection reads from existing capture records and review reports, not new instrumentation. The feedback mechanism for NF-06 is an open architecture question requiring a P3 decision (see note below).

## Acceptance Criteria

- **AC-001:** Given a task spec contains acceptance criteria and the work is submitted for review, when the reviewer evaluates the submission, then every acceptance criterion is checked for a traceable link to an active UC-ID — criteria without a traceable UC are recorded as blockers, not warnings, and the work is not forwarded until resolved.
- **AC-002:** Given 100% of acceptance criteria in a reviewed batch carry traceable UC links, when the review passes, then the traceability evidence is recorded in the review artifact — Raphael can confirm coverage without spot-checking individual criteria.
- **AC-003:** Given three or more completed session captures reveal the same failure type (e.g., a repeated scoping mistake, a recurring implementation bug pattern), when the curator runs at cycle close, then the pattern is surfaced in a capture record with explicit references to the prior occurrences — not a generic observation.
- **AC-004:** Given a failure pattern was surfaced in a previous cycle's capture record, when the next cycle's task specs are produced for the same type of work, then the task spec contains a reference to the prior pattern — evidence that it was incorporated rather than ignored.

## Out of Scope (story-level)

1. Automated lesson application without Raphael reviewing and approving the change to agent behaviour.
2. Pattern detection across projects — cross-project lesson transfer is XP-03, deferred to v1.1.
3. Vision drift detection (NF-11 — v1.1 scope).
4. Health dashboards or metrics for traceability coverage trends (NF-08 — v1.1 scope).

## Architecture Signals

- Likely touches: flow (S8 review step — traceability enforcement check; S9 curation step — pattern detection)
- Likely touches: core (UC-ID lookup; traceability field schema in task specs and capture records)
- May require: a structured pattern-detection pass that reads capture records and review reports across the last N cycles
- Unknown whether: the NF-06 feedback mechanism should inject lessons via appended system prompt blocks, a structured memory store queried at agent startup, or constraint fields in task specs — P3 must resolve this with an explicit options comparison covering at least these three approaches before shaping begins

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-09 | AI agent (quality / scoping) | 100% trace coverage enforced at review — missing UC links are blockers, not warnings |
| AC-002 | NF-09 | Raphael (multi-project human) | Traceability evidence in review artifact — Raphael can confirm coverage without spot-checking |
| AC-003 | NF-06 | AI agent (curator) | Pattern detected after 3+ sessions and surfaced in capture record with explicit prior-occurrence references |
| AC-004 | NF-06 | Raphael (multi-project human) | Next cycle shows evidence of pattern incorporation — not repeated in subsequent task specs for same work type |
