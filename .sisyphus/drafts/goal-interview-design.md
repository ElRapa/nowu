# Goal Interview Design (Q6–Q9) for vision-bootstrap

## Purpose

Define the post-vision interview extension that introduces Q6, Q7, Q8 (required) and Q9 (optional) in the vision-bootstrap flow.
This design preserves existing Q1–Q5 unchanged and adds goal elicitation after vision synthesis is complete and the human has approved `docs/vision.md`.

## Scope and Non-Goals

- In scope: interview design, synthesis rules, and target output sketch for generated `goal-NNN.md` files.
- Out of scope: editing `.claude/agents/vision-bootstrap.md` in this task.
- Constraint: Q1–Q5 remain exactly as-is.

## Interview Flow

The questions are asked **one at a time**, in the **same session**, only **after vision synthesis is complete** and `docs/vision.md` is approved.

1. Load approved `docs/vision.md`.
2. Extract the Success Horizons (6/12/24 months) as anchor context.
3. Ask Q6 and wait for complete answer.
4. Ask Q7 and wait for complete answer.
5. Ask Q8 and wait for complete answer.
6. Optionally ask Q9 if sequencing/dependencies are not already explicit.
7. Synthesize answers into `goal-001.md`, `goal-002.md`, etc.

Notes:
- The agent should explicitly frame each question around outcome change, not feature inventory.
- Success Horizons are the backbone for grouping and validating goals.
- If answers are incomplete, the agent should request clarification before synthesis.

## Questions (Q6–Q9)

### Q6 — Goal Identification (required)

> "Looking at the Success Horizons you described — what are the distinct outcome goals? Each goal is a change you want to see in the world, not a feature to build. Name them."

### Q7 — Success Criteria (required)

> "For each goal: what would prove it's achieved? What would you measure or observe?"

### Q8 — Solution Shape / Key Capabilities (required)

> "For each goal: what capabilities or systems need to exist for this to work? How do they connect to each other?"

### Q9 — Sequencing (optional)

> "Which goals depend on other goals being done first? What's the natural sequence?"

## Synthesis

The agent converts interview answers into goal files using deterministic mapping rules:

- Q6 answers → goal titles and **Outcome Goal** section.
- Q7 answers → **Success Criteria** section.
- Q8 answers → **Solution Shape / Key Capabilities** section.
- Q9 answers → **Sequencing Notes** subsection inside Solution Shape / Key Capabilities.

Additional synthesis rules:

- `UC Mapping` table starts empty (headers only).
- `Phase Coverage` table starts empty (headers only).
- Frontmatter defaults: `status: proposed`, `altitude: PRODUCT`, `phase: DECISION`.
- Goal count is agent-determined from vision/interview content.
- Soft cap is 8 goals. If >8 emerge, flag this explicitly and defer final split/merge decision to human.
- Numbering convention is strictly sequential: `goal-001`, `goal-002`, ...

## Output Format

Generated goal files should follow this structure (brief sketch):

```md
---
id: goal-001
status: proposed
altitude: PRODUCT
phase: DECISION
---

# Goal 001 — <Title from Q6>

## Outcome Goal
<Outcome statement from Q6>

## Success Criteria
- <Criterion from Q7>

## Solution Shape / Key Capabilities
- <Capability/system from Q8>

### Sequencing Notes
- <Dependency/sequence from Q9, if provided>

## UC Mapping
| UC ID | Relationship | Notes |
| --- | --- | --- |

## Phase Coverage
| Phase | Coverage | Notes |
| --- | --- | --- |
```

## Guardrails

- Do not alter or reinterpret Q1–Q5.
- Do not generate implementation tasks at this stage.
- Keep language at outcome/goal level (product intent), not technical decomposition.
