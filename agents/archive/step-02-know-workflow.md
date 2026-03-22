---
name: know-workflow-implementer
description: Add workflow lifecycle helpers to the know module (computed state + template instantiation).
---

You are a senior Python engineer extending the `know` module.
Read `ARCHITECTURE.md`, `DECISIONS.md`, and `.github/copilot-instructions.md` before starting.
The step-01 PR must be merged before starting this step.

## Goal
Implement workflow lifecycle helpers: `compute_workflow_state()` and `instantiate_workflow()`.

## Acceptance Criteria (VBR)

- [ ] `know/workflow.py` exists with both functions
- [ ] `compute_workflow_state()` returns correct state for all four cases
- [ ] `instantiate_workflow()` creates task atoms with DERIVED_FROM + DEPENDS_ON connections
- [ ] `today()` in `know/today.py` excludes `blocked` tasks
- [ ] `pytest tests/know/test_workflow.py -v` passes, 90%+ coverage

## Functions to Implement (`know/workflow.py`)

```python
from know.storage import Storage
from know.models import KnowledgeAtom, Connection, AtomType, ConnectionType

def compute_workflow_state(task_id: str, storage: Storage) -> str:
    """
    Compute one of: 'blocked', 'ready', 'active', 'done'.

    Rules:
    - If task.task_status == 'done' → 'done'
    - Elif any DEPENDS_ON target has task_status != 'done' → 'blocked'
    - Elif task.task_status == 'in_progress' → 'active'
    - Else → 'ready'
    """

def instantiate_workflow(
    template_id: str,
    instance_name: str,
    project_scope: list[str],
    storage: Storage,
) -> list[KnowledgeAtom]:
    """
    Clone a workflow template into real task atoms.

    Steps:
    1. Fetch template concept atom (template_id).
    2. Fetch child step atoms via BELONGS_TO connections (incoming).
    3. Sort steps by their own DEPENDS_ON order.
    4. For each step, create a new task atom:
       - title: f"{instance_name}: {step.title}"
       - type: AtomType.TASK
       - task_status: "open"
       - project_scope: project_scope
    5. Add DERIVED_FROM connection: new_task → step
    6. Mirror DEPENDS_ON edges between new tasks to match template order.
    7. Return list of new task atoms.
    """
```

## Update `know/today.py`

```python
from know.storage import Storage
from know.workflow import compute_workflow_state

def today(storage: Storage, project_scope: list[str] | None = None, limit: int = 5) -> list[KnowledgeAtom]:
    """
    Return top ranked open/in-progress tasks.
    Excludes tasks where compute_workflow_state() == 'blocked'.
    Ranks by: critical > high > medium > low priority, then by due_date.
    """
```

## Tests (`tests/know/test_workflow.py`)

Cover:
1. Linear workflow A→B→C: B is blocked when A is open
2. After A is done, B becomes ready
3. `instantiate_workflow` creates correct number of task atoms
4. Each instance task has DERIVED_FROM connection to template step
5. Instance task DEPENDS_ON mirrors template order
6. `today()` does not return blocked tasks
7. `today()` returns tasks sorted by priority

## Output
Branch: `feat/know-workflow`. PR: `[know] Workflow lifecycle: computed state + template instantiation`.
