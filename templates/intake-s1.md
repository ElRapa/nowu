***
id: intake-YYYY-MM-DD-slug
created: YYYY-MM-DD
status: DRAFT | READY_FOR_ARCH | BLOCKED
appetite: 2h | 4h | 8h | spike
affected_modules:
  - core
  - flow
use_case_ids:
  - UC-NNN
story_id: ~
***

# Intake Brief (Manual): intake-YYYY-MM-DD-slug

> Use this template when entering S1 directly WITHOUT a pre-workflow intake.
> If a pre-workflow `intake-NNN.md` exists with `status: READY_FOR_S1`, use that instead.

## Problem Statement

[2–3 sentences, user-centric. What is broken or missing? For whom?]

## Context

[What triggered this? Is it part of V1_PLAN.md phase X? Related UC-NNN?]

## Appetite

[How much is this worth solving? If it takes longer, cut scope — not add time.]

## Open Questions

[What must be answered before architecture analysis can proceed?]

***
```yaml
from_step: S1
to_step: S2
agent: nowu-constraints
status: READY_FOR_ARCH
```