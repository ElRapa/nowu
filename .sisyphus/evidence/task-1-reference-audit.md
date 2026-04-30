# Reference Audit — repo-cleanup-v2
Date: 2026-04-30

## 1. docs/ARCHITECTURE.md references

### Active (must fix):
- `.claude/agents/nowu-intake.md:39` — `docs/ARCHITECTURE.md (S2 territory)`
- `.claude/agents/nowu-shaper.md:36` — `docs/ARCHITECTURE.md, docs/DECISIONS.md, docs/WORKFLOW.md (upstream, settled)`
- `.claude/agents/nowu-options.md:35` — `docs/ARCHITECTURE.md (constraints already extracted in S2)`
- `.claude/agents/nowu-constraints.md:24` — `docs/ARCHITECTURE.md -- module map and boundaries`
- `.claude/agents/nowu-curator.md:55` — `write a note in docs/ARCHITECTURE.md`
- `.claude/agents/readiness-checker.md:37` — `docs/ARCHITECTURE.md, docs/DECISIONS.md, docs/vision.md`
- `.claude/agents/health-vision.md:32` — `docs/ARCHITECTURE.md, docs/DECISIONS.md`
- `.claude/agents/health-architecture.md:27` — `docs/ARCHITECTURE.md (module map and rules, if exists)`
- `.claude/agents/story-mapper.md:32` — `docs/ARCHITECTURE.md, docs/DECISIONS.md`
- `.claude/agents/nowu-implementer.md:30` — `docs/ARCHITECTURE.md, docs/DECISIONS.md, docs/WORKFLOW.md`
- `.claude/agents/health-goals.md:37` — `docs/ARCHITECTURE.md, docs/DECISIONS.md`
- `.claude/rules/architecture.md:37` — `Read full docs/ARCHITECTURE.md during implementation (S5-S7)`
- `.claude/skills/full-cycle/SKILL.md:43` — `docs/ARCHITECTURE.md`
- `docs/WORKFLOW-DETAILED.md:31` — `docs/ARCHITECTURE.md §1`
- `docs/WORKFLOW-DETAILED.md:32` — `docs/ARCHITECTURE.md §4`
- `docs/WORKFLOW-DETAILED.md:88` — `docs/ARCHITECTURE.md`
- `docs/GLOBAL-MODEL.md:36` — `docs/ARCHITECTURE.md, docs/DECISIONS.md, ...`
- `docs/CLAUDE-SETUP.md:79` — `docs/ARCHITECTURE.md §1`
- `docs/CLAUDE-SETUP.md:80` — `docs/ARCHITECTURE.md §4, contracts/`
- `docs/CLAUDE-SETUP.md:104` — `docs/ARCHITECTURE.md`
- `docs/CLAUDE-SETUP.md:220` — `docs/ARCHITECTURE.md (adapt to your modules)`
- `state/arch/intake-003-constraints.md:75` — `No docs/ARCHITECTURE.md and no docs/architecture/containers.md exist yet`
- `FILE-STRUCTURE.md:191` — `docs/ARCHITECTURE.md (or docs/architecture/containers.md post-GAP)`
- `BOOTSTRAP.md` — (referenced in plan as line 16; not in grep output directly but plan confirms it)
- `BOOTSTRAP_lean.md` — (referenced in plan as line 15; not in grep output directly but plan confirms it)

### Archived/Design/Plan (skip):
- `.sisyphus/plans/repo-cleanup.md` — multiple lines (plan file)
- `.sisyphus/plans/repo-cleanup-v2.md` — multiple lines (plan file)
- `docs/design/workflow_design/nowu Workflow v4 — Final Unified Specification.md:271` — design history
- `docs/design/workflow_design/nowu Workflow v4 — Final Unified Specification.md:341` — design history
- `docs/design/workflow_design/nowu Workflow Artifact Specification v3.md:144` — design history
- `docs/archive/adr/ADR-008-dash-scope-dependencies-and-activation-trigger.md:18` — archived
- `state/archive/2026-03-22-memory-integration-constraints.md:15` — archived
- `state/archive/global-pass-2026-03-29.md:34,130,150,175` — archived
- `state/archive/global-pass-2026-04-06.md:509` — archived
- `state/health/health-architecture-2026-03-31.md:231` — health report (state, not active doc)
- `state/health/health-vision-2026-03-31.md:198` — health report
- `state/health/health-arch-2026-03-28.md` — multiple lines, health report
- `state/health/health-sweep-2026-03-28.md` — health report
- `state/PROGRESS.md:45` — progress log (informational, not a routing reference)

---

## 2. GLOBAL-MODEL references

### Active (must fix):
- `docs/ideas/octahedron-model.md:3` — `Status: FORMALISED in docs/GLOBAL-MODEL.md`
- `docs/ideas/octahedron-model.md:49` — `docs/archive/GLOBAL-MODEL.md`
- `BOOTSTRAP.md:15` — `docs/GLOBAL-MODEL.md — C4 levels mapped to S1–S9 steps`
- `BOOTSTRAP_lean.md:14` — `docs/GLOBAL-MODEL.md — C4 levels mapped to S1–S9 steps`
- `FILE-STRUCTURE.md:22` — `GLOBAL-MODEL.md ← C4 levels ↔ workflow steps mapping`
- `state/PROGRESS.md:45` — `Updated ARCHITECTURE.md, DECISIONS.md, V1_PLAN.md, GLOBAL-MODEL.md`

### Archived/Design/Plan (skip):
- `.sisyphus/plans/goal-layer-v2.md` — plan file
- `.sisyphus/plans/goal-layer.md` — plan file
- `.sisyphus/plans/repo-cleanup.md` — plan file
- `.sisyphus/plans/repo-cleanup-v2.md` — plan file
- `.sisyphus/notepads/repo-cleanup-v2/issues.md` — notepad
- `.sisyphus/notepads/repo-cleanup-v2/decisions.md` — notepad
- `docs/design/flow/2026-04-08_3_...md` — design history (multiple lines)
- `docs/design/flow/2026-04-08_4_...md` — design history (multiple lines)
- `docs/GLOBAL-MODEL.md:1` — the file itself (being archived)

---

## 3. ARCH-WORKFLOW references

### Active (must fix):
- *(none)* — all references are in archived health reports

### Archived/Design/Plan (skip):
- `.sisyphus/plans/repo-cleanup-v2.md` — plan file
- `.sisyphus/notepads/repo-cleanup-v2/decisions.md` — notepad
- `state/health/health-architecture-2026-03-31.md:69,70,71,73,79,221` — health report (state/)

---

## 4. docs/ideas/ references

### Active (must fix):
- `.claude/agents/nowu-shaper.md:82` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/nowu-reviewer.md:95` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/nowu-decider.md:97` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/nowu-curator.md:120` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/health-vision.md:107` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/health-architecture.md:108` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/health-use-cases.md:115` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `.claude/agents/health-goals.md:130` — `Schema (full spec: docs/ideas/workflow-learning-loop.md)`
- `docs/ideas/workflow-learning-loop.md:154` — self-reference (the file itself, being moved)

### Archived/Design/Plan (skip):
- `.sisyphus/plans/goal-layer-v2.md` — plan file
- `.sisyphus/plans/goal-layer.md` — plan file
- `.sisyphus/plans/repo-cleanup-v2.md` — plan file
- `.sisyphus/notepads/repo-cleanup-v2/issues.md` — notepad
- `.sisyphus/notepads/repo-cleanup-v2/decisions.md` — notepad

---

## 5. PRE-WORKFLOW-P0-UC references

### Active (must fix):
- *(none)* — all references are in plan/notepad files only

### Archived/Design/Plan (skip):
- `.sisyphus/plans/repo-cleanup-v2.md` — multiple lines (plan file)
- `.sisyphus/notepads/repo-cleanup-v2/decisions.md` — notepad

---

## 6. soul/SESSION-STATE references

### Active (must fix):
- `docs/V1_PLAN.md:84` — `WAL appends events to soul/SESSION-STATE.md`

### Archived/Design/Plan (skip):
- `.sisyphus/plans/repo-cleanup-v2.md` — plan file
- `agents/archive/step-06-bridge-cli.md:23,28` — archived agent
- `agents/archive/step-05-flow-session.md:14,28,49` — archived agent
- `docs/archive/adr/ADR-002-wal-and-session-summary-atom-strategy.md:18,20,43` — archived ADR
- `docs/archive/ARCHITECTURE.md:42,107` — archived doc
- `docs/archive/WORKFLOW.md:72` — archived doc
- `state/archive/global-pass-2026-03-29.md:183,203` — archived

---

## Summary
- ARCHITECTURE.md active refs: **24** (across `.claude/agents/`, `.claude/rules/`, `.claude/skills/`, `docs/WORKFLOW-DETAILED.md`, `docs/GLOBAL-MODEL.md`, `docs/CLAUDE-SETUP.md`, `state/arch/intake-003-constraints.md`, `FILE-STRUCTURE.md`, `BOOTSTRAP.md`, `BOOTSTRAP_lean.md`)
- GLOBAL-MODEL active refs: **6** (`docs/ideas/octahedron-model.md`, `BOOTSTRAP.md`, `BOOTSTRAP_lean.md`, `FILE-STRUCTURE.md`, `state/PROGRESS.md`)
- ARCH-WORKFLOW active refs: **0**
- docs/ideas/ active refs: **9** (all in `.claude/agents/` pointing to `workflow-learning-loop.md`)
- PRE-WORKFLOW-P0-UC active refs: **0**
- soul/SESSION-STATE active refs: **1** (`docs/V1_PLAN.md`)
