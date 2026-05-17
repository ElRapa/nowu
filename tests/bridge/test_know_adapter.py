"""Tests for the bridge KnowAdapter implementation."""

from __future__ import annotations

import unittest
from datetime import datetime
from unittest.mock import patch

from know.schema import Connection, ConnectionType, EpistemicGrade, KnowledgeAtom, KnowledgeType

from nowu.core.contracts.types import DecisionRecord


class KnowAdapterTest(unittest.TestCase):
    """Validates MemoryService bridge behavior against know.api."""

    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_init_calls_know_init_with_data_dir(self, mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        KnowAdapter(data_dir="/tmp/know")

        mock_init.assert_called_once_with("/tmp/know")

    @patch("nowu.bridge.know_adapter.know_api.create_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_create_atom_creates_knowledge_atom_and_returns_id(
        self,
        _mock_init: unittest.mock.Mock,
        mock_create_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_create_atom.return_value = "atom:123"
        adapter = KnowAdapter()

        atom_id = adapter.create_atom(
            atom_type="fact",
            title="Title",
            content="Content",
            project_scope=["nowu"],
            tags=["k3"],
            epistemic_grade="EVIDENCE_BASED",
        )

        self.assertEqual(atom_id, "atom:123")
        called_atom = mock_create_atom.call_args.args[0]
        self.assertIsInstance(called_atom, KnowledgeAtom)
        self.assertEqual(called_atom.type, KnowledgeType.FACT)
        self.assertEqual(called_atom.title, "Title")
        self.assertEqual(called_atom.content, "Content")
        self.assertEqual(called_atom.project_scope, ["nowu"])
        self.assertEqual(called_atom.tags, ["k3"])
        self.assertEqual(called_atom.epistemic_grade, EpistemicGrade.EVIDENCE_BASED)

    @patch("nowu.bridge.know_adapter.know_api.get_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_get_atom_returns_dict_when_atom_exists(
        self,
        _mock_init: unittest.mock.Mock,
        mock_get_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_get_atom.return_value = KnowledgeAtom(
            type=KnowledgeType.FACT,
            title="A",
            content="B",
            project_scope=["p"],
        )
        adapter = KnowAdapter()

        result = adapter.get_atom("atom:1")

        self.assertIsInstance(result, dict)
        self.assertEqual(result["title"], "A")

    @patch("nowu.bridge.know_adapter.know_api.get_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_get_atom_returns_none_when_missing(
        self,
        _mock_init: unittest.mock.Mock,
        mock_get_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_get_atom.return_value = None
        adapter = KnowAdapter()

        self.assertIsNone(adapter.get_atom("missing"))

    @patch("nowu.bridge.know_adapter.know_api.update_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_update_atom_delegates_with_kwargs_and_returns_true(
        self,
        _mock_init: unittest.mock.Mock,
        mock_update_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_update_atom.return_value = KnowledgeAtom(
            type=KnowledgeType.FACT,
            title="A",
            content="B",
            project_scope=["p"],
        )
        adapter = KnowAdapter()

        updated = adapter.update_atom("atom:1", {"title": "new"})

        self.assertTrue(updated)
        mock_update_atom.assert_called_once_with("atom:1", title="new")

    @patch("nowu.bridge.know_adapter.know_api.update_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_update_atom_returns_false_when_know_raises(
        self,
        _mock_init: unittest.mock.Mock,
        mock_update_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_update_atom.side_effect = ValueError("boom")
        adapter = KnowAdapter()

        self.assertFalse(adapter.update_atom("atom:1", {"title": "new"}))

    @patch("nowu.bridge.know_adapter.know_api.delete_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_delete_atom_returns_true_on_success(
        self,
        _mock_init: unittest.mock.Mock,
        mock_delete_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()

        self.assertTrue(adapter.delete_atom("atom:1"))
        mock_delete_atom.assert_called_once_with("atom:1", hard_delete=False)

    @patch("nowu.bridge.know_adapter.know_api.delete_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_delete_atom_returns_false_on_failure(
        self,
        _mock_init: unittest.mock.Mock,
        mock_delete_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_delete_atom.side_effect = ValueError("boom")
        adapter = KnowAdapter()

        self.assertFalse(adapter.delete_atom("atom:1"))

    @patch("nowu.bridge.know_adapter.know_api.query_atoms")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_query_atoms_converts_filters_and_returns_dict_payloads(
        self,
        _mock_init: unittest.mock.Mock,
        mock_query_atoms: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_query_atoms.return_value = [
            KnowledgeAtom(
                type=KnowledgeType.DECISION,
                title="D1",
                content="C1",
                project_scope=["p1"],
            )
        ]
        adapter = KnowAdapter()

        payload = adapter.query_atoms(
            filters={"type": "decision", "project": "p1", "grade_min": 2},
            limit=25,
        )

        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "D1")
        mock_query_atoms.assert_called_once_with(
            type=KnowledgeType.DECISION,
            project="p1",
            status=None,
            grade_min=EpistemicGrade.HYPOTHESIS,
            grade_max=None,
            importance_min=None,
            tags=None,
            keyword=None,
            limit=25,
            offset=0,
        )

    @patch("nowu.bridge.know_adapter.know_api.add_connection")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_add_connection_returns_connection_id(
        self,
        _mock_init: unittest.mock.Mock,
        mock_add_connection: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_add_connection.return_value = Connection(
            id="conn:1",
            source_id="atom:1",
            target_id="atom:2",
            connection_type=ConnectionType.DEPENDS_ON,
        )
        adapter = KnowAdapter()

        connection_id = adapter.add_connection("atom:1", "atom:2", "depends_on")

        self.assertEqual(connection_id, "conn:1")
        mock_add_connection.assert_called_once_with(
            "atom:1",
            "atom:2",
            ConnectionType.DEPENDS_ON,
        )

    @patch("nowu.bridge.know_adapter.know_api.get_connections")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_get_connections_returns_serialized_connections(
        self,
        _mock_init: unittest.mock.Mock,
        mock_get_connections: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_get_connections.return_value = [
            Connection(
                id="conn:1",
                source_id="atom:1",
                target_id="atom:2",
                connection_type=ConnectionType.DEPENDS_ON,
                created_at=datetime(2026, 5, 15),
            )
        ]
        adapter = KnowAdapter()

        connections = adapter.get_connections("atom:1")

        self.assertEqual(len(connections), 1)
        self.assertEqual(connections[0]["id"], "conn:1")
        self.assertEqual(connections[0]["connection_type"], "depends_on")

    @patch("nowu.bridge.know_adapter.know_api.create_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_record_decision_maps_rationale_to_content(
        self,
        _mock_init: unittest.mock.Mock,
        mock_create_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_create_atom.return_value = "atom:decision-1"
        adapter = KnowAdapter()
        decision = DecisionRecord(
            title="Use bridge adapter",
            rationale="Needed for infrastructure boundary",
            risks=["adapter drift"],
            mitigations=["tests"],
            use_case_ids=["AP-01"],
        )

        atom_id = adapter.record_decision(decision)

        self.assertEqual(atom_id, "atom:decision-1")
        called_atom = mock_create_atom.call_args.args[0]
        self.assertEqual(called_atom.type, KnowledgeType.DECISION)
        self.assertEqual(called_atom.title, "Use bridge adapter")
        self.assertEqual(called_atom.content, "Needed for infrastructure boundary")
        self.assertIn("AP-01", called_atom.project_scope)

    @patch("nowu.bridge.know_adapter.know_api.create_atom")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_create_task_maps_task_fields(
        self,
        _mock_init: unittest.mock.Mock,
        mock_create_atom: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_create_atom.return_value = "atom:task-1"
        adapter = KnowAdapter()

        atom_id = adapter.create_task(
            title="Implement K3",
            content="Expand protocol",
            project_scope=["nowu"],
            tags=["k3"],
        )

        self.assertEqual(atom_id, "atom:task-1")
        called_atom = mock_create_atom.call_args.args[0]
        self.assertEqual(called_atom.type, KnowledgeType.TASK)
        self.assertEqual(called_atom.title, "Implement K3")
        self.assertEqual(called_atom.content, "Expand protocol")

    @patch("nowu.bridge.know_adapter.know_api.query_atoms")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_task_overview_queries_task_atoms(
        self,
        _mock_init: unittest.mock.Mock,
        mock_query_atoms: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_query_atoms.return_value = [
            KnowledgeAtom(type=KnowledgeType.TASK, title="T1", content="C1", project_scope=["p1"]),
            KnowledgeAtom(type=KnowledgeType.TASK, title="T2", content="C2", project_scope=["p1"]),
        ]
        adapter = KnowAdapter()

        overview = adapter.task_overview(project="p1")

        self.assertEqual(overview["count"], 2)
        self.assertEqual(len(overview["tasks"]), 2)
        mock_query_atoms.assert_called_once_with(
            type=KnowledgeType.TASK,
            project="p1",
            limit=100,
        )

    @patch("nowu.bridge.know_adapter.know_api.query_atoms")
    @patch("nowu.bridge.know_adapter.know_api.init")
    def test_recall_context_queries_by_keyword(
        self,
        _mock_init: unittest.mock.Mock,
        mock_query_atoms: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_query_atoms.return_value = [
            KnowledgeAtom(type=KnowledgeType.FACT, title="F1", content="about k3", project_scope=["p1"])
        ]
        adapter = KnowAdapter()

        recalled = adapter.recall_context(query="k3", project="p1", top_k=5)

        self.assertEqual(len(recalled), 1)
        self.assertEqual(recalled[0]["title"], "F1")
        mock_query_atoms.assert_called_once_with(
            project="p1",
            keyword="k3",
            limit=5,
        )


@patch("nowu.bridge.know_adapter.know_api.init")
class ToGradeParseTest(unittest.TestCase):
    """Edge-case tests for _to_grade defensive parsing (D-SESS-03)."""

    def test_to_grade_returns_speculation_for_none(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        self.assertEqual(adapter._to_grade(None), EpistemicGrade.SPECULATION)

    def test_to_grade_accepts_int(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        self.assertEqual(adapter._to_grade(1), EpistemicGrade(1))

    def test_to_grade_accepts_name_string(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        result = adapter._to_grade("EVIDENCE_BASED")
        self.assertEqual(result, EpistemicGrade["EVIDENCE_BASED"])

    def test_to_grade_accepts_digit_string(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        result = adapter._to_grade("2")
        self.assertEqual(result, EpistemicGrade(2))

    def test_to_grade_raises_on_invalid_string(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        with self.assertRaises((KeyError, ValueError)):
            adapter._to_grade("NOT_A_GRADE")

    def test_to_optional_grade_returns_none_for_none(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        self.assertIsNone(adapter._to_optional_grade(None))

    def test_to_optional_grade_delegates_for_value(self, _mock_init: unittest.mock.Mock) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        self.assertEqual(adapter._to_optional_grade("2"), EpistemicGrade(2))


@patch("nowu.bridge.know_adapter.know_api.query_atoms")
@patch("nowu.bridge.know_adapter.know_api.init")
class QueryAtomsDefensiveTest(unittest.TestCase):
    """Edge-case tests for query_atoms defensive filter parsing (D-SESS-03)."""

    def test_query_atoms_tags_non_list_raises(
        self,
        _mock_init: unittest.mock.Mock,
        _mock_query: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        with self.assertRaises(ValueError):
            adapter.query_atoms({"tags": "not-a-list"})

    def test_query_atoms_tags_none_is_accepted(
        self,
        _mock_init: unittest.mock.Mock,
        mock_query: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_query.return_value = []
        adapter = KnowAdapter()
        result = adapter.query_atoms({"tags": None})
        self.assertEqual(result, [])

    def test_query_atoms_invalid_type_raises(
        self,
        _mock_init: unittest.mock.Mock,
        _mock_query: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        adapter = KnowAdapter()
        with self.assertRaises((KeyError, ValueError)):
            adapter.query_atoms({"type": "NOT_A_TYPE"})

    def test_query_atoms_offset_defaults_to_zero(
        self,
        _mock_init: unittest.mock.Mock,
        mock_query: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_query.return_value = []
        adapter = KnowAdapter()
        adapter.query_atoms({})
        call_kwargs = mock_query.call_args.kwargs
        self.assertEqual(call_kwargs.get("offset", 0), 0)

    def test_query_atoms_offset_string_coerced_to_int(
        self,
        _mock_init: unittest.mock.Mock,
        mock_query: unittest.mock.Mock,
    ) -> None:
        from nowu.bridge.know_adapter import KnowAdapter

        mock_query.return_value = []
        adapter = KnowAdapter()
        adapter.query_atoms({"offset": "5"})
        call_kwargs = mock_query.call_args.kwargs
        self.assertEqual(call_kwargs.get("offset"), 5)


if __name__ == "__main__":
    unittest.main()
