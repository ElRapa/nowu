---
artifact_type: SESSION_LEARNINGS
session: "SYNTHESIS + Architecture Vision"
created_at: 2026-05-06
source_artifacts:
  - state/arch/SYNTHESIS-001.md
  - docs/architecture/ARCHITECTURE-VISION.md
purpose: "Decisions, insights, and process learnings to inform future synthesis/architecture work and agent/skill design"
---

# Session Learnings: SYNTHESIS + Architecture Vision

## Decisions Made

### D-SYN-01: 9 themes, not 6

**Decision:** Accept 9 cross-cutting themes instead of the 6 predicted by prior analysis.

**Context:** The handoff predicted: Continuity, Knowledge persistence, Workflow orchestration,
Epistemic awareness, Domain agnosticism, Observability.

**What happened:** All 6 confirmed with strong evidence. 3 additional themes discovered:
- T7 (Multi-Surface Access) — distinct from T5 (Domain Agnosticism): T5 is WHAT the system
  supports, T7 is WHERE/HOW the human accesses it.
- T8 (Progressive Disclosure) — distinct from T3 (Workflow Orchestration): T3 is agent
  sequencing, T8 is the human's journey from vague to structured.
- T9 (Audience-Aware Rendering) — distinct from T6 (Observability): T6 is "is it healthy?",
  T9 is "render the same data for different consumers."

**Why it matters:** Each new theme represents a distinct architectural concern with its own
ADR recommendation. Missing them would leave gaps in the architecture.

---

### D-SYN-02: Knowledge model is THE foundational ADR

**Decision:** ADR-0008 (Knowledge Atom Model) must be written FIRST. 5 of 9 themes
depend on the atom schema being defined.

**Context:** T1 (continuity state IS atoms), T4 (grades live ON atoms), T5 (domains
extend atom types), T8 (atoms have maturity stages), T9 (atoms are what gets rendered).

**Why it matters:** Without this decision, ADR writing could start with any theme. The
dependency analysis shows that starting elsewhere creates circular dependencies.

---

### D-SYN-03: "Operating environment" system classification

**Decision:** nowu is an "AI-native project operating environment" — not a framework,
platform, runtime, or tool.

**Reasoning:** The OS analogy holds:
- know = memory management
- flow = process scheduling
- core = filesystem (artifacts)
- bridge = user interface
- Approval tiers = security/permissions
- Domain configs = device drivers

**Why it matters:** Classification determines how people think about extension points
and boundaries. "Framework" implies "install into your project." "Operating environment"
implies "your projects live inside this."

---

### D-SYN-04: Quality attributes are explicitly ranked tradeoffs

**Decision:** 6 quality attributes ranked with explicit "trades off against" statements.
Continuity > Performance > Correctness > Speed > etc.

**Why it matters:** Without explicit ranking, every design decision becomes a debate.
With ranking, the answer to "should we sacrifice X for Y?" has a pre-made answer
from the architecture.

---

### D-SYN-05: Risks are part of the vision, not afterthoughts

**Decision:** 7 risks documented in the Architecture Vision with mitigation strategies.
Including: knowledge model over-engineering, epistemic bureaucracy, domain abstraction gap.

**Why it matters:** Architecture visions that don't name their risks become aspirational
documents. Naming risks commits to checking whether they're materializing.

---

## Process Insights (For Agent/Skill Design)

### Insight 1: Synthesis requires BREADTH reading, not depth

The synthesis agent must read ALL UCs (all 50). Sampling doesn't work because themes
only emerge when you see the same infrastructure need repeated across very different
domains. T4 (Epistemic Awareness) was visible only because the same confidence concern
appeared in NF-15 (framework), AP-01 (food regulation), PK-05 (learning), and RE-05
(records) — domains that have nothing else in common.

**Skill implication:** The synthesis skill must mandate "read all UCs" as a hard
prerequisite, not "sample representative UCs."

---

### Insight 2: Theme extraction is clustering by shared infrastructure need

A theme is NOT a category (like "knowledge" or "workflow"). A theme is: "these N UCs
all REQUIRE the same underlying capability that none of them can solve alone."

The test: Can you solve this concern by addressing a single UC? If yes → it's not a theme.
If no (you need a systemic capability) → it IS a theme.

**Skill implication:** The synthesis agent prompt should include this test as a validation
step for each candidate theme.

---

### Insight 3: The "3+ UC" threshold is correct but needs the "different domain" qualifier

A theme that appears in 5 NF UCs but zero AP/RE/PK/XP UCs might be a module concern, not
a cross-cutting theme. The strongest themes (T2, T4, T5) span ALL domain categories.

**Skill implication:** Theme validation should require evidence from at least 2 different
UC category prefixes (NF + at least one of PK/XP/AP/RE).

---

### Insight 4: ADR recommendations need DEPENDENCY ORDERING, not just listing

The value of the ADR roadmap is: "You cannot write ADR-0010 until ADR-0008 exists because
grades live ON atoms." Without ordering, teams start with whatever seems most interesting
and hit circular dependencies.

**Skill implication:** The synthesis output template should require a "dependency chain"
section that explains the ordering rationale.

---

### Insight 5: Architecture Vision must be DERIVED, not aspirational

Every principle in the Architecture Vision traces to specific UCs that REQUIRE it.
"We believe in X" is banned. "These UCs make X architecturally necessary" is mandatory.

The litmus test: Remove a principle. Which UCs become architecturally impossible?
If none → the principle is aspirational. Delete it.

**Skill implication:** The architecture vision agent prompt should require a
"source evidence" field for every principle, with specific UC IDs.

---

### Insight 6: System classification benefits from a concrete analogy

Calling nowu an "operating environment" is only useful because the OS analogy maps
concretely: know=memory, flow=scheduler, bridge=UI, etc. Abstract classifications
("it's a platform") without analogy mapping are useless.

**Skill implication:** The architecture vision template should include a "system
analogy" section that maps concepts to something concrete.

---

### Insight 7: Validation against prior predictions is a quality signal

The handoff predicted 6 themes. Confirming all 6 (plus finding 3 more) validates both:
1. The prior analysis was directionally correct
2. The new synthesis adds value beyond just confirming predictions

**Skill implication:** Future synthesis runs should always receive "expected themes" as
input and produce an explicit "validation result" comparing prediction to finding.

---

## Anti-Patterns Observed (What Could Go Wrong)

### Anti-Pattern 1: Synthesizing without full read

Temptation: "I've read the NF and PK groups, that's enough — they're the high-relevance
ones." Reality: T5 (Domain Agnosticism) and T9 (Audience-Aware Rendering) are only
visible from the AP/RE/XP groups. Skipping "low relevance" categories produces incomplete
synthesis.

### Anti-Pattern 2: Themes as categories instead of infrastructure needs

Temptation: Group UCs by topic (all PK UCs → "knowledge theme"). Reality: PK-01 (capture)
and PK-06 (security) have completely different architectural implications despite being
in the same category. Theme extraction must ignore categories.

### Anti-Pattern 3: Architecture Vision as wish list

Temptation: "Our architecture should be modular, scalable, testable, secure,
performant, and beautiful." Reality: Everything trades off against something. A
vision without explicit tradeoffs says nothing. The ranking IS the vision.

### Anti-Pattern 4: ADR recommendations without dependency analysis

Temptation: "Here are 9 ADRs to write. Good luck." Reality: Starting with ADR-0013
(adapters) before ADR-0008 (atoms) produces an adapter architecture with nothing to
adapt. Order matters more than completeness.

---

## What This Session Produced

| Artifact | Location | Grade | Purpose |
|----------|----------|-------|---------|
| SYNTHESIS-001 | `state/arch/SYNTHESIS-001.md` | HYPOTHESIS | 9 themes + ADR roadmap |
| Architecture Vision | `docs/architecture/ARCHITECTURE-VISION.md` | HYPOTHESIS | System classification + principles + quality attributes + risks |
| Session Learnings | `state/arch/session-learnings-synthesis-2026-05-06.md` | — | This file — process insights for future automation |

## What Should Happen Next

1. **Write ADR-0008** (Knowledge Atom Model) — the foundational ADR
2. **Write ADR-0010** (Epistemic Grades) — pervasive metadata model
3. **Write ADR-0007** (Continuity Protocol) — enables NF-01
4. **Write ADR-0009** (Orchestration Handoff) — enables first S1-S9
5. **Run first S1-S9 intake** against the hypothesis architecture
6. **Build Synthesis and Architecture Vision agents/skills** using these learnings

---

## Addendum: Perplexity Review Insights (2026-05-07)

External review by Perplexity of SYNTHESIS-001 and ARCHITECTURE-VISION.
Source: `state/arch/2026-05-07_1_review_synthesis001+architecture-vision_perplexity.md`

### Validated

- SYNTHESIS-001 rated as "research-grade" — evidence-based theme extraction confirmed
- ARCHITECTURE-VISION rated as "theory-grounded" — OS analogy praised as precise, not marketing
- STAGED-PLAN rated as "buildable" — Areas × Stages structure confirmed correct
- Session learnings rated as "goldmine metadata" — D-SYN-02 and Insight 2 highlighted

### Refinements Applied

#### R1: ADR Dependency Graph Made Explicit

**Problem:** ADR-0007 (continuity) implicitly depends on ADR-0008 (atom schema) because
"session state IS knowledge atoms." The dependency was stated in text but not in the graph.

**Fix:** Updated SYNTHESIS-001 dependency graph to show:
```
ADR-0008 → ADR-0010 + ADR-0007 (parallel) → ADR-0009
```

**Learning:** Dependency graphs should be verifiable from the graph alone, without
reading surrounding text. If a dependency is mentioned in prose but not in the diagram,
it will be missed during implementation.

#### R2: OS Analogy Missing Kernel/User Space

**Problem:** The OS analogy maps modules to OS concepts but doesn't specify where
project-specific state lives (the equivalent of "user space").

**Fix:** Added open question to ARCHITECTURE-VISION §1 for resolution in ADR-0011.
Hypothesis: each project gets isolated state directory + knowledge scope.

**Learning:** Analogies must be complete to be useful. A partial analogy that maps 5
of 6 concepts creates false confidence — the unmapped concept becomes a blind spot.

#### R3: W3.5 Fitness Functions Before W4

**Problem:** W4 (first S1-S9 intake) runs without automated architectural guardrails.
If code violates ADR-0008 (atom schema) or ADR-0001 (import boundaries), detection is manual.

**Disposition:** Valid but premature for W3. ADR-0008 hasn't defined the atom schema yet.
F2 (boundary enforcement test) already provides basic guardrails. Added W3.5 to
STAGED-PLAN as a lightweight task between W3 and W4.

**Learning:** Fitness functions need something to test. Writing checks before the
schema they validate exists is inverted — but the CONCEPT of "add guardrails before
first real usage" is sound and should be a standard step in any ADR→implementation flow.
