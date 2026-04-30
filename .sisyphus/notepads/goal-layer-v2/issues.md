# Issues — goal-layer-v2

## [2026-04-30] Session start
No issues yet.

## [2026-04-30] Task 13 verification note
- `lsp_diagnostics` is unavailable for Markdown (`.md`) in this workspace (no Markdown LSP configured), so verification relied on explicit structural grep checks plus evidence artifact generation.

## [2026-04-30] F2 code quality review findings
- Broken cross-references found in reviewed set:
  - `state/epics/epic-v1core-003.md` references `epic-004` (missing; existing file is `epic-v1core-004.md`).
  - `docs/PRE-WORKFLOW.md` contains template placeholder references `epic-001` / `epic-002` that do not exist as real artifacts.
- Goal files `docs/goals/goal-001..004.md` conform to `templates/goal-brief.md` section order and required frontmatter fields.
