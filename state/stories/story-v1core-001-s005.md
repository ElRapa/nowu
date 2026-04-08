---
id: story-v1core-001-s005
source_epic: epic-v1core-001
source_problem: problem-001
source_use_cases:
  - NF-16
  - NF-10
  - NF-01
created: 2026-04-08
status: DRAFT
stage_target: v1
deferred_from: v1-core
deferral_reason: Requires goal layer artifacts (idea-006) and cross-artifact drift query that does not exist in v1-core. Thread resumption (s001) is the correct v1-core foundation.
---

# Story: story-v1core-001-s005 — Vision-Aligned Session Orientation

## Story Statement

As Raphael (the multi-project human),
I want each session start to show me not only where the thread was left, but also what open goals, unaddressed ideas, and uncovered use cases have no active work toward them,
So that I can detect when I have been productive but drifting — working on things that felt natural next but were not aligned to what matters most.

## Appetite

Small — session start orientation is already handled by s001. This adds a drift-detection layer on top: query open goals with no active epic, ideas without follow-up tasks, and UCs without story coverage, then surface a concise "alignment pulse" alongside the standard orientation. No learning, no scoring — purely a query and display step.

## Acceptance Criteria

- **AC-001:** Given a project where at least one goal artifact exists, when Raphael starts or resumes a session, then the orientation surface shows: (a) any goals with no active epic assigned, (b) any DRAFT ideas with no derived story or intake, and (c) any ACTIVE UCs in the project's UC group that have no coverage in current epics or stories — each as a concise single-line entry.
- **AC-002:** Given the alignment pulse is shown, when Raphael reads it, then the entries are accurate — no false positives (items that do have active work) and no false negatives (items that don't but are not shown).
- **AC-003:** Given all goals, ideas, and UCs have active work, when orientation runs, then the alignment pulse shows "All goals covered — no drift detected" and does not pad the output with empty sections.
- **AC-004:** Given Raphael has had N consecutive sessions that did not touch a specific named goal, when orientation runs, then that goal is flagged as "not addressed in last N sessions" — a passive drift signal, not a blocking alert.
- **AC-005:** Given the alignment pulse surfaces an uncovered goal or idea, when Raphael chooses to act on it, then the orientation can hand off directly to the appropriate workflow entry point (e.g., start pre-workflow for an unaddressed idea, or start S1 for an uncovered UC).

## Out of Scope (story-level)

1. Automated prioritization or scoring of which gap to address first — human decides.
2. Cross-project alignment pulse (comparing drift across all projects simultaneously).
3. Behavioral changes pushed to agents based on drift patterns — all drift signals are informational only.
4. Calendar integration or deadline-based prioritization.
5. Anything built on goal layer artifacts until idea-006 is shaped and goal-NNN.md files exist — AC-001 depends on this.

## Architecture Signals

- Depends on: goal layer artifacts (`state/goals/goal-NNN.md`) — not yet created; blocked by idea-006
- Depends on: UC coverage index — a query over stories showing which UC-IDs have no story referencing them
- Depends on: s001 orientation artifact schema — s005 extends the same artifact, not a separate surface
- May require: a lightweight "coverage map" step at cycle close (S9) that writes which UCs/goals are covered vs. open

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-16 | Raphael (multi-project human) | Orientation surface shows open goals, unaddressed ideas, uncovered UCs accurately |
| AC-002 | NF-16 | Raphael (multi-project human) | No false positives or negatives in alignment pulse entries |
| AC-003 | NF-16 | Raphael (multi-project human) | Clean "no drift" output when all items have active work |
| AC-004 | NF-16 | Raphael (multi-project human) | Passive drift signal shown when a goal has not been touched in N sessions |
| AC-005 | NF-10 | Raphael (multi-project human) | Alignment pulse can hand off to workflow entry point for any surfaced gap |
