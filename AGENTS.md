# AGENTS.md — nowu

## Overview

AI-first framework runtime scaffold. Python 3.11+, src-layout, setuptools.
Five modules: `core` · `flow` · `bridge` · `soul` · `know` (external sibling at `../know`).
Contract-first design using `typing.Protocol` and frozen dataclasses in `core/contracts/`.
Currently v0.1.0 — mostly contracts and architecture scaffolding; no CLI entrypoint yet.

## Commands

```bash
# Install (uses uv — uv.lock is present)
uv sync                           # preferred: installs from lockfile
# OR: pip install -e ".[dev]"     # fallback without uv

# Tests
uv run pytest                     # runs tests/ (quiet mode via pyproject addopts)

# Quality suite (all three must pass before S8 review)
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .

# Format
uv run ruff format .

# Single test file
uv run pytest tests/architecture/test_import_boundaries.py -v
```

No Makefile, no CI workflows, no pre-commit hooks. Quality checks are enforced
by a `.claude/settings.json` pre-commit hook (runs pytest + mypy + ruff on `git commit`).

## Structure

```
src/nowu/
├── core/                # Shared contracts + boundary policy. Imports NOTHING else.
│   ├── boundaries.py    # ALLOWED_INTERNAL_IMPORTS dict — canonical import rules
│   └── contracts/       # Protocol interfaces + frozen dataclasses
│       ├── types.py     # TaskSpec, DecisionRecord, SessionSnapshot, RoleName, ApprovalTier
│       ├── memory.py    # MemoryService Protocol (know integration)
│       ├── session.py   # SessionStore, RoleOrchestrator Protocols
│       └── approval.py  # ApprovalRouter Protocol, ApprovalItem
├── flow/                # Pipeline orchestrator (P0–P4, S1–S9, GAP, health)
├── bridge/              # User-facing surface (Typer CLI, adapters)
└── soul/                # AI analytical reasoning (pattern detection, health, drift)
tests/
├── architecture/        # AST-based import boundary enforcement test
└── core/                # Contract importability smoke tests
docs/                    # Architecture docs, ADRs, vision, decisions
state/                   # Workflow artifacts (intake, tasks, arch, health, sessions)
templates/               # Markdown templates for every workflow artifact
.claude/                 # Agent definitions (19 agents) + rules + skills
```

## Import Boundary Rules (Enforced by Test)

Defined in `src/nowu/core/boundaries.py`, enforced by `tests/architecture/test_import_boundaries.py`:

```
core   → (nothing)
flow   → core
bridge → core, flow
soul   → (nothing)
```

All cross-module calls go through `core/contracts/` Protocols. Direct imports between
`flow`, `soul`, `know`, and `bridge` are forbidden (ADR-0001). `soul` ↔ `flow` communicate
only via filesystem artifacts in `state/` (ADR-0006).

## Dependency: `know`

External sibling package at `../know`. Mapped via `[tool.uv.sources]` in pyproject.toml
as an editable local dependency. The workspace file `nowu_framework.code-workspace` links
both repos. `know` provides the knowledge store (SQLite per-project); nowu accesses it
only through the `MemoryService` Protocol.

## Workflow System

This repo uses the **5×10 altitude-phase model** (D-013) with a 9-step implementation
workflow (S1–S9) and a pre-workflow (P0–P4). **Each step has a dedicated agent**
(`.claude/agents/nowu-*.md`), strict context scoping rules, and artifact-based handoffs.

| What | Where |
|------|-------|
| **5×10 model spec** | `docs/model/MODEL-REFERENCE.md` |
| **Workflow standards** | `docs/model/WORKFLOW-STANDARDS.md` |
| **Verification guide** | `docs/model/VERIFICATION-GUIDE.md` |
| Workflow reference (S1-S9) | `docs/WORKFLOW.md` |
| Pre-workflow spec (P0-P4) | `docs/PRE-WORKFLOW.md` |
| Binding decisions | `docs/DECISIONS.md` (D-001 through D-020) |
| ADRs (binding) | `docs/architecture/adr/ADR-0001..0006` |
| Implementation roadmap | `docs/STAGED-PLAN.md` |
| Context scoping table | `CLAUDE.md` (Context Scoping section) |
| Agent definitions | `.claude/agents/` (19 agents) |
| Skills (modes) | `.claude/skills/` (full-cycle, implement-loop, single-step, etc.) |
| Architecture rules | `.claude/rules/architecture.md` |
| Code style rules | `.claude/rules/code-style.md` |
| Testing rules | `.claude/rules/testing.md` |
| Workflow rules | `.claude/rules/workflow.md` |
| Research & insights | `docs/research/` |
| Worked examples | `docs/model/examples/` |

## Context Scoping (Critical)

Each workflow step loads ONLY its C4-level context. Violating this causes anchoring
bias (code during architecture) or re-litigation (architecture during coding).

- **S6–S7 (implementation)**: Load ONLY `task-NNN.md` + `in_scope_files`. Nothing else.
- **P0–P4 (pre-workflow)**: Never touch `src/` or `tests/`.
- **S8 (review)**: No full architecture docs; only VBR report + changeset + task spec + diff.

Full scoping matrix in `CLAUDE.md` and `docs/WORKFLOW.md`.

## Constraints an Agent Must Know

- **ADRs are binding.** Do not contradict without a superseding ADR (Tier 3 — requires human).
- **TDD is mandatory.** Write failing test first, then implement (D-004).
- **mypy --strict, ruff check, pytest** must all pass before review (S8).
- **Domain must not import infrastructure** (D-002). Use Protocols.
- **Scope enforcement**: `.claude/settings.json` has a Write hook that checks `state/tasks/.active-scope`.
- **Approval tiers**: Tier 1 (auto), Tier 2 (batch for human), Tier 3 (STOP and ask: merges to main, breaking changes, new ADRs, deletes, architecture boundary violations).
- **Secrets**: Never commit tokens/credentials. Environment variables only (ADR-0005).
- **`state/SESSION_STATE.md`** is a bookmark, NOT source of truth. Canonical state lives in S1–S9 artifacts.

## Code Style

- Type annotations on all public functions. Google-style docstrings.
- Functions < 20 lines, pure in domain layer.
- One class per file for domain objects.
- Test naming: `test_[unit]_[scenario]_[expected_outcome]`.
- Import order: stdlib → third party → local (ruff-enforced).
- Contracts use frozen dataclasses. Treat as immutable transfer objects.
- `contracts/__init__.py` is empty — import submodules directly (e.g., `from nowu.core.contracts.types import TaskSpec`).

## Gotchas

- **No CLI entrypoint** — the package is a library scaffold, not runnable.
- **`uv` is the package manager** — `uv.lock` at root. Use `uv run` prefix for all commands.
- **Dev tools not in pyproject extras** — ruff and mypy are in uv.lock metadata but not declared in `[project.optional-dependencies]`. `uv sync` installs them; bare `pip install -e ".[dev]"` only gets pytest.
- **Tests are unittest-style** — `unittest.TestCase` classes discovered by pytest. No conftest.py or fixtures.
- **No CI pipelines** — no `.github/workflows/`. Quality is enforced by local hooks only.
- **Heavy documentation repo** — ~250 markdown files vs ~10 Python files. The docs/state/templates directories are the primary working surface.
