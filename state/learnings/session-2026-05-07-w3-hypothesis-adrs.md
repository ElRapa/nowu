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

## Addendum: Perplexity W3 Output Evaluation (2026-05-07, session 2)

### Review Source

`state/arch/2026-05-07_2_perplexity_review_W3.md` — two-part review:
1. **Mock workflow traversal**: Full 5×9 model validation from human prompt to shipped code
2. **W3 deliverable evaluation**: Rating A+ (9/10), 4 minor gaps identified

### Insights Applied

| # | Insight | Valid? | Action |
|---|---------|--------|--------|
| R1 | Frontmatter inconsistency (`source_themes` vs `source_synthesis`) | ❌ False positive | Verified: all 4 ADRs already have both keys |
| R2 | ADR-0009 missing ADR-0006 cross-reference | ❌ False positive | Verified: ADR-0009 Related section already lists ADR-0006 (line 284) |
| R3 | ADR-0008 truncation | ❌ Search artifact | Verified: file is complete (190 lines, Related section intact) |
| R4 | No `depended_on_by` backlinks | ❌ False positive | Verified: ADR-0008 already has `depended_on_by` (lines 188-190) |
| M1 | ADR fills GOAL→UC gap for cross-module work | ✅ Valid | Noted for W4 routing — skip condition documented |
| M2 | Grade thresholds vary by altitude | ⚠️ Conflicts with D-017 | Deferred to W6 (calibration) |
| M3 | Research sub-loop concept | ✅ Valid (v1) | Recorded for Level 2 implementation |
| M4 | Security in EVALUATION, not separate phase | ✅ Valid | Recorded for future ATAM-lite template |

### Additional Process Insights from W3 Evaluation

#### Insight 5: External review of OUTPUT validates depth calibration

**Observation:** The Perplexity evaluation confirmed our hypothesis ADRs are at the right
depth — "implementation-ready specifications" not "vague architectural statements." This
validates D-017's "deep enough for agents to follow, shallow enough to be wrong" criterion
empirically. The reviewer independently concluded the ADRs are "production-grade hypothesis
architecture."

**Type:** workflow-process

**Implication:** D-017's depth criterion is well-calibrated for HYPOTHESIS grade. After W4,
we can check whether agents can actually implement from these specs — that's the definitive
validation.

---

#### Insight 6: External reviewers on truncated context produce false positive "gaps"

**Observation:** All 4 "minor gaps" identified by the Perplexity reviewer (frontmatter
inconsistency, missing cross-refs, truncation, missing backlinks) were false positives.
The ADRs already had all the things the reviewer said were missing. The reviewer was working
from truncated search result snippets, not full file content.

**Type:** workflow-process

**Implication:** When soliciting external reviews, provide FULL artifacts — not search
snippets or partial views. Alternatively, ask reviewers to qualify confidence in their
"gap" findings. A review that produces 4 false positives on minor points still validated
the overall architecture (A+ rating) — the structural assessment was correct even when
the detail checks were wrong.

---

#### Insight 7: Altitude-based routing rules belong in the orchestrator

**Observation:** The mock workflow traversal revealed that cross-module work REQUIRES the
ARCHITECTURE altitude (ADR is the "global solution"), while single-module work can skip
directly from PRODUCT to DELIVERY. This is a routing decision the orchestrator should make
based on the intake's `affected_modules` field.

**Type:** domain-insight

**Implication:** ADR-0009's orchestrator state machine should eventually support altitude
skipping for single-module intakes. Not needed for v1-core (first intake will be small),
but critical for v1 when multiple intake types coexist.

---

#### Insight 8: Bidirectional traceability (backlinks) catches orphan dependencies

**Observation:** The reviewer identified that ADR-0008 should list `depended_on_by:
[ADR-0007, ADR-0010, ADR-0009]`. Without backlinks, if ADR-0008 is amended, there's no
machine-readable way to know which downstream ADRs are affected. This is the same problem
Git solves with `git log --follow` vs forward references.

**Type:** workflow-process

**Implication:** All ADRs should carry both `depends_on` and `depended_on_by` in frontmatter.
This creates a bidirectional dependency graph that enables impact analysis when amending
hypothesis ADRs.

---

## Addendum: Perplexity+Human Review #3 — ADR Refinements (2026-05-07, session 3)

### Review Source

`state/arch/2026-05-07_3_perplexity+human_review_ADRs.md` — three questions from human,
evaluated by Perplexity with concrete recommendations.

### Insights Applied

| # | Question | Valid? | Action |
|---|----------|--------|--------|
| Q1 | Multi-session support in ADR-0007 | ✅ Valid | Added "Known Limitations" section to ADR-0007 — v1-core simplification acknowledged, session types + storage hierarchy defined for v1 |
| Q2 | Architecture docs becoming atoms | ✅ Valid | Added "Artifact-to-Atom Extraction" section to ADR-0008 — docs produce atoms, they don't become atoms. S9 curator is the extraction point. |
| Q3 | OPTIONS/DECISION cycle for agent creation | ✅ Valid for high-impact work | Recorded as process insight — apply full cycle for orchestrator and other high-impact agents, skip for routine work |

### Additional Process Insights from Review #3

#### Insight 9: Hypothesis ADRs need explicit "Known Limitations" sections

**Observation:** ADR-0007's single-session assumption was only implicit — the ADR never
stated "this is a simplification." The human correctly identified the gap through real
usage thinking ("what if we have multiple open sessions?"). Adding a "Known Limitations"
section makes simplifications explicit and prevents future readers from assuming the ADR
covers all cases.

**Type:** workflow-process

**Implication:** Every hypothesis ADR should have a "Known Limitations" section listing
v1-core simplifications. This serves as a built-in refinement backlog — each limitation
is a candidate for v1 extension. It also prevents the anti-pattern of assuming HYPOTHESIS
means "complete design" rather than "minimum viable architecture."

---

#### Insight 10: The artifact→atom extraction pattern is a key architectural concept

**Observation:** The distinction between artifacts (files, full documents) and atoms
(queryable facts extracted from those documents) is fundamental to how nowu manages
knowledge. Documents don't *become* atoms — they **produce** atoms. S9 curator is the
extraction point. This pattern was implicit in ADR-0008 but making it explicit (with a
concrete extraction table) clarifies the boundary for implementation.

**Type:** domain-insight

**Implication:** When writing S9 curator logic, this extraction table becomes the
implementation spec. Each artifact type has a defined number of atoms to extract and
their KnowledgeTypes. This is concrete enough to implement from.

---

#### Insight 11: Full OPTIONS/DECISION cycle improves quality for high-impact artifacts

**Observation:** The current process writes agents and ADRs reactively (one approach,
justified after the fact). NF-13 requires "at least 2 viable approaches before committing."
Applying the full cycle at ARCHITECTURE altitude (always) and DELIVERY altitude (for agents
and workflows) would increase quality at a 2-3x time cost.

**Type:** workflow-process

**Implication:** When creating the orchestrator agent (the `flow` module router), use the
full INTAKE→ANALYSIS→OPTIONS→DECISION→IMPLEMENTATION→VERIFICATION cycle. This is the
highest-impact agent in the system (D-019) — it deserves deliberate design, not reactive
implementation.

---

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
