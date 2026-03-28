# nowu Bootstrap — Lean Session Start Prompt

> Use this for follow-up sessions on a project where you already have full context.
> For a brand-new session or a new product, use `BOOTSTRAP.md` instead.

---

You are continuing work on a software project using the nowu framework.

## Read in this exact order

1. `CLAUDE.md`                           — commands, approval tiers, failure modes
2. `docs/WORKFLOW.md`                    — S1–S9 reference table (refresh context scoping)
2b. `docs/GLOBAL-MODEL.md`              — C4 levels mapped to S1–S9 steps (read ## 1. to ## 3. only )
3. `docs/ARCHITECTURE.md`               — module map (C4 L2)
4. `docs/DECISIONS.md`                  — existing decisions (binding — check for recent additions)
5. `docs/V1_PLAN.md`                    — current stage and active epic
6. `docs/CLAUDE-SETUP.md`              — agents, skills, and rules reference
7. `state/tasks/` — run `ls` only       — see what tasks exist and their statuses

## Load only if relevant to current work

- `docs/WORKFLOW-DETAILED.md`   — if you need narrative depth on a specific step
- `docs/PRE-WORKFLOW.md`        — if you are starting from an idea (P0–P4 mode)
- `docs/PROGRESS.md`            — current execution status
- `state/SESSION-STATE.md`      — session bookmark only — NEVER treat as source of truth
- `.claude/rules/workflow.md`   — statuses, tiers, modes
- `.claude/rules/architecture.md` — boundaries
- `.claude/rules/testing.md`    — TDD rules
- `.claude/rules/code-style.md` — style rules

---

## Health Check

Run at session start if you are unsure about alignment:

```
/health-check all
```

If any returns RED, tell me before proceeding.

---

## Confirm your understanding by telling me

1. What is the current product stage and what is the active epic or task?
2. What are the main modules and their layers?
3. What are the available skill modes (A/B/C/D + pre-workflow) and when to use each?
4. What does each approval tier (Tier 1/2/3) mean?
5. Are there any BLOCKED or CHANGES_REQUESTED items in `state/tasks/` right now?
6. Did any health check return YELLOW or RED?

## Then wait for my approval before touching any files.

---

## Approval Tiers (memorise these)

**Tier 1 — auto-proceed:**
Tests, documentation, refactors within existing ADRs, work within shaped scope.

**Tier 2 — batch for my review:**
Feature implementation, new dependencies, design changes, new stories.

**Tier 3 — STOP and ask me:**
Merges to main, breaking changes, new ADRs, file deletes, architecture boundary violations,
vision changes, new product mode selection.

When unsure: treat as Tier 2.
