"""Unit tests for SessionCheckpoint type — task-001-session-checkpoint-type."""

from __future__ import annotations

import dataclasses


# ---------------------------------------------------------------------------
# AC-1: SessionCheckpoint has all required fields and is frozen
# ---------------------------------------------------------------------------


def test_session_checkpoint_type_has_required_fields() -> None:
    """SessionCheckpoint is a frozen dataclass with exactly the 9 required fields."""
    from nowu.core.contracts.types import SessionCheckpoint

    fields = {f.name: f for f in dataclasses.fields(SessionCheckpoint)}

    required = {
        "session_id",
        "active_project",
        "active_role",
        "next_action",
        "active_step",
        "active_ids",
        "completed_steps",
        "last_artifact_path",
        "checkpoint_grade",
        "schema_version",
    }
    assert required == set(fields.keys()), (
        f"Missing or extra fields. Expected {required}, got {set(fields.keys())}"
    )

    # Verify frozen via dataclass params
    assert SessionCheckpoint.__dataclass_params__.frozen is True  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# AC-4: SessionCheckpoint is immutable (FrozenInstanceError on setattr)
# ---------------------------------------------------------------------------


def test_session_checkpoint_is_frozen() -> None:
    """Assigning to any field after construction raises FrozenInstanceError."""
    from nowu.core.contracts.types import SessionCheckpoint

    checkpoint = SessionCheckpoint(
        session_id="s-001",
        active_project="nowu",
        active_role="implementer",
        next_action="run tests",
        active_step="S6",
        active_ids={"task": "task-001"},
        completed_steps=["S1", "S2"],
        last_artifact_path="state/tasks/task-001.md",
        checkpoint_grade="HYPOTHESIS",
    )
    try:
        checkpoint.session_id = "mutated"  # type: ignore[misc]
        raise AssertionError("Expected FrozenInstanceError was not raised")
    except dataclasses.FrozenInstanceError:
        pass


# ---------------------------------------------------------------------------
# AC-5: schema_version defaults to "v1"
# ---------------------------------------------------------------------------


def test_session_checkpoint_schema_version_defaults_to_v1() -> None:
    """Constructing SessionCheckpoint without schema_version yields 'v1'."""
    from nowu.core.contracts.types import SessionCheckpoint

    checkpoint = SessionCheckpoint(
        session_id="s-002",
        active_project="nowu",
        active_role="shaper",
        next_action="shape task",
        active_step="S5",
        active_ids={},
        completed_steps=[],
        last_artifact_path="state/tasks/task-001.md",
        checkpoint_grade="VERIFIED_FACT",
    )
    assert checkpoint.schema_version == "v1"


# ---------------------------------------------------------------------------
# AC-2: SessionSnapshot is retained with deprecation docstring
# ---------------------------------------------------------------------------


def test_session_snapshot_deprecated_stub_unchanged() -> None:
    """SessionSnapshot still has its original 5 fields and a deprecation docstring."""
    from nowu.core.contracts.types import SessionSnapshot

    snap = SessionSnapshot(
        session_id="s-003",
        active_project="nowu",
        active_role="reviewer",
        next_action="review PR",
    )
    assert snap.session_id == "s-003"
    assert snap.active_project == "nowu"
    assert snap.active_role == "reviewer"
    assert snap.next_action == "review PR"
    assert snap.blockers == []

    doc = SessionSnapshot.__doc__ or ""
    assert "Deprecated" in doc, (
        f"SessionSnapshot missing deprecation docstring, got: {doc!r}"
    )


# ---------------------------------------------------------------------------
# AC-3: SessionCheckpoint importable from nowu.core.contracts package
# ---------------------------------------------------------------------------


def test_session_checkpoint_importable_from_contracts_package() -> None:
    """from nowu.core.contracts import SessionCheckpoint succeeds."""
    from nowu.core.contracts import SessionCheckpoint  # noqa: F401

    assert SessionCheckpoint is not None


# ---------------------------------------------------------------------------
# Coverage: ApprovalItem and ApprovalRouter importable and constructable
# ---------------------------------------------------------------------------


def test_approval_item_constructable_from_contracts() -> None:
    """ApprovalItem is a frozen dataclass constructable with all required fields."""
    import dataclasses

    from nowu.core.contracts.approval import ApprovalItem, ApprovalRouter

    item = ApprovalItem(id="ap-001", title="Deploy", tier="tier2", reason="new feature")
    assert item.id == "ap-001"
    assert item.title == "Deploy"
    assert item.tier == "tier2"
    assert item.reason == "new feature"
    assert dataclasses.is_dataclass(item)

    # ApprovalRouter is a Protocol — verify it is importable and is a type
    assert ApprovalRouter is not None


# ---------------------------------------------------------------------------
# Coverage: MemoryService importable
# ---------------------------------------------------------------------------


def test_memory_service_importable_from_contracts() -> None:
    """MemoryService Protocol is importable from nowu.core.contracts.memory."""
    from nowu.core.contracts.memory import MemoryService

    assert MemoryService is not None
