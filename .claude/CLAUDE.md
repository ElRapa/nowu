# nowu — AI-First Multi-Project Framework

Python 3.11+ framework using modular monolith architecture (D-002).
`know` (v0.2.0) is the external memory substrate — never bypass it (D-001).

## Current State
- Steps 00-01 complete (scaffold + contracts + AST boundary tests)
- **Active: Step 02** — MemoryService / `know` integration layer
- Read `docs/PROGRESS.md` for full status, `docs/V1_PLAN.md` for upcoming steps

## Module Map

| Module | Responsibility | Depends on |
|--------|---------------|------------|
| `know` (external) | Knowledge graph, search, today view, versions | none |
| `soul` | Identity and governance docs (VISION, AGENTS, WAL) | none |
| `core` | Domain contracts and use-case services | `know`, `soul` |
| `flow` | Session runtime, role pipeline, VBR loop | `core`, `know`, `soul` |
| `bridge` | CLI/API, approval queue, bootstrap | `flow`, `core`, `know` |
| `skills` | Reusable role skills for AI agents | none |

## Architecture Rules (NEVER violate)
- `core` must NOT import from `flow` or `bridge`
- `flow` must NOT import from `bridge`
- Only `know` persists structured memory — `flow`/`bridge` use `know` API calls
- Import boundaries are enforced by AST-based tests (D-007)

## Key Commands
```bash
uv run pytest                          # run all tests
uv run pytest tests/unit/              # unit tests only
uv run pytest --tb=short -q            # concise output (prefer this)
uv run mypy src/ --strict              # type check
uv run ruff check .                    # lint
uv run ruff format .                   # format
```

## Workflow
Follow `docs/WORKFLOW.md` for every piece of work:
Intake → Architecture analysis → Design options → Evaluation → Task shaping → Implementation → VBR → Review → Capture

## Commit Format
Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
Include use-case IDs when relevant: `feat(core): add MemoryService [NF-01, NF-02]`

## What Claude Gets Wrong (update this as patterns emerge)
- Tends to put infrastructure logic in `core` — always verify import boundaries
- Forgets to run full quality checks after changes — always run pytest + mypy + ruff
- Creates overly abstract interfaces too early — YAGNI, keep it concrete until pattern repeats 3x
- Skips reading DECISIONS.md before proposing architecture — always check existing decisions first

## Context Files (read when relevant)
- @docs/ARCHITECTURE.md — full architecture with module map and contracts
- @docs/V1_PLAN.md — current step details and acceptance criteria
- @docs/DECISIONS.md — all architecture decisions (check before proposing new ones)
- @docs/WORKFLOW.md — delivery workflow, roles, approval tiers, VBR protocol
- @docs/USE_CASES.md — use case definitions (reference by ID: NF-01, PK-03, etc.)
