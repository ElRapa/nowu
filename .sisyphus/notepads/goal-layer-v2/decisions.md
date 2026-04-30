# Decisions — goal-layer-v2

## [2026-04-30] Session start

### Architectural Decisions (from user interview)
- Goals are agent-created (vision-bootstrap extension), human-reviewed
- UC↔goal bidirectional mapping: goals list UCs, USE_CASES.md gets parent_goal column
- Bootstrap ordering: goals created first with empty UC tables; use-case-agent fills both sides on next natural run
- Altitude/phase frontmatter only (idea-004 groundwork, not full implementation)
- Agent runtime stays Claude-native (not migrated)
- D-012 supersedes reverted D-011

## [2026-04-30] Task 13 execution decisions
- Goal count set to 4 (within expected 3–6) to map cleanly to distinct outcome changes across 6/12/24-month horizons.
- `parent_vision_horizon` set per most relevant anchor (`6mo`, `12mo`, `24mo`) while preserving non-overlap between goals.
- `status` fixed to `proposed`; no UC or phase rows prefilled by design.
