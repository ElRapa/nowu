---
id: goal-NNN              # e.g. goal-001
title: ""                 # Short outcome-focused title (not a feature name)
status: proposed          # proposed|approved|in_delivery|partially_validated|achieved|retired
parent_vision_horizon: "" # "6 Months"|"12 Months"|"24 Months" — quote verbatim from vision.md
created: YYYY-MM-DD
linked_epics:             # epic IDs that deliver this goal (fill as epics are created)
  - epic-NNN
retired_reason:           # optional — fill only when status: retired
---

# Goal Brief: goal-NNN — [Title]

## Outcome Goal

[What change do we want in the world? Describe the desired outcome, not the solution.
Keep this grounded in the Success Horizon above — no reinterpretation.]

**Linked Horizon:** [Quote the horizon name verbatim from vision.md — e.g. "6 Months — The workflow is yours"]
**Desired Change:** [1-2 sentences — what is measurably different when this goal is achieved?]
**Success Signals:** [2-3 observable indicators that the goal is being achieved — no dashboards needed]
**Non-Goals:** [What this goal explicitly does NOT address — be specific]

## Solution Shape

[What form does the solution take? High-level shape only — no architecture prescriptions.
This scopes the playing field without dictating the implementation. ADRs win on any conflict.]

**Form:** [e.g. "A workflow step", "A persistent data layer", "A CLI command sequence"]
**Key Capabilities:** [What the solution must enable — 2-4 items, outcome-framed]
**Main Tradeoffs:** [What you are accepting vs. deferring — be honest]
**Sequencing Notes:** [What must exist before this goal can be delivered?]
**Epic Seeds:** [Candidate epic titles — do not create epic files here, just name them]
