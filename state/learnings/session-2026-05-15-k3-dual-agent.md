---
artifact_type: SESSION_LEARNINGS
session: "K3 dual-agent comparison: T7 (workflow) vs T8 (freeform)"
created_at: 2026-05-15
session_type: "comparison"
source_artifacts:
  - state/learnings/session-2026-05-15-k3-workflow.md
  - .sisyphus/evidence/k3-freeform/approach.md
  - src/nowu/core/contracts/memory.py
  - src/nowu/bridge/know_adapter.py
  - .sisyphus/evidence/k3-freeform/know_adapter.py
  - tests/bridge/test_know_adapter.py
  - .sisyphus/evidence/k3-freeform/test_know_adapter.py
purpose: "Compare T7 workflow output vs T8 freeform output on K3 across 8 dimensions and produce recommendations"
models_used:
  - T7: workflow-agent (committed on feat/K3)
  - T8: freeform-agent (evidence in .sisyphus/evidence/k3-freeform/)
---

# K3 Dual-Agent Comparison — 2026-05-15

Summary: Side-by-side comparison of T7 (workflow-driven, committed on feat/K3) and T8 (freeform, evidence-only) implementing K3 (MemoryService expansion + KnowAdapter). Both implementations produced passing tests (15 each), mypy strict and ruff clean in their respective contexts. This document rates both on 8 dimensions (5 standard + 3 code-specific), lists key insights, and recommends follow-ups.

Scores (1–5, higher is better). Metrics shown where quantitative.

| Dimension | T7 (workflow) | T8 (freeform) | Notes / evidence |
|---|---:|---:|---|
| Time | 3 | 5 | T7 claimed ~16m45s; T8 approach.md: start 15:39:36 — finish 15:51:39 (~12m03s). Faster = higher score.
| Artifact quality | 5 | 4 | T7: structured session learnings, evidence artifacts, ADR decision rows. T8: complete evidence set but freeform files use temporary test scaffolding and mypy disables.
| Blindspot detection | 5 | 3 | T7 recorded architecture exemption (ADR fitness) and decisions (D-SESS-01/02). T8 missed recording formal session decisions (evidence only).
| Process overhead | 2 | 5 | T7 followed S1–S9 (intake artifacts, explicit decisions) — higher overhead. T8 direct implementation = lower overhead.
| Evidence depth | 5 | 4 | T7 produced multiple evidence files and QA outputs in .sisyphus; T8 produced granular approach.md and quality-check but lacked integrated session artifact.
| Test coverage | 4 | 5 | Both report 15 tests. T8 tests include additional parsing and status-count scenarios (task_status counts, search delegation). T7 tests are thorough mapping tests. Quantitatively: 15 tests each.
| Type safety | 5 | 3 | Both pass mypy in their contexts. T7 uses targeted type: ignore for missing sibling stubs and explicit casts at boundary. T8 uses file-level mypy disable (import-untyped) in freeform artifacts — larger surface area disabled.
| API design | 4 | 4 | Both keep MemoryService generic. T7 adapter is minimal and idiomatic (explicit _to_grade helpers). T8 adapter is more defensive with many parse_* helpers; useful but may leak adapter behaviour (defaults like AtomStatus.ACTIVE).

Key quantitative facts
- Tests: T7 = 15, T8 = 15 (evidence files `.sisyphus/evidence/task-7-adapter-tests.txt` and `.sisyphus/evidence/k3-freeform/quality-check.txt`)
- MemoryService methods: 11 methods in both `src/nowu/core/contracts/memory.py` and `.sisyphus/evidence/k3-freeform/memory.py`.
- Time: T7 ~16m45s (claimed), T8 ~12m03s (approach.md timestamps).
- mypy/ruff: T7 quality gates show full-suite pass (`.sisyphus/evidence/task-7-quality-gates.txt`). T8 reported mypy/ruff pass for evidence files (`.sisyphus/evidence/k3-freeform/quality-check.txt`).
- Type-ignore / mypy disables: T7 applied targeted `# type: ignore[import-not-found]` at bridge boundary (2 occurrences in know_adapter.py). T8 applied file-level `# mypy: disable-error-code=import-untyped` in freeform artifacts (memory.py + know_adapter.py).

Key insights (min 3)

1) Workflow produces stronger audit trail and architectural discipline. T7's S1–S9 flow captured explicit decisions (D-SESS-01/D-SESS-02) and updated the ADR fitness test to reflect the bridge exemption; this reduces friction later during reviews and supports reproducible reasoning.

2) Freeform is faster and surfaced useful defensive parsing and status-handling patterns. T8's adapter implements more parsing helpers (parse_optional_status, _parse_epistemic_grade) and tests task-status aggregation — useful patterns that could harden the committed adapter.

3) Type-safety hygiene diverges: targeted ignores (T7) are preferable to file-level mypy disables (T8). Both pass mypy, but T8's broad disables increase risk of silent typing regressions when ported into src/ without adjustments.

4) Test-surface parity is strong (both 15 tests) but quality differs slightly: T8 covers more runtime parsing edge cases; T7 focuses on explicit mapping to know.schema enums. Combining both sets yields best coverage.

Recommendations (D-SESS entries)

- D-SESS-03: Adopt defensive parsing helpers from T8 into the committed KnowAdapter in `bridge/` but keep APIs in MemoryService unchanged. Add unit tests for parse_* edge cases. Rationale: improves robustness without breaking contract.

- D-SESS-04: Keep workflow S1–S9 artifact discipline for any change that affects architecture tests or ADRs. Use faster freeform experiments for rapid prototyping, but record any architectural exceptions into state/learnings and create a follow-up intake when changes are promoted to src/.

- D-SESS-05: Replace file-level mypy disables from freeform artifacts before merging any code into src/. Prefer targeted casts and `# type: ignore[...]` only when necessary; track a follow-up to add proper py.typed or stubs for `know` in the workspace.

Agents / files reviewed

- T7 (workflow): `state/learnings/session-2026-05-15-k3-workflow.md`, `src/nowu/core/contracts/memory.py`, `src/nowu/bridge/know_adapter.py`, `tests/bridge/test_know_adapter.py`, `.sisyphus/evidence/task-7-*` artifacts.
- T8 (freeform): `.sisyphus/evidence/k3-freeform/approach.md`, `.sisyphus/evidence/k3-freeform/memory.py`, `.sisyphus/evidence/k3-freeform/know_adapter.py`, `.sisyphus/evidence/k3-freeform/test_know_adapter.py`, `.sisyphus/evidence/k3-freeform/quality-check.txt`.

Follow-ups (actionable)

1. Create a small PR to incorporate safe parse_* helpers from T8 into `src/nowu/bridge/know_adapter.py`. Add 3 targeted tests demonstrating parsing robustness.
2. Add MemoryService surface tests to lock method signatures (prevent accidental API drift).
3. Remove broad mypy disables in freeform artifacts when porting code into src/ — replace with targeted ignores and/or add stubs for `know`.

Evidence files created alongside this session

- .sisyphus/evidence/task-9-comparison.txt
- .sisyphus/evidence/task-9-session-learning.txt

End of session learning.
