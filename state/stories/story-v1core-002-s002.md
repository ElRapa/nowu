---
id: story-v1core-002-s002
source_epic: epic-v1core-002
source_problem: problem-002
source_use_cases:
  - NF-02
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s002 — Decision Enforcement by Reviewer

## Story Statement

As Raphael (the multi-project human),
I want the reviewer agent to flag any implementation that contradicts a recorded decision before the work reaches my review queue,
So that decision violations are caught automatically, Raphael is notified of the specific contradiction, and work is not forwarded until the conflict is resolved.

## Appetite

Small — enforcement is a check layer on the existing review step (S8); it reads recorded decisions and compares them against the delivered work's scope and outputs. No new data model is required beyond the decision records produced by story-v1core-002-s001.

## Acceptance Criteria

- **AC-001:** Given a decision record exists for any project and an agent submits work for review, when the reviewer agent runs, then it checks the submitted work's scope and outputs against all recorded decisions that are relevant to that scope.
- **AC-002:** Given the submitted work contradicts a recorded decision, when the reviewer agent detects the contradiction, then the work is flagged as blocked with a specific reference to the decision record being violated — and the work is not forwarded to the human review queue until the contradiction is resolved.
- **AC-003:** Given a flagged contradiction is identified, when Raphael is notified, then the notification contains: which decision is being violated, the specific nature of the contradiction, and a reference to the original decision record — not a generic warning.

## Out of Scope (story-level)

1. Automatic resolution of decision conflicts without human input.
2. Enforcement of draft or proposed decisions — only ACCEPTED decisions are enforced.
3. Detection of vision drift across sessions (NF-11 — v1.1 scope).
4. Conflict resolution between two decisions that contradict each other (XP-04 — v1.1 scope).

## Architecture Signals

- Likely touches: flow (S8 review step — decision enforcement check)
- Likely touches: core (decision record retrieval; scope-to-decision matching)
- May require: a machine-readable field in each decision record identifying the scope or domain to which it applies, so the reviewer can match relevant decisions to the work under review
- Unknown whether: the enforcement check can operate on the existing work output format or requires a new structured diff input

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-02 | AI agent (reviewer) | Reviewer checks submitted work against all relevant recorded decisions |
| AC-002 | NF-02 | Raphael (multi-project human) | Contradictions detected and work blocked — human never receives unverified or decision-violating work |
| AC-003 | NF-02 | Raphael (multi-project human) | Specific contradiction surfaced with decision reference — not a generic flag |
