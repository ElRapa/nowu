---
id: ADR-0012
title: Traceability Metadata Standard for Workflow Artifacts
date: 2026-05-15
status: PROPOSED
epistemic_grade: HYPOTHESIS
superseded_by: ~
source_synthesis: SYNTHESIS-001
source_themes: [T3, T6, T4]
source_ucs: [NF-09, NF-02, AP-06, RE-06]
depends_on: [ADR-0008, ADR-0009, ADR-0010, ADR-0011]
---

# ADR-0012: Traceability Metadata Standard for Workflow Artifacts

## Status

PROPOSED (HYPOTHESIS grade) — This ADR defines a metadata contract that makes NF-09
machine-checkable across S1-S9 and across AP/RE domain evidence chains. It addresses
GAP-003 by standardizing first-class trace links for decision evidence. GAP-007 is
explicitly recorded but deferred to K12; this ADR does not change decay semantics.

## Context

NF-09 requires that every deliverable trace back to a use case through an unbroken,
machine-checkable chain. Current artifacts are partially traceable but inconsistent:

1. K2 found terminal-link gaps: capture artifacts lack explicit `review_id`; review
   artifacts lack structured `vbr_ids`; task lifecycle status can drift from actual
   completion state.
2. W5 confirmed missing metadata normalization and proposed an `artifact_type`
   vocabulary that is not yet fully standardized.
3. W27 + W28 classify GAP-003 as systemic: AP-06 and RE-06 decision evidence chains
   exceed the current thin decision structure unless links are formalized.
4. ADR-0009 already defines progressive `validation_trace` intent, but field-level
   minimum requirements are not yet codified for all artifacts.

Without a common metadata standard, traceability remains narrative and brittle,
which violates NF-09 intent at review time.

## Decision

Adopt a mandatory metadata standard for all workflow artifacts in `state/` and ADR-like
decision artifacts in `docs/architecture/adr/`.

### 1) Required Metadata for Every Artifact

Every artifact MUST include these frontmatter fields:

| Field | Type | Rule | NF-09 role |
|---|---|---|---|
| `artifact_type` | string | Required, from controlled vocabulary | Enables deterministic artifact classification in trace graph |
| `id` | string | Required, globally unique within repository namespace | Stable node key for machine linkage |
| `status` | enum | Required, lifecycle state (e.g., DRAFT/READY/DONE/APPROVED/ACCEPTED) | Prevents stale-state ambiguity in deliverable claims |
| `created_at` (or `date` for ADRs) | ISO date/time | Required | Supports temporal ordering of trace chain |
| `epistemic_grade` | enum | Required where grade model applies; labels from ADR-0010 only | Keeps trust semantics explicit without redefining grade policy |
| `use_case_ids` | non-empty list[string] | Required for all implementation-relevant artifacts; may inherit only if inheritance is explicit | Enforces deliverable→UC binding required by NF-09 |
| `trace_links` | object | Required; structured references listed below | Provides machine-checkable edge set |

`trace_links` MUST support these common edge keys (use empty arrays when not applicable):

- `intake_id`
- `story_ids`
- `task_ids`
- `decision_ids`
- `changeset_ids`
- `vbr_ids`
- `review_id`
- `capture_id`
- `supersedes_ids`

### 2) Controlled `artifact_type` Vocabulary

ADR-0012 adopts W5’s proposed vocabulary as the minimum controlled set:

- `INTAKE_BRIEF`
- `CONSTRAINTS_SHEET`
- `OPTIONS_SHEET`
- `DECISION_RECORD`
- `TASK_SPEC`
- `CHANGESET`
- `VBR_REPORT`
- `REVIEW_REPORT`
- `CAPTURE_RECORD`
- `SESSION_ANALYSIS`
- `SESSION_LEARNINGS`

Additional types are allowed only if documented in a follow-up decision artifact and
cross-referenced in this ADR’s successor.

### 3) Terminal Artifact Closure Rules (K2 gap closure)

To operationalize K2 findings, these fields are mandatory:

- `CAPTURE_RECORD` MUST include explicit `trace_links.review_id` and
  `trace_links.vbr_ids` (directly or via referenced task set).
- `REVIEW_REPORT` MUST include explicit `trace_links.vbr_ids` and
  `trace_links.task_ids`.
- `TASK_SPEC` and downstream artifacts MUST carry lifecycle-consistent `status` values;
  closure artifacts may not claim `DONE` while parent task specs remain unresolved.

These rules directly target K2’s three non-blocking observations and convert them into
required metadata behavior.

### 4) GAP-003 Decision Evidence Chain Standard

For decision-centric domains (AP-06, RE-06, and equivalent), artifacts MUST provide a
machine-linkable evidence chain. Minimum required fields:

| Field | Type | Purpose |
|---|---|---|
| `trace_links.decision_ids` | list[string] | Connects deliverable to formal decision records |
| `decision_context.option_ids` | list[string] | Preserves considered alternatives |
| `decision_context.criteria_ids` | list[string] | Preserves evaluation criteria |
| `decision_context.evidence_refs` | list[string] | References evidence artifacts or atom IDs |
| `decision_context.revisit_triggers` | list[string] | Makes reassessment conditions explicit |
| `decision_context.domain_atom_refs` | list[string] | Links decision records to AP/RE domain atoms per ADR-0011 direction |

This is the concrete metadata response to GAP-003: the evidence chain is no longer
implicit prose, but typed references that can be validated.

### 5) NF-09 Compliance Rule

No artifact can be marked as delivery-complete (`DONE`, `APPROVED`, or `ACCEPTED` in a
delivery context) unless:

1. `use_case_ids` is present and non-empty.
2. `trace_links` provides an unbroken path from artifact → task/review/capture lineage.
3. Every declared acceptance criterion in scope can be mapped to at least one listed UC.

This rule makes NF-09 enforceable as metadata validation, not only reviewer narrative.

### 6) GAP-007 Decay-Semantics Note (Deferred)

GAP-007 is acknowledged here because traceability metadata carries epistemic context,
and confidence decay affects long-lived trace interpretation.

However, ADR-0012 does **not** resolve the 90d vs 180d decay mismatch. Decay-semantics
alignment is explicitly deferred to **K12** and ADR-0010 maintenance. This ADR only
requires that grades and trace links are present; it does not redefine decay rules.

## Rationale

1. **NF-09 needs machine edges, not prose references.** Metadata fields provide explicit,
   testable links.
2. **K2 showed exactly where chains break.** The standard codifies missing terminal links
   (`review_id`, `vbr_ids`) and lifecycle coherence.
3. **GAP-003 is systemic across AP and RE.** W28 evidence requires a cross-domain,
   decision-evidence contract rather than one-domain patching.
4. **Compatibility with existing ADRs.** The standard extends ADR-0009 handoff intent,
   uses ADR-0010 grade vocabulary unchanged, and aligns with ADR-0011 domain extension
   direction for domain atom references.

## Consequences

**Positive:**

- Traceability checks can be automated at review/capture gates.
- Decision evidence chains become auditable across domains.
- Artifact typing and linkage become consistent enough for future lint/fitness checks.

**Negative:**

- Metadata overhead increases for each artifact authoring step.
- Existing legacy artifacts may need gradual backfill to satisfy full validation.

**Neutral:**

- GAP-007 remains open; decay calibration is intentionally deferred to K12.
- ADR-0010 grade assignments and promotion/decay semantics remain authoritative.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Keep traceability narrative-only | Low overhead | Unreliable machine validation; repeats K2 issues | Fails NF-09 enforceability |
| Add only terminal links (`review_id`, `vbr_ids`) | Fast local fix | Leaves GAP-003 systemic decision-evidence gap unresolved | Insufficient cross-domain coverage |
| Full metadata + evidence-chain standard (selected) | Machine-checkable NF-09 + GAP-003 coverage + W5 vocabulary alignment | Higher authoring discipline required | **Selected** |

## Related

- use_case: NF-09 (`docs/USE_CASES.md`)
- gap_register: GAP-003, GAP-007 (`state/arch/intake-007-gap-register.md`)
- validation: K2 trace observations (`state/arch/k2-trace-validation.md`)
- cross_domain_evidence: W28 systemic classification (`state/arch/w28-gap-comparison.md`)
- precursor: W5 artifact_type vocabulary (`state/arch/w5-5x10-validation.md`)
- adrs: ADR-0009, ADR-0010, ADR-0011
