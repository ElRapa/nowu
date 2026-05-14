---
artifact_type: TASK_SPEC
id: task-001-session-checkpoint-type
title: "Core Contracts: SessionCheckpoint Type"
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
depends_on: []
use_case_ids:
  - NF-01
docs_to_update:
  - None
---

# Task Spec: task-001-session-checkpoint-type

## In-Scope Files

- src/nowu/core/contracts/types.py
- src/nowu/core/contracts/session.py
- src/nowu/core/contracts/__init__.py
- tests/unit/core/test_session_checkpoint_type.py

## Out of Scope

- Everything not listed above
- src/nowu/flow/__init__.py — no flow changes in this task
- src/nowu/core/boundaries.py — import boundary checks are not modified here
- Any implementation of FileSessionStore — that is task-003
- Any new test fixtures in tests/conftest.py (unless required for the unit tests in scope)

## Acceptance Criteria

- id: AC-1
  description: >
    A frozen dataclass `SessionCheckpoint` exists in `core/contracts/types.py` with
    exactly these 10 fields: `session_id: str`, `active_project: str`,
    `active_role: RoleName`, `next_action: str`, `active_step: str`,
    `active_ids: dict[str, str]`, `completed_steps: list[str]`,
    `last_artifact_path: str`, `checkpoint_grade: str`,
    `schema_version: str`. The dataclass is frozen (`frozen=True`).
    `active_ids` and `completed_steps` use `field(default_factory=...)`.
    `schema_version` defaults to `"v1"`.
  test_function_name: test_session_checkpoint_type_has_required_fields

- id: AC-2
  description: >
    `SessionSnapshot` is retained in `core/contracts/types.py` but carries a
    deprecation docstring: "Deprecated — use SessionCheckpoint. Retained for
    compatibility; will be removed in v1." No fields removed, no behavior changed.
  test_function_name: test_session_snapshot_deprecated_stub_unchanged

- id: AC-3
  description: >
    `SessionCheckpoint` is exported from `core/contracts/__init__.py` alongside
    `SessionSnapshot`, so callers can import either via
    `from nowu.core.contracts import SessionCheckpoint`.
  test_function_name: test_session_checkpoint_importable_from_contracts_package

- id: AC-4
  description: >
    `SessionCheckpoint` is immutable: constructing one and attempting to assign to
    any field raises `dataclasses.FrozenInstanceError`.
  test_function_name: test_session_checkpoint_is_frozen

- id: AC-5
  description: >
    `schema_version` defaults to `"v1"` when not supplied; constructing
    `SessionCheckpoint` without `schema_version` keyword succeeds and returns
    an instance with `schema_version == "v1"`.
  test_function_name: test_session_checkpoint_schema_version_defaults_to_v1

## Test Strategy (TDD order)

1. Write `test_session_checkpoint_type_has_required_fields` — assert attribute names, types, frozen=True. Confirm RED (type does not exist).
2. Write `test_session_checkpoint_is_frozen` — assert FrozenInstanceError on setattr. Confirm RED.
3. Write `test_session_checkpoint_schema_version_defaults_to_v1` — construct without schema_version, assert "v1". Confirm RED.
4. Write `test_session_snapshot_deprecated_stub_unchanged` — construct existing SessionSnapshot, assert all 5 original fields still work. Confirm GREEN (no change to SessionSnapshot yet).
5. Write `test_session_checkpoint_importable_from_contracts_package` — `from nowu.core.contracts import SessionCheckpoint`. Confirm RED.
6. Add `SessionCheckpoint` to `types.py` — confirm AC-1, AC-2, AC-4, AC-5 go GREEN.
7. Export from `__init__.py` — confirm AC-3 goes GREEN.
8. Add deprecation docstring to `SessionSnapshot` — confirm AC-2 still GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-01
    story_ac: AC-001 from story-v1core-001-s002
    criteria: [AC-1, AC-4, AC-5]
    rationale: >
      AC-1 establishes the SessionCheckpoint schema that the agent reads at session
      start (story-v1core-001-s002 AC-001: agent reads persisted state and identifies
      last verified checkpoint). AC-4 ensures immutability so the loaded checkpoint
      cannot be silently mutated. AC-5 ensures the schema_version field is present for
      migration logic (task-003), which is required before the load/save path in task-002
      can be validated.
  - use_case: NF-01
    story_ac: AC-003 from story-v1core-001-s002
    criteria: [AC-2, AC-3]
    rationale: >
      AC-2 preserves the existing SessionSnapshot stub, preventing breakage of any
      existing code that imports it. AC-3 exports SessionCheckpoint as the single
      authoritative session type — both are required to ensure no callers silently
      break when the Protocol is updated in task-002 (AC-003: agent must not
      contradict prior recorded decisions — a broken import would prevent loading
      the checkpoint).
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
