---
id: story-v1core-002-s007
source_epic: epic-v1core-002
source_problem: problem-002, problem-003, problem-004
source_use_cases:
  - NF-15
  - NF-02
  - NF-06
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s007 — Decision Evidence and Epistemic Grade Recording

## Story Statement

As Raphael (the multi-project human),
I want every significant decision and options sheet produced by the framework to carry an explicit epistemic grade (drawn from the canonical 5-level scale) and a one-sentence grade justification stating what evidence raises or limits confidence,
So that I can immediately know how much trust to place in an agent output at review time — and so that future sessions can detect when a previously low-confidence decision has been superseded by stronger evidence.

## Appetite

Small — this story adds a required metadata field and justification sentence to decision records and options sheets, updates the producing agents' output contracts, and adds a grade-presence check to the reviewer checklist. It does not implement the full confidence sub-loop or retroactive grading tooling (those are idea-005, routed to v1.1).

## Acceptance Criteria

- **AC-001:** Given a decision agent or options agent produces an output, when the output is written, then it contains an `epistemic_grade` field with one of: SPECULATION, HYPOTHESIS, INFORMED_ESTIMATE, EVIDENCE_BASED, VERIFIED_FACT — and a `grade_justification` sentence of the form "GRADE: [reason evidence raises or limits confidence]."
- **AC-002:** Given a decision record or options sheet is submitted for review (S8), when the reviewer checks the output, then a missing or unjustified `epistemic_grade` is treated as a blocking defect — not a warning — and the output is returned to the producing agent.
- **AC-003:** Given a decision or options output carries a grade below INFORMED_ESTIMATE, when it is presented to Raphael at a human review gate, then the grade and its justification are surfaced prominently (not buried in metadata) — making the confidence gap visible before Raphael approves or rejects the output.
- **AC-004:** Given a lesson or decision was recorded with an epistemic grade, when S9 (Capture) runs at cycle end, then the grade is preserved in the capture record alongside the decision outcome — enabling future calibration of whether that grade level predicted reality accurately.

## Out of Scope (story-level)

1. The full "confidence sub-loop" (trigger research when grade is below a threshold, re-grade after evidence gathering) — routed to idea-005, v1.1.
2. Retroactive grading of existing artifacts (ADRs, decisions, lessons already in `state/`) — v1.1 migration task.
3. Grade-to-grade promotion rules and automated grade tracking over time — idea-005.
4. Grade requirements per altitude level (e.g., STRATEGIC decisions require EVIDENCE_BASED minimum) — idea-004 + idea-005, v1.1.
5. Conflict resolution when two knowledge atoms of different grades contradict each other — XP-04, v1.1.

## Architecture Signals

- Likely touches: templates (decision.md, options-sheet.md — add `epistemic_grade` + `grade_justification` fields)
- Likely touches: flow agents (decision agent, options agent — add grade output to prompt contract)
- Likely touches: S8 reviewer checklist (add grade-presence as blocking check)
- Likely touches: S9 capture record (preserve grade in capture output)
- Vocabulary source: `know/src/know/ontology.json` (`epistemic_grades` block) — must use these exact labels for forward compatibility with `know` integration (can be adapted if needed, but  vocabulary changes require coordination with `know` )

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-15 | Decision Agent / Options Agent | Every significant output carries a grade + justification |
| AC-002 | NF-15 | Quality Agent (S8 Reviewer) | Missing grade is a blocker, not advisory |
| AC-003 | NF-15 | Raphael (multi-project human) | Low-confidence grades are surfaced at human review gates — visible, not buried |
| AC-004 | NF-06 | Curator (S9) | Grade preserved in capture record for future calibration |
