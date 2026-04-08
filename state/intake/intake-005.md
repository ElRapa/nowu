---
id: intake-005
created: 2026-04-06
status: READY_FOR_ARCH
appetite: spike
affected_modules:
  - know
  - core
use_case_ids:
  - XP-01
  - XP-08
  - PK-02
  - PK-04
  - PK-05
  - PK-06
  - PK-07
workflow_mode: D
source_global_pass: global-pass-2026-04-06
s1_validated_at: 2026-04-06T00:00:00Z
s1_validation: >
  Well-formed. Live contradiction identified between D-006 (know is external,
  no internal reimplementation) and D-011 + containers.md (know is an internal
  container with an internal federation layer). UC anchors are the full know
  container ownership set (27 UCs); the 7 listed here are the v1 and v1-core
  subset that are immediately implementation-relevant. All referenced decisions
  (D-006, D-011, ADR-0004) are in binding records. Blocking nature confirmed:
  intake-001 (Memory Integration Layer) cannot resume until this is resolved.
s1_note: >
  Mode D (Architecture Only) spike. Resolves the live contradiction between
  D-006 and D-011. Output is either a superseding decision (D-006 →
  SUPERSEDED, new D-013) or a clarifying decision that reconciles them.
  This is BLOCKING for intake-001 and any know implementation work. Must
  run before any other know-related intake proceeds. Gap-writer designated
  know as an internal container — this spike determines whether that
  designation is correct and what it means for the sibling know library.
---

# Intake Brief: `know` Internal vs. External — D-006 Resolution Spike

## Problem Statement

D-006 (2026-03-04, ACCEPTED) states: *"Reuse the existing sibling project `know`
(v0.4.0) through `KnowledgeBase` class API and `KnowAdapter(kb)`. No internal
reimplementation in nowu."* D-011 (2026-04-06, ACCEPTED) and the global-pass
containers.md designate `know` as an **internal container** that maintains its own
SQLite files, implements a federation query layer, and owns all database connections.
These two decisions are structurally incompatible as written.

They could mean three different things:
1. **nowu's `know` module wraps the external `know` library** — D-006 holds; the
   federation layer is added inside nowu's wrapper module, which adapts the sibling
   library's `KnowledgeBase` API.
2. **Federation logic is contributed back upstream to the sibling `know` project** —
   D-006 holds; the sibling `know` grows the federation capability and nowu consumes it.
3. **nowu builds its own `know` module replacing the dependency** — D-006 is superseded;
   nowu's internal `know` module either does not depend on the sibling library or treats
   it as a low-level dependency only for atom schema/serialisation.

No implementation decision can be made correctly until this question is resolved, because
the answer determines: where the federation code lives, which test suite owns it, what the
import graph looks like, whether the sibling `know` version must be locked, and whether
D-006's "no reimplementation" constraint is still binding.

## Context

This contradiction was flagged in:
- D-011 "Review trigger": *"Review D-006 for compatibility with `know`-as-internal-container."*
- global-pass-2026-04-06 "Resolved Questions" section (note on D-006 compatibility).
- Post-GAP analysis 2026-04-06 (explicit identification of D-006/D-011 live contradiction).

The sibling `know` project is at v0.4.0. Its `KnowledgeBase` API provides atom CRUD,
search, and relationship querying. It does NOT currently have a federation layer (multi-file
cross-project querying). XP-01 requires that federation layer — the question is whether
nowu builds it inside a wrapper or whether it is contributed back to the sibling project.

The `know` sibling project in this workspace is at:
`/Users/Raphael.Weidemann/Projects/know/`

Before S2-S4 analysis begins, S2 must inspect the sibling `know` project's current API
surface (relevant files: `src/know/__init__.py`, `src/know/adapter.py`, `docs/API.md`)
to understand what is already available and what the extension point would be.

## Appetite

Spike — time-boxed to the architectural decision. Three clearly differentiated options
must be evaluated (wrap vs. contribute upstream vs. replace). The output is a binding
architectural decision (D-013 or a D-006 amendment) recorded in DECISIONS.md. If the
sibling project's API surface makes option 1 clearly dominant, S3 may reduce to two
options. The decision is the deliverable.

## Acceptance Criteria (architecture decision — Mode D)

1. S2 reads the sibling `know` API surface and establishes what capabilities exist and
   what the extension points are (constraint discovery, not design).
2. S3 evaluates all three coupling options (wrap / contribute upstream / replace) against
   XP-01 federation requirement, D-001, D-002, D-006, D-007, D-011, and the operational
   constraint that both projects live in the same workspace.
3. S4 produces a single binding decision that either:
   (a) Confirms D-006 with a clarifying corollary (how wrapping or upstream contribution
       is the correct interpretation), or
   (b) Supersedes D-006 with a new decision (D-013) that explicitly states nowu's
       relationship to the sibling `know` library going forward.
4. The superseding or clarifying decision is appended to DECISIONS.md and referenced in
   ADR-0004.
5. The intake-005-decision.md artifact records which interpretation was chosen and why,
   with explicit consequence for intake-001 resumption.
