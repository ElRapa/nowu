# nowu Bootstrap Prompt — paste once into the first Claude Code session

You are helping develop **nowu**, an AI-powered project management framework.
This framework is self-developing: you help build it using the same workflow
it will eventually run.

## Read in this exact order (do not skip)
1. `CLAUDE.md`                          — commands, arch rules, failure modes
2. `docs/WORKFLOW.md`              — 9-step workflow specification
3. `docs/GLOBAL-MODEL.md`          — how C4 levels map to S1–S9 and artifacts
4. `docs/ARCHITECTURE.md`              — module map (C4 L2)
5. `docs/DECISIONS.md`                 — existing architectural decisions
6. `docs/V1_PLAN.md`                   — current phase and active tasks
7. `docs/CLAUDE-SETUP.md`              — how agents, skills, rules, settings fit together
8. `state/tasks/` (ls only)            — see what tasks exist
9. `docs/WORKFLOW-DETAILED.md`         — detailed workflow spec (optional reference)
10. `docs/PROGRESS.md` (if exists)      — current phase + recent progress (secondary)
11. `state/SESSION-STATE.md` (if exists) — session bookmark only (never source of truth)
12. `.claude/rules/workflow.md`        — statuses, tiers, modes
13. `.claude/rules/architecture.md`    — layer + module boundaries
14. `.claude/rules/testing.md`         — TDD and coverage rules
15. `.claude/rules/code-style.md`      — style, naming, imports

> For skill modes (A/B/C/D), see the SKILL docs under `.claude/skills/` (or `docs/skills/`).


## After reading, confirm your understanding by telling me:
1. What is the nowu global model and why does it exist?
2. What are the 5 modules and which layer each belongs to?
3. What is the current V1 phase and what is the next task?
4. Which step of the workflow does each agent handle (nowu-intake, nowu-constraints, nowu-options, nowu-decider, nowu-shaper, nowu-implementer, nowu-reviewer, nowu-curator)?
5. Which skill modes (A/B/C/D) exist and when to use each?
6. How `settings.json` enforces VBR and scope during tool use.

## Then wait for my approval before touching any files.

## Approval tiers (memorise these)
- **Tier 1** — auto proceed: tests, docs, refactors following existing ADRs
- **Tier 2** — batch for my review: feature implementations, new deps, design changes
- **Tier 3** — STOP and ask me: merges to main, breaking changes, new ADRs, deletes
