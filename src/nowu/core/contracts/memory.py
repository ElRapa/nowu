"""Memory service contract for integrating with know (v0.4.0+)."""

from __future__ import annotations

from typing import Protocol, Any

from .types import DecisionRecord


class MemoryService(Protocol):
    """Stable memory operations required by flow and bridge.

    Implementation delegates to know.KnowledgeBase instance methods.
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
        """Return a project or global task overview payload.

        Replaces the former today_view() — know.today() was removed in v0.4.0.
        Implementation should use kb.query_atoms(type=KnowledgeType.TASK, ...)
        with date filtering.
        """

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
        """Create atom and return atom id."""

    def get_atom(self, atom_id: str) -> dict[str, Any] | None:
        """Return serialized atom if found, else None."""

    def update_atom(self, atom_id: str, updates: dict[str, Any]) -> bool:
        """Apply atom updates and return success."""

    def delete_atom(self, atom_id: str) -> bool:
        """Delete or archive atom and return success."""

    def query_atoms(self, filters: dict[str, Any], limit: int = 50) -> list[dict[str, Any]]:
        """Query atoms and return serialized payloads."""

    def add_connection(self, source_id: str, target_id: str, relation_type: str) -> str:
        """Add connection between atoms and return connection id."""

    def get_connections(self, atom_id: str) -> list[dict[str, Any]]:
        """Return serialized connections for atom."""
