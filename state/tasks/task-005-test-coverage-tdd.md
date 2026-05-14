---
artifact_type: TASK_SPEC
id: task-005-test-coverage-tdd
title: "Test Coverage: Migration, Schema Translation, Atomicity"
created: 2026-05-12
status: READY_FOR_IMPL
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: HYPOTHESIS
decision_id: D-024
intake_id: intake-001
story_id: story-v1core-001-s002
estimated_hours: 3
primary_module: flow
depends_on:
  - task-001-session-checkpoint-type
  - task-002-session-store-protocol-update
  - task-003-file-session-store-migration
  - task-004-flow-session-start-integration
use_case_ids:
  - NF-01
docs_to_update:
  - None
---

# Task Spec: task-005-test-coverage-tdd

## In-Scope Files

- tests/unit/flow/test_file_session_store.py
- tests/unit/flow/test_pipeline.py
- tests/unit/core/test_session_checkpoint_type.py
- tests/integration/test_session_checkpoint_roundtrip.py

## Out of Scope

- Everything not listed above
- src/nowu/ — no production source changes; this task only adds tests
- tests/architecture/ — import boundary and ADR fitness tests are pre-existing and not modified
- tests/conftest.py — shared fixtures may be extended only if required by integration tests;
  any conftest change must be explicitly justified in the implementation PR

## Context

Tasks 001–004 define the TDD tests as part of each task's test strategy. This task exists
to close three coverage gaps that are not owned by any single implementation task:

1. **Migration path exhaustiveness** — test all distinct JSON input states that
   `FileSessionStore.load()` must handle (not just old-vs-new, but edge cases).
2. **Save atomicity** — test that a simulated write failure on the JSON step does not
   produce a partial or corrupt bookmark file.
3. **Integration roundtrip** — write a checkpoint via `start_session` + `checkpoint_at_step_boundary`,
   then read it back with a fresh `FileSessionStore` instance, assert round-trip fidelity.
4. **No-hallucination guard** — test that the value returned by `start_session()` is the
   literal deserialized content of the checkpoint file, not a default-constructed object.

## Acceptance Criteria

- id: AC-1
  description: >
    `test_file_session_store_load_missing_file_returns_none` — when the checkpoint
    file does not exist at the expected path, `FileSessionStore.load()` returns `None`
    without raising an exception.
  test_function_name: test_file_session_store_load_missing_file_returns_none

- id: AC-2
  description: >
    `test_file_session_store_load_corrupt_json_raises_value_error` — when the
    checkpoint file exists but contains invalid JSON (e.g., truncated or non-JSON
    text), `FileSessionStore.load()` raises `ValueError` with a message that
    includes the file path.
  test_function_name: test_file_session_store_load_corrupt_json_raises_value_error

- id: AC-3
  description: >
    `test_file_session_store_save_atomicity_json_fail_no_bookmark_written` — when a
    `save()` call is made and the JSON write raises an `OSError` (simulated via
    monkeypatching), the bookmark file (`STATE_SESSION.md`) is not written or
    modified. The test confirms the bookmark is absent or unchanged after the
    failed save.
  test_function_name: test_file_session_store_save_atomicity_json_fail_no_bookmark_written

- id: AC-4
  description: >
    `test_session_checkpoint_roundtrip_save_then_load_is_identical` — an integration
    test that: (1) creates a `FileSessionStore` with a temp directory, (2) calls
    `checkpoint_at_step_boundary(store, checkpoint)` with a fully-populated
    `SessionCheckpoint`, (3) creates a NEW `FileSessionStore` instance pointing to
    the same temp directory, (4) calls `start_session(store2)`, (5) asserts the
    returned checkpoint equals the original in all 10 fields. The test uses real
    filesystem I/O (no mocking of file operations).
  test_function_name: test_session_checkpoint_roundtrip_save_then_load_is_identical

- id: AC-5
  description: >
    `test_start_session_returns_actual_persisted_content_not_default` — given a
    checkpoint file with a specific, distinctive `next_action` value (e.g.,
    "run-S6-on-task-003"), when `start_session(store)` is called, the returned
    checkpoint's `next_action` equals that exact string — confirming the value
    came from the file, not a default constructor or inference.
  test_function_name: test_start_session_returns_actual_persisted_content_not_default

- id: AC-6
  description: >
    Running `uv run pytest tests/unit/flow/ tests/unit/core/ tests/integration/test_session_checkpoint_roundtrip.py --cov=src/nowu/flow --cov=src/nowu/core/contracts --cov-fail-under=90`
    exits 0. Line coverage on `src/nowu/flow/session_store.py` and
    `src/nowu/flow/pipeline.py` is 90% or greater.
  test_function_name: test_coverage_gate_90_percent_on_flow_and_contracts

## Test Strategy (TDD order)

1. Write `test_file_session_store_load_missing_file_returns_none` — call load() on empty temp dir. Confirm GREEN after task-003 implementation (returns None for missing path). If RED at task-003 boundary, that indicates task-003 has a gap.
2. Write `test_file_session_store_load_corrupt_json_raises_value_error` — write "not-json" to checkpoint file, call load(). Confirm RED if task-003 does not handle this; GREEN after task-005 fixes it.
3. Write `test_file_session_store_save_atomicity_json_fail_no_bookmark_written` — monkeypatch `Path.write_text` to raise OSError on first call only, assert bookmark absent. Confirm RED if task-003 has no guard; GREEN after task-005 adds guard.
4. Write `test_session_checkpoint_roundtrip_save_then_load_is_identical` — full roundtrip with real filesystem. Confirm RED until tasks 003 + 004 complete. This test is the integration gate.
5. Write `test_start_session_returns_actual_persisted_content_not_default` — distinctive string test. Confirm RED until tasks 003 + 004 complete.
6. Run coverage command; confirm 90%+ gate. If below, identify uncovered lines and add targeted tests within this task's scope.

Note: AC-6 is verified by running the coverage command, not by a named test function per se.
The `test_coverage_gate_90_percent_on_flow_and_contracts` name refers to the CI command
that must pass — it may be implemented as a pytest marker or as a Makefile/pyproject.toml
target.

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-01
    story_ac: AC-001 from story-v1core-001-s002
    criteria: [AC-4, AC-5]
    rationale: >
      AC-4 (roundtrip) and AC-5 (no-default guard) together constitute the
      machine-verifiable test that story-v1core-001-s002 AC-001 is actually
      satisfied end-to-end: the agent reads persisted state (not a default), identifies
      the correct last checkpoint, and receives it with all fields intact. Without
      this roundtrip test, the unit tests in tasks 001-004 could all pass while a
      serialization bug silently corrupts the data read at session start.
  - use_case: NF-01
    story_ac: AC-002 from story-v1core-001-s002
    criteria: [AC-4]
    rationale: >
      AC-4 verifies that `completed_steps` round-trips correctly. story-v1core-001-s002
      AC-002 requires the agent not to re-execute completed steps — this is only
      reliable if completed_steps is written and read back without loss or corruption.
  - use_case: NF-01
    story_ac: AC-003 from story-v1core-001-s002
    criteria: [AC-2, AC-3]
    rationale: >
      AC-2 (corrupt JSON raises ValueError) prevents silent hallucination: if the
      checkpoint is unreadable, the failure is explicit, not silently filled with
      defaults. AC-3 (atomicity) prevents a partial write from leaving a corrupt
      state artifact that the agent reads as valid — either case would cause the
      agent to contradict prior decisions (story-v1core-001-s002 AC-003).
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
