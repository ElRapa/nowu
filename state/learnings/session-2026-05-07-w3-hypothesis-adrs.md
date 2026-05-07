---
artifact_type: SESSION_LEARNINGS
session: "W3 — Hypothesis ADRs + Perplexity Review Integration"
created_at: 2026-05-07
session_type: "architecture"
source_artifacts:
  - docs/architecture/adr/ADR-0007-session-continuity-protocol.md
  - docs/architecture/adr/ADR-0008-knowledge-atom-model.md
  - docs/architecture/adr/ADR-0009-orchestration-protocol.md
  - docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md
  - docs/DECISIONS.md (D-021)
  - docs/STAGED-PLAN.md (W3 → DONE, W3.5 added)
  - state/arch/SYNTHESIS-001.md (dependency graph refined)
  - docs/architecture/ARCHITECTURE-VISION.md (user space note added)
  - state/arch/session-learnings-synthesis-2026-05-06.md (Perplexity addendum)
  - state/arch/2026-05-07_1_review_synthesis001+architecture-vision_perplexity.md
purpose: "Capture decisions, insights, and process learnings from W3 ADR writing and Perplexity review evaluation"
---

# Session Learnings: W3 — Hypothesis ADRs + Perplexity Review Integration

## What Was Done

- Evaluated Perplexity review of SYNTHESIS-001 and Architecture Vision (3 gaps identified, all valid)
- Applied review refinements: dependency graph, user space boundary note, W3.5 fitness functions
- Wrote 4 hypothesis ADRs in dependency order: ADR-0008 → ADR-0010 → ADR-0007 → ADR-0009
- Updated STAGED-PLAN (W3 DONE), DECISIONS.md (D-021), session-learnings, AGENTS.md
- Pushed to main (5 commits total including prior session work)

## Decisions Made

### D-SESS-01: Adopt know's KnowledgeAtom as-is, don't reinvent

**Decision:** ADR-0008 declares the existing `know` module's `KnowledgeAtom` as the canonical
knowledge unit. No separate atom model in nowu core.

**Context:** Two options existed: (a) adopt the existing schema from `know`, or (b) define a
nowu-specific schema in `core/contracts/`. D-006 already decided to treat `know` as the
external memory system of record, which made (b) a contradiction.

**Why it matters:** Prevents schema divergence between `know` and nowu. Any future schema
change happens in one place. ADR-0008 becomes a documentation decision (formalize what exists)
rather than a design decision (invent something new).

---

### D-SESS-02: Workflow artifacts and knowledge atoms are SEPARATE concepts

**Decision:** Markdown artifacts in `state/` are agent handoff interfaces (transient, step-scoped).
Knowledge atoms in `know` are durable memory (persistent, cross-cycle). They serve different
purposes and should not be conflated.

**Context:** It was tempting to make everything an atom (including intake briefs, task specs, etc.).
But workflow artifacts carry status metadata (DRAFT → APPROVED), approval gates, and handoff
semantics that would pollute the knowledge graph. And atoms carry lifecycle metadata (decay,
grades, provenance) that would pollute workflow files.

**Why it matters:** Clear boundary prevents the "god object" anti-pattern where one data type
tries to serve both workflow orchestration and durable knowledge management.

---

### D-SESS-03: Step-boundary checkpointing is sufficient for v1-core

**Decision:** ADR-0007 checkpoints at step boundaries (S1→S2, S5→S6, etc.), not mid-step.
Recovery tolerates re-running one step from its input artifact.

**Context:** Mid-step checkpointing would require serializing partial agent state, which is
complex and fragile. Steps are bounded (< 4 hours, typically < 30 minutes), and input
artifacts are immutable once written. Re-running a step is cheap.

**Why it matters:** Eliminates an entire category of complexity (partial state serialization)
while accepting a small cost (re-running at most one step on crash).

---

## Process Insights

### Insight 1: External review catches structural gaps that self-review misses

**Observation:** The Perplexity review found the ADR-0007→ADR-0008 dependency that was
stated in prose but missing from the dependency graph. It also identified the kernel/user
space gap in the OS analogy. Both were "obvious in hindsight" — the kind of thing that's
invisible when you wrote the original document.

**Type:** workflow-process

**Implication:** Always run SYNTHESIS and Architecture Vision artifacts through an external
reviewer (Perplexity, Oracle, or human) before writing ADRs that depend on them. External
review is a quality gate, not optional.

---

### Insight 2: Grounding ADRs in existing code prevents aspirational architecture

**Observation:** ADR-0008 was straightforward because `know` already implements the atom
model. The ADR became "formalize what exists and clarify what's missing" rather than
"invent from scratch." ADR-0010 similarly grounded in `know`'s existing EpistemicGrade
enum, ontology.json confidence ranges, and curator auto-downgrade logic.

**Type:** domain-insight

**Implication:** Before writing any ADR, check whether the `know` module (or another existing
module) already implements the concept. If yes, the ADR's job is to adopt and extend — not
to reinvent. This dramatically reduces ADR writing time and prevents fantasy architecture.

---

### Insight 3: Dependency-ordered ADR writing creates natural forward references

**Observation:** Writing ADR-0008 first made ADR-0010 easier (grades live on atoms — already
defined). ADR-0010 made ADR-0007 easier (checkpoints carry grades — already defined). ADR-0007
made ADR-0009 easier (orchestrator uses checkpoints — already defined). Each ADR could
reference the previous one as a settled dependency.

**Type:** workflow-process

**Implication:** Always write ADRs in dependency order, even when they're all HYPOTHESIS grade.
The forward reference structure makes each successive ADR more grounded. Writing them in
arbitrary order would create circular references and unresolved assumptions.

---

### Insight 4: Two-layer architecture (machine + human) recurs across concerns

**Observation:** ADR-0007 (continuity) uses two layers: machine checkpoint (JSON, for agents)
and human bookmark (YAML, for orientation). ADR-0009 (orchestration) uses two layers: typed
handoff envelope (machine-parseable metadata) and step-specific body content (human-readable).
This pattern — "structured machine layer + readable human layer" — matches D-001's philosophy.

**Type:** domain-insight

**Implication:** When designing any nowu interface, default to two layers: a structured machine
layer for programmatic access and a human-readable layer for inspection. This is the
architectural expression of P3 (Inspectability > Convenience).

---

## Anti-Patterns Observed

### Anti-Pattern 1: Writing ADRs without checking existing implementation

**Temptation:** "I'll design the knowledge atom model from first principles based on
the SYNTHESIS themes."

**Reality:** The `know` module already has a KnowledgeAtom with 20+ fields, an EpistemicGrade
enum, lifecycle management, and curator logic. Designing from scratch would produce a
competing model that either duplicates `know` or contradicts it. Always check existing
code first.

### Anti-Pattern 2: Overscoping hypothesis ADRs

**Temptation:** "ADR-0008 should define every atom type, every lifecycle transition,
every cross-project query pattern, and the full extension mechanism."

**Reality:** Hypothesis ADRs are "deep enough for agents to follow, shallow enough to
be wrong" (D-017). Overscoping produces a 30-page ADR that's too detailed to be wrong
in useful ways. ADR-0008 defines the schema, lifecycle states, and cross-project scoping
— and explicitly defers domain extension to ADR-0011.

### Anti-Pattern 3: Treating dependency graph as sequential-only

**Temptation:** "ADR-0008 → ADR-0010 → ADR-0007 → ADR-0009 must be written strictly
in sequence."

**Reality:** The Perplexity review identified that ADR-0010 and ADR-0007 can be written
in parallel (both depend on ADR-0008 but not on each other). Treating a dependency graph
as a linear sequence misses parallelism opportunities. The write ORDER happened to be
sequential, but the DEPENDENCY is a DAG, not a chain.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| ADR-0008 | `docs/architecture/adr/ADR-0008-knowledge-atom-model.md` | PROPOSED (HYPOTHESIS) | Canonical atom schema, lifecycle, scoping |
| ADR-0010 | `docs/architecture/adr/ADR-0010-epistemic-grade-assignment.md` | PROPOSED (HYPOTHESIS) | Grade assignment, propagation, decay rules |
| ADR-0007 | `docs/architecture/adr/ADR-0007-session-continuity-protocol.md` | PROPOSED (HYPOTHESIS) | Checkpoint schema, recovery protocol |
| ADR-0009 | `docs/architecture/adr/ADR-0009-orchestration-protocol.md` | PROPOSED (HYPOTHESIS) | Handoff contract, state machine, failure recovery |
| D-021 | `docs/DECISIONS.md` | ACCEPTED | W3 completion decision |
| STAGED-PLAN update | `docs/STAGED-PLAN.md` | ACTIVE | W3 DONE, W3.5 added |
| Review integration | Multiple files | DONE | Perplexity insights applied |

## What Should Happen Next

1. **Execute W3.5**: Write minimal fitness functions for ADR-0008 (atom schema validation)
   and verify F2 (import boundaries) still passes. Run quality suite.
2. **Execute W4**: Select first intake for S1-S9 (recommend a small NF UC like NF-01 or NF-07).
   Run full cycle using hypothesis ADRs as architectural context.
3. **Validate ADR hypotheses**: After W4, check which ADR assumptions held and which need
   refinement. Promote validated ADRs from HYPOTHESIS to INFORMED_ESTIMATE.
4. **External review of ADRs**: Consider running ADR-0008..0010 through Perplexity before
   W4, same way SYNTHESIS-001 was reviewed. External review catches structural gaps.
5. **Unstaged files**: Several files remain uncommitted (BOOTSTRAP.md, CLAUDE.md,
   FILE-STRUCTURE.md, skill files, design research docs). These should be reviewed and
   committed separately — they are from prior session work, not this W3 session.
