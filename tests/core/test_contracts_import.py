"""Smoke tests for contract module importability."""

from __future__ import annotations

import importlib
import unittest


MODULES = [
    "nowu",
    "nowu.core",
    "nowu.core.boundaries",
    "nowu.core.contracts.types",
    "nowu.core.contracts.memory",
    "nowu.core.contracts.session",
    "nowu.core.contracts.approval",
    "nowu.flow",
    "nowu.bridge",
    "nowu.soul",
]


class ContractImportsTest(unittest.TestCase):
    def test_contract_modules_import_cleanly(self) -> None:
        for module in MODULES:
            self.assertIsNotNone(importlib.import_module(module))


if __name__ == "__main__":
    unittest.main()
