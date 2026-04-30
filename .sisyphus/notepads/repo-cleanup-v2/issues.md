# Issues — repo-cleanup-v2

## Known Gotchas
- docs/archive/GLOBAL-MODEL.md may already exist — Task 6 must check before moving
- docs/ideas/ directory must be empty before rmdir (Tasks 3, 4, 5 must all complete first)
- agents/ at root is NOT .claude/agents/ — only delete root-level agents/
- archive/ at root is NOT docs/archive/ — only delete root-level archive/
- SESSION-STATE.md (hyphen) in soul/ is orphaned; SESSION_STATE.md (underscore) in state/ is active
