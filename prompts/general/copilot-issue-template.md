# GitHub Issue Template for Copilot Agent Tasks

Use this template when creating GitHub Issues to assign to the Copilot coding agent.

---

## Issue Title Format
`[module] Short description (see agents/step-NN-module-name.md)`

Example: `[know] Core schema and SQLite storage layer (see agents/step-01-know-schema.md)`

## Issue Body Template

```
## Context
Read the full task specification in `agents/step-NN-module-name.md` before starting.
Also read `ARCHITECTURE.md` and `DECISIONS.md` for background.

## Goal
[One sentence — copy from the agent task file]

## Acceptance Criteria
[Copy the checkbox list from the agent task file]

## Files to Create or Modify
[List the files explicitly]

## Tests Required
[Describe what tests must pass — be specific]

## Boundaries
- Do NOT implement anything in V2_IDEAS.md
- Do NOT add dependencies not listed in .github/copilot-instructions.md
- Do NOT touch any module other than [module name]

## When You Are Done
1. Run `pytest tests/[module]/ -v --cov=[module] --cov-report=term-missing`
2. Confirm all acceptance criteria are checked
3. Open a PR with title `[module] Short description`
4. Add a summary of any decisions you made to DECISIONS.md
```
