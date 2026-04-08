---
id: idea-005
created: 2026-04-08
status: DRAFT
size: Epic
captured_by: human (Raphael) — surfaced during pre-workflow v1core P2 epic review
session: pre-workflow P1→P4 run
related_ucs: NF-15, NF-06, NF-02, NF-13
sibling_library: know/src/know/ontology.json (epistemic_grades already defined)
---

# Idea: Epistemic Grades as a Framework Primitive

## Raw Signal

During the P2.1 epic review for v1-core, the human noticed that epic-002 (Decision Memory
& Pipeline Quality) treats "multiple options + structured evaluation = trustworthy decision"
as sufficient. It does not ask: how confident are we in each option? On what evidence?

More importantly: the framework's own workflow has no step that demands external research
or evidence gathering before an options sheet or decision record is produced. The human
was the only source of epistemic quality injection — by consulting external sources and
asking hard questions. The framework should model this, not leave it to human vigilance.

The `know` sibling library already defines a 5-level epistemic scale in `ontology.json`:
  SPECULATION (0.1-0.3) → HYPOTHESIS (0.3-0.5) → INFORMED_ESTIMATE (0.5-0.7)
  → EVIDENCE_BASED (0.7-0.9) → VERIFIED_FACT (0.9-1.0)

This vocabulary should become the canonical confidence language across the entire nowu
framework, not just the knowledge storage layer.

## Why It Matters

1. **Wrong decisions get the same trust signal as right ones.** An options sheet produced
   from analogy and gut feel looks identical to one backed by benchmarks and prior art. The
   human cannot tell them apart at review time without reading every word carefully.

2. **The learning loop is broken without it.** NF-06 says "the system learns by running."
   But if a lesson carries no grade, future agents cannot know whether it is a validated
   pattern or a one-off coincidence. Learning from a SPECULATION-grade lesson as if it were
   VERIFIED_FACT is worse than not learning at all.

3. **The human is currently the only quality gate.** The framework delegates epistemic
   quality to human vigilance rather than building it into the workflow. This is a single
   point of failure — if the human doesn't ask hard questions, bad confidence levels pass
   unchallenged.

4. **Forward compatibility with `know`.** The `know` library already stores atoms with
   grades. If the framework uses different vocabulary or no grades at all, the integration
   point between workflow outputs and knowledge atoms will require a lossy mapping step.
   Adopting the ontology now costs nothing; fixing it later costs a migration.

## Concrete Direction

### Framework-level

- All agent prompts that produce options, decisions, recommendations, research, or lessons
  must include a `epistemic_grade` field using the `know` ontology vocabulary.
- Grade must be accompanied by a `grade_justification` — one sentence stating what raises
  or limits the grade (e.g., "INFORMED_ESTIMATE: based on 3 GitHub comparisons, no
  production usage in comparable context found").
- Grades must be surfaced to the human at review gates, not buried in metadata.
- Reviewer agents (S8) must check that grades are present and justified — missing grades
  are a blocker, not a warning.

### Confidence sub-loop (proposed)

At decision points where the producing agent's grade is below EVIDENCE_BASED:
1. Surface the grade and gap explicitly to the human.
2. Offer a "research step" — the human or a research agent gathers missing evidence.
3. After research, the agent re-assigns the grade and records what changed.
4. The delta (old grade → new grade + what evidence caused the promotion) is stored as a
   durable record in the decision artifact.

This makes epistemic quality improvement an explicit, traceable workflow action — not a
silent background improvement or a human-only responsibility.

### Knowledge atom alignment

When workflow outputs (decisions, lessons, options) are eventually ingested into the `know`
knowledge layer, the framework grade maps directly to the `know` ontology grade with no
transformation needed.

### Tracking confidence vs. reality

At S9 (Capture), the Curator records whether the decision turned out to be correct and
flags any grade-reality mismatches (e.g., "this was EVIDENCE_BASED at decision time but
turned out wrong — record this as a calibration signal"). This feeds NF-06 (learn from
past mistakes) and NF-08 (framework health).

## What Is Already Anchored

- `know/src/know/ontology.json` defines the 5-level scale with confidence ranges and icons.
- `vision.md` Principle 5: "Every significant decision is recorded, marked with its
  confidence level..." — the vision already demands this; the workflow just hasn't
  implemented it.
- `vision.md` Supporting guideline: "Know how much to trust each piece of knowledge."
- NF-15 (USE_CASES.md v2.4) is the formal UC requirement for this idea.

## Open Questions

- Who owns grade assignment — the producing agent, the reviewing human, or both? Should
  an agent be allowed to self-assign EVIDENCE_BASED, or does that require human confirmation?
- How do we handle composite outputs (an options sheet where Option A is EVIDENCE_BASED
  and Option B is HYPOTHESIS — what is the sheet's grade)?
- Should the confidence sub-loop be mandatory for any output below INFORMED_ESTIMATE, or
  only for Tier 2/3 decisions?
- How do we prevent grade inflation (agents systematically over-claiming confidence to
  avoid triggering the sub-loop)?
- How do we handle retroactive grading of existing artifacts (ADRs, decisions, lessons
  already in state/)?

## Routing

Epic-size workflow improvement. Requires:
- Agent prompt updates for all agents that produce options, decisions, or lessons
  (estimate: 8-12 agents)
- Template updates (options-sheet.md, decision.md, task-spec.md, capture-record.md)
- Reviewer checklist additions (S8)
- S9 Curator additions (grade vs. reality tracking)
- `know` integration alignment (confirm vocabulary parity)

Do NOT include in v1-core core scope — NF-15 provides a deliberate v1-core seed:
decisions and options produced in v1-core carry grades, even if the full sub-loop and
retroactive tooling comes in v1.1.

Route to pre-workflow as the first idea in the improvement backlog after the v1-core
implementation cycle completes.

## Connection to idea-003 and idea-004

- idea-003 (Learn on the way): Epistemic grades make "learn on the way" reliable — you
  can only learn from evidence-graded outputs with known confidence. Without grades,
  learning noise is indistinguishable from learning signal.
- idea-004 (2D altitude × phase model): Grade requirements can be altitude-specific. A
  STRATEGIC altitude decision may require EVIDENCE_BASED or higher; an EXECUTION step
  may tolerate HYPOTHESIS. Altitude metadata (idea-004) × grade requirement creates a
  two-dimensional quality contract.
