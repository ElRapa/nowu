---
id: idea-006
created: 2026-04-08
status: DRAFT
size: Epic
captured_by: human (Raphael) — surfaced during pre-workflow v1core P2 epic review
session: pre-workflow P1→P4 run
related_ucs: NF-02, NF-13, NF-06, NF-15, XP-01
---

# Idea: Goal Layer Between Vision and Epics

## Raw Signal

While reviewing epic-v1core-002 (Decision Memory & Pipeline Quality), the human noticed
that the current epic already operates at the "solution" level: it describes *how* we
address a problem, not *what goal we are pursuing*. This makes cross-phase thinking hard
— an epic is scoped to a phase (v1-core, v1, v1.1…) but the goal it serves spans all
phases.

There is a missing artifact layer between vision.md (horizon narrative) and state/epics/
(phase-scoped solution units). This layer should describe *what outcome we are achieving*
across all phases — independently of how and when. Epics become phase-scoped bets toward
a goal; the goal artifact holds the full cross-phase picture.

Example: "Building Trust" is a goal. "Decision Memory & Pipeline Quality" (v1-core) and
"Epistemic Grades & Confidence" (v1.1) are both child epics under that goal.

## Source

- [x] Personal frustration
- [ ] User feedback
- [ ] Market observation
- [x] Technical opportunity
- [ ] Other: ___

## Why It Matters

1. **Epics are phase-scoped; goals are not.** Right now there is no artifact that says
   "here is the full picture of what we are building toward across v1-core, v1, v1.1, v2"
   at the goal level. Each epic lives in isolation.

2. **vision.md has the language but not the structure.** The Success Horizons (6mo/12mo/24mo)
   name the outcomes in prose, but there is no structured artifact that epics can point to,
   no phase coverage table, no "done" criteria for the goal itself.

3. **UC groups are the closest thing — but they are flat lists.** USE_CASES.md has NF, XP,
   PK groups that partially encode goals, but they carry no phase mapping and no lifecycle.

4. **Without it, cross-phase planning is implicit.** You can feel what you are building
   toward but cannot point to a document. When a new epic is created, there is no natural
   place to ask "which goal does this serve?" and "what has already been done toward it?"

## Proposed Shape

A new artifact type: `state/goals/goal-NNN.md` (or `docs/goals/`).

Each goal artifact contains:
- ID and title in user-outcome language (e.g., "Users trust the AI enough to delegate fully")
- Alignment to a vision.md Success Horizon
- The UC IDs whose fulfilment proves the goal is met
- A phase coverage table: which epic delivers which slice toward this goal
- Explicit "done" criteria (when can this goal be retired?)
- Status: OPEN / PARTIALLY_MET / MET

Epics get a `parent_goal:` frontmatter field pointing to the goal ID.

The pre-workflow story-mapper and P2 agents should prompt for goal assignment when creating
a new epic.

## Initial Appetite Guess

- [ ] Tiny (< 2 h)
- [ ] Small (< 1 day)
- [x] Medium (2-3 days)
- [ ] Large (1 week+)
- [ ] Unknown -- needs decomposition

Work includes: template creation, backfilling 4 current epics with parent_goal, writing
~5 initial goal artifacts from the vision.md Success Horizons, updating story-mapper agent
instructions to set parent_goal.

## Why Now?

The v1-core epic set is complete enough that the goals they serve are now visible — it is
the right moment to name them before v1 planning starts and more epics are created without
goal anchoring.

## Related Context

- Related ideas: idea-005 (epistemic grades — would be a child epic of goal "Building Trust")
- Related use cases: NF-02, NF-13, NF-06, NF-15, XP-01
- Related artifacts: docs/vision.md (Success Horizons), docs/USE_CASES.md (UC groups),
  state/epics/epic-v1core-001 through 004
- Suggested initial goals (from vision.md horizons):
  1. goal-001 — Continuity (thread survives interruptions)
  2. goal-002 — Building Trust (decisions are traceable and confidence is visible)
  3. goal-003 — Compounding Knowledge (knowledge accumulates within and across projects)
  4. goal-004 — Self-Improving Workflow (the path from vision to shipped gets faster each cycle)
  5. goal-005 — Infrastructure (nowu runs the operation, not just individual projects)
