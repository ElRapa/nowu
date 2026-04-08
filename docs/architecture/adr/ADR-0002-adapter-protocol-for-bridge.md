---
id: ADR-0002
title: Adapter Protocol for bridge
date: 2026-04-06
status: ACCEPTED
superseded_by: ~
source_arch_pass: global-pass-2026-04-06
---

# ADR-0002: Adapter Protocol for bridge

## Status

ACCEPTED — ratified on 2026-04-07. This ADR is now binding for all `bridge`
implementation work in v1-core and later adapter work in v1.

## Context

PK-08 (v1, after v1-core CLI stable) requires `bridge` to support non-CLI interaction
modes — specifically capture, review, and light-action from a mobile or remote interface.
The P3 constraint from global-pass-2026-04-06 is explicit: any non-CLI adapter must be
added within `bridge` via an `AdapterProtocol`; no new top-level module may be created
for remote access.

Two questions must be answered before `bridge` is implemented:

1. **CLI library choice** — which Python CLI framework for the v1-core `bridge` surface?
   The choice affects how the CLI command surface is structured and whether adding adapters
   later is a two-hour task or a two-week refactor.
2. **AdapterProtocol design** — what interface must every adapter (CLI, messaging bot,
   future adapters) implement? The protocol must cover all three PK-08 interaction modes
   and be stable enough that adding a second adapter does not require changing `flow` or
   `know`.

This decision must be made before `bridge` v1-core implementation (which unlocks PK-01,
PK-03, NF-10) and before PK-08 is scoped (which unlocks Telegram adapter implementation).

## Decision

**Typer + `AdapterProtocol` in `core/contracts.py`.**

- **CLI library**: Typer is the binding choice for the v1-core `bridge` command surface.
- **Protocol location**: `AdapterProtocol` is defined in `core/contracts.py`, not in `bridge`.
- **Minimum protocol surface**:
  - `receive_capture(text: str) -> CaptureResult`
  - `send_digest(digest: Digest) -> None`
  - `receive_action(action: ActionRequest) -> ActionResult`
- **Implementations**: The CLI adapter and the Telegram adapter both implement this protocol.
- **Instantiation rule**: `bridge` is the only module permitted to instantiate concrete adapters.
- **Boundary rule**: `flow` and `know` must not depend on concrete adapter classes; they interact only through the `bridge` API surface and `core` contracts.
- **Extension rule**: Future adapters (voice, HTTP, other messaging platforms) must be added as new `AdapterProtocol` implementations inside `bridge`; no new top-level module may be created for remote access.

## Rationale

Typer was selected over Click based on type-safety alignment with the mypy-strict codebase
convention and native Protocol support. A command-bus pattern (Option C in the candidate
list) was considered but rejected as over-engineered for a single-user CLI that does not
need runtime command dispatch between processes.

The `AdapterProtocol` in `core` — not in `bridge` — ensures that `flow` and `know` can
reference the abstraction without importing from `bridge`, preserving the ADR-0001 import
graph constraint.

## Consequences

**Positive:**
- PK-08 Telegram adapter can be added without modifying `flow`, `soul`, or `know`.
- Adding a third adapter (voice, HTTP) in future requires only implementing the protocol.
- The CLI and messaging surfaces share the same behavioral contract, making testing uniform.
- Adapter multiplicity is hidden inside `bridge`; no other module needs to know which concrete adapter is active.

**Negative:**
- Typer dependency is added to `bridge`; it is not part of `core`.
- `AdapterProtocol` must be stable before any adapter implementation — changing the
  protocol later requires updating all adapters.

**Neutral:**
- `python-telegram-bot` library dependency is gated to ADR-0005 (messaging platform
  decision); it is not introduced by this ADR.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Typer + `AdapterProtocol` in `core` | Type-safe; extensible; modern Python; aligns with mypy-strict | Protocol boilerplate in `core` | Recommended direction |
| Click + plugin architecture | Established; plugin system built-in | Less type-safe; plugin model not needed for ≤3 adapters | Typer preferred for type alignment |
| Command bus pattern | Fully decoupled command dispatch | Adds in-process bus complexity; no clear benefit for solo CLI tool | Over-engineered for v1 scale |

## Related

- arch_pass: global-pass-2026-04-06
- decisions: D-002, D-003, D-007
- containers: `bridge`, `core`
- use_cases: PK-08, PK-01, PK-03, NF-10
- adr: ADR-0005 (messaging platform — Telegram selection)
