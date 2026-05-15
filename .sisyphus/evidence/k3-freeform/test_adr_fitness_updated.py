"""Updated ADR fitness test excerpt with bridge know-import exemption."""

from __future__ import annotations

import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "nowu"


class ADR0008KnowledgeAtomFitnessTest(unittest.TestCase):
    """Fitness test excerpt updated for bridge adapter boundary."""

    def test_no_direct_know_import_in_nowu_modules(self) -> None:
        """ADR-0008: nowu accesses know through adapter boundary and protocol."""
        import ast

        violations: list[str] = []

        for py_file in SRC_ROOT.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            if "bridge" in str(py_file.relative_to(SRC_ROOT)):
                continue  # bridge/ is the infrastructure adapter — direct know imports are correct here

            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("know.") or alias.name == "know":
                            relative = py_file.relative_to(SRC_ROOT)
                            violations.append(f"{relative} imports '{alias.name}' directly")
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
            "ADR-0008 violation — non-bridge nowu modules must not import know directly. "
            "Use MemoryService Protocol.\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
