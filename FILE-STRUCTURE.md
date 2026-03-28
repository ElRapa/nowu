# nowu — Canonical File Structure

> Version: 2.2 | Updated: 2026-03-26

---

## Full Directory Tree

```
project-root/
│
├── CLAUDE.md                              ← Claude Code config (load every session)
├── BOOTSTRAP.md                           ← Session bootstrap instructions
│
├── docs/
│   ├── vision.md                          ← [LANDMARK] Product vision (APPROVED before any work)
│   ├── V1_PLAN.md                         ← Stage plan and active epics
│   ├── USE_CASES.md                       ← UC-NNN catalogue (source of truth for validation traces)
│   ├── DECISIONS.md                       ← D-NNN catalogue (binding implementation decisions)
│   ├── ARCHITECTURE.md                    ← [LANDMARK] C4 L1+L2 — combined arch doc (pre-GAP)
│   ├── PROGRESS.md                        ← Cycle-level progress log (updated by S9 curator)
│   ├── GLOBAL-MODEL.md                    ← C4 levels ↔ workflow steps mapping
│   ├── WORKFLOW.md                        ← S1–S9 reference table
│   ├── WORKFLOW-DETAILED.md               ← Full S1–S9 narrative spec
│   ├── PRE-WORKFLOW.md                    ← P0–P4 full specification
│   ├── CLAUDE-SETUP.md                    ← Agent/skill/file reference guide
│   └── architecture/                      ← Created after first GAP run (gap-writer output)
│       ├── context.md                     ← [LANDMARK post-GAP] C4 L1 — system context diagram
│       ├── containers.md                  ← [LANDMARK post-GAP] C4 L2 — container diagram (binding)
│       ├── components-<module>.md         ← C4 L3 per module (updated by S2/S3)
│       └── adr/
│           └── ADR-NNN-title.md           ← Architecture Decision Records (binding)
│
├── state/
│   ├── ideas/
│   │   ├── idea-NNN.md                    ← P0.1 output — raw idea note
│   │   └── parked/
│   │       └── idea-NNN.md                ← Ideas not aligned with vision
│   ├── discovery/
│   │   └── disc-NNN-research.md           ← P1.1 output — Discovery Agent research
│   ├── problems/
│   │   └── problem-NNN.md                 ← P1.2/1.3 output — APPROVED problem statement
│   ├── epics/
│   │   └── epic-NNN.md                    ← P2.1 output — APPROVED epic
│   ├── stories/
│   │   └── story-NNN-001.md               ← P2.1 output — APPROVED story
│   ├── arch/
│   │   ├── arch-pass-NNN.md               ← P3.2 output — C4 delta + ADR candidates
│   │   ├── <intake-id>-constraints.md     ← S2 output — binding constraints sheet
│   │   ├── <intake-id>-options.md         ← S3 output — options + QA scoring
│   │   ├── <intake-id>-decision.md        ← S4 output — accepted decision (D-NNN)
│   │   └── <intake-id>-decision-handoff.md← S4 output — shaper briefing
│   ├── intake/
│   │   └── intake-NNN.md                  ← [LANDMARK] P4 assembled intake (READY_FOR_S1)
│   ├── tasks/
│   │   └── task-NNN.md                    ← S5 output — shaped task spec
│   ├── changes/
│   │   └── changes-task-NNN.md            ← S6 output — files changed
│   ├── vbr/
│   │   └── vbr-task-NNN.md                ← S7 output — VBR gate results
│   ├── reviews/
│   │   └── review-task-NNN.md             ← S8 output — verification + validation report
│   ├── capture/
│   │   └── capture-task-NNN.md            ← S9 output — cycle closure record
│   ├── health/
│   │   ├── health-vision-YYYY-MM-DD.md    ← /health-check vision output
│   │   ├── health-architecture-YYYY-MM-DD.md
│   │   ├── health-goals-YYYY-MM-DD.md
│   │   ├── health-use-cases-YYYY-MM-DD.md
│   │   └── health-sweep-YYYY-MM-DD.md     ← /health-check all output
│   └── pre-workflow/
│       ├── NNN-mode.md                    ← P-1 mode selection record
│       ├── NNN-constraint-check.md        ← P3.1 output
│       └── NNN-readiness.md               ← P4.1 output — READY or BLOCKED
│
├── templates/
│   ├── intake-s1.md                       ← Manual intake (when skipping pre-workflow)
│   ├── constraints-sheet.md               ← S2
│   ├── options-sheet.md                   ← S3
│   ├── decision.md                        ← S4
│   ├── decision-handoff.md                ← S4
│   ├── task-spec.md                       ← S5
│   ├── changeset.md                       ← S6
│   ├── vbr-report.md                      ← S7
│   ├── review-report.md                   ← S8
│   ├── capture-record.md                  ← S9
│   ├── health-report.md                   ← health checks
│   └── pre-workflow/
│       ├── vision.md                      ← P0.V (Vision Bootstrap Agent)
│       ├── idea.md                        ← P0.1
│       ├── mode-record.md                 ← P-1
│       ├── problem.md                     ← P1.2 / P1.3
│       ├── epic.md                        ← P2.1
│       ├── story.md                       ← P2.1
│       ├── intake.md                      ← P4.2 (pre-workflow assembled)
│       └── adr.md                         ← P3.3
│
├── .claude/
│   ├── agents/
│   │   ├── vision-bootstrap.md
│   │   ├── idea-decomposition.md
│   │   ├── use-case-agent.md
│   │   ├── discovery-agent.md
│   │   ├── perspective-interview.md
│   │   ├── story-mapper.md
│   │   ├── constraint-check.md
│   │   ├── architecture-bootstrap.md
│   │   ├── readiness-checker.md
│   │   ├── gap-detector.md
│   │   ├── gap-analyst.md
│   │   ├── gap-writer.md
│   │   ├── nowu-intake.md
│   │   ├── nowu-constraints.md
│   │   ├── nowu-options.md
│   │   ├── nowu-decider.md
│   │   ├── nowu-shaper.md
│   │   ├── nowu-implementer.md
│   │   ├── nowu-reviewer.md
│   │   ├── nowu-curator.md
│   │   ├── health-vision.md
│   │   ├── health-architecture.md
│   │   ├── health-goals.md
│   │   └── health-use-cases.md
│   ├── skills/
│   │   ├── pre-workflow-runner/SKILL.md
│   │   ├── full-cycle/SKILL.md
│   │   ├── implement-loop/SKILL.md
│   │   ├── single-step/SKILL.md
│   │   ├── architecture-only/SKILL.md
│   │   ├── health-sweep/SKILL.md
│   │   └── gap-chain/SKILL.md
│   └── rules/
│       ├── architecture.md
│       ├── workflow.md
│       ├── code-style.md
│       └── testing.md
│
└── src/                                   ← Source code (agents NEVER load this in pre-workflow or arch phases)
```

---

## Artifact Flows — The Data Pipeline

```
IDEA → PROBLEM → STORIES → INTAKE → [S1-S9] → CAPTURE → (next cycle)
 │                              │
 └──── DECOMPOSITION (if PRODUCT/EPIC)
       └── queued sub-ideas feed back into P0
```

### Pre-Workflow Flow (P0–P4)

```
docs/vision.md          ← P0.V creates, human approves
state/ideas/idea-NNN    ← P0.1 human writes
state/discovery/disc-NNN ← P1.1 Discovery Agent
state/problems/problem-NNN ← P1.2/P1.3 human + Perspective Interview Agent
state/epics/epic-NNN    ← P2.1 Story Mapper Agent
state/stories/story-NNN ← P2.1 Story Mapper Agent
state/arch/arch-pass-NNN ← P3.2 Architecture Bootstrap Agent
state/pre-workflow/NNN-readiness ← P4.1 Readiness Checker Agent
state/intake/intake-NNN ← P4.2 Readiness Checker assembles, human sets READY_FOR_S1
```

### Implementation Flow (S1–S9)

```
state/intake/intake-NNN (READY_FOR_S1)
  → S1: nowu-intake → annotates intake, flags open questions
  → S2: nowu-constraints → state/arch/<id>-constraints.md
  → S3: nowu-options → state/arch/<id>-options.md
  → S4: nowu-decider → D-NNN in docs/DECISIONS.md + state/arch/<id>-decision.md
  → S5: nowu-shaper → state/tasks/task-NNN.md (one per ≤4h chunk)
  → S6: nowu-implementer → implements; state/changes/changes-task-NNN.md
  → S7: nowu-implementer (VBR) → state/vbr/vbr-task-NNN.md
  → S8: nowu-reviewer → state/reviews/review-task-NNN.md
  → S9: nowu-curator → state/capture/capture-task-NNN.md
                         → updates docs/DECISIONS.md, docs/PROGRESS.md
                         → sets next_cycle_trigger
```

---

## Landmarks — The Five Files That Must Always Be Current

| File | What it is | Owner | Checked by |
|---|---|---|---|
| `docs/vision.md` | Product intent + scope boundaries | Human (agent-assisted) | health-vision |
| `docs/USE_CASES.md` | All UC-NNN entries (validation anchor) | Human + agents | readiness-checker, S8 |
| `docs/ARCHITECTURE.md` (or `docs/architecture/containers.md` post-GAP) | C4 L2 — current system architecture | Human (agent-assisted) | health-architecture, S2 |
| `docs/DECISIONS.md` | All D-NNN decisions (binding) | S4 + human | S2, S5, S8 |
| `state/intake/intake-NNN.md` | READY_FOR_S1 — current work queue | Readiness Checker + human | S1 |

If any landmark is stale, run the corresponding health check before proceeding.

---

## State Directory — What Lives Where

| Directory | Contains | Created by | Consumed by |
|---|---|---|---|
| `state/ideas/` | Raw idea notes | Human | P1.1 |
| `state/discovery/` | Research runs | Discovery Agent | P1.2, P1.3 |
| `state/problems/` | Approved problem statements | Perspective Interview + Human | P2.1 |
| `state/epics/` | Epic definitions | Story Mapper | P2.2 (human review) |
| `state/stories/` | Story definitions | Story Mapper | P3, P4, S8 |
| `state/arch/` | All architecture artifacts (passes, constraints, options, decisions) | Various agents | Various steps |
| `state/intake/` | Ready-for-S1 intake briefs | Readiness Checker + Human | S1 |
| `state/tasks/` | Shaped task specs | Shaper | S6–S8 |
| `state/changes/` | Implementation changesets | Implementer | S8 |
| `state/vbr/` | VBR gate reports | Implementer | S8 |
| `state/reviews/` | Review reports | Reviewer | S9 |
| `state/capture/` | Cycle closure records | Curator | next cycle P0 |
| `state/health/` | Health check reports | Health agents | Human review |
| `state/pre-workflow/` | Mode records, constraint checks, readiness checks | Various agents | P4, S1 |

---

## Naming Conventions

| Pattern | Example | Used for |
|---|---|---|
| `NNN` (sequence) | `001`, `042` | ideas, problems, epics, stories, arch passes |
| `story-NNN-SSS` | `story-042-001` | stories within epic NNN, sequence SSS |
| `task-NNN` | `task-023` | implementation tasks (independent sequence) |
| `intake-NNN` | `intake-042` | all intakes (pre-workflow assembled or manual) |
| `D-NNN` | `D-007` | decisions in DECISIONS.md |
| `UC-NNN` | `UC-014` | use cases in USE_CASES.md |
| `ADR-NNN` | `ADR-003` | architecture decision records |
| `arch-pass-NNN` | `arch-pass-042` | pre-workflow architecture passes |
| `disc-NNN` | `disc-042` | discovery research runs |

