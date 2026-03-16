# Code Style Rules

## Python Standards
- Python 3.11+ features encouraged (match, StrEnum, etc.)
- Line length: 100 (ruff configured)
- Strict mypy: all functions fully annotated, no `Any` without justification

## Naming
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_prefix`
- Protocols/interfaces: descriptive names, not `I`-prefixed

## Function Design
- Keep functions < 20 lines
- Single responsibility
- Pure functions in `core` wherever possible
- No side effects in domain logic

## Imports
```python
# Standard library
from pathlib import Path

# Third-party
import typer

# Local — absolute imports from src root
from nowu.core.contracts import MemoryPort
from nowu.flow.session import SessionManager
```

## Docstrings
Google-style, required on all public classes and functions:
```python
def create_task(title: str, scope: str) -> Task:
    """Create a new task atom in the knowledge graph.

    Args:
        title: Human-readable task name.
        scope: Project scope identifier.

    Returns:
        The created Task with generated ID.

    Raises:
        ValidationError: If title is empty or scope unknown.
    """
```
