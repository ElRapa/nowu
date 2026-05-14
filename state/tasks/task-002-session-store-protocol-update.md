---
id: task-002-session-store-protocol-update
title: "SessionStore Protocol Update"
created: 2026-05-12
status: READY_FOR_IMPL
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: HYPOTHESIS
decision_id: D-024
intake_id: intake-001
story_id: story-v1core-001-s002
estimated_hours: 2
primary_module: core
depends_on:
  - task-001-session-checkpoint-type
use_case_ids:
  - NF-01
docs_to_update:
  - None
---

# Task Spec: task-002-session-store-protocol-update

## In-Scope Files

- src/nowu/core/contracts/session.py
- src/nowu/core/contracts/__init__.py
- tests/unit/core/test_session_store_protocol.py

## Out of Scope

- Everything not listed above
- src/nowu/core/contracts/types.py — type definitions are task-001's scope
- src/nowu/flow/__init__.py — FileSessionStore implementation is task-003
- tests/architecture/test_import_boundaries.py — not touched; import structure is unchanged

## Breaking Change Notice

This task updates the `SessionStore` Protocol signatures. This is a Tier 3 change
explicitly approved via D-024 (Option C: Versioned Schema).

**Before:**
```python
def load(self) -> SessionSnapshot | None: ...
def save(self, snapshot: SessionSnapshot) -> None: ...
```

**After:**
```python
def load(self) -> SessionCheckpoint | None: ...
def save(self, checkpoint: SessionCheckpoint) -> None: ...
```

Any concrete implementation of `SessionStore` must update its signatures to match.
`FileSessionStore` in `flow` is the only known concrete implementation (task-003).
No callers outside `flow` currently call these methods (confirmed by empty `flow/__init__.py`
surface and empty `flow/` module body prior to this intake).

## Acceptance Criteria

- id: AC-1
  description: >
    `SessionStore.load()` return type is `SessionCheckpoint | None` (not
    `SessionSnapshot | None`). The Protocol method has the updated type annotation
    and a docstring: "Load the latest session checkpoint if one exists."
  test_function_name: test_session_store_protocol_load_returns_checkpoint_type

- id: AC-2
  description: >
    `SessionStore.save()` parameter type is `SessionCheckpoint` (not `SessionSnapshot`).
    The parameter is named `checkpoint`. The Protocol method has a docstring:
    "Persist a checkpoint to durable storage."
  test_function_name: test_session_store_protocol_save_accepts_checkpoint_type

- id: AC-3
  description: >
    A concrete class that implements `SessionStore` by defining `load()` returning
    `SessionCheckpoint | None` and `save(checkpoint: SessionCheckpoint)` satisfies
    the Protocol at runtime (verified via `isinstance` check against Protocol, or
    structural subtype duck-typing check).
  test_function_name: test_session_store_protocol_concrete_impl_satisfies_protocol

- id: AC-4
  description: >
    `RoleOrchestrator` Protocol in `session.py` is unchanged — its signature and
    docstring are identical to the pre-task state. No regression on the existing
    role orchestration contract.
  test_function_name: test_role_orchestrator_protocol_unchanged

- id: AC-5
  description: >
    `SessionStore` and `RoleOrchestrator` are exported from `core/contracts/__init__.py`
    so that callers can import via `from nowu.core.contracts import SessionStore`.
  test_function_name: test_session_store_importable_from_contracts_package

## Test Strategy (TDD order)

1. Write `test_session_store_protocol_load_returns_checkpoint_type` — inspect `load` return annotation on the Protocol class. Confirm RED (still `SessionSnapshot | None`).
2. Write `test_session_store_protocol_save_accepts_checkpoint_type` — inspect `save` parameter annotation. Confirm RED.
3. Write `test_session_store_protocol_concrete_impl_satisfies_protocol` — define minimal inline class with correct signatures, assert isinstance or structural check passes. Confirm RED.
4. Write `test_role_orchestrator_protocol_unchanged` — assert `next_role` signature unchanged (regression guard). Confirm GREEN.
5. Write `test_session_store_importable_from_contracts_package` — import path check. Confirm RED (not yet exported).
6. Update `session.py` Protocol signatures — confirm AC-1, AC-2, AC-3 go GREEN.
7. Export from `__init__.py` — confirm AC-5 goes GREEN.
8. Confirm AC-4 still GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-01
    story_ac: AC-001 from story-v1core-001-s002
    criteria: [AC-1, AC-2, AC-3]
    rationale: >
      The updated Protocol signatures are the contract that flow's FileSessionStore
      (task-003) implements. AC-1 and AC-2 define the exact interface that task-003
      and task-004 will call — without this contract, flow cannot call load() at
      session start (story-v1core-001-s002 AC-001: agent reads persisted state and
      identifies last verified checkpoint). AC-3 ensures the Protocol is structurally
      satisfied by any conforming implementation.
  - use_case: NF-01
    story_ac: AC-003 from story-v1core-001-s002
    criteria: [AC-4, AC-5]
    rationale: >
      AC-4 is a regression guard ensuring the role orchestration contract is not
      broken by this task — protecting non-session pipeline steps. AC-5 ensures the
      updated SessionStore is importable for use in task-004's flow integration
      (prevents the agent contradicting prior pipeline steps due to a broken import).
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
