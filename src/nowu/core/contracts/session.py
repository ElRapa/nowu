"""Session runtime and WAL contracts."""

from __future__ import annotations

from typing import Protocol

from .types import RoleName, SessionSnapshot


class SessionStore(Protocol):
    """Persistence boundary for session snapshots and event trail."""

    def load(self) -> SessionSnapshot | None:
        """Load the latest session snapshot if one exists."""

    def save(self, snapshot: SessionSnapshot) -> None:
        """Persist a snapshot to durable storage."""


class RoleOrchestrator(Protocol):
    """Contract for role-based execution sequencing."""

    def next_role(self, current: RoleName) -> RoleName:
        """Return the next role in the configured pipeline."""
