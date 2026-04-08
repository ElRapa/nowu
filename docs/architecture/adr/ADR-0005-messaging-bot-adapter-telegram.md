---
id: ADR-0005
title: Messaging Bot Adapter for PK-08 — Telegram
date: 2026-04-06
status: ACCEPTED
superseded_by: ~
source_arch_pass: global-pass-2026-04-06
---

# ADR-0005: Messaging Bot Adapter for PK-08 — Telegram

## Status

ACCEPTED — ratified on 2026-04-07. Telegram is the binding first non-CLI adapter for
PK-08 in v1, implemented inside `bridge` under ADR-0002.

## Context

PK-08 ("Interact with nowu from Any Interface", v1) requires `bridge` to support three
interaction modes from a mobile or remote device, without requiring an active CLI session:

1. **Capture** — send a thought to nowu from anywhere; it is routed to `know`.
2. **Review** — read a daily digest or project summary.
3. **Light action** — approve a decision, mark a task done, or answer a prompt.

PK-08 is staged at v1 (after v1-core CLI is stable, ~6 months). The adapter must be
added within `bridge` as an implementation of `AdapterProtocol` (see ADR-0002); no new
top-level module may be created.

The platform choice is a v1 external dependency. Three options were evaluated (Q2 in
global-pass-2026-04-06). Telegram was selected by the human on 2026-04-06 as part of the
gap-trigger constraint resolution. This ADR formalises that selection and records the
implementation requirements.

## Decision

**Implement PK-08 as a Telegram bot adapter in `bridge` using `python-telegram-bot`.**

- Library: `python-telegram-bot`.
- The Telegram adapter is an `AdapterProtocol` implementation defined by ADR-0002.
- The adapter must communicate with `flow` and `know` only through contracted APIs and
  must not import internal implementation submodules from either module.
- Capture messages received via Telegram are routed through `bridge` to `know` via the
  contracted `receive_capture()` protocol method.
- Digest delivery is triggered by `flow` S9 as part of the daily curator run; `bridge`
  pushes the digest to the Telegram chat.
- Light actions are received as Telegram replies and routed to `flow`'s approval queue
  via the contracted `receive_action()` protocol method.
- Telegram Bot API token is stored as a local secret in the environment and is never
  committed to the repository.
- PK-08 is optional at runtime: if Telegram is not configured, nowu core remains fully
  functional and only the PK-08 remote interface is unavailable.

## Rationale

Telegram was selected over Signal (no stable public bot API) and HTTP webhook (requires
browser/curl — poor mobile experience and cannot push light-action prompts unprompted).

By covering all three PK-08 modes with a single platform and a single API, integration
complexity is minimised. `python-telegram-bot` is actively maintained and supports the
full interaction pattern needed (incoming messages, outgoing push, inline keyboard for
approvals).

## Consequences

**Positive:**
- All three PK-08 modes (capture, review, light action) are served by one adapter on one platform.
- Works on any smartphone without a custom app.
- `python-telegram-bot` handles the platform-level retry and rate-limit logic.

**Negative:**
- nowu takes a runtime dependency on the Telegram Bot API (external platform dependency).
- If Telegram is unavailable, PK-08 is unavailable. This is acceptable given local-first
  design — all data remains local; Telegram is a delivery channel only.
- Bot token must be configured as a local secret; onboarding for new users requires a
  Telegram bot setup step.

**Neutral:**
- Telegram adoption means PK-08 is tied to a specific platform. A second adapter (e.g.,
  Signal or HTTP) would require implementing `AdapterProtocol` again — no `bridge` API
  change needed.
- Telegram is a delivery channel, not the system of record; all durable data remains local.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Telegram bot (python-telegram-bot) | All 3 PK-08 modes; single API; any smartphone; actively maintained | External platform dependency; bot token setup required | **Selected** |
| HTTP webhook | No external platform dependency; lightweight | No push capability; light-action mode requires polling or a browser; poor mobile UX | Light-action mode (PK-08 mode 3) is nearly impossible to implement cleanly |
| Cloud sync file watcher (Dropbox/iCloud drop dir) | No new API; lowest technical complexity | Light-action mode essentially impossible; captures are delayed by sync latency | Cannot serve all 3 PK-08 interaction modes |

## Related

- arch_pass: global-pass-2026-04-06
- Telegram is a delivery channel, not the system of record; all durable data remains local.
- containers: `bridge`, `core`
- use_cases: PK-08
- adr: ADR-0002 (adapter protocol — parent design decision)
