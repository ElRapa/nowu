"""Session runtime and WAL contracts.

See ADR-0007 for checkpoint schema details.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .types import RoleName, SessionCheckpoint


@runtime_checkable
class SessionStore(Protocol):
    """Persistence boundary for session checkpoints and event trail."""

    def load(self) -> SessionCheckpoint | None:
        """Load the latest session checkpoint if one exists."""

    def save(self, checkpoint: SessionCheckpoint) -> None:
        """Persist a checkpoint to durable storage."""


class RoleOrchestrator(Protocol):
    """Contract for role-based execution sequencing."""

    def next_role(self, current: RoleName) -> RoleName:
        """Return the next role in the configured pipeline."""
