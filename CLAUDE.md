# nowu — Claude Code Configuration v2.2

> Updated: 2026-03-26

---

## Quick Start

Paste `BOOTSTRAP.md` at the start of every new session.
Choose a mode and follow the skill. Every step has an agent and an artifact.

Every idea enters through the pre-workflow. Every feature enters S1 via a READY_FOR_S1 intake.
If entering S1 directly (no pre-workflow), use `templates/intake-s1.md`.

---

## Commands

| Command | What happens |
|---|---|
| `/capture` | Run signal-capture agent — interview (5 questions) → writes `state/ideas/idea-NNN.md` |
| `/pre-workflow run NNN` | Start pre-workflow for idea NNN (creates mode-record) |
| `/pre-workflow status NNN` | Show current phase, status, and next required human action |
| `/pre-workflow resume NNN --from P2` | Resume from specific phase after human gate |
| `/health-check vision` | Run health-vision agent against docs/vision.md |
| `/health-check architecture` | Run health-architecture agent against containers.md |
| `/health-check goals` | Run health-goals agent against active stories + vision |
| `/health-check use-cases` | Run health-use-cases agent against docs/USE_CASES.md |
| `/health-check all` | Run all four health checks via health-sweep |
| `/gap-check ` | Run gap-detector on current product; writes/updates state/arch/gap-trigger.md with RECOMMENDED/NOT_RECOMMENDED |
| `/gap-check run` | If gap-trigger is OPEN and RECOMMENDED, run gap-analyst to create state/arch/global-pass-YYYY-MM-DD.md (PROPOSED) |
| `/gap-check apply YYYY-MM-DD` |  Run gap-writer for that global-pass file after you have set status: APPROVED; applies deltas and closes trigger |
| `/workflow run intake-NNN` | Start S1–S9 from `state/intake/intake-NNN.md` (must be READY_FOR_S1) |
| `/workflow step S3 intake-NNN` | Jump to a specific step with a specific intake |
| `/workflow status` | Show current S1–S9 step, active task, and last agent output |

---

## Approval Tiers

**Tier 1 — auto-proceed:**
Tests, docs, refactors within existing ADRs, within shaped scope.

**Tier 2 — batch for human review:**
Feature implementation, design changes, new dependencies, new stories.

**Tier 3 — STOP and ask:**
Merges to main, breaking changes, new ADRs, deletes, architecture boundary violations,
vision changes, pre-workflow gate transitions.

When unsure, treat as Tier 2.

---

## Agents per Step

**Pre-workflow (P0–P4):**
- P0.V: `vision-bootstrap`
- P0.1: human + `idea-decomposition` (if size = PRODUCT or EPIC)
- P0.UC: `use-case-agent` (create/refresh docs/USE_CASES.md)
- P1.1: `discovery-agent`
- P1.3: `perspective-interview`
- P2.1: `story-mapper`
- P3.1: `constraint-check`
- P3.2: `architecture-bootstrap`
- P4.1: `readiness-checker`

**Implementation workflow (S1–S9):**
- S1: `nowu-intake`
- S2: `nowu-constraints`
- S3: `nowu-options`
- S4: `nowu-decider`
- S5: `nowu-shaper`
- S6/S7: `nowu-implementer`
- S8: `nowu-reviewer`
- S9: `nowu-curator`

**Health checks (anytime):**
- `health-vision`, `health-architecture`, `health-goals`, `health-use-cases`
- `health-sweep` (runs all four and suggests entry point: P0.VISION, P0.UC, P1, P3, or DIRECT-IMPLEMENT)
- If any health report is RED, `health-sweep` MUST invoke `gap-detector` once for this product, which writes/updates `state/arch/gap-trigger.md` with RECOMMENDED or NOT_RECOMMENDED.

**Global Architecture Pass (GAP, HIGH altitude)**
- G0: `gap-detector` — creates/updates `state/arch/gap-trigger.md` based on health + stage
- G1: `gap-analyst` — analyses vision/plan/UCs/arch, writes `global-pass-YYYY-MM-DD.md`
- G2: `gap-writer'` — applies APPROVED global-pass to context/containers/ADRs

---

## Context Scoping — Non-Negotiable

| Phase / Step | Load | Never Load |
|---|---|---|
| P0–P1 | `docs/vision.md`, `state/ideas/idea-NNN.md` | `src/`, architecture docs |
| **P0.UC** | `docs/vision.md`, `docs/V1_PLAN.md`, `docs/USE_CASES.md`, recent problems/epics/stories/captures | `docs/architecture/**`, `src/**`, `tests/**`, `state/arch/**`, `state/tasks/**` |
| P2 | `state/problems/problem-NNN.md`, `docs/USE_CASES.md`, `state/discovery/disc-NNN*` | `src/`, architecture docs |
| P3 | approved stories, `docs/architecture/containers.md`, `docs/DECISIONS.md` | `src/`, `tests/` |
| P4 | all P0–P3 artifacts for NNN | `src/`, `tests/` |
| GAP | `docs/vision.md`, `docs/V1_PLAN.md`, `docs/USE_CASES.md`,  `docs/architecture/context.md`, `docs/architecture/containers.md`, `docs/architecture/adr/*.md`, `docs/DECISIONS.md`, `state/arch/gap-trigger.md`, `state/arch/global-pass-*.md`| `src/`, `tests/`, `state/problems/`, `state/tasks/`, `state/epics`, `state/stories`|
| S1 | `state/intake/intake-NNN.md`, `docs/vision.md`, `docs/V1_PLAN.md`, `docs/USE_CASES.md`, `docs/PROGRESS.md` | `src/`, `tests/`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` |
| S2 | `state/intake/intake-NNN.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `contracts/`, `state/arch/arch-pass-NNN.md` (if exists) | `src/` internals, `tests/` |
| S3–S4 | `state/arch/*-constraints.md`, binding contracts, module surfaces | `src/` internals |
| S5 | `state/arch/*-decision.md`, file tree, contracts | `docs/ARCHITECTURE.md`, `docs/vision.md` |
| S6–S7 | task spec + in_scope_files ONLY | everything else |
| S8 | `state/vbr/*`, `state/arch/*-changeset.md`, task spec, diff | full arch docs, `src/` outside task scope |
| S9 | review report, `docs/DECISIONS.md`, `docs/PROGRESS.md`, git log | `src/`, `tests/` |
| Health | target file only + `docs/vision.md` | `src/`, `tests/`, `state/` (beyond what the health agent declares) |

---

## Skills

| Skill | Mode | Steps |
|---|---|---|
| `pre-workflow-runner` | BOOTSTRAP, FULL, STANDARD, LITE | P0–P4 |
| `full-cycle` | Mode A — new feature from intake | S1–S9 |
| `implement-loop` | Mode B — already-shaped tasks | S5–S9 |
| `single-step` | Mode C — small fix | S6–S9 |
| `architecture-only` | Mode D — design spike | S1–S4 + S9 |
| `health-sweep` | health | Runs all health agents and writes `health-sweep-YYYY-MM-DD.md` |
| `gap-chain` | HIGH | G0 (gap-detector) → G1 (gap-analyst) → G2 (gap-writer)|

---

## Template Locations

| Template | Path | Used at |
|---|---|---|
| vision.md | `templates/pre-workflow/vision.md` | P0.V |
| use-cases.md | `templates/pre-workflow/use-cases.md` | P0.UC |
| idea.md | `templates/pre-workflow/idea.md` | P0.1 |
| mode-record.md | `templates/pre-workflow/mode-record.md` | P-1 |
| problem.md | `templates/pre-workflow/problem.md` | P1.2 |
| epic.md | `templates/pre-workflow/epic.md` | P2.1 |
| story.md | `templates/pre-workflow/story.md` | P2.1 |
| intake.md (pre-workflow) | `templates/pre-workflow/intake.md` | P4.2 |
| adr.md | `templates/pre-workflow/adr.md` | P3.3 |
| intake-s1.md (manual) | `templates/intake-s1.md` | S1 (no pre-workflow) |
| constraints-sheet.md | `templates/constraints-sheet.md` | S2 |
| options-sheet.md | `templates/options-sheet.md` | S3 |
| decision.md | `templates/decision.md` | S4 |
| decision-handoff.md | `templates/decision-handoff.md` | S4 |
| task-spec.md | `templates/task-spec.md` | S5 |
| changeset.md | `templates/changeset.md` | S6 |
| vbr-report.md | `templates/vbr-report.md` | S7 |
| review-report.md | `templates/review-report.md` | S8 |
| capture-record.md | `templates/capture-record.md` | S9 |
| health-report.md | `templates/health-report.md` | health checks |

---

## Architecture Rules (full rules in `.claude/rules/architecture.md`)

- Pre-workflow agents never touch `src/` or `tests/`.
- Implementation agents never load `docs/architecture/` during coding (S6–S7).
- ADRs in `docs/architecture/adr/` are binding — do not contradict without a superseding ADR.
- Decisions in `docs/DECISIONS.md` are binding.
- If `arch-pass-NNN.md` exists, S2 must load it and document any divergence in constraints-sheet.

---

## Health Checks — Run Anytime

Run proactively after any significant change. Run always if >7 days since last check.

```text
/health-check vision        — Is docs/vision.md still aligned with current work?
/health-check architecture  — Is containers.md accurate and conflict-free?
/health-check goals         — Are active stories and backlog aligned with vision?
/health-check use-cases     — Is docs/USE_CASES.md aligned with vision, plan, and work?
/health-check all           — Run all four via health-sweep
```

Reports saved to `state/health/`. GREEN / YELLOW / RED status.
RED status is a hard stop — resolve before proceeding to the next step.

---

## Status Lifecycle — Quick Reference

| Artifact | Created as | Set by human to | Consumed as |
| :-- | :-- | :-- | :-- |
| vision.md | DRAFT | APPROVED | read by P0.2, health-vision, use-case-agent |
| docs/USE_CASES.md | 0.x or 1.x | (via use-case-agent + human) | read by P2, health-use-cases, S2/S8 |
| idea-NNN.md | DRAFT | (no approval needed) | read by P1.1 |
| problem-NNN.md | DRAFT | APPROVED | read by P2.1 |
| story-NNN-*.md | DRAFT | APPROVED | read by P3, P4, S8 |
| intake-NNN.md | DRAFT_FOR_REVIEW | READY_FOR_S1 | read by S1 |
| task-NNN.md | READY_FOR_IMPL | (agent sets DONE) | read by S6–S8 |
| capture-record.md | DONE | (final) | read by pre-workflow-runner for next_cycle_trigger |


---

## Failure Modes

| Symptom | Cause | Fix |
| :-- | :-- | :-- |
| Agent proposes solutions in discovery | Problem/solution contamination | Restart P1.1, enforce discovery agent constraints |
| Stories never finish | Appetite not set at P1.2 | Return to problem-NNN.md, set appetite, re-run P2 |
| Architecture drift from docs | S2 not reading arch-pass-NNN.md | Ensure S2 loads `state/arch/arch-pass-NNN.md` |
| Intake rejected by S1 | Missing required fields | Re-run P4.1 readiness-checker, fix BLOCKED items |
| Vision misalignment discovered late | vision.md stale | Run `/health-check vision` immediately |
| Scope creep in implementation | Weak shaping gate | Return to S5, tighten `in_scope_files` |
| S8 can't verify story coverage | task-spec missing `story_id` | Add `story_id` to task-spec frontmatter, re-run S8 |
| Capture has no routing signal | capture-record missing `next_cycle_trigger` | Re-run S9 with updated capture-record template |
| Many stories have no UC mapping | docs/USE_CASES.md stale | Run `/health-check use-cases` then P0.UC with `use-case-agent` |