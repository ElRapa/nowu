---
id: idea-004
created: 2026-04-07
status: DRAFT
size: Epic
captured_by: human (Raphael) + external research (Perplexity + Guo et al.)
session: pre-workflow P1→P4 run
related_ucs: NF-06
---

# Idea: 2D Altitude × Phase Workflow Model

## Raw Signal

The current nowu workflow is organised primarily as a 1D pipeline (idea → problem → epic
→ story → implementation). The actual structure needed is 2D:

- **Altitude axis**: Strategic → Product → Architecture → Feature → Implementation
- **Phase axis**: Idea → Problem → Analysis → Options → Decision → Evaluation →
  Implementation → Verification → Learn

Each altitude has its own full loop. Artifacts should declare both altitude and phase
as machine-readable metadata so agents can self-check and runners can enforce valid
transitions.

## Why It Matters

Without altitude metadata, agents tend to "fall downhill" — they start from a strategic
pain and immediately emit features or commands. This happened mildly in problem-005
(appetite rationale contained feature-altitude language during the first pre-workflow run)
and was caught at the human gate.

More importantly: each altitude having its own full loop means that learning at
implementation can correctly trigger upward movement — ARCH_PIVOT, PRODUCT_PIVOT — which
already exist in the workflow. The metadata makes this non-linear promotion explicit and
enorceable by agents rather than relying on human memory of the rule.

## Concrete Direction

Add to frontmatter of all workflow artifacts:
```yaml
altitude: STRATEGIC | PRODUCT | ARCHITECTURE | FEATURE | IMPLEMENTATION
phase: IDEA | PROBLEM | ANALYSIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN
promoted_from: <artifact-id>
promotes_to: <artifact-id>
```

Add altitude + phase contract to each agent prompt — examples:
- `discovery-agent`: writes PRODUCT/ANALYSIS only
- `perspective-interview`: writes PRODUCT/PROBLEM only
- `constraint-check`: ARCHITECTURE/ANALYSIS
- `qa-elicitation`: ARCHITECTURE/ANALYSIS
- `architecture-design`: ARCHITECTURE/OPTIONS
- `atam-lite`: ARCHITECTURE/EVALUATION
- S1–S9: mostly FEATURE and IMPLEMENTATION, with S9 emitting LEARN

## What Is Already There

The workflow already partially implements this model:
- ARCH_PIVOT and PRODUCT_PIVOT from S9 are the upward-movement mechanism
- Each agent is scoped to specific steps (D-005)
- Context scoping rules per step (CLAUDE.md) are proto-altitude rules

What is missing: machine-readable artifact metadata and explicit runner transition rules.

## Open Questions

- How many altitude levels is right — 5 (above) or a simpler 3?
- Does `promotes_to` need to be set at write time or retroactively?
- Does the phase axis need all 9 steps or can it be simplified (PROBLEM / ANALYSIS /
  DECISION / IMPLEMENTATION / LEARN)?
- How does migration work for existing artifacts — forward-only or backfill?

## Routing

Epic-size workflow improvement. Requires a design pass, agent prompt updates (10+
agents), runner enforcement rules, and optional artifact migration.

Do NOT include in v1-core scope. Route to pre-workflow when the first implementation
cycle completes and NF-06 (learn from past mistakes) is operational. This is a strong
candidate for nowu dogfooding its own workflow improvement process — the design decisions
will be much clearer after observing real altitude drift in practice than they are on
paper now.
