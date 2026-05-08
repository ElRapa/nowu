---
artifact_type: SESSION_LEARNINGS
session: "Documentation Maintenance Strategy — Research Evaluation & Minimal Implementation"
created_at: 2026-05-08
session_type: "workflow-optimization"
source_artifacts:
  - docs/research/sessions/2026-05-08_3_perplexity_Document Maintenance Strategy/docs-placement-and-maintenance-guide.md
  - docs/research/INDEX.md
  - templates/task-spec.md
  - templates/review-report.md
purpose: "Evaluate Perplexity research on docs maintenance, implement minimal viable protocols"
---

# Session Learnings: Documentation Maintenance Strategy Evaluation

## What Was Done

- Evaluated Perplexity research doc proposing 5 maintenance protocols, 4 directory subdivisions, META.md per session, and D-023 formalization
- Identified 6 issues: META.md over-engineering, premature subdirs (YAGNI), INDEX.md irony, naming convention conflict, premature D-023, future work presented as current
- Implemented minimal viable subset: INDEX.md, `docs_to_update` in S5 template, Documentation Validation in S8 template
- Deferred: META.md, comparative/literature/validation dirs, D-023, Protocols 3-5 (G0 drift, quarterly audits, automated staleness)

## Decisions Made

### D-SESS-01: Implement only Protocols 1 and 2 from research

**Decision:** Only implement the LEARN phase update rule (already implicit) and S8 documentation validation gate now. Defer Protocols 3-5 to future versions.
**Context:** Research proposes 5 protocols but only 2 are actionable before v1 exists. Can't validate if "S8 checks docs" works before running a single S1-S9 cycle.
**Why it matters:** Prevents over-formalizing unvalidated process. Allows the two immediate protocols to prove themselves through practice before adding complexity.

### D-SESS-02: No META.md per research session

**Decision:** Use INDEX.md as the single traceability lookup. Session folders are self-explanatory via naming convention.
**Context:** Research proposes YAML META.md in each session folder. But grep on INDEX.md is faster for traceability, and folder names already encode date/source/topic.
**Why it matters:** Avoids creating a maintenance artifact (META.md) in a doc about reducing maintenance burden.

### D-SESS-03: Keep existing naming convention for research sessions

**Decision:** Keep `YYYY-MM-DD_N_source_topic/` convention already in use. Don't migrate to the research-proposed `YYYY-MM-DD-brief-topic/`.
**Context:** 11 existing sessions already use the current convention. Source tool info (perplexity, sisyphus) is useful for provenance.
**Why it matters:** Zero migration cost, preserves provenance information, consistent with existing artifacts.

## Process Insights

### Insight 1: Research docs propose more than needed — curate ruthlessly

**Observation:** The Perplexity research produced a comprehensive 508-line document with 5 protocols, 4 subdirectories, INDEX.md, META.md, and a D-023 proposal. Only 3 items were actually actionable now (INDEX.md, template field, template checklist section).
**Type:** workflow-process
**Implication:** When consuming research outputs, immediately separate "actionable now" from "interesting but future." Default to implementing <30% of what's proposed.

### Insight 2: YAGNI applies to process artifacts too, not just code

**Observation:** Empty `comparative/`, `literature/`, and `validation/` directories would be premature process infrastructure — the same anti-pattern as writing abstract base classes before having two implementations.
**Type:** workflow-process
**Implication:** Don't create directories, templates, or protocols for work that hasn't been done yet. Create them the moment the first item needs to go there.

### Insight 3: Minimal template changes have high leverage

**Observation:** Adding one YAML field (`docs_to_update`) to the S5 template and one table to the S8 template creates a documentation validation gate with zero agent prompt changes. The enforcement flows naturally through existing S5→S8 handoff.
**Type:** domain-insight
**Implication:** Template changes are the highest-leverage intervention for workflow behavior because every future artifact inherits the change automatically.

## Anti-Patterns Observed

### Anti-Pattern 1: Solving documentation decay with more documentation

**Temptation:** Create META.md per session, INDEX.md, quarterly audit protocols, and a formal D-023 decision — all to prevent docs from going stale.
**Reality:** Each new doc artifact IS more documentation surface that can decay. The minimal approach (one INDEX.md + template enforcement) achieves 80% of the benefit at 20% of the maintenance cost.

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| Research INDEX | `docs/research/INDEX.md` | CREATED | Master catalog of research sessions + traceability |
| Task spec template | `templates/task-spec.md` | UPDATED | Added `docs_to_update` field for S8 validation |
| Review report template | `templates/review-report.md` | UPDATED | Added Documentation Validation checklist |

## What Should Happen Next

1. After first S1-S9 cycle completes, verify that `docs_to_update` and S8 documentation validation actually get used — adjust if not
2. When 3+ comparative studies accumulate, create `docs/research/comparative/` subdir
3. Implement Protocol 3 (G0 drift detection) after v1 dogfooding begins
