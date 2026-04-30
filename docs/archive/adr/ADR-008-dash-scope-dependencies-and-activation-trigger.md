---
id: ADR-008
status: PROPOSED
title: dash scope, dependencies, and activation trigger
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-008)
priority: at Stage 2 gate — blocks dash/ directory creation
---

# ADR-008 — dash scope, dependencies, and activation trigger

## Status

PROPOSED

## Context

`docs/ARCHITECTURE.md` §4.1 and this GAP confirm that `dash` (Visualization and Reporting UI) is out of scope for v1. However, no formal ADR defines:

- What `dash` is allowed to import (and crucially: what it is forbidden to import)
- Whether `dash` reads from `bridge`/`core` directly, or through a defined contract
- At which product stage `dash` is activated

This matters because `dash` is triggered by NF-08, AP-07, and RE-07 — all of which require audience-specific report generation and health visualization. Without a boundary definition, `dash` will naturally reach into `flow` internals (to access step-level data) and create coupling that prevents future event-driven evolution. D-007 explicitly preserves the path to an event-driven architecture; a `dash` with direct `flow` imports would close that path.

A `dash/` directory appearing in the repository before this ADR is ACCEPTED is an architecture violation per P3 constraint 6.

**Priority:** Must be ACCEPTED before `dash` is scaffolded. Scaffolding before this ADR is accepted is a P3 constraint violation.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) `dash` reads from `core` contracts only — never from `flow` internals**
`dash` may only import from `core/contracts/` and from public data sources (atoms from `know` via a `core`-defined Protocol). `flow`, `bridge`, and `soul` are fully opaque to `dash`. Cleanest boundary; future event-driven evolution is unobstructed since `dash` never holds a reference to `flow` state. Requires that all data `dash` needs is exposed through `core` contracts or `know` atoms — may require new `core` contracts to be designed before `dash` is useful.

**(B) `dash` is a `bridge` output command, not a separate module**
Instead of a new top-level module, `dash` functionality is implemented as a set of `bridge` commands (e.g. `bridge report`, `bridge dashboard`). This avoids creating a new module and keeps the 5-module structure intact. Works well if `dash` outputs are primarily CLI-rendered or file-generated reports. Does not work if `dash` eventually needs a UI runtime (web app, Electron) that is architecturally incompatible with `bridge`'s CLI scope.

**(C) `dash` emerges at Stage 3 only, blocked by a formal stage gate**
`dash` is not permitted at Stage 2. It may only be scaffolded at Stage 3 (framework product horizon), when NF-07 collaborator onboarding and AP-07/RE-07 audience-specific reports become active requirements. By Stage 3, the event-driven architecture question (D-007) will be resolved and `dash`'s boundary can be designed with full knowledge of the runtime model. Highest confidence in the final design; longest wait.

## Consequences

[HUMAN TO COMPLETE]
