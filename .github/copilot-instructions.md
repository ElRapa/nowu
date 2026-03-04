# nowu Repository — Copilot Instructions

This repository contains the **nowu** framework: a modular monolith for personal and project knowledge management, task tracking, and AI-agent orchestration.

## Architecture Overview

Five modules, strict dependency order:

```
know/       ← Foundation: knowledge atoms, tasks, connections, search, today-view, workflow lifecycle
soul/       ← Identity: VISION.md, AGENTS.md, ADR templates (no code, no DB)
flow/       ← Orchestration: agents, session state, WAL, approvals, conversation capture
bridge/     ← Integrations: MCP server, CLI proxy, webhooks
dash/       ← Presentation: web UI (v2 only)
```

**The cardinal rule:** Only `know` touches the SQLite database. All other modules call `know`'s Python API. Never bypass this.

## Tech Stack

- **Language:** Python 3.11+
- **Database:** SQLite 3 with WAL mode enabled (via `sqlite3` stdlib — no ORM in v1)
- **Testing:** pytest + pytest-cov (minimum 90% coverage enforced)
- **CLI:** Click or Typer
- **Package manager:** uv or pip with pyproject.toml
- **Data classes:** Python `dataclasses` (no Pydantic in v1)

## File Structure

```
know/
  __init__.py
  models.py          ← KnowledgeAtom, Attachment, Connection dataclasses
  storage.py         ← SQLite CRUD, FTS5 search, connections
  workflow.py        ← compute_workflow_state(), instantiate_workflow()
  today.py           ← today() ranking logic
  cli.py             ← Click CLI: create, search, today, tasks, capture
  prompts/
    conversation_capture.txt   ← LLM prompt for know capture
    session_summary.txt        ← LLM prompt for flow session summary

flow/
  __init__.py
  orchestrator.py    ← Orchestrator agent: reads today(), routes to agent roles
  session.py         ← Session state + WAL write
  session_summary.py ← Summarize session → write lesson/decision atoms to know
  prompts/

soul/
  VISION.md
  AGENTS.md

bridge/
  __init__.py
  cli_proxy.py       ← Thin wrapper exposing know + flow as one CLI surface

tests/
  know/
    test_models.py
    test_storage.py
    test_workflow.py
    test_today.py
    test_cli.py
    test_capture.py
  flow/
    test_session_summary.py

ARCHITECTURE.md     ← Authoritative design decisions (read before coding)
V1_PLAN.md          ← Scope boundary for v1
V2_IDEAS.md         ← Parking lot (do NOT implement in v1)
DECISIONS.md        ← Running ADR log
```

## Development Commands

```bash
# Install
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v --cov=know --cov=flow --cov-report=term-missing

# Run a specific module's tests
pytest tests/know/ -v

# Lint
ruff check . && ruff format --check .

# Run CLI
python -m know.cli today
python -m know.cli search "pili nut"
python -m know.cli create --type task --title "My task" --project aperitif
```

## Code Style

- Descriptive names: `create_knowledge_atom()` not `create()` or `mk()`
- Functions: snake_case. Classes: PascalCase. Constants: UPPER_SNAKE_CASE
- Type hints on all function signatures
- Docstrings on all public functions
- No magic strings: use `AtomType` and `ConnectionType` string enums

**Good example:**
```python
def compute_workflow_state(task_id: str, storage: Storage) -> str:
    """Return 'blocked', 'ready', 'active', or 'done' for a task atom."""
    task = storage.get_atom(task_id)
    if task is None:
        raise ValueError(f"Atom {task_id} not found")
    if task.task_status == "done":
        return "done"
    deps = storage.get_connections(task_id, connection_type="DEPENDS_ON")
    if any(storage.get_atom(d.target_id).task_status != "done" for d in deps):
        return "blocked"
    return "active" if task.task_status == "in_progress" else "ready"
```

**Bad example:**
```python
def get(id):
    t = db.fetch(id)
    deps = db.conn(id)
    for d in deps:
        if db.fetch(d[1]).status != "done": return "blocked"
    return "active" if t.status == "in_progress" else "ready"
```

## Git Workflow

- Branch naming: `feat/know-schema`, `feat/flow-session-summary`, `fix/today-ranking`
- One PR per implementation step (see `agents/` folder for step definitions)
- PR title format: `[module] Short description`
- All PRs require passing tests before merge
- Commit messages: `feat(know): add workflow_state computation` / `fix(flow): session WAL not writing on timeout`

## Boundaries — What Copilot Must NEVER Do

- **Never** write to the SQLite database from `flow`, `bridge`, or `dash` — always call `know`'s API
- **Never** import `flow` or `bridge` from inside `know`
- **Never** add network calls to `know` (it must work fully offline)
- **Never** implement v2 features (check `V2_IDEAS.md` — if it's there, skip it)
- **Never** commit secrets, API keys, or connection strings

## What to Do When Uncertain

1. Read `ARCHITECTURE.md` first
2. Read the relevant `agents/` task file
3. Read `DECISIONS.md` for prior decisions
4. If still unclear: write a comment in the code with `# DECISION NEEDED:` and add a note to `DECISIONS.md`
