# Testing Rules v2.1

## TDD Order (mandatory)

1. RED: write a failing test that names the acceptance criterion
2. GREEN: minimal implementation to make it pass
3. REFACTOR: clean up while keeping green

Never write implementation before a failing test exists.

## Test Naming

`test_[unit]_[scenario]_[expected_outcome]`

Examples:
- `test_search_empty_query_returns_empty_list`
- `test_session_resume_after_crash_restores_state`

## Test Structure

- Unit tests: `tests/unit/[module]/test_[file].py`
- Integration tests: `tests/integration/test_[scenario].py`
- One test class per module under test
- One test function per acceptance criterion (minimum)

## Coverage Gate

- Minimum 80% line coverage on changed files
- New public functions must have at least one test
- VBR will FAIL if coverage drops below threshold on changed files

## Scope Enforcement

Tests may only import from in_scope_files and test utilities.
Cross-module test imports require explicit justification in task spec.
