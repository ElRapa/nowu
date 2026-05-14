---
artifact_type: TASK_SPEC
id: task-003-file-session-store-migration
title: "FileSessionStore: Migration and Bookmark Writer"
created: 2026-05-12
status: READY_FOR_IMPL
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: HYPOTHESIS
decision_id: D-024
intake_id: intake-001
story_id: story-v1core-001-s002
estimated_hours: 4
primary_module: flow
depends_on:
  - task-001-session-checkpoint-type
  - task-002-session-store-protocol-update
use_case_ids:
  - NF-01
docs_to_update:
  - None
---

# Task Spec: task-003-file-session-store-migration

## In-Scope Files

- src/nowu/flow/session_store.py
- src/nowu/flow/__init__.py
- tests/unit/flow/test_file_session_store.py

## Out of Scope

- Everything not listed above
- src/nowu/core/contracts/ — contracts are task-001 and task-002's scope
- src/nowu/flow/pipeline.py — pipeline step dispatch is task-004's scope
- tests/integration/ — integration-level tests are task-005's scope
- state/SESSION_STATE.md — this file is WRITTEN to at runtime; it must not be modified by the implementer as a source file

## Acceptance Criteria

- id: AC-1
  description: >
    `FileSessionStore` class in `src/nowu/flow/session_store.py` implements the
    `SessionStore` Protocol: `load() -> SessionCheckpoint | None` and
    `save(checkpoint: SessionCheckpoint) -> None`. The constructor accepts
    `sessions_dir: Path` (where checkpoint JSON files are stored) and
    `bookmark_path: Path` (path to `state/SESSION_STATE.md`).
  test_function_name: test_file_session_store_implements_session_store_protocol

- id: AC-2
  description: >
    `FileSessionStore.save()` writes the checkpoint as JSON to
    `{sessions_dir}/{checkpoint.session_id}/checkpoint-latest.json`. The JSON
    contains all 10 fields of `SessionCheckpoint`. The `sessions_dir` and
    session-id sub-directory are created if they do not exist. The write is
    atomic: JSON is written first; if JSON write succeeds, the YAML bookmark is
    written to `bookmark_path`. If JSON write fails, no partial file is left and
    bookmark is not written.
  test_function_name: test_file_session_store_save_writes_json_and_bookmark

- id: AC-3
  description: >
    `FileSessionStore.save()` writes a YAML projection to `bookmark_path`
    (the `state/SESSION_STATE.md` human bookmark). The projection includes at
    minimum: `session_id`, `active_project`, `active_role`, `active_step`,
    `next_action`, `completed_steps`, `last_artifact_path`, `schema_version`.
    The file is valid YAML (parseable by `yaml.safe_load`).
  test_function_name: test_file_session_store_save_writes_yaml_bookmark

- id: AC-4
  description: >
    `FileSessionStore.load()` reads `{sessions_dir}/{session_id}/checkpoint-latest.json`
    and returns a `SessionCheckpoint`. When the JSON has 5 fields (old
    `SessionSnapshot` format: `session_id`, `active_project`, `active_role`,
    `next_action`, `blockers`), it upgrades to `SessionCheckpoint` with the 5
    new fields populated as: `active_step=""`, `active_ids={}`,
    `completed_steps=[]`, `last_artifact_path=""`, `checkpoint_grade="unknown"`,
    `schema_version="v0-migrated"`. When no checkpoint file exists, `load()`
    returns `None`.
  test_function_name: test_file_session_store_load_migrates_old_snapshot_format

- id: AC-5
  description: >
    `FileSessionStore.load()` when called with a valid v1 JSON file (all 10
    fields present, `schema_version="v1"`) returns a `SessionCheckpoint` with
    all fields exactly matching the JSON. No migration logic is applied when
    `schema_version` is `"v1"`.
  test_function_name: test_file_session_store_load_reads_v1_checkpoint_correctly

- id: AC-6
  description: >
    `FileSessionStore` is exported from `src/nowu/flow/__init__.py` so that
    callers can import via `from nowu.flow import FileSessionStore`.
  test_function_name: test_file_session_store_importable_from_flow_package

## Test Strategy (TDD order)

1. Write `test_file_session_store_implements_session_store_protocol` — verify class exists and satisfies Protocol (structural check). Confirm RED (class does not exist).
2. Write `test_file_session_store_load_reads_v1_checkpoint_correctly` — create temp dir, write valid v1 JSON, call `load()`, assert all fields match. Confirm RED.
3. Write `test_file_session_store_load_migrates_old_snapshot_format` — write 5-field JSON, call `load()`, assert migrated defaults. Confirm RED.
4. Write `test_file_session_store_save_writes_json_and_bookmark` — call `save(checkpoint)`, assert JSON file exists with correct content, assert bookmark file exists. Confirm RED.
5. Write `test_file_session_store_save_writes_yaml_bookmark` — call `save()`, read bookmark file with `yaml.safe_load`, assert required keys present. Confirm RED.
6. Write `test_file_session_store_importable_from_flow_package` — import check. Confirm RED.
7. Implement `FileSessionStore` in `src/nowu/flow/session_store.py` — make all tests GREEN.
8. Export from `flow/__init__.py` — confirm AC-6 GREEN.
9. Refactor: extract `_migrate_snapshot_to_checkpoint()` private helper; confirm all GREEN.

## Validation Trace

```yaml
validation_trace:
  - use_case: NF-01
    story_ac: AC-001 from story-v1core-001-s002
    criteria: [AC-4, AC-5]
    rationale: >
      AC-4 and AC-5 together implement the load path: agent reads persisted state
      at session start (story-v1core-001-s002 AC-001). AC-4 covers the migration
      case (old checkpoint exists from a previous session format) and AC-5 covers
      the steady-state case. Both are required for "agent reads persisted state
      and identifies the last verified checkpoint."
  - use_case: NF-01
    story_ac: AC-001 from story-v1core-001-s001
    criteria: [AC-2, AC-3]
    rationale: >
      AC-2 ensures the checkpoint JSON is durably written; AC-3 ensures the
      human-readable bookmark (STATE_SESSION.md) is written atomically alongside
      it. story-v1core-001-s001 AC-001 requires that Raphael receives "last
      completed, most recent decision, recommended next step" from a persisted
      artifact — the YAML bookmark is that artifact for the human path.
  - use_case: NF-01
    story_ac: AC-002 from story-v1core-001-s002
    criteria: [AC-2]
    rationale: >
      AC-2 writes `completed_steps` to the JSON. story-v1core-001-s002 AC-002
      requires the agent not to re-execute completed steps — the `completed_steps`
      field in the persisted checkpoint is the machine-readable source of truth for
      this check in task-004's flow integration.
```

---
```yaml
from_step: S5
to_step: S6
agent: nowu-implementer
status: READY_FOR_IMPL
```
