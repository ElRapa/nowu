# Testing Rules

## TDD is Non-Negotiable
1. Write a failing test first
2. Make it pass with minimal code
3. Refactor while keeping tests green

## Test Organization
```
tests/
├── unit/              # Fast, isolated, no I/O
│   ├── core/
│   ├── flow/
│   └── bridge/
├── integration/       # Real `know` instance (temp dir)
├── architecture/      # Import boundary enforcement (AST)
└── e2e/              # Full CLI flows
```

## Conventions
- Test files: `test_<module>.py`
- Test functions: `test_<behavior>_<condition>_<expected>`
- Use pytest fixtures, not setUp/tearDown
- Prefer `tmp_path` for filesystem tests
- Integration tests against `know` use temp `KNOW_DATA_DIR`

## Quality Gates (must pass before any commit)
```bash
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .
```

## Coverage
- Target 90%+ on `core` and `flow`
- No coverage exceptions without documented rationale
