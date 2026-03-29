---
id: ADR-004
status: PROPOSED
title: Cross-project isolation model
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-004)
priority: before Step 05 ships; must be resolved before first AP or RE project onboards
---

# ADR-004 — Cross-project isolation model

## Status

PROPOSED

## Context

D-007 and NF-07 (Bootstrap a New Project) assume `know` project_scope partitioning as the isolation mechanism between different projects (e.g. `nowu`, `aperitif`, `re-project`). However, neither D-007 nor any existing decision defines:

- How `know` project scopes are bootstrapped and named (naming convention)
- Whether cross-project connections are opt-in or opt-out
- What happens to atoms when a project is archived
- Whether backup, export, or compliance requirements ever require domain data to be separable from personal knowledge

If isolation is weak, AP/RE knowledge (business financials, regulatory data) could bleed into NF framework decisions (or vice versa) through cross-project connections. The `nowu bootstrap <project>` command (NF-07, Step 05) must implement whatever partitioning model this ADR defines.

**Priority:** Must be ACCEPTED before the first AP or RE project is bootstrapped into `know`.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) `project_scope` tag on all atoms, no hard isolation (current assumption)**
All atoms in `know` are tagged with a `project_scope` string (e.g. `"nowu"`, `"aperitif"`). Queries in `bridge` and `core` always filter by the active project scope. Cross-project connections are possible but require explicit opt-in (the atom referencing the other scope must declare it). Simplest to implement; relies on query-time discipline. Risk: a query without the scope filter returns all atoms across all projects.

**(B) Separate `KnowledgeBase` instances per project (strong isolation)**
Each project gets its own `KnowledgeBase` file/instance. `bridge bootstrap` creates a new KB file. There is no path for atoms to cross project boundaries without explicit export/import. Strongest isolation; clean archive path (delete or move the KB file). Cost: `core`'s `MemoryService` must support multi-KB switching; cross-project discovery (XP-01) becomes impossible without an explicit merge step.

**(C) `project_scope` with explicit cross-project link table**
Like option A, but cross-project connections are tracked in a dedicated link table (a `know` atom type or a separate index). This makes cross-project relationships auditable and reversible. Supports XP-01 (cross-project discovery) while preserving isolation. More complex schema; requires a `know` capability that does not currently exist in v0.4.0.

## Consequences

[HUMAN TO COMPLETE]
