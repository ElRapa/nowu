---
artifact_type: LEARNINGS_INDEX
created_at: 2026-05-07
purpose: "Running index of session learnings for workflow optimization"
---

# Session Learnings Index

## Purpose

Running index of all session learnings. Newest entries first.
Each entry links to the full learnings file.

When a pattern appears in 3+ sessions, it gets promoted to **Recurring Patterns**
below the table. Recurring patterns are high-priority candidates for workflow changes.

## Entries

| Date | Session | Key Learnings | Types | File |
|------|---------|---------------|-------|------|
| 2026-05-14 | W5: 5x10 Coordinate Validation | 5x10 model was correct but not operationalized (0/22 artifacts had coordinates); Consumption-position convention established for artifact tagging; S7/S8 agent mapping in MODEL-REFERENCE is wrong (WORKFLOW.md is correct); Section 13 has coverage gaps for 3 artifact types; Git history is most reliable artifact inventory | workflow-process, agent-behavior | `state/learnings/session-2026-05-14-w5-5x10-validation.md` |
| 2026-05-13 | W4 S2-S9: First end-to-end intake cycle | Agent specialization validated; TDD commit ordering matters; Task atomicity prevents scope creep; Appetite calibration needs evidence | workflow-process, agent-behavior, domain-insight | `state/learnings/session-2026-05-13-w4-s2-s9-execution.md` |
| 2026-05-11 | S1 Intake Analysis — NF-01 First Cycle | S1 inline annotations replace separate validation artifacts; Contract definitions are critical S2 blockers; UC scope narrowing is intentional for W4; Hypothesis ADRs need explicit constraint-vs-test status; Appetite binding deferred but bounded to 8h | workflow-process, agent-behavior, domain-insight | `state/learnings/session-2026-05-11-s1-intake-validation.md` |
| 2026-05-10 | Living Orientation System — ROADMAP-003 | Subtask agents corrupt YAML frontmatter when inserting markdown notices; Edge-case data items (PENDING UC) silently dropped (49/50); 4-reviewer verification wave catches category-specific bugs no single reviewer finds; Prometheus+Momus pipeline works for strategic documentation, not just code | agent-behavior, workflow-process, domain-insight | `state/learnings/session-2026-05-10-living-orientation-system.md` |
| 2026-05-10 | Roadmap Global View — Updater Agent vs. Independent Plan | Agent subtask comparison reveals altitude-specific blind spots; UC-to-work-item mapping conflates meta-tasks with implementations; Dual-output comparison (agent + manual + compare) is high-value for strategic docs; v1.2 stage was structurally invisible | agent-behavior, workflow-process | `state/learnings/session-2026-05-10-roadmap-global-view.md` |
| 2026-05-09 | Orchestrator Layer Implementation | Research frontmatter diverged from actual conventions — always validate against codebase; Phantom artifact versioning creates ghost dependencies; Historical state/ files must not be updated during renames | workflow-process, domain-insight | `state/learnings/session-2026-05-09-orchestrator-layer.md` |
| 2026-05-08 | Documentation Maintenance Strategy — Research Evaluation | Research docs propose more than needed — curate ruthlessly (<30%); YAGNI applies to process artifacts too; Minimal template changes (one field + one checklist) have high leverage for workflow behavior | workflow-process, domain-insight | `state/learnings/session-2026-05-08-docs-maintenance-strategy.md` |
| 2026-05-08 | Bootstrap Review & Cleanup — Context Loading Strategy Evaluation | "Confirm Understanding" quizzes are token-wasting AI-slop — use gate checklists; Absolute rules need escape hatches for adjacent work (contracts at ARCHITECTURE altitude); Research docs are historical, separate timeless decisions from ephemeral session planning | workflow-process, agent-behavior | `state/learnings/session-2026-05-08-bootstrap-review-cleanup.md` |
| 2026-05-08 | Altitude-Stratified Bootstrap Architecture | Research doc file paths go stale — always validate against repo; Monolithic bootstraps violate altitude-aware context scoping; Routing indexes preserve cross-cutting content while splitting altitude-specific content | workflow-process, domain-insight | `state/learnings/session-2026-05-08-altitude-stratified-bootstraps.md` |
| 2026-05-07 | W3.5 — Fitness Functions + ADR Refinements | Perplexity gap findings on truncated context are unreliable; architecture tests document ADR requirements; iCloud path-with-spaces breaks editable .pth installs; Known Limitations sections better than silence | workflow-process, tooling | `state/learnings/session-2026-05-07-w35-fitness-functions.md` |
| 2026-05-07 | W3 — Hypothesis ADRs + Perplexity Review Integration | External review catches structural gaps self-review misses; Ground ADRs in existing code (adopt not invent); Write ADRs in dependency order for natural forward refs; Two-layer pattern (machine + human) recurs across concerns | workflow-process, domain-insight | `state/learnings/session-2026-05-07-w3-hypothesis-adrs.md` |
| 2026-05-06 | SYNTHESIS + Architecture Vision | 9 themes not 6; Knowledge model is foundational ADR; Synthesis requires breadth reading not sampling | workflow-process, domain-insight | `state/arch/session-learnings-synthesis-2026-05-06.md` |

> Note: The 2026-05-06 entry predates the `state/learnings/` directory. File remains at
> its original location. Future entries will be in `state/learnings/`.

## Recurring Patterns

### RP-001: Research docs propose more than needed — implement <30%

**Sessions:** 2026-05-08 (altitude-stratified-bootstraps), 2026-05-08 (bootstrap-review-cleanup), 2026-05-08 (docs-maintenance-strategy), 2026-05-09 (orchestrator-layer)

**Pattern:** Perplexity research outputs are comprehensive but contain substantial future-work, over-engineering, and speculative structure. Wholesale implementation creates maintenance burden. Effective approach: separate "actionable now" from "interesting but future" and implement only the minimal viable subset.

**Action:** When consuming any research doc, apply YAGNI filter: implement only what's immediately verifiable and defer the rest. Default to <30% of what's proposed.

*Note (2026-05-13): The PROGRESS.md vs. ROADMAP-001 example in the pattern above is now fully resolved. PROGRESS.md has been tombstoned and all workflow references redirect to ROADMAP-003 and session-log.*


### RP-002: Superseded artifacts accumulate silently — mark immediately

**Sessions:** 2026-05-08 (bootstrap-review-cleanup), 2026-05-09 (orchestrator-layer), 2026-05-10 (roadmap-global-view)

**Pattern:** When a new artifact supersedes an old one, the old one is not immediately marked as SUPERSEDED. It lingers, creating confusion about source of truth (e.g., PROGRESS.md vs. ROADMAP-001, SESSION_STATE.md vs. session-log.md, phantom artifact versions from renames). Each cleanup session rediscovers the same problem.

**Action:** When creating or renaming an artifact that replaces an existing one, immediately add `status: SUPERSEDED` and `superseded_by: {new_artifact_path}` to the old artifact's frontmatter in the same commit. Do not defer this to a cleanup session.

### RP-003: Subtask agents need explicit structural constraints for data-integrity tasks

**Sessions:** 2026-05-10 (living-orientation-system), 2026-05-10 (roadmap-global-view), 2026-05-09 (orchestrator-layer)

**Pattern:** Subtask agents performing structured data modifications (YAML frontmatter, UC mappings, dependency graphs) introduce subtle corruption: inserting markdown inside YAML blocks, dropping edge-case items (PENDING status UC), defaulting to incomplete views (critical-path-only dependency graphs). These errors are invisible to casual review and require targeted verification.

**Action:** When delegating data-integrity tasks: (1) provide the exact target structure as a code-block template, (2) include explicit count-verification instructions ("output must have exactly N rows"), (3) flag edge cases in the data ("note: XP-02 is PENDING, not ACTIVE — include it anyway").

*Note (2026-05-14): Confirmed again in W5 — Sisyphus-Junior agent took 2+ minutes and multiple retries to edit 15 files with complex YAML frontmatter. Providing a sample of the first 10 lines of one file would have prevented the matching struggles.*
