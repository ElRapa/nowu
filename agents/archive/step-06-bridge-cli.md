---
name: bridge-cli-implementer
description: Implement the nowu CLI entry point that wraps know and flow as a single command surface.
---

Read `ARCHITECTURE.md` and `.github/copilot-instructions.md`. Steps 01–05 must be complete.

## Goal
Create a single `nowu` CLI that orchestrates `know` + `flow` for the user's daily workflow.

## Acceptance Criteria (VBR)

- [ ] `nowu continue` starts or resumes a flow session, loads today's top task
- [ ] `nowu status` prints current SESSION-STATE.md in human-readable form
- [ ] `nowu today` queries `kb.query_atoms(type=TASK)` filtered by date and prints daily briefing
- [ ] `nowu approve` lists pending Tier 2 items and accepts "all" or specific IDs
- [ ] No code from `know` or `flow` is duplicated — always imports + calls their APIs

## CLI Commands (`bridge/cli_proxy.py`)

```python
# nowu continue
# Reads soul/SESSION-STATE.md to check current state.
# If no active task, queries kb.query_atoms(type=TASK, ...) to pick the top task.
# Creates a new Session and starts the agent loop.

# nowu status
# Prints soul/SESSION-STATE.md formatted for terminal.

# nowu today
# Queries kb.query_atoms(type=KnowledgeType.TASK) filtered by date,
# prints daily briefing:
#   - Greeting with streak
#   - Yesterday's completed tasks
#   - Top 5 tasks to work on today

# nowu approve [--all] [--id ATOM_ID]
# Lists pending items from soul/pending/
# Approves and writes to know via kb.update_atom().
```

## Output
Branch: `feat/bridge-cli`. PR: `[bridge] nowu CLI entry point`.
