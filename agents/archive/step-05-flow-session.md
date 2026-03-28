---
name: flow-session-implementer
description: Implement session state management and auto-conversation capture for the flow module.
---

Read `ARCHITECTURE.md`, `DECISIONS.md (D-004)`, and `.github/copilot-instructions.md` before starting.
Steps 01–04 must be complete.

## Goal
Implement session lifecycle: WAL-based state persistence and automatic session summarization into `know` atoms.

## Acceptance Criteria (VBR)

- [ ] `flow/session.py` manages session state and writes `soul/SESSION-STATE.md` on every update
- [ ] `flow/session_summary.py` can summarize a list of session events into lessons + decisions
- [ ] At session end, `summarize_and_persist()` writes atoms to `know` storage
- [ ] LLM prompt is stored in `know/prompts/session_summary.txt`
- [ ] `pytest tests/flow/test_session_summary.py` passes with mocked LLM

## Session State (`flow/session.py`)

```python
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

SESSION_STATE_PATH = Path("soul/SESSION-STATE.md")

@dataclass
class SessionEvent:
    role: str        # "user" | "agent" | "tool"
    content: str
    ts: str          # ISO timestamp

@dataclass
class Session:
    session_id: str
    active_project: str
    active_task_id: str | None
    agent_role: str
    goal: str
    events: list[SessionEvent] = field(default_factory=list)

    def add_event(self, role: str, content: str) -> None:
        """Append event and immediately write SESSION-STATE.md (WAL)."""

    def write_wal(self) -> None:
        """Write current state to soul/SESSION-STATE.md.
        MUST be called before every agent response."""
```

## Session Summary (`flow/session_summary.py`)

```python
from dataclasses import dataclass
from know import KnowledgeBase, KnowledgeAtom, KnowledgeType

@dataclass
class SessionSummaryResult:
    summary: str
    decisions: list[str]
    lessons: list[str]

def summarize_session(events: list[SessionEvent], llm_client) -> SessionSummaryResult:
    """
    Call LLM with events formatted as conversation transcript.
    Parse JSON response into SessionSummaryResult.
    """

def persist_summary(
    result: SessionSummaryResult,
    session: Session,
    kb: KnowledgeBase,
) -> list[KnowledgeAtom]:
    """
    Write one lesson atom (summary) + one decision atom per decision.
    Set project_scope from session.active_project.
    Return list of created atoms.
    """

def summarize_and_persist(session: Session, llm_client, storage: Storage) -> list[KnowledgeAtom]:
    """Convenience: summarize + persist in one call. Call at session end."""
```

## LLM Prompt (`know/prompts/session_summary.txt`)

Write a prompt that:
1. Receives a conversation transcript (formatted as ROLE: content lines)
2. Returns JSON: `{"summary": "...", "decisions": ["..."], "lessons": ["..."]}`
3. Instructions: extract only what was explicitly decided or learned; max 3–5 bullets per list; one summary paragraph

## Tests (`tests/flow/test_session_summary.py`)

Use mocked LLM client that returns a known JSON string. Cover:
1. `summarize_session` parses LLM output correctly
2. `persist_summary` creates correct number of atoms in storage
3. Lesson atom has correct type and project_scope
4. Decision atom has correct type and content
5. Empty events list returns empty summary gracefully

## Output
Branch: `feat/flow-session`. PR: `[flow] Session state (WAL) + conversation capture`.
