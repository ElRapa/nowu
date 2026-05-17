"""Know-backed MemoryService adapter in bridge layer."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from know import api as know_api  # type: ignore[import-not-found]
from know.schema import (  # type: ignore[import-not-found]
    AtomStatus,
    ConnectionType,
    EpistemicGrade,
    KnowledgeAtom,
    KnowledgeType,
)

from nowu.core.contracts.memory import MemoryService
from nowu.core.contracts.types import DecisionRecord


class KnowAdapter(MemoryService):
    """Bridge adapter that delegates memory operations to know.api."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        know_api.init(data_dir)

    def record_decision(self, decision: DecisionRecord) -> str:
        """Persist a decision record as a decision atom and return id."""
        atom = KnowledgeAtom(
            type=KnowledgeType.DECISION,
            title=decision.title,
            content=decision.rationale,
            project_scope=decision.use_case_ids or ["nowu"],
            tags=["decision", *decision.risks, *decision.mitigations],
        )
        return cast(str, know_api.create_atom(atom))

    def create_task(
        self,
        title: str,
        content: str,
        project_scope: list[str],
        tags: list[str] | None = None,
    ) -> str:
        """Create a task atom and return id."""
        atom = KnowledgeAtom(
            type=KnowledgeType.TASK,
            title=title,
            content=content,
            project_scope=project_scope,
            tags=tags or [],
        )
        return cast(str, know_api.create_atom(atom))

    def task_overview(self, project: str | None = None) -> dict[str, Any]:
        """Return lightweight task overview payload."""
        tasks = know_api.query_atoms(type=KnowledgeType.TASK, project=project, limit=100)
        serialized = [task.to_dict() for task in tasks]
        return {
            "project": project,
            "count": len(serialized),
            "tasks": serialized,
        }

    def recall_context(
        self,
        query: str,
        project: str | None = None,
        top_k: int = 10,
    ) -> list[Any]:
        """Recall candidate atoms using keyword query."""
        atoms = know_api.query_atoms(project=project, keyword=query, limit=top_k)
        return [atom.to_dict() for atom in atoms]

    def create_atom(
        self,
        atom_type: str,
        title: str,
        content: str,
        project_scope: list[str],
        tags: list[str] | None = None,
        epistemic_grade: str | None = None,
    ) -> str:
        """Create an atom from generic memory payload."""
        atom = KnowledgeAtom(
            type=KnowledgeType(atom_type),
            title=title,
            content=content,
            project_scope=project_scope,
            tags=tags or [],
            epistemic_grade=self._to_grade(epistemic_grade),
        )
        return cast(str, know_api.create_atom(atom))

    def get_atom(self, atom_id: str) -> dict[str, Any] | None:
        """Get atom by id and serialize for protocol callers."""
        atom = know_api.get_atom(atom_id)
        if atom is None:
            return None
        return cast(dict[str, Any], atom.to_dict())

    def update_atom(self, atom_id: str, updates: dict[str, Any]) -> bool:
        """Apply partial updates; return success state."""
        try:
            know_api.update_atom(atom_id, **updates)
            return True
        except (TypeError, ValueError):
            return False

    def delete_atom(self, atom_id: str) -> bool:
        """Delete atom through know API; map exceptions to bool."""
        try:
            know_api.delete_atom(atom_id, hard_delete=False)
            return True
        except (RuntimeError, ValueError):
            return False

    def query_atoms(self, filters: dict[str, Any], limit: int = 50) -> list[dict[str, Any]]:
        """Query atoms with generic filters converted to know enums."""
        atom_type = filters.get("type")
        status = filters.get("status")
        grade_min = filters.get("grade_min")
        grade_max = filters.get("grade_max")

        tags = filters.get("tags")
        if tags is not None and not isinstance(tags, list):
            raise ValueError("tags filter must be a list[str]")

        atoms = know_api.query_atoms(
            type=KnowledgeType(atom_type) if atom_type else None,
            project=filters.get("project"),
            status=AtomStatus(status) if status else None,
            grade_min=self._to_optional_grade(grade_min),
            grade_max=self._to_optional_grade(grade_max),
            importance_min=filters.get("importance_min"),
            tags=tags,
            keyword=filters.get("keyword"),
            limit=limit,
            offset=int(filters.get("offset", 0)),
        )
        return [atom.to_dict() for atom in atoms]

    def add_connection(self, source_id: str, target_id: str, relation_type: str) -> str:
        """Create typed connection and return connection id."""
        connection = know_api.add_connection(
            source_id,
            target_id,
            ConnectionType(relation_type),
        )
        return cast(str, connection.id)

    def get_connections(self, atom_id: str) -> list[dict[str, Any]]:
        """Return serialized connection list for an atom."""
        return [connection.to_dict() for connection in know_api.get_connections(atom_id)]

    def _to_grade(self, grade: str | int | None) -> EpistemicGrade:
        if grade is None:
            return EpistemicGrade.SPECULATION
        if isinstance(grade, int):
            return EpistemicGrade(grade)
        if grade.isdigit():
            return EpistemicGrade(int(grade))
        try:
            return EpistemicGrade[grade]
        except KeyError:
            return EpistemicGrade(int(grade))

    def _to_optional_grade(self, grade: str | int | None) -> EpistemicGrade | None:
        """Normalize optional grade value used by query filters."""
        if grade is None:
            return None
        return self._to_grade(grade)
