"""Know-backed MemoryService adapter (freeform evidence implementation)."""

# mypy: disable-error-code=import-untyped

from __future__ import annotations

from pathlib import Path
from typing import Any

from nowu.core.contracts.types import DecisionRecord

import know.api as know_api
from know.schema import AtomStatus, ConnectionType, EpistemicGrade, KnowledgeAtom, KnowledgeType, TaskStatus
from know.search import search as know_search


class KnowAdapter:
    """Adapter implementing MemoryService semantics using know.api."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        """Initialize know API before using adapter operations."""
        know_api.init(data_dir=data_dir)

    def record_decision(self, decision: DecisionRecord) -> str:
        """Persist a decision as a decision atom and return atom id."""
        return self.create_atom(
            atom_type=KnowledgeType.DECISION.value,
            title=decision.title,
            content=decision.rationale,
            project_scope=decision.use_case_ids or ["nowu"],
            tags=["decision", *decision.risks, *decision.mitigations],
        )

    def create_task(
        self,
        title: str,
        content: str,
        project_scope: list[str],
        tags: list[str] | None = None,
    ) -> str:
        """Create a task atom and return atom id."""
        atom = KnowledgeAtom(
            type=KnowledgeType.TASK,
            title=title,
            content=content,
            project_scope=project_scope,
            tags=tags or [],
        )
        atom_id = know_api.create_atom(atom)
        return str(atom_id)

    def task_overview(self, project: str | None = None) -> dict[str, Any]:
        """Return compact task overview using active task atoms."""
        task_atoms = know_api.query_atoms(
            type=KnowledgeType.TASK,
            project=project,
            status=AtomStatus.ACTIVE,
            limit=500,
        )
        open_count = sum(1 for atom in task_atoms if atom.task_status == TaskStatus.OPEN)
        in_progress_count = sum(
            1 for atom in task_atoms if atom.task_status == TaskStatus.IN_PROGRESS
        )
        blocked_count = sum(1 for atom in task_atoms if atom.task_status == TaskStatus.BLOCKED)
        done_count = sum(1 for atom in task_atoms if atom.task_status == TaskStatus.DONE)
        return {
            "project": project,
            "total": len(task_atoms),
            "open": open_count,
            "in_progress": in_progress_count,
            "blocked": blocked_count,
            "done": done_count,
            "tasks": [atom.to_dict() for atom in task_atoms],
        }

    def recall_context(
        self,
        query: str,
        project: str | None = None,
        top_k: int = 10,
    ) -> list[Any]:
        """Recall relevant memory entries via know search."""
        results = know_search(
            query=query,
            project=project,
            top_k=top_k,
        )
        if not isinstance(results, list):
            return []
        return results

    def create_atom(
        self,
        atom_type: str,
        title: str,
        content: str,
        project_scope: list[str],
        tags: list[str] | None = None,
        epistemic_grade: str | None = None,
    ) -> str:
        """Create an atom and return its ID."""
        atom = KnowledgeAtom(
            type=self._parse_atom_type(atom_type),
            title=title,
            content=content,
            project_scope=project_scope,
            tags=tags or [],
            epistemic_grade=self._parse_epistemic_grade(epistemic_grade),
        )
        atom_id = know_api.create_atom(atom)
        return str(atom_id)

    def get_atom(self, atom_id: str) -> dict[str, Any] | None:
        """Get atom by id as a plain dictionary."""
        atom = know_api.get_atom(atom_id)
        if atom is None:
            return None
        payload: dict[str, Any] = atom.to_dict()
        return payload

    def update_atom(self, atom_id: str, updates: dict[str, Any]) -> bool:
        """Update atom fields and return operation success."""
        try:
            know_api.update_atom(atom_id, **updates)
        except Exception:
            return False
        return True

    def delete_atom(self, atom_id: str) -> bool:
        """Delete atom (soft delete) and return operation success."""
        try:
            know_api.delete_atom(atom_id)
        except Exception:
            return False
        return True

    def query_atoms(self, filters: dict[str, Any], limit: int = 50) -> list[dict[str, Any]]:
        """Query atoms with generic filters and return dictionaries."""
        atoms = know_api.query_atoms(
            type=self._parse_optional_atom_type(filters.get("type")),
            project=self._parse_optional_str(filters.get("project")),
            status=self._parse_optional_status(filters.get("status")),
            grade_min=self._parse_optional_grade(filters.get("grade_min")),
            grade_max=self._parse_optional_grade(filters.get("grade_max")),
            importance_min=self._parse_optional_float(filters.get("importance_min")),
            tags=self._parse_optional_str_list(filters.get("tags")),
            keyword=self._parse_optional_str(filters.get("keyword")),
            limit=limit,
            offset=self._parse_offset(filters.get("offset")),
        )
        return [atom.to_dict() for atom in atoms]

    def add_connection(self, source_id: str, target_id: str, relation_type: str) -> str:
        """Add connection and return connection id."""
        connection = know_api.add_connection(
            source_id=source_id,
            target_id=target_id,
            conn_type=ConnectionType(relation_type),
        )
        return str(connection.id)

    def get_connections(self, atom_id: str) -> list[dict[str, Any]]:
        """Get connections for an atom as dictionaries."""
        connections = know_api.get_connections(atom_id)
        return [connection.to_dict() for connection in connections]

    def _parse_atom_type(self, atom_type: str) -> KnowledgeType:
        return KnowledgeType(atom_type)

    def _parse_epistemic_grade(self, grade: str | None) -> EpistemicGrade:
        if grade is None:
            return EpistemicGrade.SPECULATION
        if grade.isdigit():
            return EpistemicGrade(int(grade))
        normalized = grade.strip().upper()
        if normalized in EpistemicGrade.__members__:
            return EpistemicGrade[normalized]
        return EpistemicGrade(int(grade))

    def _parse_optional_atom_type(self, atom_type: Any) -> KnowledgeType | None:
        if atom_type is None:
            return None
        return self._parse_atom_type(str(atom_type))

    def _parse_optional_status(self, status: Any) -> AtomStatus | None:
        if status is None:
            return AtomStatus.ACTIVE
        return AtomStatus(str(status))

    def _parse_optional_grade(self, grade: Any) -> EpistemicGrade | None:
        if grade is None:
            return None
        return self._parse_epistemic_grade(str(grade))

    def _parse_optional_str(self, value: Any) -> str | None:
        if value is None:
            return None
        return str(value)

    def _parse_optional_float(self, value: Any) -> float | None:
        if value is None:
            return None
        return float(value)

    def _parse_optional_str_list(self, value: Any) -> list[str] | None:
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError("tags filter must be a list[str]")
        return [str(item) for item in value]

    def _parse_offset(self, value: Any) -> int:
        if value is None:
            return 0
        return int(value)
