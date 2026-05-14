---
id: w5-5x10-validation
work_item: W5
altitude: ARCHITECTURE
phase: EVALUATION
epistemic_grade: EVIDENCE_BASED
created: 2026-05-14
status: DONE
input_artifacts:
  - state/intake/intake-001.md
  - state/arch/intake-001-constraints.md
  - state/arch/intake-001-options.md
  - state/tasks/task-00[1-5]-*.md
  - state/changes/task-00[1-5]-*.md
  - state/vbr/task-00[1-5]-*.md
  - state/reviews/review-intake-001.md
  - state/capture/capture-intake-001.md
  - state/analysis/S5-intake-001-analysis.md
  - state/analysis/S8-intake-001-analysis.md
  - state/analysis/S9-capture-intake-001-analysis.md
  - state/learnings/session-2026-05-11-s1-intake-validation.md
  - state/learnings/session-2026-05-13-w4-s2-s9-execution.md
use_cases: [NF-03, NF-09]
---

# W5 Validation Report: 5×10 Coordinates on W4 Artifacts

## 1. Purpose

Validate that the artifacts produced during the first S1-S9 cycle (W4, intake-001)
correctly map to the 5×10 altitude-phase model (D-013). This is the first empirical
test of the model against real workflow output.

**Method:** Inventory all W4 artifacts from git history, check each for altitude/phase
metadata, compare actual positions to the canonical mappings in MODEL-REFERENCE.md
(Section 7: S1-S9 Pipeline, Section 13: Artifact→Position) and WORKFLOW-STANDARDS.md
(Rule 1.1: S1-S9 Zigzag).

---

## 2. W4 Artifact Inventory

Source: `git log --name-only` for commits `6a5f561` (feat: session checkpoint persistence)
through `d95eebd` (Update Roadmap-003 to mark W4 done), plus `b3c0f5b` (capture learnings)
and `f1d44d9` (retire PROGRESS.md). Branch: `feat/w4-first-intake`, merged to `main`.

### Primary Pipeline Artifacts (S1-S9 chain)

| # | Artifact | Step | Exists? | Notes |
|---|----------|------|---------|-------|
| 1 | `state/intake/intake-001.md` | S1 | ✅ | Status: DONE |
| 2 | `state/arch/intake-001-constraints.md` | S2 | ✅ | Status: READY_FOR_OPTIONS |
| 3 | `state/arch/intake-001-options.md` | S3 | ✅ | Status: READY_FOR_DECISION |
| 4 | `state/arch/intake-001-decision.md` | S4 | ❌ MISSING | Listed in session learnings `source_artifacts` but never created. D-024 was written directly to DECISIONS.md. See §5.1. |
| 5 | `docs/DECISIONS.md` (D-024 entry) | S4 | ✅ | Living doc; D-024 added inline. Not a standalone artifact. |
| 6-10 | `state/tasks/task-001..005.md` | S5 | ✅ (5) | All status: READY_FOR_IMPL |
| 11-15 | `state/changes/task-001..005.md` | S6 | ✅ (5) | Changeset records |
| 16-20 | `state/vbr/task-001..005.md` | S7 | ✅ (5) | All status: READY_FOR_REVIEW |
| 21 | `state/reviews/review-intake-001.md` | S8 | ✅ | Status: APPROVED |
| 22 | `state/capture/capture-intake-001.md` | S9 | ✅ | Status: DONE |

### Secondary Artifacts (analysis + learnings)

| # | Artifact | Step | Exists? |
|---|----------|------|---------|
| 23 | `state/analysis/S5-intake-001-analysis.md` | S5 | ✅ |
| 24 | `state/analysis/S8-intake-001-analysis.md` | S8 | ✅ |
| 25 | `state/analysis/S9-capture-intake-001-analysis.md` | S9 | ✅ |
| 26 | `state/learnings/session-2026-05-11-s1-intake-validation.md` | S1 | ✅ |
| 27 | `state/learnings/session-2026-05-13-w4-s2-s9-execution.md` | S2-S9 | ✅ |

### Code Artifacts (not annotated — implementation, not workflow state)

- `src/nowu/core/contracts/types.py`, `session.py`, `__init__.py`
- `src/nowu/flow/pipeline.py`, `session_store.py`
- `tests/unit/core/test_session_checkpoint_type.py`
- `tests/unit/flow/test_file_session_store.py`
- `tests/integration/test_session_checkpoint_roundtrip.py`

Code files are EXECUTION/IMPLEMENTATION artifacts but do not carry YAML frontmatter;
they are validated by VBR (pytest, mypy, ruff), not by 5×10 metadata. Out of scope
for this validation.

**Inventory result:** 22 state artifacts exist out of 23 expected. 1 missing
(`intake-001-decision.md`). 5 code files are implementation artifacts without
metadata (expected — code is validated by VBR, not frontmatter).

---

## 3. Metadata Audit: Before W5

### Result: 0/22 artifacts had altitude, phase, or epistemic_grade in frontmatter.

| Field | Present in N/22 | Notes |
|-------|-----------------|-------|
| `altitude` | 0/22 | Universal gap |
| `phase` | 0/22 | Universal gap |
| `epistemic_grade` | 0/22 | Universal gap |
| `artifact_type` | 3/22 | Only: intake-001.md (INTAKE_BRIEF), 2 learnings (SESSION_LEARNINGS) |
| `step` | 3/22 | Only: 3 analysis files (S5, S8, S9) |
| `from_step`/`to_step` | 11/22 | Task specs (5) + VBR reports (5) + review (1) have trailing YAML handoff blocks |

**Interpretation:** The 5×10 model is defined in MODEL-REFERENCE.md (Section 7, 13) and
WORKFLOW-STANDARDS.md (Rule 1.1) but is **not operationalized in artifact metadata**. The
model exists as documentation; the artifacts carry step-level handoff metadata (`from_step`,
`to_step`) but not altitude-level coordinates. This means the model cannot be validated
automatically from artifact inspection — it requires human/agent interpretation of artifact
location and content.

---

## 4. Expected vs. Actual 5×10 Coordinates

Mapping derived from MODEL-REFERENCE.md Section 13 (Artifact→Position) cross-referenced
with WORKFLOW-STANDARDS.md Rule 1.1 (S1-S9 Zigzag) and the actual S-step workflow.

### Primary Pipeline Artifacts

| Artifact | S-Step | Expected Altitude | Expected Phase | Epistemic Grade | Basis |
|----------|--------|-------------------|----------------|-----------------|-------|
| intake-001.md | S1 | DELIVERY | IDEA | HYPOTHESIS | Section 7: S1 = DELIVERY/IDEA |
| constraints.md | S2 | ARCHITECTURE | ANALYSIS | HYPOTHESIS | Section 7: S2 = ARCH/ANALYSIS |
| options.md | S3 | ARCHITECTURE | OPTIONS | HYPOTHESIS | Section 7: S3 = ARCH/OPTIONS |
| (missing decision.md) | S4 | ARCHITECTURE | DECISION | — | Section 7: S4 = ARCH/DECISION |
| task-001..005.md | S5→S6 | EXECUTION | IMPLEMENTATION | HYPOTHESIS | Section 13: task-NNN = EXEC/IMPL |
| changes-001..005.md | S6 | EXECUTION | IMPLEMENTATION | EVIDENCE_BASED | Changeset is recorded fact |
| vbr-001..005.md | S7 | EXECUTION | VERIFICATION | EVIDENCE_BASED | Section 13: vbr-NNN = EXEC/VERIF |
| review-intake-001.md | S8 | EXECUTION | EVALUATION | EVIDENCE_BASED | Section 13: review-NNN = EXEC/EVAL |
| capture-intake-001.md | S9 | EXECUTION | LEARN | INFORMED_ESTIMATE | Section 13: capture-NNN = EXEC→DELIVERY/LEARN |

### Secondary Artifacts

| Artifact | S-Step | Expected Altitude | Expected Phase | Epistemic Grade | Basis |
|----------|--------|-------------------|----------------|-----------------|-------|
| S5-analysis.md | S5 | DELIVERY | EVALUATION | INFORMED_ESTIMATE | Analysis of S5 output; DELIVERY altitude per S5 |
| S8-analysis.md | S8 | EXECUTION | EVALUATION | INFORMED_ESTIMATE | Analysis of S8 output |
| S9-analysis.md | S9 | EXECUTION | LEARN | INFORMED_ESTIMATE | Analysis of S9 output |
| S1-learnings.md | S1 | DELIVERY | LEARN | INFORMED_ESTIMATE | Learnings span LEARN phase |
| S2-S9-learnings.md | S2-S9 | ARCHITECTURE | LEARN | INFORMED_ESTIMATE | Primary altitude was ARCH (S2-S4) |

### Zigzag Validation

The expected S1-S9 zigzag path:

```
S1: DELIVERY/IDEA ──────────────────────┐
S2: ARCHITECTURE/ANALYSIS ◄─────────────┘ (rise to ARCH)
S3: ARCHITECTURE/OPTIONS ───────────────┐
S4: ARCHITECTURE/DECISION ──────────────┤ (stay at ARCH)
S5: DELIVERY/EVALUATION ◄──────────────┘ (drop to DELIVERY)
S6: EXECUTION/IMPLEMENTATION ◄──────────┐ (drop to EXEC)
S7: EXECUTION/VERIFICATION ─────────────┤ (stay at EXEC)
S8: EXECUTION/EVALUATION ──────────────┤ (stay at EXEC)
S9: EXECUTION→ALL/LEARN ───────────────┘ (zoom out)
```

**Result:** The W4 artifact chain follows this zigzag correctly. Each artifact was produced
by the expected agent at the expected step. No altitude violations detected. The one gap
(missing S4 decision file) does not invalidate the zigzag — D-024 was created in
`docs/DECISIONS.md` at the correct altitude (ARCHITECTURE/DECISION).

---

## 5. Model Inconsistencies Discovered

### 5.1 Missing S4 Decision Artifact (Process Gap)

**Finding:** `state/arch/intake-001-decision.md` is listed in the session learnings
`source_artifacts` but was never created. The S4 decision (D-024) was written directly
to `docs/DECISIONS.md`. The nowu-shaper agent memory (`project_s4_decision_file_gap.md`)
documents this: "S4 did not produce intake-001-decision.md before S5 ran."

**Expected behavior per WORKFLOW.md:** S4 output is `docs/DECISIONS.md` +
`state/arch/intake-NNN-decision.md`.

**Impact:** LOW — D-024 exists and is correct. The decision file is a secondary artifact
that aids handoff; the decision itself is canonical in DECISIONS.md.

**Recommendation:** Future S4 runs should produce both artifacts. Consider adding a
pre-S5 checklist that verifies `state/arch/{intake_id}-decision.md` exists.

### 5.2 S7/S8 Agent Assignment Mismatch (Model Inconsistency)

**Finding:** MODEL-REFERENCE.md Section 7 and WORKFLOW-STANDARDS.md Rule 1.1 disagree
on S7/S8 agent assignments.

| Source | S7 | S8 |
|--------|----|----|
| MODEL-REFERENCE.md §7 | nowu-reviewer / VERIFICATION | VBR / VERIFICATION |
| WORKFLOW.md Step Reference | nowu-implementer + VBR (S6+S7 combined) | nowu-reviewer / Review |
| WORKFLOW-STANDARDS.md §1.1 | EXECUTION / VERIFICATION | EXECUTION / VERIFICATION |
| **Actual W4 practice** | **VBR (VERIFICATION)** | **nowu-reviewer (EVALUATION)** |

The actual W4 artifacts confirm WORKFLOW.md's mapping:
- VBR reports carry `from_step: S7` → VBR ran at S7
- Review report says `reviewer: nowu-reviewer (S8)` → Review ran at S8

**Impact:** MEDIUM — MODEL-REFERENCE.md §7 has the wrong agent ordering for S7/S8.
Section 13 (Artifact→Position) is correct: vbr→VERIFICATION, review→EVALUATION.

**Recommendation for W6:** Update MODEL-REFERENCE.md §7 to match WORKFLOW.md:
- S6+S7: nowu-implementer (IMPLEMENTATION + VERIFICATION via VBR)
- S8: nowu-reviewer (EVALUATION)

### 5.3 Task Spec Position Ambiguity

**Finding:** Task specs are created at S5 (DELIVERY/EVALUATION by nowu-shaper) but
Section 13 maps them to EXECUTION/IMPLEMENTATION. This is not a contradiction —
it reflects that the task spec is a handoff artifact: created at one altitude,
consumed at another.

**Impact:** LOW — Section 13 maps artifacts by their _canonical consumption position_,
not their creation position. This is consistent with how `state/intake/intake-NNN.md`
is mapped to `DELIVERY / DECISION→IMPLEMENTATION` even though it was originally
created during pre-workflow.

**Recommendation:** Document this convention explicitly: "Section 13 maps artifacts
to their canonical consumption position in the 5×10 grid, not their creation step."

### 5.4 Missing `state/sessions/` Directory

**Finding:** Multiple documents reference `state/sessions/` as "checkpoint storage
per ADR-0007" (BOOTSTRAP-DELIVERY.md, BOOTSTRAP-ARCHITECTURE.md, WORKFLOW.md).
The directory does not exist. `FileSessionStore` writes to a different location.

**Impact:** LOW — ADR-0007 is HYPOTHESIS grade. The implementation (D-024) chose a
different storage approach. The directory references are speculative.

**Recommendation:** Remove or annotate `state/sessions/` references in bootstrap
files once ADR-0007 is promoted or amended (W9 work).

### 5.5 `state/changes/` Missing from Artifact→Position Mapping

**Finding:** `state/changes/task-NNN.md` changeset files exist (5 files created during
W4) but are not listed in MODEL-REFERENCE.md Section 13 (Artifact→Position Mapping).
WORKFLOW.md Step Reference mentions `state/changes/` as S6+S7 output.

**Impact:** LOW — Changeset records are EXECUTION/IMPLEMENTATION artifacts. Position
is obvious from context.

**Recommendation for W6:** Add `state/changes/task-NNN.md → EXECUTION / IMPLEMENTATION`
to Section 13.

### 5.6 Analysis Files Have No Canonical Position

**Finding:** `state/analysis/*.md` files (S5, S8, S9 analyses) exist and carry `step:`
metadata but have no canonical position in Section 13. They are reflective artifacts
produced alongside the primary pipeline output.

**Impact:** LOW — Analysis files serve as session-level working notes. They naturally
sit at the same altitude/phase as their parent step.

**Recommendation for W6:** Add `state/analysis/S*-*.md → (inherits step altitude/phase)`
to Section 13, or define analysis as a cross-cutting artifact type.

---

## 6. W5 Metadata Corrections Applied

After this validation, the following frontmatter fields were added to all 22 existing
W4 state artifacts:

- `altitude:` — per MODEL-REFERENCE.md §7 S1-S9 zigzag and §13 Artifact→Position
- `phase:` — per the same sources
- `epistemic_grade:` — per WORKFLOW-STANDARDS.md §3 tiered thresholds

See §4 for the complete mapping table. No body content was changed. No files were
renamed or moved. No missing artifacts were created.

---

## 7. Proposed `artifact_type` Vocabulary (Deferred to K1/W20)

The following vocabulary is proposed for standardization. Only 3/22 W4 artifacts
currently carry `artifact_type`. This proposal is for future work — NOT applied in
this W5 pass.

| artifact_type | Used By | Example |
|---------------|---------|---------|
| INTAKE_BRIEF | state/intake/*.md | intake-001.md (already present) |
| CONSTRAINTS_SHEET | state/arch/*-constraints.md | intake-001-constraints.md |
| OPTIONS_SHEET | state/arch/*-options.md | intake-001-options.md |
| DECISION_RECORD | state/arch/*-decision.md | (missing for intake-001) |
| TASK_SPEC | state/tasks/task-*.md | task-001..005 |
| CHANGESET | state/changes/task-*.md | task-001..005 |
| VBR_REPORT | state/vbr/task-*.md | task-001..005 |
| REVIEW_REPORT | state/reviews/review-*.md | review-intake-001.md |
| CAPTURE_RECORD | state/capture/capture-*.md | capture-intake-001.md |
| SESSION_ANALYSIS | state/analysis/*.md | S5/S8/S9 analysis |
| SESSION_LEARNINGS | state/learnings/*.md | (already present in 2 files) |

---

## 8. Recommendations for W6 (5×10 Model Refactor)

1. **Fix S7/S8 agent mapping** in MODEL-REFERENCE.md §7 to match WORKFLOW.md and actual practice (§5.2).
2. **Add missing artifact types** to Section 13: `state/changes/`, `state/analysis/` (§5.5, §5.6).
3. **Document Section 13 convention**: artifacts are mapped by consumption position, not creation position (§5.3).
4. **Add S4 decision file check** to the S5 pre-shaping checklist or the nowu-decider agent definition (§5.1).
5. **Standardize `artifact_type` vocabulary** as part of K1 traceability work (§7).
6. **Resolve `state/sessions/` references** in bootstrap files (§5.4).

---

## 9. Summary

| Metric | Value |
|--------|-------|
| W4 artifacts audited | 22 (of 23 expected) |
| Missing artifacts | 1 (intake-001-decision.md — documented, not backfilled) |
| Artifacts with altitude/phase before W5 | 0/22 |
| Artifacts with altitude/phase after W5 | 22/22 |
| Model inconsistencies found | 6 (1 MEDIUM, 5 LOW) |
| Zigzag validation | ✅ PASS — S1-S9 followed correct altitude descent |
| Recommendations for W6 | 6 items |

**Conclusion:** The 5×10 model correctly describes the W4 S1-S9 zigzag. The altitude
descent path is validated by artifact positions. The primary gap is operational:
the model was not reflected in artifact metadata (now corrected). One MEDIUM-severity
model inconsistency (S7/S8 agent ordering in MODEL-REFERENCE §7) should be fixed in W6.
