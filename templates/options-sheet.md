---
id: intake-id-options
intake_id: intake-YYYY-MM-DD-slug
created: YYYY-MM-DD
status: DRAFT | READY_FOR_DECISION
recommended_option: A | B | C
---

# Options Sheet

## Option A: [Name]

[1 paragraph approach description]

| QA Attribute | Weight | Score (H=3 M=2 L=1) | Weighted |
|---|---|---|---|
| Simplicity | 5 | H | 15 |
| Testability | 5 | H | 15 |
| Modifiability | 4 | M | 8 |
| Performance | 2 | M | 4 |
| Migration Cost | 3 | L | 3 |
| **Total** | | | **45** |

**Trade-off points:** [what this improves / what it hurts]
**Effort:** Nh -- [within / exceeds] appetite
**Migration path:** [if applicable]

## Option B: [Name]

[same structure]

## Option C: [Name] (if needed)

[same structure]

## Recommendation

Option [X] recommended because [rationale referencing QA scores and constraints].

---
```yaml
from_step: S3
to_step: S4
agent: nowu-decider
status: READY_FOR_DECISION
```
