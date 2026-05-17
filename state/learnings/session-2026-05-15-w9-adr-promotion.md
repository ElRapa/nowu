---
artifact_type: SESSION_LEARNINGS
session: "W9 ADR Promotion Pass — ADR-0007..0010 HYPOTHESIS → INFORMED_ESTIMATE"
created_at: 2026-05-15
session_type: "architecture"
source_artifacts:
  - docs/architecture/adr/ADR-0007-session-continuity-protocol.md
  - docs/architecture/adr/ADR-0008-knowledge-atom-model.md
  - docs/architecture/adr/ADR-0009-orchestration-protocol.md
  - docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md
  - state/intake/intake-001.md
  - state/intake/intake-007.md
  - state/intake/intake-008.md
  - state/capture/capture-intake-001.md
  - state/capture/capture-intake-007.md
  - state/capture/capture-intake-008.md
  - state/arch/intake-007-gap-register.md
  - .sisyphus/evidence/task-6-adr-promotion.txt
  - .sisyphus/evidence/task-6-no-rewrite.txt
  - .sisyphus/evidence/task-6-session-learning.txt
purpose: "Evaluate ADR-0007..0010 against 3-intake evidence corpus and promote ≥1 from HYPOTHESIS"
---

# Session Learnings: W9 ADR Promotion Pass

## What Was Done

- Read all four ADRs (0007–0010) and all three intake evidence packages (001, 007, 008) plus
  their capture records and the W27 gap register.
- Evaluated each ADR against the D-017 promotion threshold (HYPOTHESIS → INFORMED_ESTIMATE
  requires ≥2 S1-S9 intakes confirming the hypothesis).
- Confirmed all four ADRs meet or exceed the threshold: intake-001 directly implements
  ADR-0007; intakes 007+008 validate ADR-0008/0009 domain-agnosticism; W32 calibration +
  3 intakes validate ADR-0010 grade rules.
- Promoted all four ADRs from HYPOTHESIS to INFORMED_ESTIMATE:
  - Frontmatter: `epistemic_grade` updated + 3 provenance fields added.
  - Status section: First paragraph updated to reflect promotion.
  - "## Supporting Evidence" section appended at EOF with per-intake citations.
- Created `.sisyphus/evidence/` files documenting promotions, no-rewrite verification, and
  session-learning confirmation.

## Decisions Made

### D-SESS-W9-01: Promote all 4 simultaneously rather than 1 minimum

**Decision:** All four ADRs (0007–0010) promoted to INFORMED_ESTIMATE in this pass rather
than the minimum required 1.

**Context:** Task specified "promote ≥1 ADR." After evaluating the evidence, all four ADRs
met the D-017 threshold. Deferring some would require explicit justification for non-promotion
and create artificial asymmetry in the ADR set.

**Why it matters:** Consistent epistemic state across a dependent ADR cluster (0007 depends
on 0008; 0009 depends on all three; 0010 depends on 0008) prevents promotion inconsistencies
where dependents are higher-grade than foundations. Promoting all four simultaneously maintains
the dependency graph's epistemic coherence.

---

### D-SESS-W9-02: GAP-007 decay semantics mismatch is maintenance, not demotion trigger

**Decision:** ADR-0010 was promoted to INFORMED_ESTIMATE despite GAP-007 (MEDIUM=90d vs
know baseline MEDIUM=180d decay discrepancy identified in W27).

**Context:** GAP-007 could be interpreted as a "residual risk" that prevents promotion.
The rubric question is: does GAP-007 contradict ADR-0010's grade assignment and propagation
rules? It does not — it identifies a specific value discrepancy in the decay schedule, not
a flaw in the grade model. The grade vocabulary, assignment rules, and propagation rules
are all confirmed by the intake corpus.

**Why it matters:** Conflating "implementation detail discrepancy" with "hypothesis contradiction"
would apply an excessively conservative promotion standard that no ADR could survive (every
real-world system has implementation variations from spec). GAP-007 is documented as a
residual risk in ADR-0010's Supporting Evidence section. Resolution is ADR-0010 maintenance
work, not a precondition for promotion.

---

## Process Insights

### Insight 1: Per-ADR evidence rubric prevents grade inflation and grade deflation

**Observation:** Without an explicit rubric (which intake, which specific finding, confirms or
surfaces risk), there is a tendency to either promote reflexively ("we ran 3 intakes, promote
everything") or over-conservatively ("there are still gaps, defer promotion"). Applying the
rubric per-ADR — aligning each intake's specific findings to the ADR's specific decisions —
produces defensible, differentiated conclusions.

**Type:** workflow-process

**Implication:** Future ADR promotion passes should include an explicit evaluation matrix:
ADR × intake × specific finding × confirms/surfaces-risk × conclusion. This prevents both
reflexive promotion and paralysis-by-gaps.

---

### Insight 2: "Implementation gap ≠ design contradiction" is the key ADR-0008 insight

**Observation:** ADR-0008 was the hardest case. The atom model has NOT been runtime-validated
(K3 not implemented). GAP-001..005 all identify missing capabilities. At first pass, this
looked like "the hypothesis is unconfirmed, defer promotion." But closer reading shows:
the gaps all point to MISSING IMPLEMENTATION of the atom model, not disagreement with
its design. AP-01, AP-02, AP-06, RE-01, RE-06 all need exactly the capabilities ADR-0008
specifies. The gaps are design CONFIRMATION by means of identified demand.

**Type:** domain-insight

**Implication:** When evaluating an ADR with unimplemented capabilities, the question to
ask is: "Do the gaps contradict the design, or do they confirm the design by exposing
unsatisfied demand?" For ADR-0008 (and similarly ADR-0009's programmatic state machine),
the answer is the latter. This distinction should be explicit in any future promotion rubric.

---

### Insight 3: Status section update without decision rewriting requires surgical precision

**Observation:** The task specification "metadata change + evidence section ONLY, NO decision
text rewriting" is easy to violate accidentally when updating the Status section. The Status
section in hypothesis ADRs contains both (a) grade text and (b) forward-looking validation
language like "Will be validated through first S1-S9 intake (W4)." Only (a) should be
updated; (b) should be replaced with a summary of what was validated and a pointer to the
evidence section.

**Type:** workflow-process

**Implication:** Future ADR promotion instructions should explicitly identify the Status
section as "metadata-adjacent" (update allowed) and clearly distinguish it from Decision,
Rationale, Consequences (update forbidden). A template for the post-promotion Status
paragraph would reduce promotion errors.

---

### Insight 4: Promotion provenance fields (3 new YAML fields) create audit trail

**Observation:** Adding `epistemic_grade_previous`, `epistemic_grade_promoted_at`, and
`epistemic_grade_promoted_by` to the frontmatter creates a lightweight audit trail without
modifying the grade model. These fields were not in the original ADR frontmatter schema.

**Type:** domain-insight

**Implication:** The ADR frontmatter schema should be extended to include these provenance
fields as optional (added at promotion time). Templates for hypothesis ADRs should include
these fields as commented-out stubs so they're easy to fill when promoting.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Blocking promotion on "unimplemented capabilities"

**Temptation:** If an ADR describes a capability that hasn't been implemented yet, it feels
like the hypothesis is unconfirmed. Therefore, defer promotion until the code exists.

**Reality:** ADRs are architectural decisions, not implementation specifications. Confirming
an ADR means confirming its decision is correct — not that the implementation is complete.
ADR-0008's decision is "adopt the `know` KnowledgeAtom as canonical." This is confirmed
whenever domain evidence shows that atoms are the right abstraction (which GAP-001..005 do,
by exposing unsatisfied demand). Blocking promotion on implementation completeness would
leave the ADR at HYPOTHESIS indefinitely, which defeats the purpose of the grade model.

---

### Anti-Pattern 2: Treating all residual risk as demotion-level risk

**Temptation:** There's a known gap (GAP-007, decay semantics mismatch). Therefore, ADR-0010
cannot be promoted.

**Reality:** Residual risks are expected at INFORMED_ESTIMATE grade. The grade model is not
"zero open questions" — it's "sufficient evidence for the core decisions, with documented
limitations." GAP-007 is scoped to a specific value discrepancy in the decay schedule,
not a flaw in the grade assignment or propagation rules. Document it in the evidence section,
classify it as maintenance, and promote the ADR.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| ADR-0007 promoted | `docs/architecture/adr/ADR-0007-session-continuity-protocol.md` | Updated | Frontmatter + status + evidence section |
| ADR-0008 promoted | `docs/architecture/adr/ADR-0008-knowledge-atom-model.md` | Updated | Frontmatter + status + evidence section |
| ADR-0009 promoted | `docs/architecture/adr/ADR-0009-orchestration-protocol.md` | Updated | Frontmatter + status + evidence section |
| ADR-0010 promoted | `docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md` | Updated | Frontmatter + status + evidence section |
| Promotion evidence | `.sisyphus/evidence/task-6-adr-promotion.txt` | New | Per-ADR evidence linkage |
| No-rewrite evidence | `.sisyphus/evidence/task-6-no-rewrite.txt` | New | Verification that only metadata/evidence added |
| Session learning evidence | `.sisyphus/evidence/task-6-session-learning.txt` | New | Session learning proof |
| This file | `state/learnings/session-2026-05-15-w9-adr-promotion.md` | New | Session learnings |

## What Should Happen Next

1. **ADR-0010 maintenance (GAP-007):** Reconcile decay semantics — either update
   ADR-0010 §Decay Rules to use MEDIUM=180d (matching know baseline) or formalize the
   90d policy and update the know curator. Owner: ADR-0010 maintenance work item.

2. **ADR-0007 Known Limitations note (capture-intake-001 F2):** Add a note to ADR-0007's
   Known Limitations section documenting the v1-core `SessionCheckpoint` field divergence
   from the full spec (missing `checkpoint_id`, `timestamp`, `blockers`; added
   `schema_version`). Reference D-024 as the authorizing decision.

3. **ADR frontmatter schema update:** Add `epistemic_grade_previous`, `epistemic_grade_promoted_at`,
   `epistemic_grade_promoted_by` as optional commented-out stubs to the ADR template
   (`templates/adr-template.md` or equivalent) so future promotions have a clear slot.

4. **Continue intake accumulation for EVIDENCE_BASED:** D-017 requires ≥5 intakes for
   EVIDENCE_BASED promotion. Current count: 3. Two more domain or feature intakes will
   trigger the next promotion pass for these ADRs.
