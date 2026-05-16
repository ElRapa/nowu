---
name: feedback-s9-template-gaps
description: S9 template and spec gaps discovered during capture-intake-001; apply corrections when running future S9 cycles
metadata:
  type: feedback
---

Three recurring friction points in S9 capture that require judgment calls each time:

1. **PROGRESS.md may not exist** — The S9 spec says "update docs/PROGRESS.md" but the file may not exist (S1 of intake-001 explicitly flagged this). When PROGRESS.md is absent, create it from scratch using current date, active stage, and roadmap context. No need to ask the user.

2. **Capture record template uses `task_id` (singular)** — Multi-task intakes (the norm) need `task_ids: [...]`. Use the plural form without hesitation; the template is stale.

3. **`linked_epics: []` in goal frontmatter is unreliable** — Goal files have `linked_epics: []` even when epics point to them via `parent_goal`. Use the Phase Coverage table as the authoritative source for "which epics are linked to this goal" rather than the frontmatter list.

**Why:** Discovered during S9 for intake-001 (2026-05-13). All three are template/tooling gaps, not workflow failures.

**How to apply:** In every future S9 run, do not pause or flag these as uncertainties — apply the judgment calls above silently and note them in the S9 analysis file under Friction Points.

> *Note (2026-05-13): PROGRESS.md is now fully obsolete. The template gap described below is resolved — S9 no longer writes to PROGRESS.md. It updates `docs/ROADMAP-004.md` status fields and adds a `state/session-log.md` entry instead.*
