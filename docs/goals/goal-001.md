---
id: goal-001
title: "Continuity"
status: proposed
parent_vision_horizon: "6 Months — The workflow is yours"
created: 2026-04-29
linked_epics:
  - epic-v1core-001
  - epic-v1core-003
retired_reason:
---

# Goal Brief: goal-001 — Continuity

## Outcome Goal

**Linked Horizon:** "6 Months — The workflow is yours"
**Desired Change:** Any project can be picked up after a real interruption — days, weeks — and work resumes without re-orientation overhead. The thread holds: where things stand, what was decided, and what comes next are all recoverable from the artifacts alone.
**Success Signals:**
- Returning to a project after an interruption takes under five minutes to reach a resumable state
- No decisions or reasoning are lost between work cycles
- Captures made in the moment of work remain findable and contextually linked when next needed
**Non-Goals:** This goal does not address knowledge sharing across multiple projects, searchability across a portfolio, or making the workflow faster per se — only that it survives interruption without degradation.

## Solution Shape

**Form:** A persistent context layer and a frictionless in-cycle capture mechanism
**Key Capabilities:**
- Persisted project state that survives session endings and tool restarts
- Structured capture flow that costs less than two minutes per signal
- Re-entry point that reconstructs where-things-stand from stored artifacts alone
- Cycle lifecycle management so no work-in-progress is silently abandoned
**Main Tradeoffs:** Accepting that the initial capture format is structured enough to be retrievable but not yet semantically queryable across projects — that belongs to goal-003. Deferring cross-project connection surfacing entirely.
**Sequencing Notes:** Must be the first goal delivered; every other epic depends on reliable persisted context and frictionless capture being in place before building on top.
**Epic Seeds:** Continuity & Capture, Workflow Cycle Engine
