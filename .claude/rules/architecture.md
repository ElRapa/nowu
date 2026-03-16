# Architecture Rules

## Module Boundaries (D-002, D-007)
- Modular monolith: `core`, `flow`, `bridge`, `soul`, `skills`
- `know` is consumed via `KnowAdapter` / public API only (D-001)
- Import direction: bridge → flow → core → know/soul
- NEVER create circular dependencies between modules

## Data Ownership
- Only `know` persists structured memory (atoms: TASK, DECISION, ACTION, LESSON)
- `soul/SESSION-STATE.md` is the WAL for in-flight session continuity
- `flow` and `bridge` do NOT write to private DB tables

## Contract-First Design
- Define interfaces in `core/contracts/` before implementation
- New cross-module interactions require a contract protocol
- Violations caught by AST-based architecture tests in `tests/architecture/`

## Decision Protocol
- Every non-trivial choice gets a D-NNN entry in DECISIONS.md
- Check existing decisions before proposing alternatives
- If proposing to change an existing decision, escalate (Tier 3)
