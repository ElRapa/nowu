---
artifact_type: SESSION_LEARNINGS
session: "W28 dual-agent comparison: workflow (T1) vs freeform (T2)"
created_at: 2026-05-15
session_type: "dual-agent-comparison"
source_artifacts:
  - .sisyphus/evidence/w28-freeform/process-notes.md
  - .sisyphus/evidence/w28-freeform/gap-comparison.md
  - .sisyphus/evidence/w28-freeform/intake-brief.md
  - state/arch/w28-gap-comparison.md
  - state/intake/intake-008.md
  - state/learnings/session-2026-05-15-w28-workflow.md
  - state/learnings/session-2026-05-15-dual-agent-evaluation.md
purpose: "Compare outputs of the W28 workflow (T1) and freeform (T2) across 5 dimensions and record learnings"
---

# Session Learnings: W28 dual-agent comparison

## What Was Done

- Collected T1 (workflow) artifacts and T2 (freeform) evidence for W28.
- Scored both agents on five dimensions (Time, Artifact quality, Blindspot detection, Process overhead, Evidence depth).
- Documented and analyzed the GAP-006 divergence and judged which classification is more defensible.
- Produced comparison document, updated INDEX, appended notepad, and created evidence files.

## Decisions Made

### D-SESS-04: Require side-by-side per-gap evidence when running dual-agent comparisons

**Decision:** Dual-agent comparisons must include an explicit side-by-side evidence row for each gap citing both agent outputs before classification.
**Context:** W27/W28 show that summarizing without explicit dual anchors increases disagreement and reduces defensibility.
**Why it matters:** Prevents re-litigation and supports roadmap prioritization decisions.

---

## Comparison Scores (1-5 scale)

Scoring notes: 1=poor, 5=excellent. Scores derived from source artifacts listed above.

1) Time
- Workflow (T1): 2 (full S1-S9 cycle; multi-hour effort; recorded appetite 8h; session evidence shows ~30+ min to complete chain)
- Freeform (T2): 5 (~2 minutes elapsed per process-notes)

2) Artifact quality (completeness, accuracy, specificity)
- Workflow (T1): 5 (produced full S1-S9 chain: intake, constraints, options, decision, fit, gap comparison; many accepted artifacts)
- Freeform (T2): 3 (produced intake brief + gap comparison + evidence notes; less artifact coverage, shallower per-gap detail)

3) Blindspot detection
- Workflow (T1): 5 (S2 blindspot checks, explicit per-gap AP vs RE evidence, D-SESS-01 guardrails)
- Freeform (T2): 3 (fast scan surfaced all gaps as systemic but did not include the S2 guardrail-style blindspot annotations; higher risk of overclaim)

4) Process overhead
- Workflow (T1): 1 (high overhead: full pipeline, multiple artifacts, review loops)
- Freeform (T2): 5 (minimal overhead; read 5 docs and output classification quickly)

5) Evidence depth
- Workflow (T1): 5 (cross-links to intake-008 artifacts, citations to fit-assessment and decision proofs, S1-S9 produced supporting depth)
- Freeform (T2): 3 (referenced key docs and ADRs but lacked deep cross-linking to S1-S9 fit artifacts)

## GAP-006 Divergence Analysis

Summary: T1 classified GAP-006 as domain-specific (AP-oriented) based on RE evidence not surfacing equivalent regulatory freshness urgency in this cycle. T2 classified GAP-006 as systemic, arguing freshness/staleness concerns apply in principle to RE-01 and RE-06.

Evidence from T1 (state/arch/w28-gap-comparison.md): lines 59-63 document that RE sources did not surface automated freshness need with the same structural urgency; classification labeled GAP-006 as domain-specific in current evidence.

Evidence from T2 (.sisyphus/evidence/w28-freeform/gap-comparison.md): lines 57-61 assert freshness/staleness detection is cross-domain lifecycle necessity and therefore systemic.

Assessment: Both classifications are defensible. T1's position is more conservative and evidence-grounded for this cycle because it explicitly compares per-gap AP and RE artifacts and reports absence of equivalent urgency in RE evidence during S1-S9 artifacts. T2's position is more generalist, arguing from principle that freshness matters across domains but lacks the same per-gap comparative anchor to RE S1-S9 artifacts.

Recommendation: Treat GAP-006 as provisionally domain-specific for W28 (as per T1) but add a monitoring trigger: include automated freshness checks in the next RE/AP comparative run (Wxx) and escalate if RE evidence later surfaces comparable operational urgency.

---

## Models and Agents Fired

- Models: nowu agents (mix of GPT-5.3-Codex and GPT-5.4), Oracle reviews (GPT-5.4), orchestrator (claude-opus-4-6) — see session-2026-05-15-dual-agent-evaluation.md for full mappings.
- Agents fired this session: not individually tracked in freeform evidence (T2) beyond process-notes; workflow agents are recorded across S1-S9 artifacts (T1). Marked as "not individually tracked" where unknown.

---

## Process Insights

- Freeform is valuable for rapid hypothesis checks but cannot substitute for S1-S9 depth when classification decisions affect roadmap prioritization.
- Conservative, evidence-anchored classification (T1) is preferred for roadmap actions; freeform can surface alternative perspectives that should be tested in later runs.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|---|---|---|---|
| Dual-agent comparison | `state/learnings/session-2026-05-15-w28-dual-agent.md` | DONE | Persisted dual-agent comparison and recommendation |
| Evidence: freeform outputs | `.sisyphus/evidence/w28-freeform/` | DONE | Source materials from T2 |
| Gap comparison (workflow) | `state/arch/w28-gap-comparison.md` | ACCEPTED | Source materials from T1 |

## What Should Happen Next

1. Monitor GAP-006 in the next cross-domain run; add explicit freshness prompts to RE-01/RE-06 evidence collection.
2. Institutionalize a lightweight freeform quick-scan that feeds a checklist into S1 to reduce S1 setup time while preserving per-gap evidence anchoring.
3. Keep dual-agent pattern for high-impact classification decisions (Roadmap/K3-level) and require per-gap side-by-side evidence rows (D-SESS-04).
