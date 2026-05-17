# Setting Up nowu in a New Repository

> Extracted from CLAUDE-SETUP.md Section 9 (archived 2026-05-08).

## Steps

1. Copy root files: `CLAUDE.md`, `BOOTSTRAP.md`, `BOOTSTRAP_lean.md`, `BOOTSTRAP-STRATEGIC.md`, `BOOTSTRAP-ARCHITECTURE.md`, `BOOTSTRAP-DELIVERY.md`, `BOOTSTRAP-RETROSPECTIVE.md`, `BOOTSTRAP-FULL.md`, `AGENTS.md`
2. Copy `docs/` directory. Update product-specific content in:
   - `docs/vision.md` (or run `/pre-workflow run 001 --mode Bootstrap`)
   - `docs/ROADMAP.md` (human-authored roadmap)
   - `docs/architecture/containers.md` (adapt to your modules)
   - `docs/DECISIONS.md` (start empty — add D-001 for first architecture decision)
   - `docs/USE_CASES.md` (start with 3-5 core use cases)
3. Copy `.claude/` directory entirely. Adjust module names and file paths in agents.
4. Copy `templates/` directory.
5. Create empty state skeleton:
   ```bash
   mkdir -p state/{ideas,discovery,problems,epics,stories,arch,pre-workflow,intake,tasks,changes,vbr,reviews,capture,health,sessions,learnings}
   touch state/{ideas,discovery,problems,epics,stories,arch,pre-workflow,intake,tasks,changes,vbr,reviews,capture,health,sessions,learnings}/.gitkeep
   ```
6. Run vision bootstrap if no vision.md exists:
   `/pre-workflow run 001 --mode Bootstrap`
