---
artifact_type: SESSION_LEARNINGS
session: "W27 dual-agent evaluation: nowu agents vs Oracle across S1-S8"
created_at: 2026-05-15
session_type: "workflow-optimization"
source_artifacts:
  - state/intake/intake-007.md
  - state/arch/intake-007-constraints.md
  - state/arch/intake-007-options.md
  - state/arch/intake-007-decision.md
  - state/arch/intake-007-fit-assessment.md
  - state/arch/intake-007-ap06-proof.md
  - state/arch/intake-007-ap01-mini-graph.md
  - state/arch/intake-007-ap02-mini-version-chain.md
  - state/arch/intake-007-gap-register.md
  - state/reviews/intake-007-review.md
  - state/capture/capture-intake-007.md
purpose: "Capture quality deltas and process improvements from dual-agent evaluation across workflow steps"
---

# Session Learnings: W27 Dual-Agent Evaluation (nowu vs Oracle)

## What Was Done

- Ran a dual-agent evaluation pattern across workflow steps (S1, S2, S3, S5, S6, S8), comparing baseline nowu outputs against independent Oracle assessments.
- Collected and synthesized concrete quality gaps by step, including scope/constraint violations, representational incompleteness, and review false positives.
- Used Oracle pre-review checks before final S8 to catch quality defects early (AC claim boundary, scoring math, representational limits coverage).
- Completed S9 curation for intake-007 with accepted evidence artifacts, gap register promotion, and roadmap status closure for W27.

## Decisions Made

### D-SESS-01: Adopt dual-agent review as default for high-risk artifacts

**Decision:** For architecture-heavy and evidence-claim work, run Oracle independently before final S8 submission rather than relying only on nowu step outputs.
**Context:** Oracle repeatedly surfaced deeper and more operationally specific issues than baseline nowu outputs in W27.
**Why it matters:** This reduces avoidable S8 rejection loops and raises artifact quality before formal review.

### D-SESS-02: Treat context restrictions as explicit risk inputs

**Decision:** When a step cannot load `src/` or canonical UC definitions, annotate expected blind spots upfront and compensate in adjacent steps.
**Context:** S2 missed contract-surface limitations and UC-accuracy checks due to enforced context boundaries.
**Why it matters:** Prevents overconfidence and ensures high-impact blind spots are surfaced as known limitations instead of latent defects.

---

## Process Insights

### Insight 1: S1 intake quality degraded by architecture bleed

**Observation:** S1 mixed user problem framing with thesis/architecture language, scoped `know` as in-scope instead of WATCH, and generalized concrete UC details.
**Type:** agent-behavior
**Implication:** Enforce stricter S1 prompt guardrails: no ADR/schema debates, concrete UC detail preservation, and explicit WATCH validation.

### Insight 2: S2 biggest miss was contract-surface limitation visibility

**Observation:** S2 did not characterize the MemoryService 4-method surface as the primary blocker, included lower-value noise items, and overclaimed conformance feasibility.
**Type:** agent-behavior
**Implication:** Add mandatory S2 limitation statement when `src/` is out-of-scope and require feasibility confidence grading for each major claim.

### Insight 3: S3 was template-correct but under-specific on deliverables

**Observation:** S3 had strong structural compliance (Mermaid + weighted tables) but weak operational specificity, did not characterize DecisionRecord limits deeply, and omitted gap-register structure proposal.
**Type:** agent-behavior
**Implication:** Add a required “deliverable concreteness check” (counts, exemplars, schema-level fields) before S3 handoff.

### Insight 4: S6 outputs were adequate but proof depth was partial

**Observation:** All four S6 artifacts passed as ADEQUATE, but tended to prove “can be written in Markdown” more than “structurally equivalent to NF-02,” with missing crosswalk completeness, representational limits, and scoring math accuracy.
**Type:** agent-behavior
**Implication:** Add pre-S8 artifact checks for crosswalk completeness, arithmetic verification, and explicit “limits vs proved” separation.

### Insight 5: S8 produced a false positive on legitimate workflow artifacts

**Observation:** S8 initially flagged DECISIONS.md and `.active-scope` as scope violations, though these were valid S4/S5 workflow outputs.
**Type:** workflow-process
**Implication:** Update S8 review rubric to distinguish evidence-scope files from legitimate cross-step workflow outputs.

### Insight 6: Dual-agent pattern consistently increased issue depth

**Observation:** nowu outputs were often template-compliant while Oracle provided deeper contract-surface analysis, feasibility realism, and concrete deliverable specs.
**Type:** workflow-process
**Implication:** Keep dual-agent pattern for critical cycles and use Oracle deltas as a quality overlay, not a replacement for nowu step agents.

### Insight 7: S2 context restrictions create systematic blind spots

**Observation:** Not loading `src/` prevented direct contract-surface verification; not loading USE_CASES.md reduced UC-accuracy validation.
**Type:** workflow-process
**Implication:** Introduce explicit “blindspot register” in S2 outputs when constraints block primary evidence sources.

### Insight 8: Oracle pre-review prevented a full S8 rejection cycle

**Observation:** Pre-S8 Oracle checks caught AC-3 partial-proof framing issues, scoring math errors, and incomplete limits sections before final S8.
**Type:** workflow-process
**Implication:** Institutionalize an optional pre-review checkpoint for high-risk cycles to reduce churn and reviewer turnaround time.

### Insight 9: Model-role pairing mattered materially

**Observation:** nowu agents used GPT-5.3-Codex (via deep/unspecified-high category) for some steps and GPT-5.4 for others; Oracle reviews consistently used GPT-5.4 (via oracle subagent); orchestrator (Sisyphus) ran on claude-opus-4-6. The GPT-5.4 Oracle reviews produced stronger critical depth and operational specificity than both GPT-5.3-Codex and GPT-5.4 nowu agent outputs, suggesting the oracle subagent's system prompt and read-only constraint focus reasoning quality more than model alone.
**Type:** tooling
**Implication:** Keep cheaper models for throughput drafting and GPT-5.4 Oracle for critical evaluation gates where defect-cost is high.

### Insight 10: Auto-compaction destroys learnings fidelity

**Observation:** Session learnings were written at end of session after auto-compaction had already compressed earlier turns. The S9 capture agent had access to artifact contents but not the nuanced conversational context (e.g., exact model names used per step, specific Oracle critique phrasing, orchestrator reasoning for revision choices).
**Type:** workflow-process
**Implication:** Write learnings incrementally during the session (after each dual-agent comparison) rather than batching at S9. Alternatively, persist key observations to a scratch file as they occur so compaction doesn't erase them.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Architecture bleed in S1

**Temptation:** Add architecture context early (“more context = better intake quality”).
**Reality:** This pre-loads S2/S3 conclusions, violates altitude discipline, and contaminates problem framing with solution bias.

### Anti-Pattern 2: Overclaiming in acceptance criteria

**Temptation:** Write ambitious ACs (“created, stored, queried”) to show stronger value.
**Reality:** If contract surfaces cannot support the claim (e.g., MemoryService limits), downstream steps are forced into infeasible or misleading proof narratives.

---

## Models and Agent Configuration Used

- **nowu agents (S1, S2, S3, S5, S6, S8):** Mix of GPT-5.3-Codex and GPT-5.4 (deep/unspecified-high category)
- **Oracle independent reviews:** GPT-5.4 (oracle subagent)
- **Orchestrator (Sisyphus main):** claude-opus-4-6

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| W27 capture record | `state/capture/capture-intake-007.md` | DONE | S9 closure summary with next-cycle trigger and commit guidance |
| Dual-agent learnings | `state/learnings/session-2026-05-15-dual-agent-evaluation.md` | DONE | Persist quality and process findings from nowu-vs-Oracle evaluations |
| W27 roadmap closure | `docs/ROADMAP-003.md` | ACTIVE | Mark W27 done and advance Section 7 to W28 |

## What Should Happen Next

1. Add S1 guardrails to prevent architecture bleed and enforce concrete UC fidelity.
2. Add S2 blindspot reporting requirements when `src/`/USE_CASES context is restricted.
3. Add a lightweight Oracle pre-review checkpoint before S8 for high-risk evidence cycles.
4. Update S8 reviewer rubric to distinguish legitimate workflow outputs from true scope drift.
5. Add arithmetic and crosswalk-completeness checks to S6 artifact verification checklists.
