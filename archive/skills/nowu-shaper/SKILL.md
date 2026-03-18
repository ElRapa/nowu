---
name: nowu-shaper
description: Task-shaping workflow for nowu implementation work. Use when turning ideas or architecture decisions into bounded, dependency-aware execution plans with acceptance criteria and verification commands.
---

# Nowu Shaper

Use this skill to convert goals into small, executable tasks that AI agents can complete reliably.

## Workflow

1. Load inputs.
- Read the relevant decision/architecture context.
- Extract target use-case IDs.
- Identify module boundaries and non-goals.

2. Define scope boundaries.
- State in-scope work in concrete terms.
- State out-of-scope items explicitly.
- Mark dependencies and sequencing constraints.

3. Slice work.
- Break into tasks that target <=4 hours each.
- Keep each task vertically meaningful (not random file churn).

4. Specify each task.
- Goal
- Changed files/modules
- Acceptance criteria
- Verification commands
- Rollback/mitigation notes

5. Validate shape quality.
- Use checklist from `references/task-shaping-template.md`.
- Reject tasks with ambiguous done state or missing tests.

6. Publish execution order.
- Sequence tasks by dependency graph.
- Highlight parallel-safe tasks.

## Output Contract

For each task, always provide:

1. ID and title
2. use-case IDs covered
3. in-scope / out-of-scope
4. acceptance criteria (testable)
5. verification command list

## Guardrails

- Do not produce tasks without explicit acceptance criteria.
- Do not mix multiple modules in one task unless required by a contract boundary.
- Do not hide architecture changes inside implementation tasks.
- If a task cannot be verified, split it or redesign it.

## Resources

- Template and checklist: `references/task-shaping-template.md`

