# nowu — AI-Powered Project Management Framework

Python 3.11+ | DDD (Domain/Application/Infrastructure/Interface) | 5 modules:
`core` (contracts+services) · `flow` (orchestration) · `bridge` (human-AI) ·
`soul` (identity) · `know` (knowledge graph)

## Commands
- `uv run pytest --tb=short -q`     — run tests
- `uv run mypy src/ --strict`       — type check
- `uv run ruff check .`             — lint
- `uv run ruff format .`            — format

## Architecture Rules (see docs/ARCHITECTURE.md §4.1)
Domain layer must NOT import infrastructure. All cross-module calls go through
protocols in `core/contracts/`. Violations are Tier 3 — stop and escalate.

## Workflow (see docs/WORKFLOW.md)
9 steps: S1 Intake → S2 Constraints → S3 Options → S4 Decision →
         S5 Shape → S6 Implement → S7 VBR → S8 Review → S9 Capture

Each step has a dedicated agent and a fixed context scope. Load only what
is listed in the active task spec (`state/tasks/`) and relevant state files.

## Session Bookmark (optional)
If `state/SESSION-STATE.md` exists:

- At the start of a session: skim it to see the current step and task.
- At natural stopping points: update `step`, `task_id`, summary, and next checkpoint.

This file is a human+AI bookmark only. All authoritative decisions,
requirements, and specs live in the S1–S9 artifacts.

## What Claude Gets Wrong
- Puts infrastructure concerns in domain layer — always verify imports
- Skips mypy after changes — always run the full quality suite
- Loads too much context — read ONLY files listed in the task spec
- Re-litigates settled decisions — if D-NNN exists and is ACCEPTED, follow it
- Creates >8h tasks — break down until each task is ≤4h
