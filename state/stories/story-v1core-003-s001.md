---
id: story-v1core-003-s001
source_epic: epic-v1core-003
source_problem: problem-005
source_use_cases:
  - NF-12
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-003-s001 — Lightweight Idea Exploration

## Story Statement

As Raphael (the multi-project human),
I want to enter a half-formed idea with no required structure and receive clarifying questions and optional light research in return — with no binding artifact created unless I explicitly ask for one,
So that early-stage thoughts can enter the system without being killed by premature structure and discarded or promoted at any point on my own terms.

## Appetite

Small — idea exploration is a lightweight input mode with a minimal record schema. The clarifying-questions response is the primary output; research is optional. No intake artifact, no project scaffold, and no mandatory fields.

## Acceptance Criteria

- **AC-001:** Given Raphael has a vague thought he wants to explore, when he enters it into the system with no additional structure or categorisation, then the system accepts it, stores the raw input, and responds with 2–4 clarifying questions — within the same interaction and without requiring any additional fields to be filled.
- **AC-002:** Given the system has responded with clarifying questions, when Raphael decides to discard the idea, then no binding artifact has been created — the exploration record can be discarded at any point without any workflow or approval step.
- **AC-003:** Given Raphael has explored an idea across one or more sessions, when he explicitly requests promotion to a fuller artifact (discovery record, problem statement, or project intake), then the existing exploration notes carry forward into the promoted artifact — no information is lost and no re-entry is required.

## Out of Scope (story-level)

1. Automatic promotion of an idea based on maturity signals — promotion is always human-initiated.
2. Project scaffolding or bootstrapping within this story — that is story-v1core-003-s002.
3. Domain-specific template layers for AP or RE — those are deferred to problem-008 scope.
4. Multi-session idea decay or automatic archival of un-promoted captures.

## Architecture Signals

- Likely touches: core (exploration record schema — zero mandatory fields beyond the raw input)
- Likely touches: soul (clarifying-questions generation; optional research response)
- Likely touches: bridge (CLI exploration entry point — distinct from structured intake)
- May require: a lifecycle state on the exploration record (e.g., seed → explored → promoted) that carries forward cleanly on promotion
- Unknown whether: exploration records live in the current project's context, a separate sandbox space, or a global ideas namespace

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-12 | Raphael (multi-project human) | Entered in under 2 minutes — no mandatory fields — clarifying questions provided in the same interaction |
| AC-002 | NF-12 | Raphael (multi-project human) | No binding artifact created — discardable at any point without a workflow step |
| AC-003 | NF-12 | Raphael (multi-project human) | Promotable when ready — exploration notes carry forward with no re-entry required |
