# nowu Bootstrap — Lean Session Start Prompt

> Use this for follow-up sessions on a project where you already have full context.
> For a brand-new session, use the altitude-specific bootstrap (see `BOOTSTRAP.md` routing index).

---

You are continuing work on the nowu framework. **If you need to refresh context, read the altitude-specific bootstrap:**
- STRATEGIC/PRODUCT: `BOOTSTRAP-STRATEGIC.md`
- ARCHITECTURE: `BOOTSTRAP-ARCHITECTURE.md`
- DELIVERY/EXECUTION: `BOOTSTRAP-DELIVERY.md`
- RETROSPECTIVE: `BOOTSTRAP-RETROSPECTIVE.md`

Otherwise, proceed directly to your skill invocation.

## Minimal Refresh (if needed)

1. `CLAUDE.md`                           — commands, approval tiers
2. `docs/model/MODEL-REFERENCE.md`       — 5x10 altitude-phase model
3. `docs/DECISIONS.md`                   — check for new decisions since last session
4. `docs/ROADMAP.md`                 — current implementation roadmap + execution status

## Health Check (if unsure)

```
/health-check all
```

If any returns RED, tell me before proceeding.

## Confirm Understanding
1. What altitude are you working in? (STRATEGIC, ARCHITECTURE, DELIVERY, RETROSPECTIVE)
2. What is the current roadmap stage and active work item?
3. Are there any BLOCKED or CHANGES_REQUESTED items in state/tasks/?

## Then wait for user approval before touching files.

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
