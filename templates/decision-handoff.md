***
id: intake-NNN-decision
intake_id: intake-NNN
decision_id: D-NNN
created: YYYY-MM-DD
status: READY_FOR_SHAPING
***

# Decision Handoff: [intake-id]

## What Was Decided

[1-paragraph summary of D-NNN for the shaper — what approach was chosen and why,
without repeating the full decision document.]

## Chosen C4 L2 View

```mermaid
C4Container
  %% The winning option's module interaction diagram
  %% Show only the affected containers and their interactions
```


## Key Constraints for Shaper

[What the shaper MUST NOT violate — from the decision + binding contracts]

1. [constraint]
2. [constraint]

## Suggested Task Decomposition (hint — not binding)

[Architect's first guess at task breakdown. Shaper may revise based on file tree.]

1. [task hint]
2. [task hint]

***
```yaml
from_step: S4
to_step: S5
agent: nowu-shaper
status: READY_FOR_SHAPING
```