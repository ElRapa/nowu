---
id: 2026-05-12-task-001-session-checkpoint-type
task_id: task-001-session-checkpoint-type
created: 2026-05-12
---

# Changeset: task-001-session-checkpoint-type

## Files Changed

| File | Type | Lines Added | Lines Removed |
|---|---|---|---|
| src/nowu/core/contracts/types.py | modified | 13 | 1 |
| src/nowu/core/contracts/__init__.py | modified | 18 | 0 |
| tests/unit/core/test_session_checkpoint_type.py | added | 127 | 0 |
| tests/unit/__init__.py | added | 0 | 0 |
| tests/unit/core/__init__.py | added | 0 | 0 |

## Summary

Added `SessionCheckpoint` frozen dataclass to `core/contracts/types.py` with 10 fields
(9 required + `schema_version` defaulting to `"v1"`), and updated `SessionSnapshot` with
a deprecation docstring. Exported `SessionCheckpoint` from the `core/contracts` package
`__init__.py` alongside the existing `SessionSnapshot`.

## AC Coverage

| AC | Test Function | Status |
|---|---|---|
| AC-1 | test_session_checkpoint_type_has_required_fields | PASS |
| AC-2 | test_session_snapshot_deprecated_stub_unchanged | PASS |
| AC-3 | test_session_checkpoint_importable_from_contracts_package | PASS |
| AC-4 | test_session_checkpoint_is_frozen | PASS |
| AC-5 | test_session_checkpoint_schema_version_defaults_to_v1 | PASS |

---
```yaml
from_step: S6
to_step: S7
agent: nowu-implementer (VBR)
status: READY_FOR_VBR
```
