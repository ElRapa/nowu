---
id: story-v1core-004-s004
source_epic: epic-v1core-004
source_problem: problem-008
source_use_cases:
  - RE-01
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-004-s004 — RE Process Documentation as Structured Knowledge

## Story Statement

As Raphael (the multi-project human),
I want core RE business processes documented as structured knowledge — with steps, handoffs, participants, and at least one identified bottleneck per process — sufficient to make a confident prioritisation decision about the first digitalisation sprint,
So that the digitalisation effort starts from a verified understanding of how the business actually operates today, not from assumptions.

## Appetite

Small — the deliverable is the right number of documented processes to make the prioritisation decision, not a comprehensive process inventory. The scope is explicitly outcome-gated: enough to decide, no more.

## Acceptance Criteria

- **AC-001:** Given the RE project is bootstrapped, when core business processes are documented as structured knowledge records, then each process record contains: the sequence of steps, the participants at each step, the inputs and outputs, and at least one identified bottleneck — all captured from direct knowledge input, not synthesised from assumptions.
- **AC-002:** Given the documented processes exist in the knowledge base, when Raphael applies them to prioritise the first digitalisation sprint, then the documentation is sufficient to rank at least 3 processes by impact and feasibility — confirming the documentation threshold has been met.
- **AC-003:** Given the process documentation is complete, when Raphael reviews it, then the bottlenecks identified are specific and actionable — not generic observations — and each links to the step in the process where it occurs.

## Out of Scope (story-level)

1. Prioritisation tooling or scoring models for the digitalisation decision — the documentation is the deliverable; the prioritisation decision itself is Raphael's.
2. Property lifecycle tracking, stakeholder mapping, or digitisation impact analysis (RE-02, RE-03, RE-04 — v1.2 scope).
3. Investment decision analytics across multiple properties — the first RE investment decision is story-v1core-004-s003.
4. Report generation for external audiences (RE-07 — v1.2 scope).
5. Determining the exact number of processes to document in advance — the stopping criterion is "enough to confidently prioritise the first sprint", not a fixed count.

## Architecture Signals

- Likely touches: know (structured process knowledge atoms; step sequencing; participant and bottleneck fields)
- Likely touches: core (RE project context; process record schema)
- Likely touches: soul (process documentation session agent — elicits steps, participants, handoffs, and bottlenecks through structured questions)
- May require: a process knowledge atom type distinct from decision records and regulatory requirements — with step sequencing as a first-class field
- Unknown whether: the existing knowledge atom model supports ordered step sequences natively or requires a compositional pattern (parent process → ordered child steps)

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | RE-01 | Raphael (multi-project human) | Process records contain steps, participants, inputs/outputs, and at least one bottleneck — captured from direct knowledge, not assumptions |
| AC-002 | RE-01 | Raphael (multi-project human) | Enough processes documented to make the digitalisation prioritisation decision — at least 3 processes rankable by impact and feasibility |
| AC-003 | RE-01 | Raphael (multi-project human) | Bottlenecks are specific and actionable — linked to the step where they occur, not generic observations |
