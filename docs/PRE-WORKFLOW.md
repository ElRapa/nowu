# nowu Pre-Workflow — Unified Specification v2.1

> **Version:** 2.1 | **Status:** ACTIVE
> **Scope:** P0–P4, producing `state/intake/intake-NNN.md [READY_FOR_S1]`
> **Mode:** Claude Code native

---

## Design Principles

1. **Artifacts are the API.** Agents read and write files. A broken artifact breaks
   the pipeline visibly. A broken conversation fails silently.
2. **Human gates are blocking, not advisory.** A gate that can be skipped is not a gate.
3. **Narrow context beats broad context.** Each agent receives only what it needs.
4. **Problem space before solution space.** Discovery agents are constitutionally
   prohibited from mentioning architecture or solutions.
5. **Traceability is non-negotiable.**
   `idea-NNN → disc-NNN → problem-NNN → epic-NNN → story-NNN → intake-NNN`
6. **Ideas have sizes.** A product idea and a bug report route differently.
7. **Vision is a living document.** Bootstrapped before first use, refreshable anytime.
8. **Feedback loops close the cycle.** S9 re-enters pre-workflow with new knowledge.

---

## Idea Sizes and Routing

| Size | Definition | Mode | Entry point |
|---|---|---|---|
| Bug / Hotfix | Single broken behavior, known module | Lite | P0 → P2 → P4 |
| Story | Single behavior change, fits 1 day | Standard | P0 → P1 → P2 → P4 |
| Epic | 2–5 related stories, 1–2 week slice | Full | P0 → P1 → P2 → P3 → P4 |
| Product / Initiative | Multi-epic, new domain or product | Bootstrap | P0.V → P0.D → P1 → P2 → P3 → P4 |

The **Idea Decomposition Agent** (P0.D) classifies and routes. For Product-size ideas,
it fans out into a Stage Map and queued seed ideas before any discovery work begins.

---

## Product Stages

Products evolve through named stages. The current stage is recorded in `docs/V1_PLAN.md`.

| Stage | Name | Done when |
|---|---|---|
| 0 | Concept | `docs/vision.md` APPROVED, team aligned |
| 1 | Foundation | Core architecture decided, first story shipped |
| 2 | Core Loop | Primary user workflow works end-to-end |
| 3 | Hardening | Test coverage, observability, edge cases handled |
| 4 | Ship | Users can self-serve; deployment fully documented |
| 5 | Growth | Iteration on real user feedback (ongoing) |

Idea Decomposition (P0.D) checks whether an idea is appropriate for the current stage.
Optimisation ideas at Stage 1, or "make it multi-tenant" at Stage 2, are flagged
for parking or deferral — not because they're wrong, but because order matters.

---

## Global Architecture Pass

There are two distinct architecture activities:

- **P3 Architecture Bootstrap (per-epic):** Sized to the current problem/epic, runs whenever mode = Full or Bootstrap and containers may change.
- **Global Architecture Pass (GAP, product-level):** Looks at the **entire** use case catalog and product vision to shape or revise the global C4 L1/L2 and major module boundaries.

GAP is heavier and more strategic. It should not run every cycle.

### When to run GAP

Run a Global Architecture Pass (via gap-chain) when:

- A new product is bootstrapped (Stage 0 → Stage 1), or
- The product stage increases (e.g., Stage 1 → Stage 2 in `V1_PLAN.md`), or
- A large number of new use cases are added for the same product family, or
- Health checks report **RED** on architecture drift for two consecutive runs.

### GAP Inputs

- `docs/vision.md` (approved)
- `docs/V1_PLAN.md` (current stage and steps)
- `docs/USE_CASES.md` (full catalog, not filtered)
- Existing architecture docs: `docs/architecture/context.md`, `docs/architecture/containers.md`
- Existing decisions: `docs/DECISIONS.md`, `docs/architecture/adr/*`
- Recent health reports: `state/health/arch-*.md` (optional)

### GAP Outputs

- Updated `docs/architecture/context.md` and `docs/architecture/containers.md` (global L1/L2)
- One or more ADRs capturing structural decisions or reversals
- A short summary file: `state/arch/global-pass-YYYY-MM-DD.md` that records:
  - Why GAP was run (trigger)
  - What changed at L1/L2
  - Any new constraints for per-epic P3 work

### Relationship to P3

- GAP works **above** any specific NNN. It changes the global architecture.
- P3 Architecture Bootstrap for a given NNN must:
  - Read the current global architecture docs
  - Respect GAP constraints, unless it explicitly proposes an ADR to change them

Think of GAP as reshaping the "city plan"; P3 is about placing or extending individual buildings.

---

## Architecture Overview

```
HEALTH CHECKS (run anytime — especially at session start if >7 days)
  /health-check vision | architecture | goals | all
        |
        v  (findings inform next P0 or pre-workflow entry)

P-1: Mode Selection
  Bug → Lite   Story → Standard   Epic → Full   Product → Bootstrap

P0: Signal Capture
  P0.V  Vision Bootstrap Agent    [if vision.md missing or stale]
  P0.1  Idea Note                 [Human, 5–10 min]
  P0.D  Idea Decomposition        [Agent → NNN-decomp.md]
  P0.2  Vision Alignment Check    [Human, 2 min]

P1: Discovery                     [Skip in Lite]
  P1.1  Research Run              [Discovery Agent → disc-NNN-research.md]
  P1.2  Perspective Interview     [Interview Agent → problem-NNN.md DRAFT]
  P1.3  Problem Statement Gate    [HUMAN GATE → status: APPROVED]

P2: Story Mapping
  P2.1  Epic + Story Draft        [Story Mapper → epic-NNN.md + story-NNN-*.md]
  P2.2  Story Review Gate         [HUMAN GATE → status: APPROVED]

P3: Architecture Bootstrap        [Skip in Lite and Standard]
  P3.1  Constraint Check          [Agent → NNN-constraint-check.md]
  P3.2  Architecture Bootstrap    [Agent → arch-pass-NNN.md]
  P3.3  ADR Creation              [Human, per flagged decision]

P4: Readiness Assembly
  P4.1  Readiness Check           [Agent → NNN-readiness.md; BLOCKS if incomplete]
  P4.2  Intake Brief Assembly     [Agent → intake-NNN.md DRAFT_FOR_REVIEW]
  P4.3  Human Final Approval      [Human → status: READY_FOR_S1]
                    |
                    v
        state/intake/intake-NNN.md [READY_FOR_S1]
                    |
                    v
           S1 → S2 → S3 → S4 → S5 → S6/S7 → S8 → S9
                    |
          next_cycle_trigger:
          CONTINUE | ARCH_PIVOT | PRODUCT_PIVOT | COMPLETE
                    |
           re-enters pre-workflow at appropriate phase
```

---

## Mode Selection (P-1)

Run this checklist before starting any work:

```
Does docs/vision.md exist and have status: APPROVED?          YES / NO
Does docs/USE_CASES.md have relevant UC-NNN entries?          YES / NO
Does docs/architecture/containers.md exist and look current?  YES / NO
Is this idea smaller than 1 day of work?                      YES / NO
Is this a known feature on a project with active backlog?     YES / NO
```

| Pattern | Mode | Phases | Typical duration |
|---|---|---|---|
| All YES | Lite | P0 → P2 → P4 | 30–90 min |
| Mixed (2–3 YES) | Standard | P0 → P1 → P2 → P4 | 90–150 min |
| All/most NO | Full | P0 → P1 → P2 → P3 → P4 | 2–4 h |
| New product, no docs | Bootstrap | P0.V → full | 4–8 h |

Record mode before starting: create `state/pre-workflow/NNN-mode.md` from `templates/pre-workflow/mode-record.md`.

---

## Artifact: `docs/vision.md`

Vision is the highest-level document in the system. Every other artifact traces to it.
It is created by the Vision Bootstrap Agent (P0.V) via interview, then edited and approved by the human.

**Required sections:**

```markdown
# Vision: [Product Name]

## Status
status: DRAFT | APPROVED
last_approved: YYYY-MM-DD
version: N

## One-Liner
[One sentence: what this product does and for whom]

## Problem We Solve
[2–3 sentences: the core pain, who experiences it, why current solutions fail]

## Who We Serve
### Primary Persona: [Name]
- Who they are:
- What they struggle with:
- What success looks like:

### Secondary Persona (optional): [Name]
[same structure]

## What Success Looks Like (Success Horizons)
[3–5 measurable outcomes at 3-month, 6-month, 12-month horizons]
- 3 months: [outcome]
- 6 months: [outcome]
- 12 months: [outcome]

## What We Are NOT
[Explicit non-goals — things this product will deliberately never do]
- Not a [X]
- Not for [Y]

## Current Stage
stage: 0 | 1 | 2 | 3 | 4 | 5
stage_name: Concept | Foundation | Core Loop | Hardening | Ship | Growth

## Revision History
| Date | Changed by | What changed |
|---|---|---|
```

**Freshness rule:** Run `/health-check vision` if >90 days since `last_approved`, or whenever
active work feels misaligned with stated goals. Vision should be refreshed, not silently drift.

---

## Artifact: `docs/V1_PLAN.md`

V1_PLAN is the product roadmap at stage resolution. It is created by the human
after vision is approved (typically during or after Bootstrap mode P0.D).

**Required sections:**

```markdown
# V1 Plan: [Product Name]

## Status
status: ACTIVE | PAUSED | COMPLETE
current_stage: [0–5]
current_stage_name: [Concept | Foundation | ...]
last_updated: YYYY-MM-DD

## Stage Goals
### Stage 1 — Foundation
Goal: [1–2 sentences]
Done when: [measurable exit criterion]
Epics:
- epic-001: [title]
- epic-002: [title]

### Stage 2 — Core Loop
[same structure]

## Active Epic
epic_id: epic-NNN
title: [title]
status: IN_PROGRESS

## Parked / Future
- [idea or epic title] — parked because [reason]
```

**Who creates it:** Human, after reviewing the Stage Map output from `idea-decomposition` (P0.D).
The decomposition agent produces a Stage Map draft; the human authors V1_PLAN.md from it.

---

## Phase P0 — Signal Capture

**Purpose:** Structure the raw idea before it mutates.
**Actors:** Human (P0.1, P0.2), Vision Bootstrap Agent (P0.V), Decomposition Agent (P0.D)

### P0.V — Vision Bootstrap (conditional)

**Triggered when:** `docs/vision.md` is missing, status is not APPROVED,
or `last_approved` is >90 days ago.

**Agent:** `.claude/agents/vision-bootstrap.md`
**Inputs:** none — interview-based (5 focused questions about product, personas, outcomes)
**Output:** `docs/vision.md` [DRAFT]

Human must edit and set `status: APPROVED` before any other P0 work begins.
The Vision Bootstrap Agent does not touch any other files.

### P0.1 — Idea Note [Human, 5–10 min]

Create `state/ideas/idea-NNN.md` using `templates/pre-workflow/idea.md`.

Required fields:
- Raw signal (1–5 sentences, unpolished)
- Source (personal frustration / user feedback / market observation / technical opportunity)
- Appetite guess (Tiny <2h / Small <1d / Medium 2–3d / Large 1w+)
- Why now (one sentence: why does this matter at this moment)
- Related context (optional): related idea-NNN, UC-NNN, D-NNN

### P0.D — Idea Decomposition [Decomposition Agent]

**Agent:** `.claude/agents/idea-decomposition.md`
**Inputs:** `state/ideas/idea-NNN.md`, `docs/vision.md`, `docs/V1_PLAN.md` (if exists)
**Output:** `state/pre-workflow/NNN-decomp.md`

The agent:
1. Classifies idea size (Bug / Story / Epic / Product)
2. Identifies current product stage from V1_PLAN.md (or notes it's missing)
3. Checks if idea is appropriate for the current stage
4. For Product-size: produces a Stage Map (Stage 0–5 sketch) and queues 2–5 seed
   ideas as `state/ideas/idea-NNN-a.md`, `idea-NNN-b.md`, etc.
5. Recommends pre-workflow mode (Lite / Standard / Full / Bootstrap)
6. Flags if V1_PLAN.md is missing (human must create it before proceeding with Product mode)

Human reviews and approves routing before any further steps.

### P0.2 — Vision Alignment Check [Human, 2 min]

Read `docs/vision.md`. Answer: does this idea serve the current vision?

- **YES** → proceed
- **NO** → park in `state/ideas/parked/idea-NNN.md` with one-line reason. Stop.
- **UNSURE** → vision needs refresh. Run P0.V first, then re-check.

---

## Phase P1 — Discovery

**Purpose:** Understand the problem deeply before any solution thinking.
**Actors:** Discovery Agent (P1.1), Perspective Interview Agent (P1.2), Human (P1.3 gate)

### P1.1 — Research Run [Discovery Agent]

**Agent:** `.claude/agents/discovery-agent.md`
**Inputs:** `state/ideas/idea-NNN.md`, `docs/vision.md`
**Output:** `state/discovery/disc-NNN-research.md`

Required sections: problem context, known approaches (3–5), personas (max 2),
outcome goals (3–5), implicit assumptions check (MANDATORY), risks and unknowns,
related prior work.

**Hard constraint:** Zero solution language. Forbidden words: implement, build, create,
API, database, architecture, component, service, framework, library. If a goal implies
a solution, flag it in the implicit assumptions check.

### P1.2 — Perspective Interview [Interview Agent]

**Agent:** `.claude/agents/perspective-interview.md`
**Inputs:** `state/discovery/disc-NNN-research.md`, `state/ideas/idea-NNN.md` (context)
**Output:** `state/problems/problem-NNN.md` [DRAFT]

The agent plays three roles sequentially:
1. **User Advocate** (3 questions): validates pain points, personas, success criteria
2. **Skeptic** (3 questions): challenges assumptions, probes for hidden complexity
3. **Scope Enforcer** (2 questions): clarifies appetite, extracts explicit out-of-scope

Questions are short — multiple-choice or 1–2 sentence answers. No essays.
The agent synthesizes 8 answers into a complete `problem-NNN.md` draft.
The human edits the draft rather than writing from scratch.

### P1.3 — Problem Statement Gate [HUMAN GATE 🛑]

Human edits `state/problems/problem-NNN.md`, sets `status: APPROVED`.

**Gate checklist (all must pass):**
- [ ] Core problem statement has no solution language
- [ ] Appetite is set with rationale
- [ ] Out of scope section is non-empty and explicit
- [ ] Success criteria are measurable (observable states or numbers)
- [ ] All assumption FLAGs from P1.1 §5 are resolved

---

## Phase P2 — Story Mapping

**Purpose:** Decompose the validated problem into implementation-ready stories.
**Actors:** Story Mapper Agent (P2.1), Human (P2.2 gate)

### P2.1 — Epic and Story Draft [Story Mapper Agent]

**Agent:** `.claude/agents/story-mapper.md`
**Inputs:** `state/problems/problem-NNN.md`, `docs/USE_CASES.md`,
           `state/discovery/disc-NNN-research.md`
**Outputs:** `state/epics/epic-NNN.md` + `state/stories/story-NNN-*.md` [DRAFT]

Each story requires: As/I want/So that statement (using validated persona),
appetite, 2–5 Given/When/Then ACs (observable outcomes), out of scope,
architecture signals (hedged: "likely touches", "may require"),
validation trace table (AC → UC-NNN → persona → success criterion).

Epic requires: summary, UC mapping table, story index with appetite + priority,
Scope Hammer Log (cut stories with reason — mandatory, never empty).

### P2.2 — Story Review Gate [HUMAN GATE 🛑]

Human applies scope hammer. Sets `status: APPROVED` on passing stories.

**Scope hammer actions:**
- **Split:** story too large → divide into story-NNN-001 and story-NNN-002
- **Cut:** doesn't fit appetite → move to scope hammer log in epic
- **Clarify:** AC is ambiguous → rewrite with observable "Then" clause
- **Merge:** two trivially small stories → combine

**Gate checklist per story (all must pass):**
- [ ] Uses validated persona from problem-NNN.md
- [ ] Each AC: Given/When/Then format, observable "Then" clause
- [ ] No AC describes implementation (no "the function should…")
- [ ] Appetite realistic for solo dev in current stage
- [ ] Every AC has UC-NNN link in validation trace
- [ ] Out of scope section is non-empty

---

## Phase P3 — Architecture Bootstrap

**Purpose:** Establish or update architectural context before implementation begins.
**Skip if:** Mode = Lite or Standard AND `docs/architecture/containers.md` is current.

### P3.1 — Constraint Check [Agent]

**Agent:** `.claude/agents/constraint-check.md`
**Inputs:** All approved `state/stories/story-NNN-*.md`, `docs/architecture/containers.md` (if exists),
            `docs/DECISIONS.md` (if exists)
**Output:** `state/pre-workflow/NNN-constraint-check.md`

Results: CLEAR | CONFLICTS_FOUND
If CONFLICTS_FOUND: human resolves all CONFLICT entries before P3.2 starts.

### P3.2 — Architecture Bootstrap [Agent]

**Agent:** `.claude/agents/architecture-bootstrap.md`
**Inputs:** `state/problems/problem-NNN.md`, approved stories, `state/pre-workflow/NNN-constraint-check.md`,
            `docs/vision.md` (scope boundary reference),
            `docs/architecture/context.md` (if exists), `docs/architecture/containers.md` (if exists),
            `docs/architecture/adr/` (if exists), 
**Output:** `state/arch/arch-pass-NNN.md`

Mode: NEW_PROJECT | NEW_CAPABILITY | FEATURE
Produces: C4 L1/L2 delta (Mermaid), affected components table, ADR candidates,
S2 Conflict Protocol section, hard constraints for S2, open questions for S2.

### P3.3 — ADR Creation [Human]

For each flagged ADR candidate, human authors `docs/architecture/adr/ADR-NNN-title.md`
using `templates/adr.md`. ADRs are binding on all downstream steps and agents.

## When to load the full USE_CASES.md

The architecture-bootstrap agent loads the full UC catalog ONLY when mode = BOOTSTRAP
or mode = FULL and the product stage is transitioning (e.g., Stage 1 → Stage 2).

Purpose: ensure C4 L1/L2 containers are sized for the full product horizon, not just
the current epic. This prevents premature narrowing of module boundaries.

In all other modes (STANDARD, LITE): the architecture-bootstrap agent loads only the
USE_CASES referenced in the current stories (the UC-IDs from the validation_trace),
not the full catalog.

---

## Phase P4 — Readiness Assembly

**Purpose:** Final completeness gate. Produce `intake-NNN.md`.
**Agents:** Readiness Checker (P4.1–P4.2), Human (P4.3)

### P4.1 — Readiness Check [Agent]

**Agent:** `.claude/agents/readiness-checker.md`
**Inputs:** All P0–P3 artifacts for this NNN (idea, disc, problem, epic, stories, arch-pass,
            constraint check, mode record)
**Output:** `state/pre-workflow/NNN-readiness.md`

If `status: BLOCKED`: pipeline halts. Every FAIL listed with specific, actionable fix instruction.
Agent does NOT create `intake-NNN.md` when BLOCKED.

### P4.2 — Intake Brief Assembly [Agent]

Runs only when `NNN-readiness.md` has `status: READY`.
**Output:** `state/intake/intake-NNN.md` [DRAFT_FOR_REVIEW]

Assembled from verified artifacts. Human does not write this file.

### P4.3 — Human Final Approval [Human]

Human reviews `state/intake/intake-NNN.md`.
Sets `status: READY_FOR_S1`. This is the only field the human writes in this file.

S1 will not process an intake brief without `status: READY_FOR_S1`.

---

## Health Checks

Health check agents validate key documents without modifying them.
Run at session start if >7 days since last run, or when something feels off.

| Command | Agent | Checks | Output |
|---|---|---|---|
| `/health-check vision` | `health-vision.md` | Freshness, completeness, active work alignment | `state/health/vision-YYYY-MM-DD.md` |
| `/health-check architecture` | `health-architecture.md` | C4 accuracy, ADR coverage, implementation drift | `state/health/arch-YYYY-MM-DD.md` |
| `/health-check goals` | `health-goals.md` | Story/backlog alignment with vision, staleness | `state/health/goals-YYYY-MM-DD.md` |
| `/health-check all` | All three | All above | All three reports |

Status: **GREEN** (no issues) / **YELLOW** (minor drift, address soon) / **RED** (blocking — address before next cycle).

### Vision Check (`health-vision`) examines:
- `status: APPROVED` present
- `last_approved` within 90 days (assumption: configurable per project)
- Active stories' personas match vision's defined personas
- Active epics' outcome goals traceable to vision success horizons
- "What We Are NOT" still holds given current work

### Architecture Check (`health-architecture`) examines:
- `containers.md` reflects modules that actually exist in `src/`
- All ADRs in `adr/` are referenced in `DECISIONS.md`
- No new modules in `src/` without corresponding architecture docs
- No superseded decisions still referenced as active

### Goals Check (`health-goals`) examines:
- All APPROVED stories trace to ≥1 UC-NNN that traces to vision
- Stories in `state/stories/` with `APPROVED` but no corresponding intake
- Intakes `READY_FOR_S1` older than 14 days (staleness risk)
- Active epic scope still fits stated appetite from `problem-NNN.md`

---

## S9 Feedback Loop

S9 Capture sets `next_cycle_trigger` in the intake record:

| Value | Meaning | Pre-workflow re-entry |
|---|---|---|
| `CONTINUE` | Next story from same epic | P2.1 (problem-NNN already approved) |
| `ARCH_PIVOT` | Architecture assumptions proved wrong | P3.1 (re-run constraint check) |
| `PRODUCT_PIVOT` | Problem definition changed | P1.1 (new discovery run) |
| `COMPLETE` | Epic / product goal met | Pre-workflow closed for this cycle |

The curator agent sets this field based on what the review surfaced.
