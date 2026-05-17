---
name: project-w4-milestone
description: W4 (first S1-S9 intake) completed 2026-05-13; v1-core stage in progress; next is W5
metadata:
  type: project
---

W4 (first S1-S9 intake, intake-001) completed 2026-05-13. NF-01 v1-core satisfied. `SessionCheckpoint` persistence implemented in `core` and `flow`. 43 tests, 98.54% coverage. D-024 ACCEPTED.

**Why:** W4 was the first end-to-end validation of the S1-S9 workflow and the primary probe for goal-001 (continuity). Its completion unblocked W5 and K2 in ROADMAP.md.

**How to apply:** When starting the next session, W5 (validate 5×10 coordinates on W4 artifacts) is the next roadmap item. `docs/PROGRESS.md` now exists and should be the first status reference. `intake-001` is DONE. `goal-001` is now `in_delivery`.

Follow-on items flagged (low effort, not yet done as of 2026-05-13):
- F1: Add `pyyaml>=6.0` to `[project.dependencies]` in pyproject.toml
- F2: Add "Known Limitations" note to ADR-0007 (v1-core schema divergence, D-024)

> *Note (2026-05-13): PROGRESS.md is now fully tombstoned. Use `docs/ROADMAP.md` as the first status reference instead.*
