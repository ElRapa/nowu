---
id: story-v1core-002-s003
source_epic: epic-v1core-002
source_problem: problem-003
source_use_cases:
  - NF-03
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s003 — Task Scoping and Scope Enforcement

## Story Statement

As Raphael (the multi-project human),
I want every task entering execution to carry an explicit in-scope boundary, explicit exclusions, and measurable acceptance criteria — and for the implementer to be held to that boundary,
So that the pipeline never delivers work that reached beyond what was approved and I can trust that execution stays within the agreed scope.

## Appetite

Small — scoping is a shaping step (S5) that produces a bounded task spec; enforcement is a check in the review step (S8). Both operate on existing workflow steps with defined artifact schemas.

## Acceptance Criteria

- **AC-001:** Given a task is promoted to execution (S5 shaping complete), when the task spec is produced, then it contains: a named list of in-scope items, a named list of explicit exclusions, and at least one measurable acceptance criterion — before the implementer begins work.
- **AC-002:** Given the task spec defines an in-scope boundary and the implementer completes the work, when the reviewer checks the submission, then any modification outside the declared in-scope boundary is flagged as a scope violation and treated as a blocker — not a warning.
- **AC-003:** Given a task spec has been produced, when the reviewer evaluates completeness, then every acceptance criterion in the spec has a corresponding verifiable outcome in the submitted work — unresolved criteria are flagged as blockers.

## Out of Scope (story-level)

1. Automated scope violation prevention at the moment of modification — enforcement is at review time (S8), not inline during implementation.
2. Health metrics or scope-creep trend tracking across multiple cycles (NF-08 — v1.1 scope).
3. Non-technical task verification (documentation, diagrams) — VBR scope is code-producing tasks only.
4. Dynamic scope expansion during execution — any scope change requires a new shaping step.

## Architecture Signals

- Likely touches: flow (S5 shaping step — task spec schema; S8 review step — scope enforcement check)
- Likely touches: core (task spec schema definition; in-scope/exclusion field conventions)
- May require: a machine-readable in-scope field format that the reviewer can compare to the actual list of modified items
- Unknown whether: scope enforcement compares against a declared file list, a declared capability list, or both

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-03 | AI agent (shaper) | Scope defined before execution — in-scope items, exclusions, and measurable ACs all present in task spec |
| AC-002 | NF-03 | Raphael (multi-project human) / AI agent (reviewer) | No out-of-scope modifications reach review — scope violations are blockers |
| AC-003 | NF-03 | Raphael (multi-project human) | Every AC in the spec has a verifiable outcome — incomplete criteria are blockers at review |
