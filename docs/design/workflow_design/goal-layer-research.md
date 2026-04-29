# Goal Layer Research

**Date:** 2026-04-29

## Framework Comparison Table

| Framework | Goal Artifact | Solution Artifact | Unified? |
|---|---|---|---|
| Shape Up (Basecamp) | Appetite | Shaped Concept | Unified (pitch) |
| OKR (Doerr) | Objective | Key Results | Separate |
| Continuous Discovery (Torres) | Opportunity | Solution Tree | Separate |
| Inspired (Cagan) | Outcome | Feature | Separate |
| Lean Startup | Hypothesis | MVP | Separate |
| SVPG (Cagan) | Problem | Solution | Separate |
| nowu | Outcome Goal | Solution Shape | **Unified** (Goal Brief) |

## Why Unified for nowu

- 6/7 frameworks separate goals/solutions, but unified suits solo builder + AI agents context
- Thin goals (outcome only) get interpreted inconsistently by agents without solution shape context
- Shape Up's "pitch" model is the closest analog — combines why + what in one bounded artifact
- 3-5 artifact layers optimal (Cagan, Torres, Perri, Kniberg); adding Goals = 5 layers (upper bound, supported)
- McKinsey 2017: 70% strategy execution failure without intermediate goal checkpoints

## Failure Modes WITHOUT This Layer

1. **Strategy gap**: epics created ad-hoc without outcome anchoring → vision drift over 6-month cycles
2. **Premature convergence**: AI agents jump to solutions without validating the outcome goal
3. **Vision drift**: 6-month cycles drift from 24-month intent without intermediate checkpoints
4. **Agent inconsistency**: AI interprets "build X" differently without a "why" artifact to reference

## Oracle Recommendation

- Unified Goal Brief (outcome + solution shape in one artifact)
- Location: `docs/goals/` (durable reference, not transient state)
- Creation timing: at vision approval, before epics
- Keep under 1 page — if bigger, the goal is too broad
- Lifecycle: proposed → approved → in_delivery → partially_validated → achieved → retired

## Metis-Identified Risks (Addressed)

- Goal lifecycle across multiple epics → tracked via status field + linked_epics list
- Approval tier → Tier 2 (batch for human review)
- Retirement process → `retired` status with `retired_reason` field
- Agent guardrails → story-mapper enforces non-TBD parent_goal; health-goals validates goal health

## Decision

Unified Goal Brief adopted over separate goal+solution artifacts because:
- Agents need both context dimensions simultaneously to avoid misinterpretation
- Solo builder context: separate artifacts create coordination overhead with no benefit
- Shape Up evidence: unified pitch model prevents scope creep better than split artifacts