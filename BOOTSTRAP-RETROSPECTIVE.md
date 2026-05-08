# nowu Bootstrap — RETROSPECTIVE Altitude

**Use this for:** GAP analysis (G0-G2), health checks, session learnings, drift detection.

## Read in this exact order

### Workflow Model (always)
1. `docs/model/MODEL-REFERENCE.md`         — 5x10 altitude-phase model (focus on RETROSPECTIVE)
2. `docs/model/WORKFLOW-STANDARDS.md`      — epistemic grades, artifact standards

### Strategic Context (for alignment)
3. `docs/vision.md`                        — product vision (reference for drift detection)
4. `docs/DECISIONS.md`                     — all D-NNN decisions (check for violations)

### Retrospective Context (altitude-specific)
5. `state/health/` — run `ls`              — health check reports
6. `state/arch/gap-*.md` — run `ls`        — prior GAP analysis outputs
7. `state/learnings/INDEX.md`              — running index of session learnings

### Evidence Gathering (for pattern detection)
8. `state/tasks/` — run `ls`               — task statuses (for blocked/deferred patterns)
9. `state/SESSION_STATE.md` (if filled)    — session bookmark (for handoff quality)
10. `git log --oneline -20`                — recent commits (for drift detection)

### Tools
11. `CLAUDE.md`                            — commands (especially /health-check)

## Before Proceeding
Verify: ☐ I know the RETROSPECTIVE altitude and how it differs from EXECUTION ☐ I know the GAP steps (G0-G2) ☐ I know the health check categories ☐ I know the epistemic grade scale. If any unclear, re-read the relevant file above.
