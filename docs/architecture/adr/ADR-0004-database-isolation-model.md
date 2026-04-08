---
id: ADR-0004
title: Database Isolation Model — Per-Project SQLite with Federation
date: 2026-04-06
status: ACCEPTED
superseded_by: ~
source_arch_pass: global-pass-2026-04-06
---

# ADR-0004: Database Isolation Model — Per-Project SQLite with Federation

## Status

ACCEPTED — ratified via D-011 (intake-003, 2026-04-06). This ADR records the full
decision; D-011 in DECISIONS.md is the canonical reference for status and review trigger.

## Context

`know` must store and query knowledge atoms across multiple concurrent projects. Two use
cases create a structural tension:

- **XP-01** (v1-core) requires cross-project semantic search — the ability to discover
  connections and relevant atoms across all a user's active projects in a single query.
- **XP-08** (v1.1) requires per-project portable export — a full project snapshot that
  is semantically complete and can be transferred to another system.

A single shared SQLite database with a `project_id` column makes XP-01 trivial but makes
XP-08 semantically incomplete: relationship edges between atoms in different projects
cannot be cleanly attributed to one project without a stub-reference rule that produces
exports requiring the receiving system to resolve external IDs.

Per-project SQLite files solve XP-08 cleanly (export = file copy) but require a
federation layer for XP-01 cross-project search.

A third option (Markdown directories + spanning vector index) was evaluated but rejected
on query performance and maintainability grounds at the expected atom counts.

This decision was URGENT at v1-core — XP-01 is in scope for intake-001, and the `know`
storage layer could not be implemented without it.

## Decision

**Per-project SQLite files with a `know`-internal federation query layer (Option B).**

`know` maintains one SQLite file per project in a user-controlled directory. A federation
query layer inside `know` — not a new module — fans out XP-01 cross-project queries across
all project files and merges results in memory. The fan-out is acceptable at ≤ 20
concurrent active projects for v1-core.

If the 20-project threshold is exceeded before v1.1, a `know`-internal materialized-index
fallback (`federation-index.db`, refreshed on every write) is activated; this is an
internal implementation detail of `know` and requires no API change.

**Q5 resolution (corollary):** `core/contracts.py` defines `KnowledgeStoreProvider` as a
Protocol only — no I/O, no database library imports, no concrete implementation in `core`.
`know` provides the sole concrete implementation and owns all per-project SQLite file
handles and connection lifecycle. `core` remains I/O-free.

## Rationale

Option A (single shared DB) is simpler and faster for XP-01 queries but produces a broken
XP-08 — portable export requires the receiving system to resolve cross-project stub IDs.
This was judged to be a design defect, not a tradeoff, because XP-08 semantics require
human-inspectable, self-contained snapshots.

Option B accepts federation-layer complexity in exchange for three structural benefits:
1. XP-08 export is a file copy — semantically complete by design.
2. Project isolation is structural (filesystem level), not query-filter level.
3. v2 multi-user path (XP-10) becomes a directory-routing decision inside `know`, not a
   breaking schema migration requiring coordinated data movement.

## Consequences

**Positive:**
- XP-08 export is a file copy — semantically complete by design, no external ID resolution.
- `core` remains I/O-free; `KnowledgeStoreProvider` is a Protocol with no DB imports.
- v2 multi-user isolation (XP-10) is additive — directory routing inside `know`, not a schema migration.
- Each project's data is independently portable and inspectable.

**Negative:**
- Federation query layer is non-trivial code; must be implemented and tested before XP-01
  is considered complete.
- XP-01 performance is bounded at ≤ 20 concurrent projects before materialized-index
  fallback is required.
- Active project count must be monitored; breach before v1.1 triggers a follow-on intake.

**Neutral:**
- The materialized-index fallback (`federation-index.db`) is a `know`-internal implementation
  detail — no API change or migration required when activated.

**Future storage engines (graph DB, etc.):**
This ADR constrains the isolation and federation model, not the concrete storage
technology. A future graph-native backend is permitted if it preserves:
- per-project structural isolation (one project = one isolated store),
- XP-08 export as a self-contained, semantically complete project snapshot, and
- a `know`-internal federation layer that remains invisible behind the
  `KnowledgeStoreProvider` Protocol in `core/contracts.py`.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Single shared SQLite DB with `project_id` column (Option A) | Simpler queries; faster XP-01 | XP-08 produces semantically incomplete exports; cross-project edges require stub-reference rule | Design defect in XP-08 semantics — not a tradeoff |
| Per-project SQLite files + federation query layer (Option B) | Clean XP-08 export; structural isolation; XP-10 path is additive | Federation layer complexity; bounded fan-out performance | **Selected** |
| Per-project Markdown dirs + spanning vector index (Option C) | Maximum portability; no SQL | Performance unknown at scale; graph edges are awkward in Markdown; harder to query relationship data | Performance and relational query risk too high for 27 UC scope |

## Related

- arch_pass: global-pass-2026-04-06
- decisions: D-011 (canonical status record)
- containers: `know`, `core`
- use_cases: XP-01, XP-08
