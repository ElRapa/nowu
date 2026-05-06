---
artifact_class: workflow_phase
altitude: ARCHITECTURE
phase: OPTIONS
session_id: session-2026-05-05-alpha
epistemic_grade: INFORMED_ESTIMATE
grade_justification: "Analysis of 5 comparable systems; no nowu prototype yet"
---

# OPTIONS-007: Session State Storage Strategy

**Upstream:** SYNTHESIS-001 Theme 1 (Persistent Session State)
**Blocking UCs:** NF-01, NF-14, PK-08

## Context

SYNTHESIS-001 identified that 3 approved use cases all require durable session state. This OPTIONS artifact explores structural alternatives for how nowu stores and retrieves session-scoped artifacts.

## Evaluation Criteria

1. **Concurrent access** — multiple entry points (CLI, Telegram) writing simultaneously
2. **Query capability** — can we traverse relationships (atoms -> links)?
3. **Migration effort** — how much existing code changes?
4. **Operational complexity** — what new dependencies are introduced?

## Option A: Filesystem (Status Quo)

Markdown files in `state/` with YAML frontmatter. JSON index files for lookup.

| Criterion | Assessment |
|---|---|
| Concurrent access | Poor — file locking is fragile, race conditions likely |
| Query capability | Poor — manual grep/parse, no relationship traversal |
| Migration effort | None — already in place |
| Operational complexity | None — no dependencies |

**Best for:** v1-core if concurrency is not needed yet.

## Option B: SQLite with WAL Mode

Single SQLite database per project. WAL mode for concurrent reads. FTS5 for text search.

| Criterion | Assessment |
|---|---|
| Concurrent access | Good — WAL supports concurrent readers + single writer |
| Query capability | Moderate — SQL joins, FTS5 search, but no native graph queries |
| Migration effort | Moderate — new storage layer, data migration script |
| Operational complexity | Low — SQLite is embedded, no server |

**Best for:** v1.0 if graph queries are not critical.

## Option C: Hybrid (Filesystem + SQLite Index)

Markdown files remain the source of truth. SQLite index mirrors frontmatter for fast queries.

| Criterion | Assessment |
|---|---|
| Concurrent access | Moderate — file writes still have race risk, but index is SQLite |
| Query capability | Good — SQL queries over metadata, file content via FTS |
| Migration effort | Low — existing files stay, add indexing layer |
| Operational complexity | Low — SQLite embedded, sync script |

**Best for:** transitional approach if we want to preserve file readability.

## Option D: Event-Sourced State

Append-only event log. State reconstructed by replaying events. Snapshots for performance.

| Criterion | Assessment |
|---|---|
| Concurrent access | Excellent — append-only, no conflicts |
| Query capability | Good — projected views can be anything |
| Migration effort | High — complete rearchitecture of state layer |
| Operational complexity | Medium — event store, projection engine |

**Best for:** v2+ if audit trail and temporal queries are important.

## Recommendation

**v1-core:** Option A (Filesystem) — sufficient for single-user CLI, no new dependencies.
**v1.0:** Option C (Hybrid) — preserves file readability, adds query capability.
**v1.1+:** Option B (SQLite) — when `know` module needs proper storage.
**v2+:** Evaluate Option D if audit trail requirements emerge.

## Decision Criteria for Human Review

- Is concurrent access needed before v1.0? (If yes, skip A, go to B or C)
- Is graph query needed before v1.1? (If yes, skip A and C, go to B with graph extension)
- Is file readability important? (If yes, favor C over B)
