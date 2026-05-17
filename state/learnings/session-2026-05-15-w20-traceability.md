---
artifact_type: SESSION_LEARNINGS
session: "W20 traceability metadata ADR"
created_at: 2026-05-15
session_type: "architecture"
source_artifacts:
  - docs/architecture/adr/ADR-0012-traceability-metadata-standard.md
  - state/arch/intake-007-gap-register.md
  - state/arch/k2-trace-validation.md
  - state/arch/w5-5x10-validation.md
  - state/arch/w28-gap-comparison.md
  - docs/architecture/adr/ADR-0009-orchestration-protocol.md
  - docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md
  - docs/architecture/adr/ADR-0011-domain-extension-model.md
  - docs/USE_CASES.md
purpose: "Define a binding metadata standard for machine-checkable NF-09 traceability while addressing GAP-003 and deferring GAP-007 to K12"
---

# Session Learnings: W20 traceability metadata ADR

## What Was Done

- Produced ADR-0012 as a HYPOTHESIS-grade traceability metadata standard.
- Converted K2 trace observations into explicit mandatory fields (review/VBR/task closure links).
- Anchored controlled `artifact_type` vocabulary on W5 as the predecessor proposal.
- Mapped traceability requirements directly to NF-09 enforceability conditions.
- Documented GAP-007 decay mismatch as deferred to K12 without altering ADR-0010 semantics.

## Decisions Made

### D-SESS-01: Require a universal `trace_links` object for machine-checkable chains

**Decision:** Every relevant artifact must carry `trace_links` with normalized linkage keys
(`intake_id`, `task_ids`, `decision_ids`, `vbr_ids`, `review_id`, etc.).
**Context:** K2 found narrative back-references were present but structured link fields
were missing in terminal artifacts.
**Why it matters:** Enables deterministic NF-09 chain validation and removes reviewer
dependence on prose-only references.

---

### D-SESS-02: Standardize GAP-003 evidence chains with domain atom references

**Decision:** Decision-centric artifacts must include `decision_context` fields for options,
criteria, evidence refs, revisit triggers, and domain atom links.
**Context:** W27 + W28 showed GAP-003 is systemic in AP and RE; current thin decision shape
cannot represent full evidence chains without supplementary structure.
**Why it matters:** Formalizes cross-domain decision traceability and aligns W20 with
ADR-0011 direction without changing `core/contracts/`.

---

### D-SESS-03: Keep GAP-007 explicitly deferred

**Decision:** Record GAP-007 decay mismatch and reference K12 as the resolution path; make
no policy change in ADR-0012.
**Context:** ADR-0010 defines epistemic model semantics; W20 scope is metadata traceability,
not decay calibration.
**Why it matters:** Prevents scope bleed and preserves ADR consistency while still making
the unresolved risk visible.

---

## Process Insights

### Insight 1: K2 observations are directly translatable into schema requirements

**Observation:** The three K2 findings map cleanly to specific frontmatter requirements.
**Type:** workflow-process
**Implication:** Convert recurring review observations into mandatory metadata keys as early
as possible instead of relying on reviewer memory.

---

### Insight 2: W5 vocabulary proposals reduce naming ambiguity

**Observation:** Reusing W5’s `artifact_type` candidates avoided inventing parallel naming.
**Type:** domain-insight
**Implication:** Treat precursor validation reports as canonical seed vocabularies for
standards work.

---

### Insight 3: Explicit deferral language is necessary when adjacent gaps exist

**Observation:** GAP-007 naturally appears in traceability discussions due to grade metadata,
but resolving it would violate scope.
**Type:** workflow-process
**Implication:** Include explicit "not resolved here" sections when cross-cutting issues are
known but out of scope.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Solving adjacent policy mismatches inside metadata ADRs

**Temptation:** Resolve decay semantics (GAP-007) while editing traceability metadata because
both involve epistemic fields.
**Reality:** This creates ADR contradictions and scope creep; policy stays in ADR-0010/K12,
while ADR-0012 should stay metadata-structural.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| ADR-0012 | `docs/architecture/adr/ADR-0012-traceability-metadata-standard.md` | PROPOSED | Define required metadata and evidence-chain standards for NF-09 traceability |
| Session learnings | `state/learnings/session-2026-05-15-w20-traceability.md` | DONE | Capture W20 architecture and process learnings |

## What Should Happen Next

1. Add validation checks that enforce `trace_links` and `use_case_ids` presence before S8/S9 approval.
2. Backfill high-value legacy terminal artifacts with `review_id`/`vbr_ids` link fields.
3. Execute K12 to resolve GAP-007 decay semantics mismatch and update ADR-0010 (or know baseline) accordingly.
