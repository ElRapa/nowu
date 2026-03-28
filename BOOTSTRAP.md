# nowu Bootstrap — Full Session Start Prompt

> Paste this at the start of every new Claude Code session on a new product.
> For follow-up sessions on a project you already know, use `BOOTSTRAP_lean.md` instead.

---

You are helping develop a software project using the nowu framework.
This framework is self-developing: you help build it using the same workflow it runs.

## Read in this exact order

1. `CLAUDE.md`                           — commands, approval tiers, failure modes
2. `docs/WORKFLOW.md`                    — S1–S9 reference table and context scoping rules
2b. `docs/GLOBAL-MODEL.md`              — C4 levels mapped to S1–S9 steps (read ## 1. to ## 3. only )
3. `docs/ARCHITECTURE.md`               — module map (C4 L2)
4. `docs/DECISIONS.md`                  — existing architectural decisions (binding)
5. `docs/V1_PLAN.md`                    — current product stage and active epics
6. `docs/CLAUDE-SETUP.md`              — how agents, skills, health checks, and rules fit together
7. `state/tasks/` — run `ls` only       — see what tasks currently exist
8. `docs/WORKFLOW-DETAILED.md`          — full narrative spec (read S1–S9 sections)
9. `docs/PRE-WORKFLOW.md`               — P0–P4 specification (read if you may need to start from an idea)
10. `docs/PROGRESS.md` (if exists)      — current execution status
11. `state/SESSION-STATE.md` (if exists) — session bookmark only — NEVER treat as source of truth
12. `.claude/rules/workflow.md`         — statuses, tiers, iteration modes
13. `.claude/rules/architecture.md`     — layer and module boundaries
14. `.claude/rules/testing.md`          — TDD and coverage rules
15. `.claude/rules/code-style.md`       — style, naming, imports

> For skill mode details (A/B/C/D and pre-workflow), see `.claude/skills/`.

---

## Health Check (run before confirming)

After reading, run:

```
/health-check all
```

If any health check returns RED, tell me before proceeding. Do not start implementation work
with a RED health check outstanding.

---

## Confirm your understanding by telling me

1. What is this product, who is it for, and what problem does it solve? (from vision.md)
2. What does the C4 model mean in this workflow — which step operates at which level?
3. What are the main modules/containers and which layer does each belong to?
4. What is the current product stage and what is the active epic?
5. Which agent handles each step: P0–P4, S1, S2, S3, S4, S5, S6/S7, S8, S9?
6. Which skill modes exist (A/B/C/D + pre-workflow modes) and when to use each?
7. What do Tier 1, Tier 2, and Tier 3 approval mean — give one example of each.

## Then wait for my approval before touching any files.

---

## Approval Tiers (memorise these — apply throughout the session)

**Tier 1 — auto-proceed:**
Tests, documentation updates, refactors within existing ADRs, work within already-shaped scope.

**Tier 2 — batch for my review:**
Feature implementation, new dependencies, design changes, new stories, new health check items.

**Tier 3 — STOP and ask me:**
Merges to main, breaking changes, new ADRs, file deletes, architecture boundary violations,
vision changes, pre-workflow mode selection for new product ideas.

When unsure: treat as Tier 2.
