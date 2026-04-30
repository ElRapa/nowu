# Learnings — repo-cleanup-v2

## Conventions
- Use `git mv` for all file moves (preserves history)
- Use `git rm` for deletions
- Evidence files go to `.sisyphus/evidence/task-{N}-{slug}.{ext}`
- Single commit at end (Task 10)

## Key Paths
- Active agents: `.claude/agents/` (DO NOT TOUCH)
- Archive destination: `docs/archive/`
- Design destination: `docs/design/concepts/` and `docs/design/research/`
- Canonical architecture docs: `docs/architecture/containers.md`
