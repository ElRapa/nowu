"""Architecture fitness functions for ADR-0008 (Knowledge Atom Model) and ADR-0010 (Epistemic Grades).

Validates structural properties required by hypothesis ADRs:
- ADR-0008: know module's KnowledgeAtom has required fields per schema contract
- ADR-0010: EpistemicGrade enum has exactly 5 levels with correct values
- ADR-0008: MemoryService Protocol exists in core/contracts/memory.py
- ADR-0008: nowu modules access know only through MemoryService Protocol (no direct import)
"""

from __future__ import annotations

import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "nowu"
KNOW_ROOT = Path(__file__).resolve().parents[3] / "know" / "src" / "know"


class ADR0008KnowledgeAtomFitnessTest(unittest.TestCase):
    """Validates structural properties required by ADR-0008: Knowledge Atom Model."""

    def test_know_module_exists(self) -> None:
        """ADR-0008 requires know module at ../know — verify it's accessible."""
        self.assertTrue(
            KNOW_ROOT.exists(),
            f"know module not found at {KNOW_ROOT}. "
            "ADR-0008 depends on know's KnowledgeAtom schema.",
        )

    def test_knowledge_atom_has_required_fields(self) -> None:
        """ADR-0008 specifies required atom fields — verify they exist on KnowledgeAtom."""
        try:
            from know.schema import KnowledgeAtom
        except ImportError:
            self.skipTest("know package not importable — run `uv sync` first")

        # Fields required by ADR-0008 for the atom model to function
        required_fields = {
            "type",
            "title",
            "content",
            "epistemic_grade",
            "project_scope",
            "status",
            "created_at",
            "last_verified",
            "decay_rate",
        }

        atom_fields = set()
        if hasattr(KnowledgeAtom, "__annotations__"):
            atom_fields.update(KnowledgeAtom.__annotations__.keys())
        if hasattr(KnowledgeAtom, "__dataclass_fields__"):
            atom_fields.update(KnowledgeAtom.__dataclass_fields__.keys())

        missing = required_fields - atom_fields
        self.assertFalse(
            missing,
            f"KnowledgeAtom missing ADR-0008 required fields: {sorted(missing)}",
        )

    def test_memory_service_protocol_exists(self) -> None:
        """ADR-0008 requires MemoryService Protocol in core/contracts/memory.py."""
        from nowu.core.contracts.memory import MemoryService

        self.assertTrue(
            hasattr(MemoryService, "__protocol_attrs__")
            or hasattr(MemoryService, "_is_protocol")
            or "Protocol" in str(MemoryService.__mro__),
            "MemoryService must be a typing.Protocol",
        )

    def test_memory_service_has_recall_context(self) -> None:
        """ADR-0008 requires MemoryService to expose recall_context for atom queries."""
        from nowu.core.contracts.memory import MemoryService

        self.assertTrue(
            hasattr(MemoryService, "recall_context"),
            "MemoryService must define recall_context() method",
        )

    def test_no_direct_know_import_in_nowu_modules(self) -> None:
        """ADR-0008: nowu accesses know only through MemoryService Protocol — no direct imports."""
        import ast

        violations: list[str] = []

        for py_file in SRC_ROOT.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            if "bridge" in str(py_file.relative_to(SRC_ROOT)):
                continue  # bridge/ is the infrastructure adapter layer — know imports are architecturally correct here

            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("know.") or alias.name == "know":
                            relative = py_file.relative_to(SRC_ROOT)
                            violations.append(
                                f"{relative} imports '{alias.name}' directly"
                            )
                elif isinstance(node, ast.ImportFrom):
                    if node.module and (
                        node.module.startswith("know.") or node.module == "know"
                    ):
                        relative = py_file.relative_to(SRC_ROOT)
                        violations.append(
                            f"{relative} imports from '{node.module}' directly"
                        )

        self.assertFalse(
            violations,
            "ADR-0008 violation — nowu modules must not import know directly. "
            "Use MemoryService Protocol.\n" + "\n".join(violations),
        )


class ADR0010EpistemicGradeFitnessTest(unittest.TestCase):
    """Validates structural properties required by ADR-0010: Epistemic Grade Assignment."""

    def test_epistemic_grade_enum_has_five_levels(self) -> None:
        """ADR-0010 defines exactly 5 epistemic grades — verify enum completeness."""
        try:
            from know.schema import EpistemicGrade
        except ImportError:
            self.skipTest("know package not importable — run `uv sync` first")

        expected_names = {
            "SPECULATION",
            "HYPOTHESIS",
            "INFORMED_ESTIMATE",
            "EVIDENCE_BASED",
            "VERIFIED_FACT",
        }

        actual_names = {member.name for member in EpistemicGrade}
        self.assertEqual(
            actual_names,
            expected_names,
            f"EpistemicGrade enum members don't match ADR-0010 spec. "
            f"Expected: {sorted(expected_names)}. Got: {sorted(actual_names)}",
        )

    def test_epistemic_grade_ordering(self) -> None:
        """ADR-0010 defines grade ordering: SPECULATION(1) < ... < VERIFIED_FACT(5)."""
        try:
            from know.schema import EpistemicGrade
        except ImportError:
            self.skipTest("know package not importable — run `uv sync` first")

        self.assertEqual(EpistemicGrade.SPECULATION.value, 1)
        self.assertEqual(EpistemicGrade.HYPOTHESIS.value, 2)
        self.assertEqual(EpistemicGrade.INFORMED_ESTIMATE.value, 3)
        self.assertEqual(EpistemicGrade.EVIDENCE_BASED.value, 4)
        self.assertEqual(EpistemicGrade.VERIFIED_FACT.value, 5)

    def test_knowledge_atom_carries_grade(self) -> None:
        """ADR-0010 requires every atom to carry an epistemic_grade field."""
        try:
            from know.schema import KnowledgeAtom
        except ImportError:
            self.skipTest("know package not importable — run `uv sync` first")

        atom_fields = set()
        if hasattr(KnowledgeAtom, "__annotations__"):
            atom_fields.update(KnowledgeAtom.__annotations__.keys())
        if hasattr(KnowledgeAtom, "__dataclass_fields__"):
            atom_fields.update(KnowledgeAtom.__dataclass_fields__.keys())

        self.assertIn(
            "epistemic_grade",
            atom_fields,
            "ADR-0010 requires epistemic_grade on KnowledgeAtom — field missing",
        )


class ADR0007ContinuityContractFitnessTest(unittest.TestCase):
    """Validates structural properties required by ADR-0007: Session Continuity."""

    def test_session_snapshot_type_exists(self) -> None:
        """ADR-0007 requires SessionSnapshot in core/contracts/types.py."""
        from nowu.core.contracts.types import SessionSnapshot

        self.assertTrue(
            hasattr(SessionSnapshot, "__annotations__")
            or hasattr(SessionSnapshot, "__dataclass_fields__"),
            "SessionSnapshot must be a dataclass or have annotations",
        )

    def test_session_store_protocol_exists(self) -> None:
        """ADR-0007 requires SessionStore Protocol in core/contracts/session.py."""
        from nowu.core.contracts.session import SessionStore

        self.assertTrue(
            hasattr(SessionStore, "__protocol_attrs__")
            or hasattr(SessionStore, "_is_protocol")
            or "Protocol" in str(SessionStore.__mro__),
            "SessionStore must be a typing.Protocol",
        )


if __name__ == "__main__":
    unittest.main()
