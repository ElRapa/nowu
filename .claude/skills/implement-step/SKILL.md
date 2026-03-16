---
name: implement-step
description: Implement a specific V1 plan step. Use when you want to execute a single step from V1_PLAN.md with full TDD and VBR.
---

# Implement V1 Step

Execute one step from docs/V1_PLAN.md following the full workflow.

## Before Starting
1. Read docs/V1_PLAN.md — find the step to implement
2. Read docs/PROGRESS.md — confirm the step is next and dependencies are met
3. Read docs/DECISIONS.md — check for relevant existing decisions
4. Read docs/ARCHITECTURE.md Section 5 — if step involves `know` integration

## Execution
1. Follow the step's own "Architecture analysis → Design options → Evaluation → Implementation → Verification" structure from V1_PLAN.md
2. For each design option evaluation, present to human before proceeding
3. Implement with TDD: tests first, then code, then refactor
4. After implementation, run VBR:
   ```bash
   uv run pytest --tb=short -q
   uv run mypy src/ --strict
   uv run ruff check .
   ```
5. Use the `nowu-reviewer` agent for quality review
6. Use the `nowu-curator` agent to capture decisions and update progress

## Commit
```
feat(<module>): <description> [<use-case-IDs>]

Step NN: <step title>
- <key changes>
- <decisions made>
```
