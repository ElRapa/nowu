# Code Style Rules v2.1

## Python Style

- Follow PEP 8
- Type annotations required on all public functions and methods
- Docstrings required on public functions (one-line minimum)
- No unused imports -- ruff will fail
- Import order: stdlib -> third party -> local (enforced by ruff)

## Naming

- Classes: PascalCase
- Functions and variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Private methods: _prefixed_snake_case
- Test functions: `test_[unit]_[scenario]_[expected]`

## File Structure

- One class per file for domain objects
- Helper functions in `utils.py` within the module
- Public API in `__init__.py` -- expose only what contracts require

## Tooling

- Formatter: ruff format
- Linter: ruff check
- Type checker: mypy --strict
- Test runner: pytest with uv run

All tools must pass with zero errors before S8 review.
