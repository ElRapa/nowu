---
artifact_type: LEARNINGS
altitude: ARCHITECTURE
phase: LEARN
epistemic_grade: INFORMED_ESTIMATE
created_at: 2026-05-06
session: "5×10 workflow model design + Perplexity evaluation"
source_artifacts:
  - nowu-5x10-implementation-package/perplexity_evaluation/
  - .sisyphus/drafts/idea-004-2d-altitude-phase-model.md
related_decisions: [D-WF-001 through D-WF-013]
status: ACTIVE
---

# Session Insights & Learnings: 5×10 Model Design

> These are the **insights** — the "why" behind decisions, the named failure modes,
> the methodology patterns. Decisions are in `5x10-session-synthesis-2026-05-06.md`.
> These learnings should inform ALL future workflow sessions.

---

## Insight 1: SYNTHESIS Is the Missing Link

**What we discovered:** The project is stuck between "approved UCs exist" and "architecture that supports them." S1-S9 ASSUMES architecture already exists — it doesn't create it. Without SYNTHESIS, every intake starts from scratch with no shared architectural understanding.

**Named failure mode:** "Altitude drift" — going from PRODUCT (UCs) directly to DELIVERY (epics) without ARCHITECTURE synthesis. Research name: "Premature decomposition" (Boehm 1988).

**Implication:** SYNTHESIS must be an explicit step that happens BEFORE any S1-S9 intake when ≥2 UCs have architectural implications. It's not optional overhead — it's the thing that makes intakes coherent with each other.

---

## Insight 2: The 5×10 Grid Is Cognitive GPS, Not Enforcement Matrix

**What we learned:** The grid tells agents "where you are" and "what valid next moves look like." It does NOT prescribe a single path or forbid cells.

**Analogy:** Like a city map showing streets and landmarks. You can take any route, but the map helps you know if you're heading toward your destination or away from it.

**Anti-pattern:** Don't implement the grid as a state machine with allowed/forbidden transitions. Implement it as a registry that agents can query: "Given my altitude and phase, what do I typically produce? What comes next?"

---

## Insight 3: S1-S9 Is a Default Traversal, Not THE Workflow

**What we learned:** S1-S9 zigzags DELIVERY→ARCHITECTURE→DELIVERY→EXECUTION. This is the most common path for feature intakes. But it's not the only valid path.

**Alternative traversals (validated):**
- Bug fix: EXECUTION only (no architecture needed)
- Spike/exploration: ARCHITECTURE only (no implementation)
- Strategic pivot: STRATEGIC→PRODUCT (no delivery yet)
- SYNTHESIS: ARCHITECTURE only (triggered by UC accumulation)

**Implication:** The model should DESCRIBE observed patterns, not PRESCRIBE mandatory sequences. The default traversal is a convenience, not a constraint.

---

## Insight 4: JIT Specification Methodology

**Source:** Perplexity strategic analysis, citing Martinelli 2026

**The pattern:** Write specs BEFORE code, keep them SHORT (1-2 pages), update EVERY TIME you learn something new. Specs are living artifacts, not paperwork.

**How it applies to nowu:** Each altitude's spec stabilizes BEFORE the next altitude starts implementation. PRODUCT specs (UCs) stabilize before ARCHITECTURE work begins. ARCHITECTURE specs (ADRs) stabilize before DELIVERY shaping. DELIVERY specs (tasks) stabilize before EXECUTION coding.

**Key distinction from waterfall:** Specs are SHORT, version-controlled, and updated per iteration — not written once and frozen.

---

## Insight 5: Manual SYNTHESIS Bootstrap Is Valid Methodology

**Source:** AFLOW (ICLR 2025), Shape Up (Basecamp 2018)

**The pattern:** AFLOW started with a completely blank template and discovered its operators through 6,300 executions. Shape Up ran one cycle before formalizing the shaping process.

**Applied to nowu:** Running SYNTHESIS manually BEFORE it's formalized in the model is not circular reasoning — it's the same bootstrap methodology validated by both AFLOW and Shape Up.

**Validation criteria:** Does the manual SYNTHESIS produce themes that (a) align with existing ADRs and (b) surface at least one new gap? If yes, the process is validated.

---

## Insight 6: Virtuous vs. Vicious Circularity

**Source:** Perplexity Q1 analysis, philosophy literature

**The distinction:**
- Vicious: "My gas gauge is reliable because my gas gauge says it's reliable" (no independent ground truth)
- Virtuous: "This process works because executing it once produced expected outcomes, and iteration improved them measurably" (ground truth exists)

**Applied to nowu:** We have independent ground truth: 50 approved UCs with known architectural implications, 6 existing ADRs, 4 goals with success criteria. The manual SYNTHESIS can be validated against these.

---

## Insight 7: Phases Are Cognitive Modes, Not Fixed Positions

**Source:** AFLOW operator analysis, Rombaut 2026

**What this means:** IMPLEMENTATION is not "always at EXECUTION altitude." You IMPLEMENT at ARCHITECTURE altitude when writing an ADR. You IMPLEMENT at DELIVERY when creating a task spec. You IMPLEMENT at EXECUTION when writing code.

**The only exception:** SYNTHESIS is altitude-locked to ARCHITECTURE. It's the only phase that doesn't make sense at other altitudes, because its purpose is cross-cutting pattern detection across artifacts from lower altitudes.

---

## Insight 8: Agents Should Be Altitude-Agnostic Executors

**Source:** Hierarchical MAS research, Redis 2026 multi-agent patterns

**The pattern:** S1-S9 agents don't need to know their altitude. The orchestrator/router knows altitude and routes appropriately. This is better than making agents "altitude-aware" because:
1. Agents stay simple and focused on their cognitive mode
2. Routing logic is centralized and testable
3. The same agent can operate at different altitudes if needed

**The 10% exception:** GAP/reflective agents ARE altitude-aware because their job IS to reason about cross-altitude patterns.

---

## Insight 9: The Current Block Is Structural, Not Motivational

**What we diagnosed:** The project isn't stuck because of laziness or lack of ideas. It's stuck because there's a structural gap in the workflow: UCs exist → [MISSING: global synthesis + architecture vision] → ADRs → S1-S9. The workflow literally can't proceed without SYNTHESIS output.

**Why this matters:** Adding more UCs, refining existing docs, or trying to run S1-S9 without SYNTHESIS will produce the same "patchwork" result. The ONLY forward path is W1 (SYNTHESIS) + W2 (Architecture Vision).

---

## Insight 10: Epistemic Grades Create Trust Calibration

**Source:** Novel innovation in nowu — no comparable mechanism found in existing frameworks

**Why it matters:** Without explicit confidence grades, downstream agents (and humans) can't distinguish between "this ADR was carefully validated through 5 intakes" and "this ADR was our first guess." Both look the same in markdown.

**The mechanism:** Grade every artifact at creation. HYPOTHESIS = "best guess, will likely change." INFORMED_ESTIMATE = "validated through some usage." EVIDENCE_BASED = "proven through multiple cycles." This lets agents weight decisions appropriately.

---

## Insight 11: Triage Is the Missing Primitive for "What Next?"

**What we discovered:** Neither S1-S9 nor P0-P4 answers "what should we do next?" They assume you already KNOW what to work on. In practice, with 50 UCs and multiple possible next steps, you need explicit triage.

**Triage = Intake → Assessment (Impact × Altitude) → Routing**

**Deferred until:** After SYNTHESIS validates (the themes tell you what's high-impact), before S1-S9 scales (when you have multiple things competing for attention).

---

## Insight 12: Fitness Functions > Manual Review for Architectural Guardrails

**Source:** InfoQ, evolutionary architecture literature

**The pattern:** Instead of relying on S8 (Review) to catch architectural violations, encode architectural characteristics as automated checks that run after every change.

**Examples:** Import boundary test (already exists!), artifact frontmatter validation (verify-artifact.py), grade threshold checks at decision gates.

**When to add:** v1.1 (after SYNTHESIS + hypothesis ADRs exist to define what to check).

---

## Meta-Insight: Research Validation Changes Confidence

**Pattern observed:** Every time Perplexity found independent research validating a nowu design choice, our confidence (epistemic grade) increased. This is the grade promotion mechanism in action:

- "SYNTHESIS is needed" → confirmed by TOGAF Phase A → HYPOTHESIS → INFORMED_ESTIMATE
- "Manual bootstrap is valid" → confirmed by AFLOW + Shape Up → HYPOTHESIS → EVIDENCE_BASED
- "Soft enforcement" → confirmed by ADR lifecycle research → HYPOTHESIS → INFORMED_ESTIMATE
- "Router-based agents" → confirmed by hierarchical MAS → HYPOTHESIS → INFORMED_ESTIMATE

This is what the epistemic grade system looks like in practice. Future sessions should explicitly track these promotions.
