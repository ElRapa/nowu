---
id: intake-003
created: 2026-04-06
status: READY_FOR_ARCH
appetite: spike
affected_modules:
  - know
  - core
use_case_ids:
  - XP-01
  - XP-08
workflow_mode: D
source_global_pass: global-pass-2026-04-06
s1_validated_at: 2026-04-06T09:00:00Z
s1_validation: >
  Well-formed. UC anchors XP-01 (v1-core, ACTIVE) and XP-08 (v1.1, ACTIVE)
  verified in USE_CASES.md. Affected modules know+core correct (ADR-D and Q5
  respectively). Global-pass Q1/Q5 mapping confirmed. Constraint 7 reference
  verified. No body corrections required.
s1_note: >
  Mode D (Architecture Only) spike. No implementation expected. Resolves two
  open questions from global-pass-2026-04-06 that block v1-core: Q1 (ADR-D,
  cross-project isolation model) and Q5 (core DB session factory vs. per-module
  ownership). Outputs are binding decisions recorded in DECISIONS.md (D-NNN)
  and a decision file for reference by gap-writer. May run in parallel with
  intake-002 (different concern: isolation architecture vs. access control policy).
---

# Intake Brief: Cross-Project Knowledge Architecture and DB Session Pattern

## Problem Statement

`know` must store and query knowledge atoms across multiple concurrent projects.
XP-01 (v1-core) requires cross-project semantic search, while XP-08 requires
per-project portable export. These two requirements create a structural tension:
a single shared database makes cross-project queries simple but makes per-project
export and isolation harder; per-project database files give clean isolation and
portability but require a federation layer for XP-01. No architectural decision
currently exists to resolve this tension. Additionally, it is unclear whether
`core` should provide a shared database connection factory (simpler module
initialization, tighter coupling) or whether each module should own its database
files entirely (more isolation, consistent with per-project file option for ADR-D).

## Context

This spike is triggered by global-pass-2026-04-06 open questions Q1 and Q5.
XP-01 is v1-core — the `know` module's storage layer cannot be implemented
without knowing the isolation model. intake-001 (Memory Integration Layer) is
already in progress and references XP-01. The decision made here is a hard
prerequisite for any `know` implementation work. P3 constraint 7 from the
global-pass states: "Cross-project federation before v1.1 knowledge UCs" —
this spike establishes the architectural foundation for that constraint.

## Appetite

Spike — time-boxed to the decision. If the options analysis runs deeper than
expected, cut options to two (shared vs. per-project) and defer edge cases
(e.g., migration path, federation query design) to a follow-on intake. The
decision is the deliverable, not a complete design.

## Open Questions

1. **ADR-D — Isolation model:** Per-project SQLite files + federation query
   layer (Option B) vs. single shared SQLite with `project_id` namespace
   (Option A)? Option B is directionally preferred by the global-pass due to
   XP-08 portability, but Option A is simpler for XP-01 queries. S2 should
   model the tradeoff explicitly.

2. **Q5 — Core DB session pattern:** If per-project files are chosen, does
   `core` expose a shared session factory (e.g., a `DatabaseProvider` protocol
   that all modules call), or does each module manage its own SQLite connection?
   The shared factory is simpler at startup; per-module ownership is more
   consistent with the "modules own their state" principle.

3. **Migration concern:** Whatever is decided must be migratable if the load
   characteristics of v1.1+ knowledge UCs demand a different approach. S3
   options should include a migration path assessment.
