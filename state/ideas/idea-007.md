---
id: idea-007
created: 2026-04-30
status: DRAFT
size: Story
source: Dogfooding
related_ucs: NF-06
---

# Idea: Failing is a Valid Outcome

## Raw Signal

When a cycle ends without delivering the intended feature — appetite exceeded, blocked, wrong direction — the system currently has no way to capture this explicitly. Failure gets left in limbo or forced into a success shape. We should support capturing failure as a first-class outcome: record the failure mode and reason so future cycles can learn from it.

## Source

- [x] Personal frustration
- [ ] User feedback
- [ ] Market observation
- [ ] Technical opportunity
- [ ] Other: ___

## Initial Appetite Guess

- [ ] Tiny (< 2 h)
- [x] Small (< 1 day)
- [ ] Medium (2-3 days)
- [ ] Large (1 week+)
- [ ] Unknown -- needs decomposition

## Why Now?

The workflow already tracks session state and cycle outcomes — adding a failure outcome type is a natural extension before more cycles accumulate without a clean close.

## Related Context

- Related ideas: idea-006 (goal layer — failed cycles affect goal progress)
- Related use cases: NF-06 (learn from past mistakes)
