---
id: ADR-003
status: PROPOSED
title: Approval queue storage format and lifecycle
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-003)
priority: before Step 05 ships
---

# ADR-003 — Approval queue storage format and lifecycle

## Status

PROPOSED

## Context

`bridge` manages the approval queue lifecycle; `soul/pending/` is the physical storage location. `V1_PLAN.md` Step 05 assumes this `soul/pending/` area without defining:

- The schema for individual queue items (fields, required vs optional)
- What states an item can be in (pending, approved, rejected, expired?)
- When items expire or are pruned
- How `bridge` reads, writes, and transitions item state

The overlap between `bridge` (logic owner) and `soul` (storage owner) creates an implicit contract that must be made explicit before Step 05 implementation. A poorly designed schema makes approval review slow and audit trails incomplete.

This ADR governs the `soul/pending/` storage contract and the `bridge` queue management protocol.

**Priority:** Must be ACCEPTED before Step 05 implementation begins.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) YAML files, one per queue item**
Each approval item is a separate YAML file in `soul/pending/`. Filename encodes item ID and creation timestamp. State transitions are applied by updating the YAML file in place (or moving to `soul/approved/` / `soul/rejected/` subdirectories). Matches the Markdown/YAML-as-state principle (D-001); easy to inspect with a text editor; natural Git history.

**(B) A single JSON queue file in `soul/`**
One `soul/pending.json` file contains all queue items as a JSON array. `bridge` reads and rewrites the whole file on every state transition. Simple structure; single file means easy atomic reads using Python's `json` module. Risk: concurrent writes (even from two sequential agent steps) could corrupt the file; entire file history in Git is noisy.

**(C) `know` TASK atoms as the queue**
Each approval item is stored as a TASK atom in `know` with a specific `project_scope` and status field. `bridge` queries `know` for pending TASK atoms rather than reading files. Zero additional schema design needed if TASK atoms already cover the required fields. Tightly couples the approval lifecycle to `know` availability; may be over-engineered for Tier 2/3 approvals that are human-in-the-loop.

## Consequences

[HUMAN TO COMPLETE]
