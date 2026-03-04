---
name: know-schema-implementer
description: Implement the core KnowledgeAtom schema and SQLite storage layer for the know module.
---

You are a senior Python engineer implementing the `know` module foundation.
Read `ARCHITECTURE.md` and `.github/copilot-instructions.md` first.

## Goal
Create the data model and SQLite storage for the knowledge atom system.

## Acceptance Criteria

All of the following must be true before you mark this done (VBR — Verify Before Reporting):
- [ ] `know/models.py` exists with `KnowledgeAtom`, `Attachment`, `Connection` dataclasses
- [ ] `know/storage.py` exists with `Storage` class
- [ ] `~/.know/know.db` is created on first `Storage()` call with WAL mode enabled
- [ ] All atom types from ARCHITECTURE.md are accepted without error
- [ ] All connection types from ARCHITECTURE.md are accepted without error
- [ ] `pytest tests/know/test_storage.py -v` passes with 100% coverage of storage.py
- [ ] No external dependencies added (sqlite3 stdlib only)

## Models to Implement (`know/models.py`)

```python
from dataclasses import dataclass, field
from typing import Optional

class AtomType:
    FACT = "fact"
    CONCEPT = "concept"
    TASK = "task"
    DECISION = "decision"
    LESSON = "lesson"
    REFERENCE = "reference"
    PREFERENCE = "preference"
    EPHEMERAL = "ephemeral"

class ConnectionType:
    BELONGS_TO = "BELONGS_TO"
    DEPENDS_ON = "DEPENDS_ON"
    DERIVED_FROM = "DERIVED_FROM"
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    RELATED = "RELATED"

@dataclass
class Attachment:
    filename: str
    stored_path: str
    mime_type: str
    size_bytes: int
    sha256: str

@dataclass
class Connection:
    source_id: str
    connection_type: str
    target_id: str
    created_at: str = ""

@dataclass
class KnowledgeAtom:
    type: str
    title: str
    content: str = ""
    project_scope: list[str] = field(default_factory=list)
    epistemic_grade: Optional[int] = None          # 1–5
    epistemic_justification: Optional[str] = None
    task_status: Optional[str] = None              # open | in_progress | done
    task_priority: Optional[str] = None            # low | medium | high | critical
    due_date: Optional[str] = None                 # ISO date string
    tags: list[str] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    id: Optional[str] = None                       # assigned by Storage on create
    created_at: str = ""
    updated_at: str = ""
    deleted_at: Optional[str] = None
```

## Storage to Implement (`know/storage.py`)

Implement a `Storage` class with these methods:

```python
class Storage:
    def __init__(self, db_path: str = "~/.know/know.db"):
        ...  # Create DB, enable WAL, create tables + FTS5 virtual table

    def create_atom(self, atom: KnowledgeAtom) -> KnowledgeAtom:
        ...  # Assign ID (atom:NNNN), set timestamps, insert into DB

    def get_atom(self, atom_id: str) -> Optional[KnowledgeAtom]:
        ...  # Fetch by ID (returns None if deleted)

    def update_atom(self, atom: KnowledgeAtom) -> KnowledgeAtom:
        ...  # Update all fields, bump updated_at

    def delete_atom(self, atom_id: str) -> None:
        ...  # Soft delete: set deleted_at = now()

    def add_connection(self, connection: Connection) -> Connection:
        ...  # Insert connection

    def get_connections(self, atom_id: str, connection_type: Optional[str] = None, direction: str = "outgoing") -> list[Connection]:
        ...  # Fetch connections. direction: "outgoing" | "incoming" | "both"

    def search_keyword(self, query: str, project_scope: Optional[list[str]] = None) -> list[KnowledgeAtom]:
        ...  # FTS5 full-text search over title + content; filter by project_scope if provided
```

## Schema

```sql
CREATE TABLE atoms (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT DEFAULT '',
    project_scope TEXT DEFAULT '[]',   -- JSON array
    epistemic_grade INTEGER,
    epistemic_justification TEXT,
    task_status TEXT,
    task_priority TEXT,
    due_date TEXT,
    tags TEXT DEFAULT '[]',            -- JSON array
    attachments TEXT DEFAULT '[]',     -- JSON array of Attachment dicts
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT
);

CREATE VIRTUAL TABLE atoms_fts USING fts5(
    title, content,
    content=atoms, content_rowid=rowid
);

CREATE TABLE connections (
    source_id TEXT NOT NULL,
    connection_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (source_id, connection_type, target_id)
);
```

## Tests to Write (`tests/know/test_storage.py`)

Cover:
1. Creating an atom returns it with a non-null ID
2. Getting a created atom by ID returns equal object
3. Updating an atom changes the updated_at timestamp
4. Soft deleting an atom means `get_atom` returns None
5. Adding a connection and retrieving it with `get_connections`
6. Keyword search finds an atom by title keyword
7. Keyword search respects project_scope filter

## Output
Commit to branch `feat/know-schema`. PR title: `[know] Core schema and SQLite storage layer`.
