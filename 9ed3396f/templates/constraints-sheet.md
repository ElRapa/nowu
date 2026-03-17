---
# Constraints Sheet
id: <intake-id>-constraints
intake_id: intake-<YYYY-MM-DD>-<slug>
created: YYYY-MM-DD
status: DRAFT | READY_FOR_OPTIONS | BLOCKED
c4_l1_update_needed: false
affected_modules: [core]
---

## Fixed Constraints
<!-- Each must reference a D-NNN or a hard technical fact -->
- constraint: "..."
  source: D-NNN | technical reason

## Flexible Constraints
<!-- What CAN be changed if needed -->

## Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| ...  | high/med/low | ... |

## Assumptions
| Assumption | Validated |
|-----------|-----------|
| ...       | true/false/unknown |

## Open Questions for S3
<!-- What must Options Designer resolve? -->

## C4 L1 Update (if needed)
```mermaid
<!-- Only include if c4_l1_update_needed = true -->
```

## Handoff
```yaml
from_step: S2
to_step: S3
agent: nowu-options
status: READY_FOR_OPTIONS
```
