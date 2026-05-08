# nowu Bootstrap — Session Start Routing

> **Choose the bootstrap that matches your work altitude.**
>
> For focused work sessions, **start with a skill invocation instead** — see the
> Session Entry table in `AGENTS.md` → "How We Work" section. Each skill loads
> only the context it needs, keeping your session focused and lean.
>
> For lean follow-up sessions, see `BOOTSTRAP_lean.md`.

---

## Altitude Routing

| Altitude | Bootstrap File | Use When |
|---|---|---|
| **STRATEGIC** | `BOOTSTRAP-STRATEGIC.md` | Vision, goals, roadmap, SYNTHESIS, Architecture Vision |
| **PRODUCT** | `BOOTSTRAP-STRATEGIC.md` | Use case discovery, P0-P4 pre-workflow |
| **ARCHITECTURE** | `BOOTSTRAP-ARCHITECTURE.md` | ADRs, module design, contracts, hypothesis ADRs, orchestrator implementation |
| **DELIVERY** | `BOOTSTRAP-DELIVERY.md` | S1-S9 workflow execution, task shaping, implementation loops |
| **EXECUTION** | `BOOTSTRAP-DELIVERY.md` | Code, tests, S6-S7 implementation, S8 review |
| **RETROSPECTIVE** | `BOOTSTRAP-RETROSPECTIVE.md` | GAP analysis, health checks, session learnings |

If you are unsure which altitude you are in:
- Read `docs/model/MODEL-REFERENCE.md` → "Altitude x Phase Examples" table
- Or start with `BOOTSTRAP-STRATEGIC.md` (most general)

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

After reading your altitude bootstrap, run:

```
/health-check all
```

If any health check returns RED, tell me before proceeding. Do not start implementation work
with a RED health check outstanding.

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
