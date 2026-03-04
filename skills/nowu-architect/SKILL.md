---
name: nowu-architect
description: Architecture analysis and decision workflow for the nowu framework. Use when defining or revising module boundaries, interface contracts, ADRs, integration strategy with know, or evaluating competing designs before implementation.
---

# Nowu Architect

Use this skill to produce architecture decisions that are executable by AI agents and traceable over time.

## Workflow

1. Load minimum context.
- Read `ARCHITECTURE.md`, `V1_PLAN.md`, `WORKFLOW.md`, and relevant sections of `USE_CASES.md`.
- Read `DECISIONS.md` before proposing new architecture choices.

2. Define the decision surface.
- State the affected modules and boundaries.
- State the use-case IDs being optimized.
- State non-negotiable constraints (for example: `know` is external system-of-record).

3. Generate options.
- Produce 2-3 realistic options.
- For each option, specify interfaces, ownership, and migration impact.

4. Evaluate options.
- Use the rubric in `references/architecture-rubric.md`.
- Score delivery speed, reliability, modularity, operational cost, and governance.

5. Commit a decision.
- Select one option and record rationale.
- Record explicit risks and mitigations.
- If architecture changes, update `ARCHITECTURE.md`, `V1_PLAN.md`, and `DECISIONS.md`.

6. Emit implementation guidance.
- Produce boundaries, invariants, and test requirements.
- Hand off to shaper with strict scope language.

## Output Contract

Always output:

1. Problem statement (1-3 lines)
2. Option table with scores
3. Selected option and rationale
4. Risks and mitigations
5. Required file or contract updates

## Guardrails

- Do not jump to implementation before option evaluation.
- Do not choose options that bypass `know` persistence contracts.
- Do not expand scope beyond referenced use-case IDs.
- Prefer reversible architecture choices when uncertainty is high.

## Resources

- Scoring rubric: `references/architecture-rubric.md`

