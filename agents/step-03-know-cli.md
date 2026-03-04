---
name: know-cli-implementer
description: Implement the know command-line interface with create, search, today, tasks, and capture subcommands.
---

Read `ARCHITECTURE.md`, `.github/copilot-instructions.md`, and `know/models.py` first.
Steps 01 and 02 must be merged before starting.

## Goal
Expose `know` functionality via a clean CLI. Users and agents both use this.

## Acceptance Criteria (VBR)

- [ ] `python -m know.cli --help` shows all subcommands
- [ ] `know create --type task --title "Test" --project aperitif` creates an atom and prints its ID
- [ ] `know search "pili nut"` returns matching atoms formatted as a readable list
- [ ] `know today` returns up to 5 ranked, non-blocked tasks
- [ ] `know tasks --status open` returns all open tasks
- [ ] `know capture --project aperitif` reads stdin and creates atoms via LLM
- [ ] `pytest tests/know/test_cli.py` passes

## CLI Design (`know/cli.py`)

Use Click or Typer. Subcommands:

### `know create`
```
know create --type ATOMTYPE --title TITLE [--content TEXT] [--project SCOPE] [--priority PRIORITY] [--due DATE] [--tag TAG]...
```
Prints: `Created atom:NNNN — "Title"`

### `know search`
```
know search QUERY [--project SCOPE] [--type ATOMTYPE] [--limit N]
```
Prints atoms as:
```
atom:0001 [task/high] "Implement pili nut recipe" (aperitif)
atom:0007 [fact] "Pili nut harvest season is Oct-Feb" (aperitif, learning)
```

### `know today`
```
know today [--project SCOPE]
```
Prints: Greeting, streak, yesterday wins, top 5 tasks.

### `know tasks`
```
know tasks [--status STATUS] [--project SCOPE] [--all]
```
Table format with ID, title, status, priority, due date.

### `know capture`
```
know capture [--project SCOPE]
```
Reads from stdin. Sends to LLM using prompt at `know/prompts/conversation_capture.txt`.
Prints created atom IDs grouped by type.

## LLM Prompt File (`know/prompts/conversation_capture.txt`)

The prompt must ask the LLM to return JSON with this structure:
```json
{
  "facts": ["fact text 1", "fact text 2"],
  "decisions": ["decision text"],
  "lessons": ["lesson text"],
  "tasks": ["task title 1", "task title 2"],
  "concepts": ["concept text"]
}
```

Write the full prompt in this file. Include instructions for:
- Extract only information explicitly stated in the conversation
- Do not infer or hallucinate
- Be concise (each item ≤ 2 sentences)

## Tests (`tests/know/test_cli.py`)

Use Click's `CliRunner` or Typer's `TestClient`.
Cover all subcommands with mocked `Storage` and mocked LLM client.

## Output
Branch: `feat/know-cli`. PR: `[know] CLI: create, search, today, tasks, capture`.
