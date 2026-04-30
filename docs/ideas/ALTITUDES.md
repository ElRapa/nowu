---
title: ALTITUDES — Same Steps at Different Levels
version: 1.0
status: ACTIVE
type: framework-pattern
---

# ALTITUDES — The Universal Workflow Pattern

> *The same eight steps, at every level of resolution.*
> *Artifacts and agents change. The loop does not.*

---

## 1. Why This Exists

Working on a product long enough, a pattern becomes visible: you do the
same things over and over, just at different scales. You capture a signal,
understand the context, research it, shape it, make a decision, build,
check, and reflect. Whether "it" is a product vision, a domain expansion,
a feature epic, or a single bug fix — the loop is the same.

This document names that pattern, maps it across the three main altitudes
in the nowu workflow, and shows how each altitude derives its concrete
workflow from the generic loop.

---

## 2. Reference Models

This pattern is not invented from scratch. Several established frameworks
independently converge on the same structure:

| Model | Loop structure | Altitude coverage |
|---|---|---|
| **Brian Foote's Fractal Model** (1994) | Prototype → Expansion → Consolidation, repeated at every level | Class → Framework → Product |
| **SAFe Portfolio / ART / Team** | Same PI planning cadence at every level, different timescales | Portfolio → Solution → Team |
| **Wardley Mapping** | Anchor → Orient → Discover → Act, updated per horizon | Strategy → Capability → Feature |
| **Iterative SDLC** | Requirements → Design → Build → Test → Reflect, per iteration | Product → Release → Sprint |
| **Double Diamond (Design Council)** | Discover → Define → Develop → Deliver, applied recursively | Product → Feature → Task |
| **OODA Loop (Boyd)** | Observe → Orient → Decide → Act | Applied at any decision timescale |

The nowu workflow synthesises these into a single 8-step generic loop,
then applies it at three named altitudes.

---

## 3. The Generic Loop (Altitude-Neutral)

```
┌─────────────────────────────────────────────────────────┐
│                    THE GENERIC LOOP                     │
│                                                         │
│  1. SIGNAL    Detect or receive a change trigger        │
│  2. ORIENT    Understand current state and context      │
│  3. DISCOVER  Research the problem space                │
│  4. SHAPE     Decompose, slice, bound, set appetite     │
│  5. DECIDE    Choose approach; commit; record           │
│  6. BUILD     Implement / create / draft                │
│  7. VERIFY    Check against acceptance criteria         │
│  8. CAPTURE   Reflect, route, close or continue        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

Each step produces one or more artefacts. Artefacts are the API between
steps (Principle 1: Artifacts are the API). No step reads a previous
step's reasoning — it reads its output file.

---

## 4. The Three Altitudes

### Altitude metaphor

Think of a helicopter. At high altitude you see cities, coastlines, and
mountain ranges. The same helicopter at mid altitude shows neighbourhoods
and roads. At low altitude you see individual houses and people.

The terrain does not change. The resolution does.

| Altitude | Name | Scale | Cadence | Trigger |
|---|---|---|---|---|
| **HIGH** | Product / Stage | Entire product, all UCs, global architecture | Months (stage change) | Stage advance, GAP trigger, major scope shift |
| **MID** | Epic / Problem | One bounded problem, 1-3 stories | 1-3 weeks | Idea approved, pre-workflow P0-P4 |
| **LOW** | Story / Task | One user-facing behaviour, <1 day | Hours | Intake READY_FOR_S1, S1-S9 |

---

## 5. Loop Mapping per Altitude

### HIGH Altitude — Product / Stage Loop

| Generic step | nowu activity | Primary artefact | Actor |
|---|---|---|---|
| 1. SIGNAL | stage change, major UC wave, RED arch checks | gap-trigger.md | gap-detector (auto) |
| 2. ORIENT | review vision, plan, last GAP | vision.md, V1_PLAN.md | gap-detector reads these |
| 3. DISCOVER | UC-to-container analysis, structural risks | global-pass-YYYY-MM-DD.md (PROPOSED) | gap-analyst |
| 4. SHAPE | decide container structure, ADR candidates | global-pass-YYYY-MM-DD.md (APPROVED by human) | human review |
| 5. DECIDE | author ADRs, approve container changes | ADR-NNN-*.md | human |
| 6. BUILD | update context.md, containers.md, ADR stubs | updated context.md + containers.md | gap-writer |
| 7. VERIFY | architecture health check | state/health/arch-*.md | health-architecture |
| 8. CAPTURE | update V1_PLAN stage, refresh UC catalog | V1_PLAN.md, USE_CASES.md | human + use-case-agent |

**Typical duration:** 2-8 hours (mostly human thinking and review time)
**How often:** Once per product stage; triggered automatically by drift

---

### MID Altitude — Epic / Problem Loop (Pre-Workflow P0–P4)

| Generic step | nowu activity | Primary artefact | Actor |
|---|---|---|---|
| 1. SIGNAL | raw idea captured | idea-NNN.md | human (P0.1) |
| 2. ORIENT | vision alignment, mode selection, decomposition | NNN-mode.md, NNN-decomp.md | human + idea-decomposition |
| 3. DISCOVER | domain research, persona interviews | disc-NNN-research.md, problem-NNN.md | discovery-agent + perspective-interview |
| 4. SHAPE | epic and story mapping, scope hammer | epic-NNN.md, story-NNN-*.md | story-mapper + human gate |
| 5. DECIDE | architecture bootstrap, constraint check | arch-pass-NNN.md, ADR candidates | architecture-bootstrap + human ADRs |
| 6. BUILD | readiness assembly | intake-NNN.md [READY_FOR_S1] | readiness-checker + human |
| 7. VERIFY | readiness checklist enforced | NNN-readiness.md | readiness-checker |
| 8. CAPTURE | intake handed to S1; loop routing set | intake-NNN.md status: READY_FOR_S1 | human sign-off |

**Typical duration:** 30 min (Lite) to 4-8 hours (Bootstrap)
**How often:** Once per epic; triggered by P0 idea capture

---

### LOW Altitude — Story / Task Loop (S1–S9)

| Generic step | nowu activity | Primary artefact | Actor |
|---|---|---|---|
| 1. SIGNAL | intake brief arrives | intake-NNN.md [READY_FOR_S1] | nowu-intake (S1) |
| 2. ORIENT | constraints analysis, risk surface | intake-NNN-constraints.md | nowu-constraints (S2) |
| 3. DISCOVER | options generation | intake-NNN-options.md | nowu-options (S3) |
| 4. SHAPE | task spec, file scope, ACs | task-NNN.md | nowu-shaper (S5) |
| 5. DECIDE | option decision, ADR if needed | intake-NNN-decision.md | nowu-decider (S4) |
| 6. BUILD | implementation + VBR | changeset, vbr-report | nowu-implementer (S6/S7) |
| 7. VERIFY | review: code, tests, story coverage | review-report | nowu-reviewer (S8) |
| 8. CAPTURE | lessons, routing, knowledge atoms | capture-record.md, next_cycle_trigger | nowu-curator (S9) |

**Typical duration:** 30 min to 4 hours
**How often:** Once per story; triggered by READY_FOR_S1 intake

---

## 6. Where Are We? — Position Tracker

At any point in time, you are at one step of one altitude.
Reading the artefact tells you which step:

```
State artefact                         → Altitude / Step
─────────────────────────────────────────────────────────
state/arch/gap-trigger.md OPEN        → HIGH / 1-2 (Signal/Orient)
state/arch/global-pass-*.md PROPOSED  → HIGH / 3-4 (Discover/Shape)
docs/architecture/adr/*.md PROPOSED   → HIGH / 5 (Decide)
docs/architecture/containers.md       → HIGH / 6 (Build, after gap-writer)
state/health/arch-*.md                → HIGH / 7 (Verify)
V1_PLAN.md stage updated              → HIGH / 8 (Capture)

state/ideas/idea-NNN.md               → MID / 1 (Signal)
state/pre-workflow/NNN-mode.md        → MID / 2 (Orient)
state/discovery/disc-NNN-research.md  → MID / 3 (Discover)
state/stories/story-NNN-*.md DRAFT    → MID / 4 (Shape)
state/arch/arch-pass-NNN.md           → MID / 5 (Decide)
state/intake/intake-NNN.md DRAFT      → MID / 6 (Build)
state/pre-workflow/NNN-readiness.md   → MID / 7 (Verify)
state/intake/intake-NNN.md READY      → MID / 8 (Capture/handoff)

state/intake/intake-NNN.md READY_FOR_S1 → LOW / 1 (Signal)
state/arch/*-constraints.md           → LOW / 2 (Orient)
state/arch/*-options.md               → LOW / 3 (Discover)
state/tasks/task-NNN.md               → LOW / 4-5 (Shape/Decide)
state/changes/changes-task-NNN.md     → LOW / 6 (Build)
state/vbr/vbr-task-NNN.md            → LOW / 7 (Verify)
state/capture/capture-task-NNN.md     → LOW / 8 (Capture)
```

This is also your answer to "where are we now?" — the newest, most
incomplete artefact tells you.

---

## 7. Loop Interactions

Altitudes are not isolated. They interact in two directions:

### Downward: HIGH constrains MID constrains LOW

- HIGH altitude GAP → produces constraints for P3.
- MID altitude arch-pass → produces constraints for S2.
- MID altitude story ACs → become acceptance criteria at LOW.
- LOW altitude never overrides MID or HIGH without a new artefact.

### Upward: LOW signals MID signals HIGH

- LOW S9 `next_cycle_trigger: ARCH_PIVOT` → re-enters MID at P3.
- LOW S9 `next_cycle_trigger: PRODUCT_PIVOT` → re-enters MID at P1 or HIGH at Signal.
- MID P3 repeated conflicts → triggers HIGH GAP (gap-detector picks this up).
- MID problem-NNN scope expansion → may require updating V1_PLAN (HIGH).

```
HIGH ──── constrains ────► MID ──── constrains ────► LOW
HIGH ◄─── signals ─────── MID ◄──── signals ──────── LOW
```

---

## 8. Project-Level Mapping

The Altitude pattern applies to all nowu-managed projects, not just
software. The artefact names may change; the loop does not.

| Altitude | nowu Framework (NF) | Aperitif Business (AP) | Real Estate (RE) | Personal Knowledge (PK) |
|---|---|---|---|---|
| HIGH Signal | architecture drift, stage advance | new regulatory wave, market shift | property portfolio change | life event, interest pivot |
| HIGH Artefact | global-pass-NNN.md, containers.md | domain-model-AP-NNN.md | RE-domain-model-NNN.md | pk-catalog-NNN.md |
| MID Signal | new feature need | new product variant | new property to digitize | new topic cluster |
| MID Artefact | epic-NNN.md + problem-NNN.md | AP-epic-NNN.md | RE-epic-NNN.md | PK-epic-NNN.md |
| LOW Signal | READY_FOR_S1 intake | task for formulation step | task for process mapping | task for capture/link |
| LOW Artefact | task-NNN.md | task-AP-NNN.md | task-RE-NNN.md | task-PK-NNN.md |

For non-software projects, the BUILD step produces documents, decisions,
and domain models rather than code. The VERIFY step reviews against
outcome criteria rather than running tests. All other steps are identical.

---

## 9. Routing Vocabulary

Consistent language helps agents and humans know which altitude and step
they are at. Use these terms:

| Term | Meaning |
|---|---|
| **Altitude** | Which of the three loops (HIGH / MID / LOW) |
| **Step** | Which of the 8 generic steps (SIGNAL ... CAPTURE) |
| **Position** | Altitude + Step (e.g., "MID / SHAPE") |
| **Artefact** | The file that carries the output of a step |
| **Gate** | A human-approval checkpoint between two steps |
| **Trigger** | The event that starts a loop at a given altitude |
| **Handoff** | The artefact transfer from one altitude to the next |
| **Pivot** | A CAPTURE output that routes to a different position |
| **Drift** | Growing gap between what an artefact says and reality |
| **GAP** | A HIGH-altitude loop run specifically for architecture |
| **Pass** | A run of one full altitude loop (e.g., "arch pass", "GAP pass") |

---

## 10. Evaluation of the Pattern

### What works well

1. **Orientation.** "Where are we?" is always answerable by checking
   the newest incomplete artefact. This reduces context-recovery time at
   session start (NF-01).

2. **Onboarding.** New agents (and new humans) need to learn one loop,
   not three. The altitude tells them what level to think at; the step
   tells them what to produce.

3. **Pivoting.** The routing vocabulary makes pivots explicit.
   `ARCH_PIVOT` vs `PRODUCT_PIVOT` tells the system exactly where to
   re-enter without human narration.

4. **Cross-domain.** The pattern works for AP, RE, and PK because the
   generic steps are outcome-neutral. The artefact schema adapts;
   the loop structure does not.

5. **Fractal.** Each altitude loop produces artefacts that constrain the
   next altitude. Lessons from LOW bubble up. Plans from HIGH flow down.
   This mirrors how real product development actually works.

### What to watch out for

1. **Loop stacking.** It is possible to be at MID / SHAPE and accidentally
   start a LOW loop prematurely. The gate discipline (human approvals at
   MID / 8 before LOW / 1) prevents this — but only if gates are respected.

2. **HIGH altitude inflation.** Every time something feels uncertain, the
   temptation is to "run a GAP." GAPs are expensive. The gap-detector agent
   enforces trigger conditions precisely to prevent this.

3. **Altitude confusion.** An S2 (LOW / Orient) agent loading
   `docs/USE_CASES.md` is operating at the wrong altitude. Context scoping
   rules in CLAUDE.md are the enforcement mechanism.

4. **Non-software adaptation gap.** The AP and RE altitudes are named here
   but not yet fully specified. The generic loop applies; the artefact
   schemas for AP/RE domain-model passes need to be defined when those
   projects reach MID altitude.

5. **Velocity mismatch.** HIGH altitude moves monthly; LOW altitude moves
   hourly. If the human spends too much time at HIGH, the LOW loop stalls.
   The right cadence is: LOW loops daily, MID loops weekly, HIGH loops
   only when a trigger fires.

---

## 11. Quick Reference

```
At any moment, ask:
  "What altitude am I at?"    → Check the newest incomplete artefact.
  "What step am I at?"        → The step whose artefact is DRAFT or missing.
  "What do I produce next?"   → The artefact for the next step.
  "When do I go up?"          → When CAPTURE says PRODUCT_PIVOT or ARCH_PIVOT,
                                 or when gap-detector fires.
  "When do I go down?"        → When CAPTURE says CONTINUE or COMPLETE,
                                 or when a HIGH artefact is APPLIED.
```
