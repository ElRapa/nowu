# Code Style Rules

## Python Version
Python 3.11+ features encouraged: match statements, tomllib, ExceptionGroup.

## Tooling
- `ruff` for lint + format (line-length=100, target-version=py311)
- `mypy --strict` — no `Any` unless absolutely necessary, all functions typed

## Naming
Classes: `PascalCase` | functions/methods: `snake_case` | constants: `UPPER_SNAKE`
Private: prefix `_` | Type vars: `T`, `V`, or descriptive `TModel`

## Function Design
- < 20 lines ideally, single responsibility
- Pure functions in domain layer — no side effects
- Prefer immutable value objects over mutable state

## Imports (always in this order)
1. stdlib  2. third-party  3. local (absolute: `from nowu.domain.models import X`)

## Docstrings
Google-style for public APIs. One-line for internal helpers.
