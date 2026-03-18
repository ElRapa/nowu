# nowu Bootstrap Prompt — minimal variant for new Claude Code sessions

You are helping develop **nowu**, an AI-powered project management framework.
This framework is self-developing: you help build it using the same workflow
it will eventually run.

## Read in this exact order (do not skip)
1. `CLAUDE.md`                    — commands, arch rules, failure modes
2. `docs/WORKFLOW.md`             — 9-step workflow specification
3. `docs/ARCHITECTURE.md`         — module map (C4 L2)
4. `docs/DECISIONS.md`            — existing architectural decisions
5. `docs/V1_PLAN.md`              — current phase and active tasks
6. `docs/CLAUDE-SETUP.md`         — how agents, skills, rules, settings fit together

## Optional references (only if needed)
- `docs/WORKFLOW-DETAILED.md`     — deeper workflow spec (S0–S9, C4 levels)
- `docs/PROGRESS.md`              — v1 steps status and current focus
- `state/SESSION-STATE.md`        — session bookmark (never source of truth)
- `.claude/rules/workflow.md`     — statuses, tiers, modes
- `.claude/rules/architecture.md` — layer + module boundaries
- `.claude/rules/testing.md`      — TDD and coverage rules
- `.claude/rules/code-style.md`   — style, naming, imports

## After reading, confirm your understanding by telling me:
1. What is the nowu global model and why does it exist?
2. What are the 5 modules and which layer each belongs to?
3. What is the current V1 phase and what is the next task?
4. Which step of the workflow does each agent handle?
5. Which skill modes (A/B/C/D) exist and when to use each?

## Then wait for my approval before touching any files.

## Approval tiers (memorise these)
- **Tier 1** — auto proceed: tests, docs, refactors following existing ADRs
- **Tier 2** — batch for my review: feature implementations, new deps, design changes
- **Tier 3** — STOP and ask me: merges to main, breaking changes, new ADRs, deletes
