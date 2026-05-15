---
step: S8
artifact_id: intake-007
artifact_path: state/reviews/intake-007-review.md
run_date: 2026-05-15
agent: nowu-reviewer
outcome: CHANGES_REQUESTED
---

# S8 Analysis — intake-007

## What Went Well

- Evidence artifacts were concrete, internally consistent, and trace-linked to `intake-007` and `D-027`.
- Gap register quality was strong: structured summary matrix + 7 detailed cards + AC matrix + explicit claim boundary.
- Validation trace coverage across AP-01/AP-02/AP-06 was straightforward to confirm from task specs and artifact content.

## Friction Points

- AC phrasing mismatch: task-011 AC-2 requires S1-S9 proof while artifact title/body provide S1-S4 only, creating binary-review ambiguity.
- Artifact-only scope was asserted in content but not clean in working tree (`src/nowu.egg-info/SOURCES.txt` modified), forcing scope-integrity failure.
- Multi-task aggregate review lacked a precompiled AC-to-section index, increasing manual cross-referencing effort.

## Quality Assessment

- **Input quality:** MEDIUM-HIGH — task specs and evidence were present and readable, but AC granularity mismatch reduced determinism.
- **Output quality:** HIGH — binary verdict with explicit failed checks and remediation paths.
- **Confidence:** HIGH — blockers are objective (AC text mismatch + non-artifact `src/` modification in diff).

## Review Verdict

- **verdict:** CHANGES_REQUESTED
- **primary_reason:** task-011 AC-2 not satisfied as written (S1-S9 required vs S1-S4 delivered), plus artifact-only scope breach in repository diff.

## Failure Classification

- **failure_type:** missing-ac
- **failure_detail:** AC-2 (task-011) requires S1-S9 artifact-shape walkthrough; delivered proof only demonstrates S1-S4.

## Improvement Signals

1. Add an explicit `ac_scope_shape` field in task specs when AC references workflow stages (e.g., `S1-S4` vs `S1-S9`) to avoid interpretation drift.
2. Add a required S8 preflight checklist item template: `git status --short` must show no out-of-scope path families (`src/`, `tests/`) for artifact-only runs.
3. Include a mandatory “AC Evidence Pointers” section in each artifact with direct section anchors per AC for deterministic review.

## Tags

- [step:S8, outcome:CHANGES_REQUESTED, friction:ac-mismatch, friction:scope-drift, module:state-arch, intake:intake-007, decision:D-027]
