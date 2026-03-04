"""Architecture compliance tests for module import boundaries."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from nowu.core.boundaries import ALLOWED_INTERNAL_IMPORTS


SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "nowu"


def _module_owner(py_file: Path) -> str:
    relative = py_file.relative_to(SRC_ROOT)
    parts = relative.parts
    return parts[0]


def _imported_internal_modules(py_file: Path) -> set[str]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    imports: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("nowu."):
                    parts = alias.name.split(".")
                    if len(parts) > 1:
                        imports.add(parts[1])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("nowu."):
                parts = node.module.split(".")
                if len(parts) > 1:
                    imports.add(parts[1])

    return imports


class ImportBoundariesTest(unittest.TestCase):
    def test_internal_import_boundaries_are_respected(self) -> None:
        py_files = [p for p in SRC_ROOT.rglob("*.py") if p.name != "__init__.py"]
        self.assertTrue(py_files, "Expected at least one Python module to validate")

        violations: list[str] = []

        for py_file in py_files:
            owner = _module_owner(py_file)
            allowed = ALLOWED_INTERNAL_IMPORTS.get(owner, set())
            imported = _imported_internal_modules(py_file)

            for imported_module in sorted(imported):
                if imported_module == owner:
                    continue
                if imported_module not in allowed:
                    relative = py_file.relative_to(SRC_ROOT)
                    violations.append(
                        f"{relative} imports nowu.{imported_module}, "
                        f"but {owner} only allows {sorted(allowed)}"
                    )

        self.assertFalse(violations, "\n".join(violations))


if __name__ == "__main__":
    unittest.main()
