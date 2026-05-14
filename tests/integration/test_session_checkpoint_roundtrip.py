"""Integration tests for the full session checkpoint roundtrip.

These tests exercise the complete save-then-load cycle using real filesystem I/O.
No mocking of file operations is performed.

task-005 ACs covered:
  AC-4: test_session_checkpoint_roundtrip_save_then_load_is_identical
  AC-5: test_start_session_returns_actual_persisted_content_not_default
"""

from __future__ import annotations

from pathlib import Path

from nowu.core.contracts import SessionCheckpoint


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_full_checkpoint(
    session_id: str = "sess-roundtrip-001",
) -> SessionCheckpoint:
    """Return a fully-populated SessionCheckpoint for roundtrip verification."""

    return SessionCheckpoint(
        session_id=session_id,
        active_project="nowu",
        active_role="implementer",
        next_action="run-S6-on-task-005",
        active_step="S6",
        last_artifact_path="state/tasks/task-005-test-coverage-tdd.md",
        checkpoint_grade="confirmed",
        active_ids={"intake": "intake-001", "task": "task-005"},
        completed_steps=["S1", "S2", "S3", "S4", "S5"],
        schema_version="v1",
    )


# ---------------------------------------------------------------------------
# task-005 AC-4: full roundtrip — save then load with fresh store instance
# ---------------------------------------------------------------------------


def test_session_checkpoint_roundtrip_save_then_load_is_identical(
    tmp_path: Path,
) -> None:
    """AC-4 (task-005): checkpoint saved via checkpoint_at_step_boundary and
    loaded via start_session with a NEW store instance is identical in all 10 fields.

    Uses real filesystem I/O — no mocking.
    """
    from nowu.flow.pipeline import checkpoint_at_step_boundary, start_session
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-roundtrip-001"
    original = _make_full_checkpoint(session_id)

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"

    # Store 1: write
    store1 = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )
    checkpoint_at_step_boundary(store1, original)

    # Store 2: fresh instance, same directory — simulates a new session start
    store2 = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )
    recovered = start_session(store2)

    assert recovered is not None, "start_session must return the persisted checkpoint"
    assert isinstance(recovered, SessionCheckpoint)

    # All 10 fields must round-trip without loss or mutation
    assert recovered.session_id == original.session_id
    assert recovered.active_project == original.active_project
    assert recovered.active_role == original.active_role
    assert recovered.next_action == original.next_action
    assert recovered.active_step == original.active_step
    assert recovered.last_artifact_path == original.last_artifact_path
    assert recovered.checkpoint_grade == original.checkpoint_grade
    assert recovered.active_ids == original.active_ids
    assert recovered.completed_steps == original.completed_steps
    assert recovered.schema_version == original.schema_version


# ---------------------------------------------------------------------------
# task-005 AC-5: start_session returns actual persisted content, not defaults
# ---------------------------------------------------------------------------


def test_start_session_returns_actual_persisted_content_not_default(
    tmp_path: Path,
) -> None:
    """AC-5 (task-005): start_session returns the exact value from the file,
    not a default-constructed object.

    A distinctive next_action string is used as the probe value. If the
    implementation ever returns a default, the assertion will fail.
    """
    from nowu.flow.pipeline import checkpoint_at_step_boundary, start_session
    from nowu.flow.session_store import FileSessionStore

    session_id = "sess-no-default-002"
    distinctive_action = "run-S6-on-task-003"

    checkpoint = SessionCheckpoint(
        session_id=session_id,
        active_project="nowu-probe",
        active_role="curator",
        next_action=distinctive_action,
        active_step="S9",
        last_artifact_path="state/capture/capture-001.md",
        checkpoint_grade="verified",
        active_ids={"story": "story-v1core-001-s002"},
        completed_steps=["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
        schema_version="v1",
    )

    sessions_dir = tmp_path / "sessions"
    bookmark_path = tmp_path / "SESSION_STATE.md"

    store_write = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )
    checkpoint_at_step_boundary(store_write, checkpoint)

    store_read = FileSessionStore(
        sessions_dir=sessions_dir,
        bookmark_path=bookmark_path,
        session_id=session_id,
    )
    result = start_session(store_read)

    assert result is not None
    assert result.next_action == distinctive_action, (
        f"start_session must return the persisted next_action '{distinctive_action}', "
        f"not a default. Got: {result.next_action!r}"
    )
    # Extra probe: role is also distinctive
    assert result.active_role == "curator", (
        f"start_session must return persisted role 'curator', got: {result.active_role!r}"
    )
    assert result.active_ids == {"story": "story-v1core-001-s002"}
