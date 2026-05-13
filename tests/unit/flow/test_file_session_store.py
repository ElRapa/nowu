"""Tests for FileSessionStore (task-003).

TDD order:
  AC-1 -> AC-5 -> AC-4 -> AC-2 -> AC-3 -> AC-6
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# AC-1: protocol conformance
# ---------------------------------------------------------------------------


def test_file_session_store_implements_session_store_protocol() -> None:
    """AC-1: FileSessionStore satisfies the SessionStore Protocol at runtime."""
    from nowu.core.contracts import SessionStore
    from nowu.flow.session_store import FileSessionStore

    assert issubclass(FileSessionStore, SessionStore), (
        "FileSessionStore must satisfy the SessionStore Protocol"
    )
    # Also verify the constructor signature accepts sessions_dir and bookmark_path
    import inspect

    sig = inspect.signature(FileSessionStore.__init__)
    params = list(sig.parameters.keys())
    assert "sessions_dir" in params, f"__init__ must have 'sessions_dir'; got {params}"
    assert "bookmark_path" in params, (
        f"__init__ must have 'bookmark_path'; got {params}"
    )


# ---------------------------------------------------------------------------
# AC-5: load — valid v1 checkpoint
# ---------------------------------------------------------------------------


def test_file_session_store_load_reads_v1_checkpoint_correctly(
    tmp_path: Path,
) -> None:
    """AC-5: load() returns a SessionCheckpoint with all fields from v1 JSON."""
    from nowu.core.contracts import SessionCheckpoint
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-abc-001"
    checkpoint_data = {
        "session_id": session_id,
        "active_project": "nowu",
        "active_role": "implementer",
        "next_action": "run tests",
        "active_step": "S6",
        "last_artifact_path": "state/tasks/task-003.md",
        "checkpoint_grade": "confirmed",
        "active_ids": {"task": "task-003"},
        "completed_steps": ["S1", "S2"],
        "schema_version": "v1",
    }

    sessions_dir = tmp_path / "sessions"
    session_dir = sessions_dir / session_id
    session_dir.mkdir(parents=True)
    (session_dir / "checkpoint-latest.json").write_text(
        json.dumps(checkpoint_data), encoding="utf-8"
    )

    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    result = store.load()

    assert result is not None
    assert isinstance(result, SessionCheckpoint)
    assert result.session_id == session_id
    assert result.active_project == "nowu"
    assert result.active_role == "implementer"
    assert result.next_action == "run tests"
    assert result.active_step == "S6"
    assert result.last_artifact_path == "state/tasks/task-003.md"
    assert result.checkpoint_grade == "confirmed"
    assert result.active_ids == {"task": "task-003"}
    assert result.completed_steps == ["S1", "S2"]
    assert result.schema_version == "v1"


# ---------------------------------------------------------------------------
# AC-4: load — old SessionSnapshot migration
# ---------------------------------------------------------------------------


def test_file_session_store_load_migrates_old_snapshot_format(
    tmp_path: Path,
) -> None:
    """AC-4: load() migrates a 5-field SessionSnapshot to SessionCheckpoint."""
    from nowu.core.contracts import SessionCheckpoint
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-legacy-002"
    old_data = {
        "session_id": session_id,
        "active_project": "legacy-project",
        "active_role": "architect",
        "next_action": "design something",
        "blockers": ["waiting for approval"],
    }

    sessions_dir = tmp_path / "sessions"
    session_dir = sessions_dir / session_id
    session_dir.mkdir(parents=True)
    (session_dir / "checkpoint-latest.json").write_text(
        json.dumps(old_data), encoding="utf-8"
    )

    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    result = store.load()

    assert result is not None
    assert isinstance(result, SessionCheckpoint)
    # Original fields preserved
    assert result.session_id == session_id
    assert result.active_project == "legacy-project"
    assert result.active_role == "architect"
    assert result.next_action == "design something"
    # Migrated defaults for missing fields
    assert result.active_step == ""
    assert result.active_ids == {}
    assert result.completed_steps == []
    assert result.last_artifact_path == ""
    assert result.checkpoint_grade == "unknown"
    assert result.schema_version == "v0-migrated"


# ---------------------------------------------------------------------------
# AC-4 (load-none branch): returns None when no session file exists
# ---------------------------------------------------------------------------


def test_file_session_store_load_returns_none_when_missing(
    tmp_path: Path,
) -> None:
    """AC-4: load() returns None when checkpoint file does not exist."""
    from nowu.flow.session_store import FileSessionStore

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id="nonexistent-session",
    )

    result = store.load()

    assert result is None


# ---------------------------------------------------------------------------
# AC-2: save — JSON + bookmark written; directories created
# ---------------------------------------------------------------------------


def test_file_session_store_save_writes_json_and_bookmark(
    tmp_path: Path,
) -> None:
    """AC-2: save() writes full JSON checkpoint and creates bookmark file."""
    from nowu.core.contracts import SessionCheckpoint
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-save-003"
    checkpoint = SessionCheckpoint(
        session_id=session_id,
        active_project="nowu",
        active_role="shaper",
        next_action="shape task-004",
        active_step="S5",
        last_artifact_path="state/tasks/task-004.md",
        checkpoint_grade="confirmed",
        active_ids={"intake": "intake-001"},
        completed_steps=["S1", "S2", "S3", "S4"],
        schema_version="v1",
    )

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    store.save(checkpoint)

    # JSON file must exist
    json_path = sessions_dir / session_id / "checkpoint-latest.json"
    assert json_path.exists(), f"JSON checkpoint not written to {json_path}"

    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["session_id"] == session_id
    assert loaded["active_project"] == "nowu"
    assert loaded["active_role"] == "shaper"
    assert loaded["next_action"] == "shape task-004"
    assert loaded["active_step"] == "S5"
    assert loaded["last_artifact_path"] == "state/tasks/task-004.md"
    assert loaded["checkpoint_grade"] == "confirmed"
    assert loaded["active_ids"] == {"intake": "intake-001"}
    assert loaded["completed_steps"] == ["S1", "S2", "S3", "S4"]
    assert loaded["schema_version"] == "v1"

    # Bookmark file must exist
    assert bookmark_path.exists(), f"Bookmark not written to {bookmark_path}"


# ---------------------------------------------------------------------------
# AC-3: save — YAML bookmark is valid and has required keys
# ---------------------------------------------------------------------------


def test_file_session_store_save_writes_yaml_bookmark(
    tmp_path: Path,
) -> None:
    """AC-3: save() writes a valid YAML bookmark with required fields."""
    from nowu.core.contracts import SessionCheckpoint
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-yaml-004"
    checkpoint = SessionCheckpoint(
        session_id=session_id,
        active_project="nowu",
        active_role="reviewer",
        next_action="review PR-42",
        active_step="S8",
        last_artifact_path="state/vbr/task-003.md",
        checkpoint_grade="confirmed",
        active_ids={"task": "task-003"},
        completed_steps=["S1", "S2", "S3", "S4", "S5", "S6", "S7"],
        schema_version="v1",
    )

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    store.save(checkpoint)

    assert bookmark_path.exists(), "Bookmark file must be written"
    raw = bookmark_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)

    assert data is not None, "Bookmark must be valid YAML"

    required_keys = {
        "session_id",
        "active_project",
        "active_role",
        "active_step",
        "next_action",
        "completed_steps",
        "last_artifact_path",
        "schema_version",
    }
    missing = required_keys - set(data.keys())
    assert not missing, f"Bookmark YAML missing required keys: {missing}"

    assert data["session_id"] == session_id
    assert data["active_project"] == "nowu"
    assert data["active_role"] == "reviewer"
    assert data["active_step"] == "S8"
    assert data["next_action"] == "review PR-42"
    assert data["completed_steps"] == ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
    assert data["last_artifact_path"] == "state/vbr/task-003.md"
    assert data["schema_version"] == "v1"


# ---------------------------------------------------------------------------
# AC-6: importable from flow package
# ---------------------------------------------------------------------------


def test_file_session_store_importable_from_flow_package() -> None:
    """AC-6: FileSessionStore is importable from nowu.flow."""
    from nowu.flow import FileSessionStore  # noqa: F401

    assert FileSessionStore is not None


# ---------------------------------------------------------------------------
# Atomicity: JSON failure leaves no partial state, bookmark not written
# ---------------------------------------------------------------------------


def test_file_session_store_atomicity_rollback_on_json_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Atomicity: if JSON write fails, no partial file and bookmark not written."""
    from nowu.core.contracts import SessionCheckpoint
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-atomic-005"
    checkpoint = SessionCheckpoint(
        session_id=session_id,
        active_project="nowu",
        active_role="implementer",
        next_action="nothing",
        active_step="S6",
        last_artifact_path="",
        checkpoint_grade="unknown",
    )

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    # Patch Path.replace to simulate atomic rename failure for JSON
    original_replace = Path.replace

    def _fail_replace(self: Path, target: Path) -> Path:  # type: ignore[override]
        raise OSError("simulated disk failure")

    monkeypatch.setattr(Path, "replace", _fail_replace)

    with pytest.raises(OSError):
        store.save(checkpoint)

    # No partial JSON file
    json_path = sessions_dir / session_id / "checkpoint-latest.json"
    assert not json_path.exists(), "Partial JSON must not be left after failure"

    # Bookmark must not have been written
    assert not bookmark_path.exists(), (
        "Bookmark must not be written if JSON write failed"
    )

    # Restore and verify monkeypatch cleanup (pytest handles this automatically)
    monkeypatch.setattr(Path, "replace", original_replace)


# ---------------------------------------------------------------------------
# task-005 AC-1: load — missing file returns None (exact AC name)
# ---------------------------------------------------------------------------


def test_file_session_store_load_missing_file_returns_none(
    tmp_path: Path,
) -> None:
    """AC-1 (task-005): load() returns None without raising when checkpoint file is absent."""
    from nowu.flow.session_store import FileSessionStore

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id="no-such-session",
    )

    result = store.load()

    assert result is None


def test_file_session_store_load_empty_session_id_returns_none(
    tmp_path: Path,
) -> None:
    """load() returns None when session_id is empty string (no session configured)."""
    from nowu.flow.session_store import FileSessionStore

    store = FileSessionStore(
        sessions_dir=tmp_path / "sessions",
        bookmark_path=tmp_path / "SESSION_STATE.md",
        session_id="",
    )

    result = store.load()

    assert result is None


# ---------------------------------------------------------------------------
# task-005 AC-2: load — corrupt JSON raises ValueError with path in message
# ---------------------------------------------------------------------------


def test_file_session_store_load_corrupt_json_raises_value_error(
    tmp_path: Path,
) -> None:
    """AC-2 (task-005): load() raises ValueError when checkpoint contains invalid JSON."""
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-corrupt-006"
    sessions_dir = tmp_path / "sessions"
    session_dir = sessions_dir / session_id
    session_dir.mkdir(parents=True)
    checkpoint_path = session_dir / "checkpoint-latest.json"
    checkpoint_path.write_text("not-valid-json{{{", encoding="utf-8")

    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    with pytest.raises(ValueError) as exc_info:
        store.load()

    assert str(checkpoint_path) in str(exc_info.value), (
        f"ValueError message should include the file path; got: {exc_info.value}"
    )


# ---------------------------------------------------------------------------
# task-005 AC-3: atomicity — JSON write failure leaves bookmark untouched
# ---------------------------------------------------------------------------


def test_file_session_store_save_atomicity_json_fail_no_bookmark_written(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC-3 (task-005): bookmark is absent/unchanged when JSON atomic rename fails."""
    from nowu.core.contracts import SessionCheckpoint
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-atomicity-007"
    checkpoint = SessionCheckpoint(
        session_id=session_id,
        active_project="nowu",
        active_role="implementer",
        next_action="verify atomicity",
        active_step="S6",
        last_artifact_path="state/tasks/task-005.md",
        checkpoint_grade="confirmed",
    )

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"
    store = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )

    # Ensure no prior bookmark exists
    assert not bookmark_path.exists()

    original_replace = Path.replace

    def _fail_replace(self: Path, target: Path) -> Path:  # type: ignore[override]
        raise OSError("simulated disk failure on JSON rename")

    monkeypatch.setattr(Path, "replace", _fail_replace)

    with pytest.raises(OSError):
        store.save(checkpoint)

    # After failed save, bookmark must NOT be written
    assert not bookmark_path.exists(), (
        "Bookmark must not be written when JSON write fails (atomicity guarantee)"
    )

    # Also confirm partial JSON file is not left behind
    json_path = sessions_dir / session_id / "checkpoint-latest.json"
    assert not json_path.exists(), (
        "Partial JSON checkpoint must not remain after failed atomic rename"
    )

    monkeypatch.setattr(Path, "replace", original_replace)
