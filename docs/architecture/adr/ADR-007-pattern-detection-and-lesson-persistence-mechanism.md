---
id: ADR-007
status: PROPOSED
title: Pattern detection and lesson persistence mechanism
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-007)
priority: before Stage 2; not blocking Stage 1 completion
---

# ADR-007 — Pattern detection and lesson persistence mechanism

## Status

PROPOSED

## Context

NF-06 (Learn From Past Mistakes Across Sessions) and XP-03 (Transfer Lessons Learned Between Projects) both require:

1. A mechanism for detecting recurring patterns across sessions
2. A storage channel for persisting lessons so they survive session boundaries and full re-clones

Currently: `flow` (nowu-curator, S9) captures lessons as Markdown artifacts in `state/` and occasionally as updates to `.claude/rules/` files. These lessons:
- Are not machine-verifiable (relying on prompt-injection)
- Do not survive a full re-clone unless the `.claude/rules/` files are committed
- Cannot be queried programmatically for cross-project transfer (XP-03)

The gap-analyst identified the following division of responsibility:
- `flow` owns the detection trigger and escalation logic
- `know` owns the storage and recall of lessons
- The detection algorithm lives in `flow`

This ADR decides the lesson storage channel and the detection mechanism.

**Priority:** Must be resolved before Stage 2, when multi-project lesson transfer becomes active. Not blocking Stage 1.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) Lessons as `know` DECISION atoms with `type=lesson`, surfaced at next session start**
S9 curator writes each lesson as a DECISION atom (with `type=lesson`) to `know`. At the start of the next session (`flow` session-open), `core`'s `MemoryService` queries recent `type=lesson` atoms and surfaces them. Machine-verifiable; survives re-clone; queryable for XP-03 cross-project transfer. Requires `know` to support `type=lesson` atoms (may need `know` schema extension); requires session-start surfacing logic in `flow`.

**(B) Lessons as additions to `.claude/rules/` files (prompt-level)**
S9 curator appends lessons to the relevant `.claude/rules/*.md` file. Lessons affect agent behavior via prompt injection at load time. No `know` dependency; zero engineering cost. Not machine-verifiable; lessons do not survive a re-clone unless `.claude/rules/` files are committed (they currently are). Cross-project transfer (XP-03) requires manual copy-paste between repos.

**(C) Hybrid — lessons to `know`, critical structural lessons to `.claude/rules/`**
Lessons are categorised at S9: operational lessons (e.g. "always check X before Y") go to `know` DECISION atoms for recall; structural lessons that change how agents behave (e.g. new rule for VBR) go to `.claude/rules/`. Most powerful; both programmatic recall and prompt-level behavior change are possible. Most complex: requires a categorisation decision at S9, and two write paths to maintain. Lessons in `.claude/rules/` and in `know` can drift.

## Consequences

[HUMAN TO COMPLETE]
