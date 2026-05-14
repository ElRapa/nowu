---
id: capture-intake-001
task_ids: [task-001, task-002, task-003, task-004, task-005]
intake_id: intake-001
decision_id: D-024
captured: 2026-05-13
next_cycle_trigger: CONTINUE
status: DONE
altitude: EXECUTION
phase: LEARN
epistemic_grade: INFORMED_ESTIMATE
---

# Capture Record: intake-001 — W4 First S1-S9 Cycle

## Progress Update

- intake-001: COMPLETED (all 5 tasks DONE)
- Use cases addressed: NF-01
- Story covered: story-v1core-001-s002 (Agent Checkpoint Resumption)
- Next: W5 — Validate 5×10 coordinates on W4 artifacts (now unblocked)

---

## What Changed

Session checkpoint persistence was introduced across `core` and `flow` modules. A new `SessionCheckpoint` dataclass (10 fields, versioned schema) replaced the prior 5-field `SessionSnapshot`, and the `SessionStore` protocol was updated to match. `FileSessionStore` now writes an atomic JSON checkpoint alongside a human-readable YAML bookmark (`state/SESSION_STATE.md`), with migration logic for the old format. The `flow` pipeline reads the checkpoint at session start and surfaces it for agent consumption.

---

## Why It Matters

This cycle delivers NF-01 v1-core: agents can read persisted state, identify the last verified step, and propose the correct next action without hallucinating progress. Humans receive a YAML bookmark that communicates current project state clearly on resume. This is the foundation of the continuity layer that goal-001 ("project momentum survives interruptions") requires — W4 is the first probe of that goal's core hypothesis. The cycle also validates the S1-S9 workflow end-to-end for the first time.

---

## Lessons Learned

1. **D-024 versioned schema was the right option.** Option C (Versioned Schema) resolved the SessionSnapshot migration cleanly with minimal blast radius. The `schema_version` field enables forward migration without API churn. The atomicity pattern (tempfile + rename) is now established as a reusable idiom for any future file-based state writes.

2. **Dependency hygiene gap in VBR.** `pyyaml` is imported at runtime in `session_store.py` but is not declared in `[project.dependencies]` — only the type stubs are. The transitive availability through `know` masked this through all 5 VBR runs. VBR should include a check that every production `import X` maps to a direct declared dependency, not just an available transitive one.

3. **Cross-task writes need an assigned owner in S5.** Necessary workflow artifacts that span multiple tasks (e.g., D-024 addition to DECISIONS.md) landed outside all task `in_scope_files` and `docs_to_update` declarations. S5 shaping should explicitly assign cross-cutting writes to a specific task or a named "workflow housekeeping" task.

4. **ADR-0007 field divergence is authorized but undocumented.** `SessionCheckpoint` omits `checkpoint_id`, `timestamp`, and `blockers` relative to ADR-0007's full spec, adding `schema_version` instead. D-024 authorizes this as a v1-core simplification, but ADR-0007 itself carries no note of the divergence. This will confuse the next engineer unless a "Known Limitations" note is added to ADR-0007.

5. **TDD ordering cannot be verified post-hoc from git log.** All implementation was committed as a working-tree batch. S7 (VBR) should require test files to be committed ahead of implementation files, or at minimum include a creation-timestamp ordering check.

---

## Decisions Captured

D-024 — Versioned Session Checkpoint Schema (module level, ACCEPTED, 2026-05-12). Implemented as Option C: 10-field `SessionCheckpoint` dataclass with `schema_version`, atomic YAML bookmark, migration from old 5-field format. Review trigger satisfied — migration complete, schema translation tested, atomicity proven.

No new decisions required beyond D-024 (already recorded during S4).

---

## Follow-On Items (non-blocking, flagged for next cycle)

**F1 (W5 or standalone):** Add `"pyyaml>=6.0"` to `[project.dependencies]` in `pyproject.toml`. Low effort. Blocks clean deployment in environments where the transitive `know` path changes.

**F2 (W9 or ADR amendment):** Add a "Known Limitations" note to ADR-0007 documenting the v1-core `SessionCheckpoint` field simplification (missing `checkpoint_id`, `timestamp`, `blockers`; added `schema_version`). Reference D-024 as the authorizing decision. Prevents future confusion about the schema divergence.

---

## Next Cycle Trigger

**trigger:** CONTINUE
**reason:** Review APPROVED with no architectural surprises. Story story-v1core-001-s002 is the only story in this intake cycle; W4 is now complete, unblocking W5 (validate 5×10 coordinates on W4 artifacts). Remaining stories in epic-v1core-001 (s001, s003, s004) are in-scope for subsequent intakes. CONTINUE to W5, then next intake from epic-v1core-001.

---

## Commit Message

```
feat(flow,core): session checkpoint persistence — NF-01 [W4 complete]

- SessionCheckpoint (10-field versioned schema) replaces SessionSnapshot
- FileSessionStore writes atomic JSON + YAML bookmark (state/SESSION_STATE.md)
- Pipeline reads checkpoint at start; agent receives verified next-action context
- 43 tests, 98.54% coverage; mypy --strict clean; ruff clean
- Decision followed: D-024 (Versioned Schema, Option C)
- Follow-on: add pyyaml to project.dependencies; add Known Limitations to ADR-0007
- Next: W5 (validate 5×10 coordinates on W4 artifacts)

Use case: NF-01 (Resume Work After Context Loss)
```

---

## Architecture Model Updates

No module boundaries changed. `core` and `flow` already existed in the C4 L2 architecture; this intake populated their session contract surfaces. The `SessionStore` protocol and `FileSessionStore` implementation are within the declared module boundaries (D-003).

**Pending note for ARCHITECTURE.md:** `flow` module now owns `FileSessionStore` as the concrete session persistence adapter. `core/contracts/session.py` is the binding protocol. `state/SESSION_STATE.md` is the canonical human-readable bookmark artifact produced by `FileSessionStore`. These are new operational surfaces not previously documented at C4 L3.
