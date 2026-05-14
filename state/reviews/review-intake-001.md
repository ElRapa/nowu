---
id: review-intake-001
altitude: EXECUTION
phase: EVALUATION
epistemic_grade: EVIDENCE_BASED
intake_id: intake-001
task_ids: [task-001, task-002, task-003, task-004, task-005]
story_id: story-v1core-001-s002
created: 2026-05-13
status: APPROVED
decision_id: D-024
reviewer: nowu-reviewer (S8)
---

# Review Report: intake-001 W4 Implementation (Tasks 001–005)

## Summary

Five-task implementation of NF-01 session checkpoint continuity (D-024, Option C:
Versioned Schema). All VBR gates pass live. 43 tests, 98.54% coverage on in-scope
modules. One warning issued (undeclared runtime dependency) — does not block approval.

---

## Verification Checklist (built it right?)

| # | Check | Result | Evidence |
|---|---|---|---|
| V-1 | TDD: tests written before implementation | PASS (conditional) | Task specs enumerate explicit RED→GREEN TDD order for all 5 tasks; VBR reports confirm no pre-existing tests were broken. Git history shows all changes as uncommitted working tree — TDD ordering cannot be verified from commit log. Verified by: (a) each task spec has step-ordered test strategy; (b) VBR reports note specific new-test counts per task; (c) tests reference non-existent modules via local imports (deferred until GREEN step) |
| V-2 | VBR: all 5 tasks PASS pytest, mypy --strict, ruff, coverage 90%+ | PASS | Live-verified: `uv run pytest` → 43 passed 0 failed; `uv run mypy src/ --strict` → no issues (13 source files); `uv run ruff check .` → all checks passed; coverage 98.54% on flow+contracts |
| V-3 | Scope: only in_scope_files modified | PASS (with caveats — see warnings) | Combined `.active-scope` matches all modified src/test files. Out-of-scope modifications: `docs/DECISIONS.md` (D-024 added — necessary prerequisite, not declared in any task's `docs_to_update`), `scripts/verify-artifact.py` (formatting only), `.sisyphus/reports/t8-agent-spec-review.md` (model version), `state/intake/intake-001.md` (appetite update), `src/nowu.egg-info/SOURCES.txt` (auto-generated), `state/tasks/.active-scope` (tooling). None alter production behavior. |
| V-4 | Contracts: SessionStore Protocol updated correctly (D-024) | PASS | `session.py`: `load() -> SessionCheckpoint \| None`, `save(checkpoint: SessionCheckpoint) -> None`, `@runtime_checkable` added. Breaking change is intentional per D-024 (Tier 3, explicitly approved). Zero call sites outside `flow` (confirmed by empty flow body pre-intake). |
| V-5 | No new runtime dependencies added | WARNING | `pyyaml` is imported at runtime in `session_store.py` but is NOT declared as a direct runtime dependency in `pyproject.toml[project.dependencies]`. Only `types-pyyaml` is added (to `[dependency-groups].dev`). `pyyaml` is available transitively via `know` → `sentence-transformers` → `huggingface_hub`. This is fragile — a future `know` update could remove the transitive path. Remediation: add `pyyaml` to `[project.dependencies]`. Does not block approval (tests pass; dependency is available). |
| V-6 | Atomicity: FileSessionStore handles concurrent writes safely | PASS | `_atomic_write_json()` uses `tempfile.mkstemp` + `Path.replace` (POSIX-atomic rename). Bookmark written only after rename succeeds. Test `test_file_session_store_atomicity_rollback_on_json_failure` and `test_file_session_store_save_atomicity_json_fail_no_bookmark_written` verify no partial state on failure. |
| V-7 | No print/debug statements left in code | PASS | Grep of `session_store.py`, `pipeline.py`, `types.py`, `session.py` returns zero hits for `print`, `pdb`, `breakpoint`. |

---

## Validation Checklist (built the right thing?)

| # | Check | Result | Evidence |
|---|---|---|---|
| Va-1 | AC-1: Agent can read checkpoint and propose next action | PASS | `test_session_checkpoint_roundtrip_save_then_load_is_identical` (task-005 AC-4) and `test_start_session_returns_actual_persisted_content_not_default` (task-005 AC-5) together prove that `start_session()` returns the persisted checkpoint with all 10 fields intact — the agent has everything needed to identify the last verified step and propose the correct next action. |
| Va-2 | AC-2: Human receives clear signal (YAML bookmark) | PASS | `test_file_session_store_save_writes_yaml_bookmark` (task-003 AC-3) verifies a valid YAML file is written to `bookmark_path` with 8 required keys including `active_step`, `next_action`, `completed_steps`. File is parseable by `yaml.safe_load`. This is the `state/SESSION_STATE.md` artifact the human reads at session start. |
| Va-3 | AC-3: No hallucination — agent reads from artifact, not infers | PASS | `test_start_session_returns_actual_persisted_content_not_default` uses a distinctive `next_action="run-S6-on-task-003"` probe value that cannot be a default. Assertion fails if any non-persisted value is returned. `test_file_session_store_load_corrupt_json_raises_value_error` ensures corrupt state raises `ValueError` (explicit failure) rather than silently filling defaults. |
| Va-4 | NF-01 acceptance criteria fully satisfied | PASS | AC-1 (read checkpoint → propose next action): covered by tasks 001+002+003+004+005. AC-2 (human receives YAML bookmark): covered by task-003 AC-3. AC-3 (no hallucination): covered by task-005 AC-2 + AC-5. All three intake ACs have named passing tests. |
| Va-5 | Use case traceability: every test links to NF-01 AC or story AC | PASS | All 5 task validation_traces point to `use_case: NF-01` with story_ac references from `story-v1core-001-s002`. Story ACs (AC-001, AC-002, AC-003) are covered by: AC-001 → task-001 AC-1/4/5 + task-003 AC-4/5 + task-004 AC-1/2 + task-005 AC-4/5; AC-002 → task-003 AC-2 + task-004 AC-3 + task-005 AC-4; AC-003 → task-002 AC-4/5 + task-004 AC-5 + task-005 AC-2/3. No orphan tests identified. |
| Va-6 | Module boundaries respected: only core + flow modified | PASS | No imports from `know`, `bridge`, `soul` were added. `session_store.py` imports only from `nowu.core.contracts` (permitted cross-module path via contracts API). Architecture rule: modules communicate through `core/contracts`. |
| Va-7 | D-024 decision implemented as approved (SessionCheckpoint replaces SessionSnapshot in SessionStore) | PASS | Protocol signatures updated per D-024 Option C. `SessionCheckpoint` dataclass created with 10 fields (matching D-024 "10 fields required"). Migration logic in `FileSessionStore` reads old 5-field format and upgrades. YAML bookmark written atomically. D-024 Status: ACCEPTED. |
| Va-8 | ADR-0007 hypothesis tested: 10-field checkpoint + versioning works | PASS (partial — v1-core scope) | The 10-field schema is implemented and roundtrip-verified. `schema_version` field enables forward migration. Fields differ from ADR-0007 full spec (missing: `checkpoint_id`, `timestamp`, `blockers`; added: `schema_version`) — this is a deliberate v1-core simplification authorized by D-024 and task-001 AC-1 which explicitly enumerate the 10 fields. ADR-0007 remains PROPOSED (evidence run complete; promotion to ACCEPTED is W9 work per intake-001 deferred list). |

---

## Documentation Validation

| Check | Result | Notes |
|---|---|---|
| All `docs_to_update` fields satisfied | PASS | All 5 tasks declare `docs_to_update: None`. Confirmed: no new ADRs created, no binding docs modified within task scope. |
| D-024 exists in DECISIONS.md with status ACCEPTED | PASS | D-024 added to `docs/DECISIONS.md` (outside task scope but necessary prerequisite; acceptable workflow artifact). |
| ADR-0007 referenced correctly | PASS | `session.py` docstring references ADR-0007. ADR-0007 status remains PROPOSED (correct — not promoted within this intake per deferred list). |
| `intake-001.md` appetite updated (medium, 14h) | PASS | Reflects S4 decision to extend for comprehensive test coverage. Workflow metadata update, appropriate. |

---

## Critical Issues

None. No blockers to approval.

---

## Warnings (non-blocking)

**W-1: `pyyaml` is an undeclared direct runtime dependency**

`src/nowu/flow/session_store.py` imports `yaml` at runtime (line 15). `pyyaml` is not
declared in `[project.dependencies]` in `pyproject.toml`. Only `types-pyyaml` (type stubs)
is added to `[dependency-groups].dev`.

`pyyaml` is available transitively through `know` → `sentence-transformers` → `huggingface_hub`
→ `pyyaml`. This works today but is fragile: a future version of `know` that upgrades or
swaps its ML dependencies could break `nowu`'s YAML writes silently.

Remediation: add `"pyyaml>=6.0"` to `[project.dependencies]` in `pyproject.toml`.

**W-2: Out-of-scope file modifications (non-production)**

Three files modified outside any task's `in_scope_files` or `docs_to_update`:
- `scripts/verify-artifact.py` — formatting-only change (list style). Zero behavioral impact.
- `.sisyphus/reports/t8-agent-spec-review.md` — model version string update. Unrelated to implementation.
- `state/tasks/.active-scope` — tooling file, expected side effect of task management.

None affect production behavior. Flagged for workflow hygiene.

**W-3: ADR-0007 schema divergence is undocumented**

The implemented `SessionCheckpoint` omits three fields from ADR-0007's specified schema
(`checkpoint_id`, `timestamp`, `blockers`) and adds one (`schema_version`). D-024 authorizes
this as a v1-core simplification, but no note in ADR-0007 records that the intake-001
implementation intentionally differs from the full spec. Recommend adding a note to
ADR-0007 "Known Limitations" or a comment in `types.py` linking to D-024 and explaining
the v1-core field set, so the next engineer understands why `checkpoint_id` is absent.

---

## Lessons for S9

1. **Dependency hygiene gate**: VBR should check that every `import X` in production
   `src/` corresponds to a declared dependency in `[project.dependencies]`. The
   transitive `pyyaml` availability masked a missing declaration through all 5 VBR runs.

2. **Out-of-scope change tracking**: The workflow produces multi-task intakes where some
   necessary changes (D-024 addition to DECISIONS.md) span across task boundaries and
   land outside any task's declared scope. S5 shaping should explicitly assign
   cross-cutting writes (DECISIONS.md updates, intake appetite corrections) to a
   specific task's `docs_to_update` or create a separate "workflow housekeeping" task.

3. **TDD verification gap**: All implementation work is uncommitted (working tree), making
   it impossible to verify RED→GREEN ordering from git log. S7 (VBR) should include a
   git commit ordering check or require that test files have creation timestamps earlier
   than implementation files.

---

## Status: APPROVED

All 3 intake acceptance criteria (NF-01 AC-1, AC-2, AC-3) are satisfied by named, passing
tests. 43 tests pass, 98.54% coverage. `mypy --strict` clean. `ruff` clean. The
implementation correctly realizes D-024 Option C (Versioned Schema). Warning W-1
(undeclared pyyaml) is the only meaningful finding and does not block approval given the
transitive dependency is confirmed present.

---

```yaml
from_step: S8
to_step: S9
agent: nowu-curator
status: APPROVED
next_action: >
  S9 (nowu-curator): capture D-024 learnings, update docs/ROADMAP-003.md status fields,
  write state/capture/capture-intake-001.md. Flag W-1 (pyyaml) as a
  pyproject.toml fix for the next task cycle.
```
