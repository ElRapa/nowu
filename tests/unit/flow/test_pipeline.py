"""Tests for nowu.flow.pipeline — session start / step-boundary functions."""

from __future__ import annotations

from unittest.mock import MagicMock

from nowu.core.contracts import SessionCheckpoint


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_checkpoint(
    session_id: str = "s-001", active_step: str = "S2"
) -> SessionCheckpoint:
    """Return a minimal valid SessionCheckpoint for use in tests."""
    return SessionCheckpoint(
        session_id=session_id,
        active_project="proj",
        active_role="implementer",
        next_action="run tests",
        active_step=active_step,
        last_artifact_path="state/tasks/task-001.md",
        checkpoint_grade="high",
    )


def _make_mock_store(*, returns: SessionCheckpoint | None = None) -> MagicMock:
    """Return a MagicMock that satisfies the SessionStore Protocol."""
    store = MagicMock()
    store.load.return_value = returns
    return store


# ---------------------------------------------------------------------------
# AC-1: start_session calls store.load()
# ---------------------------------------------------------------------------


def test_pipeline_start_session_calls_store_load() -> None:
    """start_session must delegate to store.load() exactly once."""
    from nowu.flow.pipeline import start_session

    store = _make_mock_store(returns=None)
    start_session(store)
    store.load.assert_called_once_with()


# ---------------------------------------------------------------------------
# AC-2: start_session propagates checkpoint or None
# ---------------------------------------------------------------------------


def test_pipeline_start_session_propagates_checkpoint_or_none() -> None:
    """start_session returns the checkpoint from store.load() unchanged, or None."""
    from nowu.flow.pipeline import start_session

    # Case A: store has a checkpoint
    checkpoint = _make_checkpoint()
    store_with = _make_mock_store(returns=checkpoint)
    result_with = start_session(store_with)
    assert result_with is checkpoint

    # Case B: store returns None (no prior session)
    store_none = _make_mock_store(returns=None)
    result_none = start_session(store_none)
    assert result_none is None


# ---------------------------------------------------------------------------
# AC-3: checkpoint_at_step_boundary calls store.save(checkpoint)
# ---------------------------------------------------------------------------


def test_pipeline_checkpoint_at_step_boundary_calls_store_save() -> None:
    """checkpoint_at_step_boundary must delegate to store.save(checkpoint) exactly once."""
    from nowu.flow.pipeline import checkpoint_at_step_boundary

    checkpoint = _make_checkpoint()
    store = _make_mock_store()
    checkpoint_at_step_boundary(store, checkpoint)
    store.save.assert_called_once_with(checkpoint)


# ---------------------------------------------------------------------------
# AC-4: both functions are importable from nowu.flow
# ---------------------------------------------------------------------------


def test_flow_pipeline_functions_importable_from_flow_package() -> None:
    """start_session and checkpoint_at_step_boundary must be importable from nowu.flow."""
    from nowu.flow import checkpoint_at_step_boundary, start_session  # noqa: F401

    assert callable(start_session)
    assert callable(checkpoint_at_step_boundary)


# ---------------------------------------------------------------------------
# AC-5: type annotations use SessionStore Protocol (verified via inspect)
# ---------------------------------------------------------------------------


def test_pipeline_functions_typed_against_session_store_protocol() -> None:
    """Both functions must have 'store' typed as SessionStore (not a concrete class)."""
    import inspect

    from nowu.flow.pipeline import checkpoint_at_step_boundary, start_session
    from nowu.core.contracts import SessionStore

    sig_start = inspect.signature(start_session)
    store_param_start = sig_start.parameters["store"]
    assert store_param_start.annotation is SessionStore, (
        f"start_session 'store' annotation should be SessionStore, "
        f"got {store_param_start.annotation!r}"
    )

    sig_boundary = inspect.signature(checkpoint_at_step_boundary)
    store_param_boundary = sig_boundary.parameters["store"]
    assert store_param_boundary.annotation is SessionStore, (
        f"checkpoint_at_step_boundary 'store' annotation should be SessionStore, "
        f"got {store_param_boundary.annotation!r}"
    )
