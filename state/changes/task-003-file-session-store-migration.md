---
id: 2026-05-12-task-003-file-session-store-migration
task_id: task-003-file-session-store-migration
created: 2026-05-12
altitude: EXECUTION
phase: IMPLEMENTATION
epistemic_grade: EVIDENCE_BASED
---

# Changeset: task-003-file-session-store-migration

## Files Changed

| File | Type | Lines Added | Lines Removed |
|---|---|---|---|
| src/nowu/flow/session_store.py | added | 216 | 0 |
| src/nowu/flow/__init__.py | modified | 4 | 0 |
| tests/unit/flow/test_file_session_store.py | added | 359 | 0 |
| tests/unit/flow/__init__.py | added | 0 | 0 |
| pyproject.toml | modified | 1 | 0 |
| uv.lock | modified | ~40 | 0 |

## Summary

`FileSessionStore` is a concrete implementation of the `SessionStore` Protocol that persists `SessionCheckpoint` objects as JSON (one file per session under `sessions_dir/{session_id}/checkpoint-latest.json`) and writes a YAML human-readable bookmark to `bookmark_path` after each save. The save path is atomic: JSON is written via a temp-file-and-rename sequence; the bookmark is only written after the rename succeeds, guaranteeing no partial state on failure. The load path detects old 5-field `SessionSnapshot` JSON (missing `schema_version`) and migrates it to `SessionCheckpoint` with safe defaults, setting `schema_version="v0-migrated"`.

## AC Coverage

| AC | Test Function | Status |
|---|---|---|
| AC-1 | test_file_session_store_implements_session_store_protocol | PASS |
| AC-2 | test_file_session_store_save_writes_json_and_bookmark | PASS |
| AC-3 | test_file_session_store_save_writes_yaml_bookmark | PASS |
| AC-4 | test_file_session_store_load_migrates_old_snapshot_format | PASS |
| AC-4 (None branch) | test_file_session_store_load_returns_none_when_missing | PASS |
| AC-5 | test_file_session_store_load_reads_v1_checkpoint_correctly | PASS |
| AC-6 | test_file_session_store_importable_from_flow_package | PASS |
| Atomicity | test_file_session_store_atomicity_rollback_on_json_failure | PASS |

---
```yaml
from_step: S6
to_step: S7
agent: nowu-implementer (VBR)
status: READY_FOR_VBR
```
