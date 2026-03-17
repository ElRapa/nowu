# Architecture Rules

## Layer Dependency (never violate)
Interface → Application → Domain
     ↓            ↓
Infrastructure (used by Application + Interface, NEVER by Domain)

## Module Boundaries
core ← depended on by all | flow → core | bridge → flow,core
soul → core | know → core

All cross-module calls go through `core/contracts/*.py` Protocol classes.
Direct instantiation across module boundaries is forbidden.

## Import Check (run after every change)
`uv run python -c "import ast, sys, pathlib; [...]"` or `uv run pytest tests/unit/core/test_architecture.py`

## ADR compliance
Before shaping or designing architecture (S2–S5), check `docs/DECISIONS.md`.
Implementers (S6–S7) and reviewers (S8) must follow the active task spec and
rules here; they do NOT load `docs/DECISIONS.md` directly.
Any deviation from a relevant D-NNN = Tier 3 escalation. Do not workaround settled decisions.

Scope by step:
- S2–S4 (constraints, options, decision): may read DECISIONS.md and ARCHITECTURE.md.
- S5 (shaping): may read the decision handoff, file tree, contracts; not DECISIONS.md.
- S6–S7 (implement+VBR): only task spec, in-scope files, tests, pyproject.toml.
- S8 (review): VBR report, changeset, task spec, git diff, this rules file.
- S9 (capture): DECISIONS.md, PROGRESS.md, review, git log; never src/ or tests/.