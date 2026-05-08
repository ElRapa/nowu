# nowu Bootstrap — Full Orientation (Comprehensive)

**Use this for**: True onboarding, deep troubleshooting, or when you need maximum context.
**For routine work**: Use altitude-specific bootstraps — see `BOOTSTRAP.md` routing index.

---

You are helping develop a software project using the nowu framework.
This framework is self-developing: you help build it using the same workflow it runs.

## Read in this exact order

### Core (always read)

1. `CLAUDE.md`                              — commands, approval tiers, failure modes
2. `docs/WORKFLOW.md`                       — S1–S9 reference table and context scoping rules
3. `docs/model/MODEL-REFERENCE.md`          — 5×10 altitude-phase model (THE conceptual framework)
4. `docs/model/WORKFLOW-STANDARDS.md`       — binding workflow rules (epistemic grades, phases)
5. `docs/architecture/containers.md`        — module map (C4 L2)
6. `docs/DECISIONS.md`                      — all D-NNN decisions (binding)
7. `docs/STAGED-PLAN.md`                    — current implementation roadmap (areas × stages)

### Workflow detail (read when executing S1-S9 or P0-P4)

8. `docs/WORKFLOW-DETAILED.md`              — full narrative spec (read S1–S9 sections)
9. `docs/PRE-WORKFLOW.md`                   — P0–P4 specification (read if starting from an idea)
10. `state/tasks/` — run `ls` only          — see what tasks currently exist

### Context (read when orienting)

11. `docs/vision.md`                        — product vision (APPROVED)
12. `docs/USE_CASES.md`                     — approved use cases
13. `docs/goals/`                           — goal-001 through goal-004

### Rules (skim, then reference when needed)

14. `.claude/rules/workflow.md`             — statuses, tiers, iteration modes
15. `.claude/rules/architecture.md`         — layer and module boundaries
16. `.claude/rules/testing.md`              — TDD and coverage rules
17. `.claude/rules/code-style.md`           — style, naming, imports

### State (check before acting)

18. `state/SESSION_STATE.md` (if filled)    — session bookmark only — NEVER treat as source of truth
19. `state/arch/` — run `ls`                — architecture artifacts, SYNTHESIS, handoffs
20. `state/sessions/` — run `ls`            — checkpoint storage per ADR-0007 (may be empty)
21. `state/PROGRESS.md`                     — cycle-level execution status

> For skill mode details (A/B/C/D and pre-workflow), see `.claude/skills/`.

---

## Document Map — "What question does each doc answer?"

| Question | Read This |
|---|---|
| What IS nowu? What problem does it solve? | `docs/vision.md` |
| What's the conceptual framework? (altitudes, phases, grades) | `docs/model/MODEL-REFERENCE.md` |
| What are the binding rules? | `docs/model/WORKFLOW-STANDARDS.md` + `docs/DECISIONS.md` |
| How do I execute S1-S9? | `docs/WORKFLOW.md` + `docs/WORKFLOW-DETAILED.md` |
| How do I start from a vague idea? | `docs/PRE-WORKFLOW.md` |
| What's the implementation roadmap? | `docs/STAGED-PLAN.md` |
| What are we building for users? | `docs/USE_CASES.md` + `docs/goals/` |
| How do I verify correctness? | `docs/model/VERIFICATION-GUIDE.md` |
| What's the module architecture? | `docs/architecture/containers.md` + ADRs |
| What research informed the model? | `docs/research/` |
| What templates exist for artifacts? | `templates/` |
| What's an example of a good artifact? | `docs/model/examples/` |

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
2. What are the 5 altitudes and 10 phases in the model? What's the S1-S9 zigzag?
3. What are the main modules/containers and which layer does each belong to?
4. What is the current stage and what's the critical path? (from STAGED-PLAN)
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
