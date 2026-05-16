"""Memory service contract for integrating with know (v0.4.0+)."""

# mypy: disable-error-code=import-untyped

from __future__ import annotations

from typing import Any, Protocol

from nowu.core.contracts.types import DecisionRecord


class MemoryService(Protocol):
    """Stable memory operations required by flow and bridge.

    Implementation delegates to know APIs behind a bridge adapter.
    """

    def record_decision(self, decision: DecisionRecord) -> str:
        """Persist a decision and return memory id."""

    def create_task(
        self,
        title: str,
        content: str,
        project_scope: list[str],
        tags: list[str] | None = None,
    ) -> str:
        """Create task memory entry and return id."""

    def task_overview(self, project: str | None = None) -> dict[str, Any]:
        """Return a project or global task overview payload."""

    def recall_context(
        self,
        query: str,
        project: str | None = None,
        top_k: int = 10,
    ) -> list[Any]:
        """Recall context candidates from memory."""

    def create_atom(
        self,
        atom_type: str,
        title: str,
        content: str,
        project_scope: list[str],
        tags: list[str] | None = None,
        epistemic_grade: str | None = None,
    ) -> str:
        """Create a generic knowledge atom and return its id."""

    def get_atom(self, atom_id: str) -> dict[str, Any] | None:
        """Retrieve one atom as a generic dictionary."""

    def update_atom(self, atom_id: str, updates: dict[str, Any]) -> bool:
        """Update atom fields and return success."""

    def delete_atom(self, atom_id: str) -> bool:
        """Delete (soft-delete) an atom and return success."""

    def query_atoms(
        self,
        filters: dict[str, Any],
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Query atoms via generic filters and return dictionaries."""

    def add_connection(self, source_id: str, target_id: str, relation_type: str) -> str:
        """Add a typed atom connection and return connection id."""

    def get_connections(self, atom_id: str) -> list[dict[str, Any]]:
        """Return connections for an atom as dictionaries."""
