---
id: session-review-2026-04-08
created: 2026-04-08
type: session-learning
session: pre-workflow v1-core P1→P4 review + approval
status: COMPLETE
applies_to: pre-workflow agents, story-mapper, use-case-agent, epic template, workflow
---

# Session Learning: v1-core Pre-Workflow Review — 2026-04-08

## What Happened

Full review and approval pass over all v1-core pre-workflow artifacts (P1→P4). Started with
4 consistency fixes, then two quality passes, then an interactive approval loop that surfaced
5 significant design insights before approving all epics and stories.

---

## Learning 1: Epics Are Written at the Solution Level — a Goal Layer Is Missing

**What surfaced:** epic-v1core-002 was reviewed and felt off. The title "Decision Memory &
Pipeline Quality" describes *how* we're solving a problem, not *what we're achieving*. The
human noticed this naturally: "shouldn't 'Building Trust' be the parent epic?"

**The real pattern:** The current hierarchy skips a level:

```
vision.md (horizon narrative)   ← "why"
                ↓  [GAP]
epic-v1core-NNN                 ← "how / solution" — wrong altitude
        ↓
story-NNN                       ← implementation unit
```

What's missing is a **goal layer** — artifacts that name the outcome being pursued across all
phases, independently of how and when. "Building Trust" is a goal. "Decision Memory &
Pipeline Quality" (v1-core) and "Epistemic Grades" (v1.1) are both phase-scoped bets toward
that goal.

**What we did:**
- Created idea-006 to capture the full shape of the goal layer
- Added `parent_goal` frontmatter to all 4 epics as placeholders
- Renamed epic-002 to "Building Trust: Decision Memory & Pipeline Quality"
- Mapped initial 5 goals from vision.md Success Horizons

**What to fix in pre-workflow:**
- P2.1 story-mapper: when creating an epic, prompt for `parent_goal` assignment
- P0.UC use-case-agent: UC groups (NF, XP, PK…) are currently flat lists; they partially
  encode goals but have no lifecycle or phase coverage table
- New artifact template needed: `state/goals/goal-NNN.md` with: ID, UC coverage, phase table,
  done criteria, status (OPEN/PARTIALLY_MET/MET)

---

## Learning 2: "Productive But Drifting" Is a Distinct Problem From "Where Was I?"

**What surfaced:** During s001 review, the human said: "What if we don't have loose ends? What
if we have an idea we haven't followed up on, or a goal we haven't addressed?" Then: "I remember
good Copilot sessions where I did solid work but at the end of the day I built something I
wasn't planning to build."

**The real pattern:** There are two distinct orientation problems:
- **Thread resumption** (NF-01/NF-10): "What was I doing? What's next?" — point-in-time
- **Strategic alignment** (NF-16): "Am I working on the right things?" — cross-time, cross-goal

Session momentum creates its own gravity. Each next step is locally coherent, globally
misaligned. No orientation artifact prevents this unless it actively compares trajectory
against goals.

**What we did:**
- Created NF-16 (Detect and Surface Strategic Drift — v1)
- Created story-v1core-001-s005 (Vision-Aligned Session Orientation — deferred to v1)
- Kept s001 as-is (thread resumption is valuable and bounded; Medium appetite correct)
- Marked s005 explicitly blocked by idea-006 (needs goal layer to query)
- Updated USE_CASES.md to v2.5

**What to fix in pre-workflow:**
- story-mapper should check: does the epic address orientation/resumption only, or does it
  also address strategic alignment? These need separate stories.
- When a new story touches "session start" or "orientation", prompt: is this thread resumption
  or drift detection? They are not the same.

---

## Learning 3: "Isolated Memory" Was the Wrong Concept — Namespace Separation Is Correct

**What surfaced:** story-v1core-003-s002 said "own isolated memory space" and AC-002 enforced
"no state from project-A visible in project-B." The human paused: "I want cross-project
knowledge too. Maybe isolation via privilege restriction later."

**The real pattern:** "Isolated memory" implies hermetic sealing — no cross-contamination AND
no deliberate cross-access. But XP-01 (Cross-Project Discovery) is already a v1-core UC. The
two were in direct conflict. "Namespace separation" is the correct framing:
- Accidental contamination: prevented
- Deliberate cross-project access (XP-01 queries, future privilege-scoped views): always possible

**What we did:**
- Changed Story Statement, AC-002, Architecture Signals, and Validation Trace in s003-s002
  from "isolated" to "namespace-separated"
- Added explicit note: "deliberate cross-project access (XP-01) is not blocked by this story"
- Flagged P3 must decide: file-system boundary vs. project ID namespace filter

**What to fix in pre-workflow:**
- story-mapper should use "namespace-separated" not "isolated" when describing project memory
- When writing bootstrap stories, add a prompt: "Does this isolation model conflict with any
  cross-project UC (XP group)?"

---

## Learning 4: vision.md Has the Goal Language but Not the Goal Structure

**What surfaced:** When asked "does vision.md have a goal layer?", analysis showed it has
Success Horizons (6mo/12mo/24mo) in prose and Guiding Principles as *how*, but no structured
artifacts that epics can link to.

**The real pattern:** vision.md is the right document for the *narrative* of goals, not for
the *structured* goal artifacts. The Success Horizons name the outcomes; the goal layer
*operationalises* them. Without the structured layer, there is no machine-readable way to ask
"which epics serve which goal?" or "when is this goal met?"

**Implication:** When idea-006 goes through pre-workflow, the output should be ~5 goal
artifacts derived directly from the vision.md Success Horizons — not invented separately.
The story-mapper agent should have a step that reads the nearest horizon and proposes a
`parent_goal` before writing epic frontmatter.

---

## Learning 5: Review Loop Surfaced Real Design Gaps, Not Just Style Issues

The interactive approval loop was not purely administrative — it surfaced 4 genuine design
gaps (see above). This suggests the approval loop should be treated as a **design review**,
not just a status flip. The right framing for future sessions:

> "For each hotspot story: what is the hardest thing this story gets wrong? What
>  open question, if answered wrong at P3, will cause real problems?"

Stories that have no open questions and no architectural risk should be batched and approved
without review. Stories with open architecture questions (feedback mechanism, namespace
boundary, goal coverage) need focused review even if they feel "small."

**What to fix in story-mapper / S5 shaper:**
- Add a "hardest failure mode" field to hotspot stories (1 sentence)
- Add a "P3 must decide" field explicitly flagging open P3 questions — not buried in
  Architecture Signals prose

---

## Key Artifacts Created This Session

| Artifact | Type | Note |
|---|---|---|
| idea-005.md | Idea | Epistemic grades as framework primitive |
| idea-006.md | Idea | Goal layer between vision and epics |
| story-v1core-002-s007.md | Story | Decision evidence + epistemic grade recording (APPROVED) |
| story-v1core-001-s005.md | Story | Vision-aligned session orientation (DRAFT, v1 deferred) |
| NF-15 | UC | Epistemic grades (v1-core) — USE_CASES.md v2.4 |
| NF-16 | UC | Strategic drift detection (v1) — USE_CASES.md v2.5 |
| `parent_goal` frontmatter | Convention | Added to all 4 epics |
| epic-002 rename | Convention | "Building Trust: Decision Memory & Pipeline Quality" |

## Consistency Fixes Applied

| File | Fix |
|---|---|
| state/archive/intake-002-constraints.md | Deleted corrupted file, reconstructed clean |
| state/problems/problem-006.md | PK-08 staging: v1.1 → v1 (3 locations) |
| state/epics/epic-v1core-003.md | PK-08 in Out-of-Scope: v1.1 → v1; self-dependency typo |
| All 4 epics | agent_version: story-mapper@2.2 → story-mapper@2.3 (enriched) |
| story-v1core-003-s002 | "isolated memory" → "namespace-separated" (Story Statement, AC-002, Validation Trace, Architecture Signals) |
