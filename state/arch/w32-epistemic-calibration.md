---
artifact_type: VALIDATION_REPORT
id: w32-epistemic-calibration
work_item: W32
altitude: ARCHITECTURE
phase: DECISION
epistemic_grade: EVIDENCE_BASED
created: 2026-05-14
status: DONE
use_cases: [NF-15, NF-16]
depends_on: [W4, W5, ADR-0010, D-015]
consumed_by: [W8]
---

# W32 Epistemic Threshold Calibration

## 1. Purpose

Calibrate epistemic grade thresholds for Level 1 (advisory) and Level 2 (blocking)
enforcement by comparing ADR-0010's theoretical defaults against W4's actual artifact
grades. This calibration produces the canonical threshold table that W8 will consume.

**Input sources:**
- MODEL-REFERENCE §6 "Epistemic Grades" (per-altitude thresholds — coarse-grained)
- ADR-0010 §"Default grades by artifact type" (per-artifact-type defaults — theoretical)
- D-015 §"Enforcement Levels" (enforcement tier definitions)
- W4 intake-001 artifacts (22 artifacts with `epistemic_grade` frontmatter)
- W5 validation report (confirmed all W4 artifacts carry grade metadata)

**Relationship to §6:** MODEL-REFERENCE §6 defines per-altitude thresholds (e.g.,
"ARCHITECTURE minimum = HYPOTHESIS"). W32 refines these to per-artifact-type thresholds
(e.g., "TASK_SPEC minimum = HYPOTHESIS, aspirational = INFORMED_ESTIMATE"). The §6
altitude thresholds remain as the coarse floor; W32's artifact-type thresholds are the
fine-grained overlay that W8 will enforce.

---

## 2. W4 Artifact Grade Inventory

### 2.1 Actual grades assigned during W4 (intake-001)

| Artifact | artifact_type | Step | Actual Grade | ADR-0010 Default | Match |
|---|---|---|---|---|---|
| intake-001.md | INTAKE_BRIEF | S1 | HYPOTHESIS | HYPOTHESIS | ✅ |
| intake-001-constraints.md | CONSTRAINTS_SHEET | S2 | HYPOTHESIS | HYPOTHESIS | ✅ |
| intake-001-options.md | OPTIONS_SHEET | S3 | HYPOTHESIS | HYPOTHESIS | ✅ |
| (no S4 artifact) | DECISION_RECORD | S4 | — | INFORMED_ESTIMATE | N/A |
| task-001..005.md | TASK_SPEC | S5 | HYPOTHESIS | INFORMED_ESTIMATE | ❌ lower |
| changes/task-001..005.md | CHANGESET | S6 | EVIDENCE_BASED | EVIDENCE_BASED* | ✅ |
| vbr/task-001..005.md | VBR_REPORT | S7 | EVIDENCE_BASED | EVIDENCE_BASED* | ✅ |
| review-intake-001.md | REVIEW_REPORT | S8 | EVIDENCE_BASED | INFORMED_ESTIMATE | ⬆️ higher |
| capture-intake-001.md | CAPTURE_RECORD | S9 | INFORMED_ESTIMATE | inherits | ❓ |
| S5/S8/S9 analysis | SESSION_ANALYSIS | S5/S8/S9 | INFORMED_ESTIMATE | (unspecified) | — |
| learnings/*.md | SESSION_LEARNINGS | post | INFORMED_ESTIMATE | (unspecified) | — |

*ADR-0010 says "EVIDENCE_BASED (if VBR passes)" — the conditional was met.

### 2.2 Non-W4 artifacts with grades (for reference)

| Artifact | artifact_type | Actual Grade | ADR-0010 Default | Match |
|---|---|---|---|---|
| ADR-0007..0010 | ADR | HYPOTHESIS | HYPOTHESIS | ✅ |
| SYNTHESIS-001.md | SYNTHESIS | INFORMED_ESTIMATE | HYPOTHESIS | ⬆️ higher |
| w5-5x10-validation.md | VALIDATION_REPORT | EVIDENCE_BASED | (unspecified) | — |
| k2-trace-validation.md | VALIDATION_REPORT | EVIDENCE_BASED | (unspecified) | — |

---

## 3. Deviation Analysis

### 3.1 Task specs: HYPOTHESIS (actual) vs INFORMED_ESTIMATE (default)

**Root cause:** ADR-0010 assigns INFORMED_ESTIMATE to task specs because they are
"Human-approved decomposition." In W4, the shaper agent (S5) generated the task specs
and the human approved them as a batch, but the grade was not explicitly promoted from
the agent's initial HYPOTHESIS assignment.

**Calibration decision:** The ADR-0010 default is correct in intent — task specs
SHOULD be INFORMED_ESTIMATE after human approval at S4/S5 gates. The gap is in the
S5 agent's behavior: it should promote the grade when human approval is received.

**Threshold:** Minimum = HYPOTHESIS (agent-generated pre-approval).
Aspirational = INFORMED_ESTIMATE (post-human-approval).
Level 1 advisory: warn if task spec enters S6 at HYPOTHESIS (suggests human approval
step was skipped or grade not promoted).

### 3.2 Review report: EVIDENCE_BASED (actual) vs INFORMED_ESTIMATE (default)

**Root cause:** ADR-0010 says "Review is judgment, not proof." However, the S8
reviewer in W4 ran the full quality suite (pytest + mypy + ruff), verified VBR reports,
and checked scope compliance — producing a review backed by verifiable evidence.

**Calibration decision:** The default should be split:
- **Lightweight review** (docs, refactors): INFORMED_ESTIMATE — judgment-based.
- **Full review** (with VBR + quality suite): EVIDENCE_BASED — the review itself
  is evidence-backed.

**Threshold:** Minimum = INFORMED_ESTIMATE (any review requires judgment).
Aspirational = EVIDENCE_BASED (full review with quality suite evidence).

### 3.3 Capture record: INFORMED_ESTIMATE (actual) vs "inherits" (default)

**Root cause:** ADR-0010 says capture "inherits from reviewed artifact." The review
was graded EVIDENCE_BASED, so the capture should have been EVIDENCE_BASED too. The
S9 curator assigned INFORMED_ESTIMATE — a conservative default rather than inheriting.

**Calibration decision:** Enforce the inheritance rule. The capture grade should
equal the review grade, since capture is a recording step (no new judgment added).

**Threshold:** Minimum = (review grade). Aspirational = (review grade).
Level 1 advisory: warn if capture grade < review grade.

### 3.4 Unspecified artifact types

ADR-0010 does not define defaults for:
- SESSION_ANALYSIS (produced at S5/S8/S9): INFORMED_ESTIMATE is reasonable.
- SESSION_LEARNINGS: INFORMED_ESTIMATE is reasonable (reflection-based).
- VALIDATION_REPORT (W5/K2): EVIDENCE_BASED is correct (evidence-driven validation).

**Calibration decision:** Add these to the threshold table.

---

## 4. Canonical Threshold Table

### 4.1 S1-S9 Workflow Artifacts

| artifact_type | Step | Minimum Grade (Level 1) | Aspirational Grade (Level 2) | Notes |
|---|---|---|---|---|
| INTAKE_BRIEF | S1 | HYPOTHESIS | HYPOTHESIS | Unvalidated problem statement; HYPOTHESIS is correct floor |
| CONSTRAINTS_SHEET | S2 | HYPOTHESIS | HYPOTHESIS | Analysis without verification |
| OPTIONS_SHEET | S3 | HYPOTHESIS | HYPOTHESIS | Generated alternatives, unselected |
| DECISION_RECORD | S4 | INFORMED_ESTIMATE | INFORMED_ESTIMATE | Human-approved choice; must exceed HYPOTHESIS |
| TASK_SPEC | S5 | HYPOTHESIS | INFORMED_ESTIMATE | HYPOTHESIS before approval; INFORMED_ESTIMATE after S4/S5 human gate |
| CHANGESET | S6 | EVIDENCE_BASED | EVIDENCE_BASED | Implementation with passing tests = evidence |
| VBR_REPORT | S7 | EVIDENCE_BASED | EVIDENCE_BASED | Verification by automated quality suite |
| REVIEW_REPORT | S8 | INFORMED_ESTIMATE | EVIDENCE_BASED | Lightweight=IE, full review with VBR=EB |
| CAPTURE_RECORD | S9 | ≥ review grade | ≥ review grade | Inherits; never below review grade |
| SESSION_ANALYSIS | S5/S8/S9 | INFORMED_ESTIMATE | INFORMED_ESTIMATE | Reflection-based analysis |

### 4.2 Pre-Workflow Artifacts (P0-P4)

| artifact_type | Step | Minimum Grade (Level 1) | Aspirational Grade (Level 2) | Notes |
|---|---|---|---|---|
| IDEA | P0 | SPECULATION | HYPOTHESIS | Initial idea; lowest bar acceptable |
| PROBLEM | P1 | HYPOTHESIS | INFORMED_ESTIMATE | Problem statement; needs structured analysis |
| EPIC | P2 | HYPOTHESIS | INFORMED_ESTIMATE | Story decomposition; pre-validation |
| STORY | P2 | HYPOTHESIS | INFORMED_ESTIMATE | Individual story; pre-approval |
| OPTIONS_SHEET (arch) | P3 | HYPOTHESIS | HYPOTHESIS | Architecture options; pre-decision |
| CONSTRAINTS_SHEET (arch) | P3 | HYPOTHESIS | HYPOTHESIS | Architecture constraints; pre-decision |

### 4.3 Architecture & Knowledge Artifacts

| artifact_type | Step | Minimum Grade (Level 1) | Aspirational Grade (Level 2) | Notes |
|---|---|---|---|---|
| SYNTHESIS | W1 | HYPOTHESIS | INFORMED_ESTIMATE | Cross-cutting analysis; elevated after review |
| ARCHITECTURE_VISION | W2 | HYPOTHESIS | INFORMED_ESTIMATE | Derived from synthesis; elevated after review |
| ADR (hypothesis) | W3 | HYPOTHESIS | HYPOTHESIS | Untested; promotes via D-017 rules |
| ADR (validated) | post-W4 | INFORMED_ESTIMATE | EVIDENCE_BASED | After 2+ intakes; then 5+ for EB |
| VALIDATION_REPORT | K/W | EVIDENCE_BASED | EVIDENCE_BASED | Evidence-driven validation |
| SESSION_LEARNINGS | post | INFORMED_ESTIMATE | INFORMED_ESTIMATE | Reflection-based |
| ROADMAP | orch | INFORMED_ESTIMATE | INFORMED_ESTIMATE | Strategic planning; human-approved |
| GOAL | P0 | INFORMED_ESTIMATE | INFORMED_ESTIMATE | Human-authored strategic intent |

### 4.4 Grade Propagation Thresholds

Per ADR-0010 §"Propagation Rules":

| Rule | Threshold | Level 1 Advisory |
|---|---|---|
| Derived artifact ≥ min(input grades) | Composite inherits lowest input grade | Warn if output grade > min(input grades) without explicit evidence justification |
| Capture ≥ review grade | S9 inherits S8 grade | Warn if capture < review |
| Promotion requires evidence | No silent upgrades | Warn if grade increases without `justification` field |
| ADR promotion: D-017 rules | HYPOTHESIS→IE after 2 intakes; IE→EB after 5 | Warn if ADR promotion attempted with fewer intakes |

---

## 5. W8 Input: Level 1 Advisory Rules

These are the actionable rules W8 will implement for Level 1 enforcement:

### 5.1 Grade-exists check (Level 0 — already passing)

Every artifact with `artifact_type` in §13.1 vocabulary MUST have an `epistemic_grade`
field in YAML frontmatter. (Validated by W5.)

### 5.2 Grade-minimum check (Level 1 — new)

For each artifact entering a workflow step, check:
```
actual_grade >= minimum_grade[artifact_type]
```
If violated: emit advisory warning (non-blocking).

### 5.3 Grade-inheritance check (Level 1 — new)

For capture records: check `capture.grade >= review.grade`.
If violated: emit advisory warning.

### 5.4 Grade-promotion check (Level 1 — new)

When an artifact's grade increases from a previous version:
- Check that a `justification` or `evidence` field exists in frontmatter or body.
- For ADR promotions: check intake count against D-017 thresholds.
If violated: emit advisory warning.

### 5.5 Aspirational grade check (Level 2 — future, v1.1)

At S4/S5 gates: check that inputs meet aspirational grade thresholds from §4.
If violated: block the gate transition (requires human override).

---

## 6. Calibration Confidence

This calibration is based on **1 completed intake** (intake-001 / W4). D-015 recommends
recalibration after 5+ intakes. Current confidence:

| Threshold | Confidence | Basis |
|---|---|---|
| S1-S3 minimum = HYPOTHESIS | HIGH | ADR-0010 + W4 confirmed; all 3 artifacts matched |
| S4 minimum = INFORMED_ESTIMATE | MEDIUM | No S4 artifact in W4 (decision was inline); default from ADR-0010 |
| S5 minimum = HYPOTHESIS, aspirational = IE | HIGH | W4 deviation explained; split makes sense |
| S6-S7 minimum = EVIDENCE_BASED | HIGH | W4 confirmed; VBR-backed evidence |
| S8 minimum = IE, aspirational = EB | HIGH | W4 showed full review justifies EB |
| S9 inheritance rule | HIGH | Logic-based; capture adds no judgment |
| Pre-workflow thresholds | LOW | No pre-workflow artifacts have been through W5 validation |
| ADR promotion thresholds | MEDIUM | D-017 rules are theoretical; only 1 intake completed |

**Recalibration trigger:** After 5 completed intakes, re-run W32 to validate thresholds
empirically and adjust where needed. Track as K-item on ROADMAP-003.

---

## 7. Summary

W32 establishes the canonical threshold table for epistemic grade enforcement:

1. **Level 0 (v1-core, current):** Grade field exists — ✅ validated by W5.
2. **Level 1 (v1, via W8):** Advisory warnings when grade < minimum threshold.
   Threshold table defined in §4 above and added to MODEL-REFERENCE §12.1.
3. **Level 2 (v1.1):** Blocking at gates when grade < aspirational threshold.
   Aspirational thresholds defined in §4; enforcement deferred to v1.1.

Three W4 deviations identified and resolved:
- Task spec grades: process gap (S5 should promote after human approval)
- Review grades: ADR-0010 default too conservative for full reviews
- Capture grades: inheritance rule not enforced by S9 curator

These findings feed both W8 (Level 1 implementation) and future S5/S9 agent improvements.
