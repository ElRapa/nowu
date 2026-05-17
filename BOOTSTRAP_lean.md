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

## If `context_plan` Is Present

If `work-scheduler` provided a `context_plan`, follow it exactly:
- Load only `context_plan.required_files` (plus at most 1–2 from `optional_files` if needed)
- Use `context_plan.summary_bullets` to reconstruct session context — do not scan the repo
- Respect `token_constraints.max_files` (default ≤6) unless user overrides
- Use the `bootstrap` field to select the altitude bootstrap; use `runner_hint` to select the skill

## Minimal Refresh (if no `context_plan`)

1. `CLAUDE.md`                           — commands, approval tiers
2. `docs/model/MODEL-REFERENCE.md`       — 5x10 altitude-phase model
3. `docs/DECISIONS.md`                   — check for new decisions since last session
4. `docs/ROADMAP.md`                     — current implementation roadmap + execution status

## Health Check (if unsure)

```
/health-check all
```

If any returns RED, tell me before proceeding.

## Orientation Check

Before touching files, confirm:
- What altitude are you working in? (STRATEGIC, ARCHITECTURE, DELIVERY, RETROSPECTIVE)
- What is the active work item and its status in the roadmap?

Then wait for user approval before touching files.

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
