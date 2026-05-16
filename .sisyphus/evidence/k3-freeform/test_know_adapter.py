"""Tests for freeform KnowAdapter evidence implementation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from know.schema import AtomStatus, EpistemicGrade, TaskStatus
from nowu.core.contracts.types import DecisionRecord


EVIDENCE_DIR = Path(__file__).resolve().parent
if str(EVIDENCE_DIR) not in sys.path:
    sys.path.insert(0, str(EVIDENCE_DIR))

from know_adapter import KnowAdapter  # noqa: E402


class FakeAtom:
    """Simple fake atom object with task state and serialization."""

    def __init__(self, task_status: TaskStatus, payload: dict[str, object]) -> None:
        self.task_status = task_status
        self._payload = payload

    def to_dict(self) -> dict[str, object]:
        return self._payload


class KnowAdapterTest(unittest.TestCase):
    """Validate all MemoryService methods implemented by KnowAdapter."""

    @patch("know_adapter.know_api.init")
    def test_init_initializes_know_api(self, mock_init: MagicMock) -> None:
        KnowAdapter(data_dir="/tmp/know-test")
        mock_init.assert_called_once_with(data_dir="/tmp/know-test")

    @patch("know_adapter.know_api.create_atom")
    @patch("know_adapter.know_api.init")
    def test_record_decision_uses_rationale_as_content(
        self,
        mock_init: MagicMock,
        mock_create_atom: MagicMock,
    ) -> None:
        mock_create_atom.return_value = "atom:dec1"
        adapter = KnowAdapter()
        decision = DecisionRecord(
            title="Adopt adapter",
            rationale="Bridge isolates know dependency.",
            risks=["drift"],
            mitigations=["tests"],
            use_case_ids=["UC-1"],
        )

        atom_id = adapter.record_decision(decision)

        self.assertEqual(atom_id, "atom:dec1")
        created_atom = mock_create_atom.call_args[0][0]
        self.assertEqual(created_atom.title, "Adopt adapter")
        self.assertEqual(created_atom.content, "Bridge isolates know dependency.")
        self.assertEqual(created_atom.project_scope, ["UC-1"])

    @patch("know_adapter.know_api.create_atom")
    @patch("know_adapter.know_api.init")
    def test_create_task_creates_task_atom(
        self,
        mock_init: MagicMock,
        mock_create_atom: MagicMock,
    ) -> None:
        mock_create_atom.return_value = "atom:task1"
        adapter = KnowAdapter()

        atom_id = adapter.create_task(
            title="Write tests",
            content="TDD first",
            project_scope=["nowu"],
            tags=["k3"],
        )

        self.assertEqual(atom_id, "atom:task1")
        created_atom = mock_create_atom.call_args[0][0]
        self.assertEqual(created_atom.type.value, "task")
        self.assertEqual(created_atom.title, "Write tests")

    @patch("know_adapter.know_api.query_atoms")
    @patch("know_adapter.know_api.init")
    def test_task_overview_returns_counts(
        self,
        mock_init: MagicMock,
        mock_query_atoms: MagicMock,
    ) -> None:
        mock_query_atoms.return_value = [
            FakeAtom(TaskStatus.OPEN, {"id": "1"}),
            FakeAtom(TaskStatus.IN_PROGRESS, {"id": "2"}),
            FakeAtom(TaskStatus.BLOCKED, {"id": "3"}),
            FakeAtom(TaskStatus.DONE, {"id": "4"}),
        ]
        adapter = KnowAdapter()

        overview = adapter.task_overview(project="nowu")

        self.assertEqual(overview["project"], "nowu")
        self.assertEqual(overview["total"], 4)
        self.assertEqual(overview["open"], 1)
        self.assertEqual(overview["in_progress"], 1)
        self.assertEqual(overview["blocked"], 1)
        self.assertEqual(overview["done"], 1)

    @patch("know_adapter.know_search")
    @patch("know_adapter.know_api.init")
    def test_recall_context_delegates_to_search(
        self,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        mock_search.return_value = [{"id": "atom:1"}]
        adapter = KnowAdapter()

        results = adapter.recall_context(query="adapter", project="nowu", top_k=3)

        self.assertEqual(results, [{"id": "atom:1"}])
        mock_search.assert_called_once_with(query="adapter", project="nowu", top_k=3)

    @patch("know_adapter.know_api.create_atom")
    @patch("know_adapter.know_api.init")
    def test_create_atom_parses_epistemic_grade_name(
        self,
        mock_init: MagicMock,
        mock_create_atom: MagicMock,
    ) -> None:
        mock_create_atom.return_value = "atom:new"
        adapter = KnowAdapter()

        atom_id = adapter.create_atom(
            atom_type="fact",
            title="Known fact",
            content="Something true",
            project_scope=["nowu"],
            tags=["fact"],
            epistemic_grade="VERIFIED_FACT",
        )

        self.assertEqual(atom_id, "atom:new")
        created_atom = mock_create_atom.call_args[0][0]
        self.assertEqual(created_atom.epistemic_grade, EpistemicGrade.VERIFIED_FACT)

    @patch("know_adapter.know_api.get_atom")
    @patch("know_adapter.know_api.init")
    def test_get_atom_returns_none_when_missing(
        self,
        mock_init: MagicMock,
        mock_get_atom: MagicMock,
    ) -> None:
        mock_get_atom.return_value = None
        adapter = KnowAdapter()
        self.assertIsNone(adapter.get_atom("missing"))

    @patch("know_adapter.know_api.get_atom")
    @patch("know_adapter.know_api.init")
    def test_get_atom_returns_dict_when_found(
        self,
        mock_init: MagicMock,
        mock_get_atom: MagicMock,
    ) -> None:
        atom = MagicMock()
        atom.to_dict.return_value = {"id": "atom:1"}
        mock_get_atom.return_value = atom
        adapter = KnowAdapter()
        self.assertEqual(adapter.get_atom("atom:1"), {"id": "atom:1"})

    @patch("know_adapter.know_api.update_atom")
    @patch("know_adapter.know_api.init")
    def test_update_atom_returns_true_on_success(
        self,
        mock_init: MagicMock,
        mock_update_atom: MagicMock,
    ) -> None:
        adapter = KnowAdapter()
        self.assertTrue(adapter.update_atom("atom:1", {"title": "new"}))
        mock_update_atom.assert_called_once_with("atom:1", title="new")

    @patch("know_adapter.know_api.update_atom", side_effect=ValueError("missing"))
    @patch("know_adapter.know_api.init")
    def test_update_atom_returns_false_on_failure(
        self,
        mock_init: MagicMock,
        mock_update_atom: MagicMock,
    ) -> None:
        adapter = KnowAdapter()
        self.assertFalse(adapter.update_atom("atom:missing", {"title": "new"}))

    @patch("know_adapter.know_api.delete_atom")
    @patch("know_adapter.know_api.init")
    def test_delete_atom_returns_true_on_success(
        self,
        mock_init: MagicMock,
        mock_delete_atom: MagicMock,
    ) -> None:
        adapter = KnowAdapter()
        self.assertTrue(adapter.delete_atom("atom:1"))
        mock_delete_atom.assert_called_once_with("atom:1")

    @patch("know_adapter.know_api.delete_atom", side_effect=ValueError("missing"))
    @patch("know_adapter.know_api.init")
    def test_delete_atom_returns_false_on_failure(
        self,
        mock_init: MagicMock,
        mock_delete_atom: MagicMock,
    ) -> None:
        adapter = KnowAdapter()
        self.assertFalse(adapter.delete_atom("atom:missing"))

    @patch("know_adapter.know_api.query_atoms")
    @patch("know_adapter.know_api.init")
    def test_query_atoms_maps_filters_and_returns_dicts(
        self,
        mock_init: MagicMock,
        mock_query_atoms: MagicMock,
    ) -> None:
        atom = MagicMock()
        atom.to_dict.return_value = {"id": "atom:1"}
        mock_query_atoms.return_value = [atom]
        adapter = KnowAdapter()

        result = adapter.query_atoms(
            filters={
                "type": "task",
                "project": "nowu",
                "status": "active",
                "grade_min": "2",
                "grade_max": "VERIFIED_FACT",
                "importance_min": 0.5,
                "tags": ["k3"],
                "keyword": "adapter",
                "offset": 1,
            },
            limit=10,
        )

        self.assertEqual(result, [{"id": "atom:1"}])
        kwargs = mock_query_atoms.call_args.kwargs
        self.assertEqual(kwargs["type"].value, "task")
        self.assertEqual(kwargs["status"], AtomStatus.ACTIVE)
        self.assertEqual(kwargs["limit"], 10)
        self.assertEqual(kwargs["offset"], 1)

    @patch("know_adapter.know_api.add_connection")
    @patch("know_adapter.know_api.init")
    def test_add_connection_returns_connection_id(
        self,
        mock_init: MagicMock,
        mock_add_connection: MagicMock,
    ) -> None:
        connection = MagicMock()
        connection.id = "conn:1"
        mock_add_connection.return_value = connection
        adapter = KnowAdapter()

        connection_id = adapter.add_connection("atom:1", "atom:2", "supports")

        self.assertEqual(connection_id, "conn:1")
        kwargs = mock_add_connection.call_args.kwargs
        self.assertEqual(kwargs["conn_type"].value, "supports")

    @patch("know_adapter.know_api.get_connections")
    @patch("know_adapter.know_api.init")
    def test_get_connections_returns_dict_payloads(
        self,
        mock_init: MagicMock,
        mock_get_connections: MagicMock,
    ) -> None:
        conn = MagicMock()
        conn.to_dict.return_value = {"id": "conn:1"}
        mock_get_connections.return_value = [conn]
        adapter = KnowAdapter()

        payload = adapter.get_connections("atom:1")

        self.assertEqual(payload, [{"id": "conn:1"}])
        mock_get_connections.assert_called_once_with("atom:1")


if __name__ == "__main__":
    unittest.main()
