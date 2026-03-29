---
id: ADR-002
status: PROPOSED
title: WAL and session summary atom strategy
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-002)
priority: immediate — before Step 03 ships
---

# ADR-002 — WAL and session summary atom strategy

## Status

PROPOSED

## Context

`soul/SESSION-STATE.md` serves as a Write-Ahead Log (WAL) for the nowu session. `V1_PLAN.md` Step 03 (Memory Integration Layer) depends on session summary atoms being persisted to `know`, but no formal ADR defines:

- The WAL schema for `soul/SESSION-STATE.md` (what fields, what format)
- When WAL entries are synced to `know` as summary atoms
- What constitutes a valid checkpoint (i.e. when is a session "done enough" to persist?)

An incorrect WAL schema cannot be migrated cheaply once sessions accumulate. The Step 03 implementation must not proceed without a binding decision on this schema.

This ADR governs `soul`'s ownership of the WAL format and `flow`'s responsibility for triggering persistence to `know`.

**Priority:** Must be ACCEPTED before Step 03 implementation begins.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) Sync every session end**
At the close of every S9 (curator) step, `flow` triggers a sync of the current WAL to a summary atom in `know`. Simple lifecycle: one sync event per session. Risk: if a session crashes before S9, the WAL is never synced and context is lost.

**(B) Sync on every significant event (checkpoint after each role step)**
`flow` writes a checkpoint to `know` after each S-step completes. More granular recovery; session can be resumed from the last completed step. Higher write volume to `know`; requires the WAL schema to be append-friendly and the sync to be idempotent.

**(C) WAL-only with periodic batch sync**
WAL accumulates in `soul/SESSION-STATE.md` indefinitely. A separate periodic process (`bridge` command or `flow` hook) batches and syncs WAL entries to `know` on a schedule (e.g. daily, or manually triggered). Lowest runtime overhead; highest risk of complete context loss if the batch sync is never run.

## Consequences

[HUMAN TO COMPLETE]
