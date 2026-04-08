---
id: story-v1core-001-s002
source_epic: epic-v1core-001
source_problem: problem-001
source_use_cases:
  - NF-01
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-001-s002 — Agent Checkpoint Resumption

## Story Statement

As an AI agent operating within the nowu workflow pipeline,
I want to read persisted state at the start of a new session and identify the last verified checkpoint,
So that I propose the correct next action without repeating completed steps or contradicting prior decisions.

## Appetite

Small — checkpoint detection reads from existing persisted state artifacts; no new data model is required. The scope is the agent's ability to identify the resume point, not the broader human orientation experience.

## Acceptance Criteria

- **AC-001:** Given a work cycle was interrupted at any step (S1 through S8) and the session ended, when a new session starts for that cycle, then the agent reads the persisted state and identifies the step at which work was last verified as complete — without asking the human to describe what was done.
- **AC-002:** Given the agent has identified the last verified checkpoint, when it proposes the next action, then it does not re-execute any step already marked complete in the persisted state — verified across at least 3 distinct mid-cycle interruption scenarios.
- **AC-003:** Given the persisted state contains a prior decision record, when the agent proposes actions in the resumed session, then none of those proposed actions contradict the recorded decisions in the prior session's state.

## Out of Scope (story-level)

1. Human-facing project orientation (that is story-v1core-001-s001).
2. Automatic resumption without a human confirmation gate — the agent proposes, the human confirms.
3. Cross-step rollback or state repair if the persisted state is corrupt or incomplete.

## Architecture Signals

- Likely touches: core (persisted state schema; checkpoint markers)
- Likely touches: flow (session start step that reads checkpoint and proposes next action)
- May require: a checkpoint marker or status field in each step's state artifact
- Unknown whether: the existing step-level status conventions are sufficient or whether an explicit checkpoint index is needed

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-01 | AI agent (workflow pipeline) | Agent reads persisted state, identifies last verified checkpoint, and proposes correct next action within first response — without hallucinating progress |
| AC-002 | NF-01 | AI agent (workflow pipeline) | No completed task is re-executed — verified across at least 3 distinct mid-cycle interruption scenarios |
| AC-003 | NF-01 | AI agent (workflow pipeline) | Agent correctly identifies the resume point and does not contradict prior recorded decisions |
