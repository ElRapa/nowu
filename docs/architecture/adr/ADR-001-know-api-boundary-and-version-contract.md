---
id: ADR-001
status: PROPOSED
title: know API boundary and version contract
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-001)
priority: immediate — before Step 03 ships
---

# ADR-001 — know API boundary and version contract

## Status

PROPOSED

## Context

D-006 records the decision to use the `know` sibling project as the sole system of record for durable knowledge in nowu. However, D-006 does not specify which `know` APIs are permitted in each nowu module, how `know` version upgrades are handled, or whether nowu pins a specific `know` version.

The `know` package is an active sibling project currently at v0.4.0. A breaking API change would today cascade unpredictably through `core` (MemoryService), `flow` (lesson storage), and `bridge` (atom capture and query). The Step 02 task wraps `know` via `MemoryService` in `core`, but the wrapper boundary is not formalised.

This ADR addresses:
- Which `know` API methods are permitted in which nowu modules
- How `know` version upgrades are reviewed and merged
- Whether nowu pins a specific `know` version in `pyproject.toml`

**Priority:** Must be ACCEPTED before `know` ships v0.5.0, and before Step 03 begins.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) Pin exact `know` version, explicit upgrade gate**
Lock `know` to a specific version in `pyproject.toml`. Any upgrade requires a formal review step, a regression test run, and an updated task spec before merging. Simple to enforce; creates a clear accountability moment, but may cause the sibling projects to drift if upgrades are deferred.

**(B) Use a compatibility shim in `core` that abstracts `know` API changes**
`MemoryService` (or a dedicated `KnowAdapter` in `core`) absorbs API differences. All other nowu modules depend on the shim interface, never on raw `know` methods. More engineering cost, but protects `flow`, `bridge`, and tests from upstream changes. Nowu code remains stable across `know` version bumps as long as the shim is maintained.

**(C) Declare `know` a first-class dependency with a shared changelog**
Both projects update in concert. A shared CHANGELOG entry documents breaking changes. `nowu` CI runs its test suite against the new `know` version before merging. Requires coordination discipline between the two sibling projects; no code indirection needed. Only viable if both repos are maintained by the same developer or team.

## Consequences

[HUMAN TO COMPLETE]
