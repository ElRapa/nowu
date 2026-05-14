---
id: task-004-flow-session-start-integration
title: "Integration: Flow Session Start"
created: 2026-05-12
status: READY_FOR_IMPL
decision_id: D-024
intake_id: intake-001
story_id: story-v1core-001-s002
estimated_hours: 3
primary_module: flow
depends_on:
  - task-001-session-checkpoint-type
  - task-002-session-store-protocol-update
  - task-003-file-session-store-migration
use_case_ids:
  - NF-01
docs_to_update:
  - None
---

# Task Spec: task-004-flow-session-start-integration

## In-Scope Files

- src/nowu/flow/__init__.py
- src/nowu/flow/pipeline.py
- tests/unit/flow/test_pipeline.py

## Out of Scope

- Everything not listed above
- src/nowu/flow/session_store.py — FileSessionStore is task-003's scope
- src/nowu/core/contracts/ — contracts are task-001 and task-002's scope
- tests/integration/ — integration-level tests are task-005's scope
- state/SESSION_STATE.md — a runtime-written artifact; never a source file
- Any changes to agent prompt text or LLM call logic — this task defines the
  interface contract for passing checkpoint data to the agent context, not the
  LLM integration itself

## New File Note

`src/nowu/flow/pipeline.py` does not currently exist. This task creates it.
It is the session-start and step-boundary orchestration module.

## Acceptance Criteria

- id: AC-1
  description: >
    A `start_session(store: SessionStore) -> SessionCheckpoint | None` function
    exists in `src/nowu/flow/pipeline.py`. It calls `store.load()`, returns the
    result, and does nothing else. It is importable from `nowu.flow`.
  test_function_name: test_pipeline_start_session_calls_store_load

- id: AC-2
  description: >
    `start_session()` when `store.load()` returns a `SessionCheckpoint` returns
    that checkpoint unchanged. When `store.load()` returns `None` (no prior
    session), `start_session()` returns `None`. No exception is raised in either
    case.
  test_function_name: test_pipeline_start_session_propagates_checkpoint_or_none

- id: AC-3
  description: >
    A `checkpoint_at_step_boundary(store: SessionStore, checkpoint: SessionCheckpoint) -> None`
    function exists in `src/nowu/flow/pipeline.py`. It calls
    `store.save(checkpoint)` and does nothing else. It is importable from
    `nowu.flow`.
  test_function_name: test_pipeline_checkpoint_at_step_boundary_calls_store_save

- id: AC-4
  description: >
    `start_session()` and `checkpoint_at_step_boundary()` are exported from
    `src/nowu/flow/__init__.py` so that callers can import via
    `from nowu.flow import start_session, checkpoint_at_step_boundary`.
  test_function_name: test_flow_pipeline_functions_importable_from_flow_package

- id: AC-5
  description: >
    The `SessionStore` parameter in both pipeline functions is typed as
    `SessionStore` (the Protocol from `core/contracts`). Mypy strict mode passes
    on `pipeline.py` without `type: ignore` suppressions.
  test_function_name: test_pipeline_functions_typed_against_session_store_protocol

## Test Strategy (TDD order)

1. Write `test_pipeline_start_session_calls_store_load` — create a mock `SessionStore`, call `start_session(store)`, assert `store.load()` was called exactly once. Confirm RED (module does not exist).
2. Write `test_pipeline_start_session_propagates_checkpoint_or_none` — mock store returning a checkpoint, assert propagated; mock store returning None, assert None returned. Confirm RED.
3. Write `test_pipeline_checkpoint_at_step_boundary_calls_store_save` — create mock store and checkpoint, call function, assert `store.save(checkpoint)` called once with correct argument. Confirm RED.
4. Write `test_flow_pipeline_functions_importable_from_flow_package` — import check. Confirm RED.
5. Write `test_pipeline_functions_typed_against_session_store_protocol` — type annotation inspection or mypy subprocess call. Confirm RED.
6. Create `src/nowu/flow/pipeline.py` with both functions — confirm AC-1, AC-2, AC-3, AC-5 go GREEN.
7. Export from `flow/__init__.py` — confirm AC-4 goes GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-01
    story_ac: AC-001 from story-v1core-001-s002
    criteria: [AC-1, AC-2]
    rationale: >
      AC-1 and AC-2 implement the session-start load path: the agent reads persisted
      state at the start of a new session (story-v1core-001-s002 AC-001). The
      `start_session()` function is the explicit hook in flow where the checkpoint
      is retrieved and made available to the agent context. Returning None vs.
      SessionCheckpoint correctly distinguishes "first session ever" from
      "session resumption."
  - use_case: NF-01
    story_ac: AC-002 from story-v1core-001-s002
    criteria: [AC-3]
    rationale: >
      AC-3 implements the step-boundary checkpoint write path.
      story-v1core-001-s002 AC-002 requires the agent not to re-execute completed
      steps. The `checkpoint_at_step_boundary()` function is the mechanism by which
      `completed_steps` is written to durable storage after each step — so the
      next session load can read accurate completion state.
  - use_case: NF-01
    story_ac: AC-003 from story-v1core-001-s002
    criteria: [AC-5]
    rationale: >
      AC-5 ensures the Protocol typing is enforced, which prevents runtime type
      errors that could cause the agent to contradict prior decisions. If the store
      parameter is not typed against SessionStore, a wrong implementation could be
      passed silently — which is the failure mode story-v1core-001-s002 AC-003
      is guarding against.
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
