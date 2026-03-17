# GitHub Copilot Instructions for nowu

## Architecture
Python 3.11+, DDD layers (Domain → Application → Infrastructure → Interface).
5 modules: core · flow · bridge · soul · know
Domain must NOT import from infrastructure. All cross-module calls via core/contracts/.

## Workflow
9-step cycle: Intake→Constraints→Options→Decision→Shape→Implement→VBR→Review→Capture
See docs/WORKFLOW.md. Read active task spec in state/tasks/ before coding.

## Code Standards
- Type hints everywhere, mypy --strict compliant
- TDD: write failing test first, then implement
- Functions < 20 lines, pure in domain layer
- Google-style docstrings for public APIs

## Before Coding
1. Read state/tasks/ for the active task spec
2. Load ONLY in_scope_files listed in the spec
3. Follow existing D-NNN decisions in docs/DECISIONS.md
4. Run full quality suite after changes: pytest + mypy + ruff

## What Goes Wrong
- Infrastructure imports in domain layer (always check)
- Skipping mypy after changes
- Loading too much context (read only in_scope_files)