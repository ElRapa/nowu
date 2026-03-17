# Testing Rules

## TDD Order (non-negotiable)
1. Write a failing test (RED) — commit message: `test: add failing test for <AC-N>`
2. Make it pass with minimal code (GREEN)
3. Refactor — keep tests green

## Test Naming
`test_<unit>_<scenario>_<expected_outcome>`
Example: `test_session_store_when_full_raises_capacity_error`

## Structure
tests/unit/<module>/      — fast, no I/O, mock all externals
tests/integration/        — real deps, slower, tagged @pytest.mark.integration
tests/e2e/                — CLI/API surface only

## Coverage Gate
`--cov=nowu --cov-fail-under=90` — must stay above 90%

## Fixtures
Shared fixtures in `tests/conftest.py`. Never duplicate fixture logic.
Use `pytest.mark.parametrize` for boundary/edge-case variants.
