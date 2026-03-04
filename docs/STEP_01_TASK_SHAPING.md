# Step 01 Task Shaping

Date: 2026-03-04
Use-case IDs: `NF-01`, `NF-02`, `NF-03`

## S1-T1: Create package scaffold and Python project metadata

In scope:
- Create `pyproject.toml` with `src` package layout.
- Create baseline packages: `nowu.core`, `nowu.flow`, `nowu.bridge`, `nowu.soul`.

Out of scope:
- Runtime business logic.
- CLI commands and external integrations.

Acceptance criteria:
1. Project has valid `src` package structure.
2. Top-level packages import successfully.
3. Metadata and test config are present.

Verification commands:
- `PYTHONPATH=src python3 -c "import nowu, nowu.core, nowu.flow, nowu.bridge, nowu.soul"`

## S1-T2: Add explicit core contracts for later slices

In scope:
- Add shared contract types.
- Add protocols for memory, session, and approvals.

Out of scope:
- Concrete implementations of these protocols.

Acceptance criteria:
1. Contract modules exist and are importable.
2. Contracts represent Step 02+ interfaces (memory/session/approvals).

Verification commands:
- `PYTHONPATH=src python3 -m unittest tests/core/test_contracts_import.py -v`

## S1-T3: Add architecture boundary policy and compliance tests

In scope:
- Define allowed internal imports by module owner.
- Add automated tests to detect boundary violations.

Out of scope:
- Enforcing external dependency policy (for example direct `know` usage) beyond Step 01 baseline.

Acceptance criteria:
1. Boundary policy is codified in one place.
2. Tests fail if disallowed cross-module imports are added.

Verification commands:
- `PYTHONPATH=src python3 -m unittest tests/architecture/test_import_boundaries.py -v`

## S1-T4: Run integrated verification for Step 01

In scope:
- Execute full Step 01 test suite.
- Confirm no regressions from current baseline.

Out of scope:
- Coverage gating.

Acceptance criteria:
1. Contract and boundary tests pass.
2. Step 01 artifacts are committed and traceable.

Verification commands:
- `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v`

