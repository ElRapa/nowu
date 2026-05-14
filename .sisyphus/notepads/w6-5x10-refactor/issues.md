# W6 5×10 Refactor — Issues & Gotchas

## [2026-05-14] Known Issues
- S7/S8 mapping bug exists in: MODEL-REFERENCE §7, MODEL-REFERENCE §11 (check), WORKFLOW-STANDARDS §1.1
- WORKFLOW.md and WORKFLOW-DETAILED.md are CORRECT — do NOT change them
- 31 agent files need altitude/phase (not 35 — 4 already have it)
- Section 13 missing 6+ artifact type entries (state/changes, state/reviews, state/learnings, etc.)
- 16 existing artifact_type values in repo — vocabulary must be superset

## [2026-05-14] Task 12 Findings
- AC-5 failed expected-zero check because `src/nowu.egg-info/SOURCES.txt` changed within HEAD~4 window (12 diff lines).
- AC-8 failed coverage check: literal value `GOAL | USE_CASE | ADR | SYNTHESIS | LESSON` exists in templates/docs but is not represented in MODEL-REFERENCE §13.1 vocabulary table.
