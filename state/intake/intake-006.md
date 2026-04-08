---
id: intake-006
created: 2026-04-06
status: READY_FOR_ARCH
appetite: spike
affected_modules:
  - bridge
  - core
use_case_ids:
  - PK-08
  - PK-01
  - PK-03
  - NF-10
workflow_mode: D
source_global_pass: global-pass-2026-04-06
s1_validated_at: 2026-04-06T00:00:00Z
s1_validation: >
  Well-formed. UC anchors confirmed: PK-08 (v1, ACTIVE) is the primary force;
  PK-01, PK-03, NF-10 are the other bridge UCs affected by module boundary
  decisions. D-003 (bootstrap, 2026-02-25) identified as the decision under
  review — no intake, no S2-S4 analysis, one-sentence tradeoff rationale.
  Not blocking v1-core. Must run before bridge implementation begins and before
  PK-08 is scoped. ADR-0002 and ADR-0005 are predicated on D-003's constraint
  and will require amendment if D-003 is superseded.
s1_note: >
  Mode D (Architecture Only) spike. Reevaluates D-003 (5-module structure)
  specifically against the PK-08 fit in `bridge`. The question is whether an
  async messaging bot adapter is architecturally coherent inside a synchronous
  CLI module, or whether a 6th `adapter` module is justified. Output is either
  D-003 confirmed (no change) or a superseding decision (D-003 → SUPERSEDED).
  If superseded, ADR-0001, ADR-0002, and ADR-0005 require amendment. Deferred
  until bridge v1-core implementation is about to start.
---

# Intake Brief: 5-Module Structure Reevaluation — `adapter` Module for PK-08

## Problem Statement

D-003 (2026-02-25, ACCEPTED) establishes a 5-module structure: `core`, `flow`, `bridge`,
`soul`, `know`. It was a bootstrapping assumption with no intake, no S2-S4 analysis, and
one sentence of tradeoff reasoning ("Simplicity vs. granularity. Five modules is lean.").
All subsequent decisions that reference module count inherited this constraint.

The global-pass-2026-04-06 assigned PK-08 to `bridge` with the note: *"NO new top-level
module."* PK-08 requires an async messaging bot adapter (Telegram) with:
- Inbound webhook / long-poll event handling
- Outbound push delivery
- Three distinct interaction modes (capture, review, light-action)
- External API token management and retry logic
- A different execution lifecycle from the synchronous CLI surface

The current `bridge` container owns: PK-01 (CLI capture routing), PK-03 (today view CLI
assembly), NF-10 (CLI orientation rendering), and PK-08 (async messaging adapter). The
first three are coherent: synchronous CLI, local rendering, structured output display.
PK-08 is categorically different in execution model, external dependency surface, and
lifecycle.

The question: is forcing PK-08 into `bridge` to preserve the 5-module count the right
architectural decision when evaluated against the full UC catalog and proper design
criteria — or does PK-08 warrant its own `adapter` module?

## Context

This reevaluation is triggered by:
- D-003's weak evidence base at time of creation (no UC catalog, no GAP, no constraints
  analysis).
- The gap-analyst's treatment of PK-08: assigned to `bridge` with an explicit "NO new
  module" constraint note — accepted D-003 as a fixed constraint rather than evaluating it.
- ADR-0002 (Adapter Protocol for bridge) exists almost entirely to accommodate PK-08
  inside `bridge` without modifying `flow` or `know`. If a separate `adapter` module is
  justified, ADR-0002's scope changes significantly.
- The execution model mismatch: `bridge` as a Typer CLI is synchronous and
  request-driven; a Telegram bot adapter is event-driven, long-lived, and requires
  background task handling.

The reevaluation is **not urgent** — PK-08 is staged at v1 (after v1-core CLI is stable,
approximately 6 months away). However, the decision must be made before `bridge` v1-core
implementation begins, because the `AdapterProtocol` design in `core` depends on where the
implementation will live.

An `adapter` module as a 6th module would affect:
- ADR-0001: one additional entry in the legal import graph
- ADR-0002: scope changes (protocol still in `core`; CLI adapter stays in `bridge`; bot
  adapter moves to `adapter`)
- ADR-0005: Telegram bot implementation moves from `bridge` to `adapter`
- D-003: superseded by a new D-NNN
- containers.md: `bridge` shrinks to 3 UCs; new `adapter` container owns PK-08

A 5-module confirmation would mean ADR-0002 and ADR-0005 proceed as currently drafted.

## Appetite

Spike — time-boxed to the architectural decision. Evaluate three options: (1) keep PK-08
in `bridge` as currently designed; (2) create an `adapter` module for PK-08; (3) hybrid
— `bridge` defines the protocol and synchronous CLI adapter; a separate `adapter` plugin
directory (not a Python module) holds bot adapter implementations. The decision is the
deliverable, with explicit consequence for ADR-0001, ADR-0002, ADR-0005, and containers.md.

## Acceptance Criteria (architecture decision — Mode D)

1. S2 identifies all constraints that bear on the module count question: D-003, D-007
   (modular monolith), D-002 (DDD layers), ADR-0001 (import graph), ADR-0002 (adapter
   protocol), and any execution-model constraints (sync CLI vs. async event loop).
2. S3 evaluates at minimum: option 1 (keep in bridge), option 2 (6th adapter module), and
   option 3 (protocol plugin directory). Scoring must include: PK-08 fit, bridge cohesion,
   ADR-0002 complexity, v1.1+ second-adapter extensibility, and module count penalty.
3. S4 produces a binding decision that either confirms D-003 or supersedes it with an
   explicit statement of the new module structure.
4. If D-003 is superseded: impact on ADR-0001, ADR-0002, ADR-0005, and containers.md is
   documented in the decision file. Gap-writer (or human) applies the delta to those docs.
5. The decision is appended to DECISIONS.md before bridge v1-core implementation starts.
