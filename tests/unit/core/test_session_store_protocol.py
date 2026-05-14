"""Tests for the SessionStore Protocol contract (task-002)."""

from __future__ import annotations

import inspect
import typing


def test_session_store_protocol_load_returns_checkpoint_type() -> None:
    """AC-1: SessionStore.load() return type is SessionCheckpoint | None."""
    from nowu.core.contracts import SessionStore
    from nowu.core.contracts import SessionCheckpoint

    hints = typing.get_type_hints(SessionStore.load)
    return_hint = hints.get("return")
    # Must be Optional[SessionCheckpoint] / SessionCheckpoint | None
    args = typing.get_args(return_hint)
    assert SessionCheckpoint in args, (
        f"load() return type must include SessionCheckpoint; got {return_hint}"
    )
    assert type(None) in args, (
        f"load() return type must include None; got {return_hint}"
    )


def test_session_store_protocol_save_accepts_checkpoint_type() -> None:
    """AC-2: SessionStore.save() parameter named 'checkpoint' of type SessionCheckpoint."""
    from nowu.core.contracts import SessionStore
    from nowu.core.contracts import SessionCheckpoint

    hints = typing.get_type_hints(SessionStore.save)
    # Parameter must be named 'checkpoint'
    sig = inspect.signature(SessionStore.save)
    param_names = list(sig.parameters.keys())
    assert "checkpoint" in param_names, (
        f"save() must have a parameter named 'checkpoint'; found {param_names}"
    )
    assert hints.get("checkpoint") is SessionCheckpoint, (
        f"save() 'checkpoint' parameter must be typed SessionCheckpoint; got {hints.get('checkpoint')}"
    )


def test_session_store_protocol_concrete_impl_satisfies_protocol() -> None:
    """AC-3: A concrete class with correct signatures satisfies SessionStore at runtime."""
    from nowu.core.contracts import SessionStore, SessionCheckpoint

    class _Impl:
        def load(self) -> SessionCheckpoint | None:
            return None

        def save(self, checkpoint: SessionCheckpoint) -> None:
            pass

    impl = _Impl()
    assert isinstance(impl, SessionStore), (
        "Concrete implementation with correct signatures must satisfy SessionStore Protocol"
    )


def test_role_orchestrator_protocol_unchanged() -> None:
    """AC-4: RoleOrchestrator.next_role() signature is unchanged (regression guard)."""
    from nowu.core.contracts import RoleOrchestrator

    sig = inspect.signature(RoleOrchestrator.next_role)
    params = list(sig.parameters.keys())
    assert params == ["self", "current"], (
        f"RoleOrchestrator.next_role signature must have params ['self', 'current']; got {params}"
    )
    hints = typing.get_type_hints(RoleOrchestrator.next_role)
    from nowu.core.contracts import RoleName

    assert hints.get("current") is RoleName or hints.get("current") == RoleName, (
        f"RoleOrchestrator.next_role 'current' param must be RoleName; got {hints.get('current')}"
    )
    assert hints.get("return") is RoleName or hints.get("return") == RoleName, (
        f"RoleOrchestrator.next_role return type must be RoleName; got {hints.get('return')}"
    )


def test_session_store_importable_from_contracts_package() -> None:
    """AC-5: SessionStore and RoleOrchestrator are importable from nowu.core.contracts."""
    from nowu.core.contracts import SessionStore, RoleOrchestrator  # noqa: F401

    assert SessionStore is not None
    assert RoleOrchestrator is not None
