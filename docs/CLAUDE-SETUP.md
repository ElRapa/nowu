# nowu — Claude Workflow, C4 Model, and Setup Guide

> Read this when: setting up a new repo, onboarding to an existing project,
> or when you need a reference for which file/agent/skill to use.
> Commands are in `CLAUDE.md`. Session start is in `BOOTSTRAP.md`.

---

## TL;DR

- **Pre-Workflow (P0–P4):** raw ideas → structured intake brief.
- **Implementation Loop (S1–S9):** intake brief → shipped, documented code.
- **Health Checks:** run anytime to validate vision, architecture, goal alignment.
- **C4 Levels:** define exactly what context each step may load — this is non-negotiable.
- **One agent per step.** Skills orchestrate the order and modes.
- **All decisions:** recorded as D-NNN in `docs/DECISIONS.md` — binding on all agents.

---

## Cheat Sheet: Which Skill to Use When

### Pre-Workflow (P0–P4)

Use when you are **not yet at an intake brief**.

| Situation | Skill | Mode | Outcome |
|---|---|---|---|
| New product / big idea (from zero) | `pre-workflow-runner` | Bootstrap | `docs/vision.md` + `docs/V1_PLAN.md` + first `intake-NNN` READY_FOR_S1 |
| New epic on existing product | `pre-workflow-runner` | Full | `problem-NNN`, `epic-NNN`, `story-NNN-*`, `arch-pass-NNN`, `intake-NNN` READY_FOR_S1 |
| New story on existing epic (arch current) | `pre-workflow-runner` | Standard | new `story-NNN-*` + `intake-NNN` READY_FOR_S1, no arch pass |
| Small feature / tweak on known project | `pre-workflow-runner` | Lite | 1–few approved stories + `intake-NNN` READY_FOR_S1 |

### Implementation (S1–S9)

Use when you **already have `state/intake/intake-NNN.md [READY_FOR_S1]`**.

| Situation | Skill | Mode | Entry |
|---|---|---|---|
| Full feature from intake → shipped | `full-cycle` | A | `intake-NNN.md [READY_FOR_S1]` |
| You have shaped tasks, just execute | `implement-loop` | B | `task-NNN [READY_FOR_IMPL]` |
| Quick bugfix / refactor / docs | `single-step` | C | thin `task-NNN` or direct |
| Architecture / design spike, no code | `architecture-only` | D | `intake-NNN.md [READY_FOR_S1]` |

### Health Checks (run anytime)

| Question | Command | Output |
|---|---|---|
| Is vision.md still accurate and current? | `/health-check vision` | `state/health/vision-YYYY-MM-DD.md` |
| Does architecture match reality? | `/health-check architecture` | `state/health/arch-YYYY-MM-DD.md` |
| Is active work aligned with vision? | `/health-check goals` | `state/health/goals-YYYY-MM-DD.md` |
| Is USE_CASES.md aligned with vision + active work? | `/health-check use-cases` | `state/health/health-use-cases-YYYY-MM-DD.md` |
| All of the above | `/health-check all` | All four reports + `health-sweep-YYYY-MM-DD.md` |

Run at session start if >7 days since last run, or whenever something feels off.

---

## 1. The Two Loops

### Pre-Workflow (P0–P4)
Converts raw ideas into `state/intake/intake-NNN.md [READY_FOR_S1]`.
Full specification: `docs/PRE-WORKFLOW.md`.

### Implementation Loop (S1–S9)
Converts intake briefs into shipped, documented code.
Reference table: `docs/WORKFLOW.md`.
Full narrative: `docs/WORKFLOW-DETAILED.md`.

**Connection point:** `state/intake/intake-NNN.md` with `status: READY_FOR_S1`
**Feedback loop:** S9 `next_cycle_trigger` routes back to the appropriate pre-workflow phase

---

## 2. C4 Levels and Context Scoping

| Level | Name | Question answered | Main artifacts |
|---|---|---|---|
| Above L1 | Problem space | What problem? For whom? | `docs/vision.md`, `state/problems/` |
| L1 — Context | System | What does the system do? | `docs/ARCHITECTURE.md` §1 |
| L2 — Containers | Modules | How do modules interact? | `docs/ARCHITECTURE.md` §4, `contracts/` |
| L3 — Components | Files / classes | What files exist, what do they expose? | file tree, `__init__.py` surfaces |
| L4 — Code | Implementation | How does it work internally? | `src/`, `tests/` |

Each agent loads **only** the context appropriate to its C4 level.
See `docs/WORKFLOW.md` for the full context scoping matrix.

---

## 3. Files Reference

### Core Documents

| File | Purpose | Who maintains |
|---|---|---|
| `CLAUDE.md` | Commands, approval tiers, failure modes | Human |
| `BOOTSTRAP.md` | Full session start prompt | Human |
| `BOOTSTRAP_lean.md` | Lean follow-up session prompt | Human |
| `CLAUDE-SETUP.md` | This file — master reference | Human |
| `docs/WORKFLOW.md` | S1–S9 reference table | Human |
| `docs/WORKFLOW-DETAILED.md` | Full narrative workflow spec | Human |
| `docs/PRE-WORKFLOW.md` | P0–P4 full specification | Human |
| `docs/vision.md` | Product vision — highest authority | Human (agent-assisted draft) |
| `docs/V1_PLAN.md` | Stage plan and active epics | Human |
| `docs/ARCHITECTURE.md` | Module map, C4 L1/L2 | Human (agent-assisted) |
| `docs/DECISIONS.md` | D-NNN decision registry (binding) | Human + nowu-decider |
| `docs/USE_CASES.md` | UC-NNN use case registry | Human |
| `docs/PROGRESS.md` | Execution status per stage | Human + nowu-curator |

### State Files (agent-produced, human-approved)

| Path | Produced at | Purpose |
|---|---|---|
| `state/SESSION-STATE.md` | Any step | Session bookmark — never source of truth |
| `state/ideas/idea-NNN.md` | P0.1 | Raw captured ideas |
| `state/pre-workflow/NNN-decomp.md` | P0.D | Idea classification and routing |
| `state/discovery/disc-NNN-research.md` | P1.1 | Problem research and personas |
| `state/problems/problem-NNN.md` | P1.2 / P1.3 | Approved problem statement |
| `state/epics/epic-NNN.md` | P2.1 | Epic definition and story index |
| `state/stories/story-NNN-*.md` | P2.1 / P2.2 | Approved stories with ACs |
| `state/pre-workflow/NNN-constraint-check.md` | P3.1 | Architecture signal compatibility |
| `state/arch/arch-pass-NNN.md` | P3.2 | C4 L1/L2 delta + ADR candidates |
| `state/pre-workflow/NNN-readiness.md` | P4.1 | Gate check results |
| `state/intake/intake-NNN.md` | P4.2 | Bridge: pre-workflow → S1–S9 |
| `state/arch/intake-NNN-constraints.md` | S2 | Architecture risk analysis |
| `state/arch/intake-NNN-options.md` | S3 | Design options (2–3) |
| `state/arch/intake-NNN-decision.md` | S4 | Decision handoff for shaping |
| `state/tasks/task-NNN.md` | S5 | Shaped task spec with ACs + validation trace |
| `state/changes/changes-task-NNN.md` | S6 | Implementation notes |
| `state/vbr/vbr-task-NNN.md` | S7 | VBR gate results |
| `state/reviews/review-task-NNN.md` | S8 | Review report |
| `state/capture/capture-task-NNN.md` | S9 | Capture record + next_cycle_trigger |
| `state/health/` | Health checks | Health check reports |
| `docs/architecture/adr/ADR-NNN-*.md` | P3.3 / S4 | Architecture Decision Records (created after first GAP run) |

---

## 4. Agents Reference

### Pre-Workflow Agents

| Agent file | Invoked at | Model | Role |
|---|---|---|---|
| `vision-bootstrap.md` | P0.V | Sonnet | Vision creation / refresh via 5-question interview |
| `idea-decomposition.md` | P0.D | Sonnet | Sizing, routing, stage mapping, seed idea queuing |
| `use-case-agent.md` | P0.UC | Sonnet | Create or refresh docs/USE_CASES.md |
| `discovery-agent.md` | P1.1 | Sonnet | Research, personas, outcomes, assumption flags |
| `perspective-interview.md` | P1.2 | Sonnet | 3-role interview → problem-NNN.md draft |
| `story-mapper.md` | P2.1 | Sonnet | Epic + story generation with scope hammering |
| `constraint-check.md` | P3.1 | Haiku | Architecture signal compatibility check |
| `architecture-bootstrap.md` | P3.2 | Sonnet | C4 L1/L2 delta + ADR candidates |
| `readiness-checker.md` | P4.1–P4.2 | Haiku | Gate check + intake brief assembly |

### GAP Agents (Global Architecture Pass)

| Agent file | Invoked at | Model | Role |
|---|---|---|---|
| `gap-detector.md` | G0 / `/gap-check` | Haiku | Passive sentinel — writes gap-trigger.md |
| `gap-analyst.md` | G1 / `/gap-check run` | Sonnet | Analyses full product context, produces global-pass proposal |
| `gap-writer.md` | G2 / `/gap-check apply` | Sonnet | Applies approved proposal to architecture docs + ADR stubs |

### Health Check Agents

| Agent file | Command | Checks |
|---|---|---|
| `health-vision.md` | `/health-check vision` | Freshness, completeness, active work alignment |
| `health-architecture.md` | `/health-check architecture` | C4 accuracy, ADR coverage, drift |
| `health-goals.md` | `/health-check goals` | Story/backlog alignment with vision, staleness |
| `health-use-cases.md` | `/health-check use-cases` | USE_CASES.md alignment with vision, plan, and active work |

### S1–S9 Agents

| Agent file | Step | Model | Role |
|---|---|---|---|
| `nowu-intake.md` | S1 | Haiku | Confirm intake readiness; thin step if from pre-workflow |
| `nowu-constraints.md` | S2 | Sonnet | Architecture risk and constraint analysis |
| `nowu-options.md` | S3 | Sonnet | Design option proposals with trade-offs |
| `nowu-decider.md` | S4 | Sonnet | Decision record D-NNN |
| `nowu-shaper.md` | S5 | Sonnet | Task specs with ACs and validation trace |
| `nowu-implementer.md` | S6–S7 | Sonnet | TDD implementation + VBR gates |
| `nowu-reviewer.md` | S8 | Sonnet | Verification + validation (fresh context) |
| `nowu-curator.md` | S9 | Haiku | Capture record + next_cycle_trigger |

---

## 5. Skills Reference

| Skill folder | Mode | Phases / Steps |
|---|---|---|
| `pre-workflow-runner/` | — | P0–P4 orchestration (Bootstrap / Full / Standard / Lite) |
| `full-cycle/` | A | S1–S9 |
| `implement-loop/` | B | S5 → [S6–S7]×n → S8–S9 |
| `single-step/` | C | S6–S9 |
| `architecture-only/` | D | S1–S4–S9 |
| `health-sweep/` | health | Runs all four health agents; writes health-sweep-YYYY-MM-DD.md |
| `gap-chain/` | HIGH | G0 (gap-detector) → G1 (gap-analyst) → G2 (gap-writer) |

Skills orchestrate agents. Agents do the work. The main Claude session handles
human communication and Tier 2/3 decisions.

---

## 6. Key Invariants (always true, cannot be overridden)

1. S1 will not proceed without `intake-NNN.md [READY_FOR_S1]`.
2. S6 loads only `in_scope_files` from the task spec. Nothing else.
3. S8 always runs in a fresh context window.
4. ADRs are binding. Contradict one only by creating a superseding ADR first.
5. A human gate that can be skipped under pressure is not a gate.
6. `validation_trace` in every task spec must be complete — no broken links.
7. The readiness checker does not create an intake brief when status is BLOCKED.

---

## 7. How to Copy This Setup to Another Repo

1. Copy root files: `CLAUDE.md`, `BOOTSTRAP.md`, `BOOTSTRAP_lean.md`, `CLAUDE-SETUP.md`
2. Copy `docs/` directory. Update product-specific content in:
   - `docs/vision.md` (or run `/pre-workflow run 001 --mode Bootstrap`)
   - `docs/V1_PLAN.md` (human-authored from Stage Map)
   - `docs/ARCHITECTURE.md` (adapt to your modules)
   - `docs/DECISIONS.md` (start empty — add D-001 for first architecture decision)
   - `docs/USE_CASES.md` (start with 3–5 core use cases)
3. Copy `.claude/` directory entirely. Adjust module names and file paths in agents.
4. Copy `templates/` directory.
5. Create empty state skeleton:
   ```bash
   mkdir -p state/{ideas,discovery,problems,epics,stories,arch,pre-workflow,intake,tasks,changes,vbr,reviews,capture,health}
   touch state/{ideas,discovery,problems,epics,stories,arch,pre-workflow,intake,tasks,changes,vbr,reviews,capture,health}/.gitkeep
   ```
6. Run vision bootstrap if no vision.md exists:
   `/pre-workflow run 001 --mode Bootstrap`
