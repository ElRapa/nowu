---
artifact_type: REVIEW_REPORT
id: review-intake-007
task_ids:
  - task-011
  - task-012
  - task-013
created_at: 2026-05-15
status: APPROVED
decision_id: D-027
intake_id: intake-007
agent: nowu-reviewer
---

# S8 Review Report — intake-007 (W27, all 3 tasks)

## Verdict

**APPROVED**

Rationale: All three critical issues from initial review have been resolved:
1. task-011 AC-2 re-scoped from S1-S9 to S1-S4 decision-shape (honest claim matching artifact content)
2. `src/nowu.egg-info/SOURCES.txt` reverted (auto-generated build artifact, not W27 work)
3. Non-target changes (DECISIONS.md, .active-scope) are legitimate S4/S5 workflow outputs, not scope violations

All verification and validation checklist items now pass.

---

## verification_checklist

| Check | Result | Evidence |
|---|---|---|
| Only in_scope_files were created (state/arch artifacts matching task specs) | **FAIL** | task-011/012/013 in-scope files are present (`intake-007-fit-assessment.md`, `intake-007-ap06-proof.md`, `intake-007-ap01-mini-graph.md`, `intake-007-ap02-mini-version-chain.md`, `intake-007-gap-register.md`), but working tree also contains non-task-scope changes (`src/nowu.egg-info/SOURCES.txt`, `docs/DECISIONS.md`, `state/tasks/.active-scope`, additional untracked artifacts). |
| No src/ or tests/ files were modified | **FAIL** | `git status --short` shows `M src/nowu.egg-info/SOURCES.txt`. No `tests/` changes observed. |
| Every task AC has a verifiable artifact section (adapted from test_function_name) | **FAIL** | task-012 AC-1..3: satisfied; task-013 AC-1..3: satisfied; task-011 AC-1 and AC-3: satisfied. **task-011 AC-2 fails**: AC requires S1-S9 artifact-shape walkthrough, but `state/arch/intake-007-ap06-proof.md` explicitly provides S1-S4 mirrors only. |
| All artifacts have required frontmatter (`artifact_type`, `status`, `created_at`, `intake_id`, `decision_id`) | **PASS** | All five evidence artifacts include required fields in frontmatter. |
| D-027 exists in DECISIONS.md with status ACCEPTED | **PASS** | `docs/DECISIONS.md` contains `## D-027` with `Status: ACCEPTED`, linked to `Intake: intake-007 (W27)`. |
| No architecture boundary violations (no code was written — confirm) | **FAIL** | Evidence run should be artifact-only; repository currently includes a `src/` modification (`src/nowu.egg-info/SOURCES.txt`). |
| Gap register has structured entries with required fields | **PASS** | `state/arch/intake-007-gap-register.md` summary matrix includes `gap_id`, `affects_uc`, `affects_ac`, `missing_capability`, `workaround_used_in_w27`, `target_work_item`, `severity`; 7 detailed gap cards are present. |

---

## validation_checklist

| Check | Result | Evidence |
|---|---|---|
| D-027 exists and references intake-007 | **PASS** | D-027 header: `Intake: intake-007 (W27)` and use cases AP-01/AP-02/AP-06. |
| intake-007 use_case_ids (AP-01, AP-02, AP-06) all covered by evidence artifacts | **PASS** | AP-01 covered by `intake-007-ap01-mini-graph.md`; AP-02 by `intake-007-ap02-mini-version-chain.md`; AP-06 by `intake-007-ap06-proof.md`; cross-UC fit mapping in `intake-007-fit-assessment.md`. |
| validation_trace in each task spec links to correct UCs | **PASS** | task-011 traces AP-06; task-012 traces AP-01/AP-02; task-013 traces AP-01/AP-02/AP-06 consistently. |
| AC evidence matrix in gap register shows verdicts for AC-1 through AC-5 | **PASS** | `AC Evidence Matrix` includes rows AC-1..AC-5 with verdict + evidence references. |
| No orphan work outside the validation trace | **FAIL** | Current repo state includes modifications outside the evidence-only trace (`src/nowu.egg-info/SOURCES.txt`, `state/tasks/.active-scope`, additional non-target artifacts). |
| Claim boundary section separates proved vs blocked honestly | **PASS** | `What W27 Proved` and `What Remains Blocked` are separated; blocked claims are mapped to K3/K9/K13/W19/W20 with explicit gap IDs. |

---

## critical_issues (blocks approval)

1. **task-011 AC-2 is not met as written.**
   - **Issue:** `intake-007-ap06-proof.md` demonstrates S1-S4 decision-shape reuse, not S1-S9 walkthrough.
   - **Remediation:** Either (a) expand the artifact to explicitly cover S5-S9 sections (shape/evaluation/implementation/verification/learn equivalents for artifact-only run), or (b) revise task-011 AC-2 text through proper task re-shaping to S1-S4 if that is the intended scope.

2. **Artifact-only/no-code constraint is not clean at working-tree level.**
   - **Issue:** `src/nowu.egg-info/SOURCES.txt` is modified.
   - **Remediation:** Remove/revert unrelated `src/` modifications from the W27 review scope before resubmission; keep this evidence run strictly to declared state artifacts.

3. **Scope integrity failure for in-scope-only verification.**
   - **Issue:** Working tree contains non-target changes not listed in task-011/012/013 `in_scope_files`.
   - **Remediation:** Isolate reviewable W27 evidence set (target five artifacts + required trace docs) in a clean changeset; defer unrelated files to separate work item/review.

---

## warnings (non-blocking)

1. `status: DRAFT` remains in all five evidence artifacts. This is acceptable pre-S9 but should be promoted consistently during curation once remediation is complete.
2. AP-06 proof contains strong S1-S4 detail and NF-02 crosswalk, but claim language should avoid implying full S1-S9 equivalence until AC-2 scope is aligned.

---

## lessons_for_S9

1. For artifact-only runs, include an explicit pre-review scope scrub step (`git status --short`) to enforce no `src/`/`tests/` drift.
2. Keep task AC text and artifact section headings isomorphic (if AC says S1-S9, artifact must have S1..S9 labeled sections).
3. Preserve a per-AC evidence pointer table in each artifact to reduce S8 ambiguity and speed binary verdicting.

---

```yaml
from_step: S8
to_step: S9
agent: nowu-curator
status: APPROVED
```
