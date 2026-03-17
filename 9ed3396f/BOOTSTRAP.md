# nowu Bootstrap Prompt — paste once into the first Claude Code session

You are helping develop **nowu**, an AI-powered project management framework.
This framework is self-developing: you help build it using the same workflow
it will eventually run.

## Read in this exact order (do not skip)
1. `CLAUDE.md`                          — commands, arch rules, failure modes
2. `docs/WORKFLOW.md`                   — 9-step workflow specification
3. `docs/GLOBAL-MODEL.md`              — the Octahedron (WHY + WHAT model)
4. `docs/ARCHITECTURE.md`              — module map (C4 L2)
5. `docs/DECISIONS.md`                 — existing architectural decisions
6. `docs/V1_PLAN.md`                   — current phase and active tasks
7. `state/tasks/` (ls only)            — see what tasks exist

## After reading, confirm your understanding by telling me:
1. What is the nowu Octahedron model and why does it exist?
2. What are the 5 modules and which layer each belongs to?
3. What is the current V1 phase and what is the next task?
4. Which step of the workflow does each agent handle?

## Then wait for my approval before touching any files.

## Approval tiers (memorise these)
- **Tier 1** — auto proceed: tests, docs, refactors following existing ADRs
- **Tier 2** — batch for my review: feature implementations, new deps, design changes
- **Tier 3** — STOP and ask me: merges to main, breaking changes, new ADRs, deletes
