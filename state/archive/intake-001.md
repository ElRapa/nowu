---
id: intake-001
created: 2026-03-22
status: READY_FOR_ARCH
appetite: 8h (or two 4h tasks — to be confirmed in S5)
affected_modules: [core]
use_case_ids: [NF-01, NF-02, NF-09, PK-03, XP-01]
---

## Problem Statement
Without a concrete `MemoryService` implementation, the system has no durable memory layer: decisions, tasks, and session context cannot be persisted across context window boundaries or crashes (NF-01). There is no way to enforce or trace architectural decisions programmatically (NF-02), surface relevant open tasks across sessions (PK-03), or answer cross-project queries (XP-01). More critically, without a centralised place to attach use-case IDs to every recorded task and decision, there is no machine-checkable `validation_trace` — making NF-09 traceability impossible upstream in S5/S8.

## Context
Step 02 of V1_PLAN. Step 01 produced a `MemoryService` protocol in `core/contracts/` and the module scaffold — but no concrete implementation. Without an implementation, all downstream steps (session runtime, role pipeline, CLI) have nowhere to write decisions, tasks, or session context. This is the foundational gap blocking all persistent behaviour in the system.

The high-level direction (V1_PLAN decision: Option B) is to centralise memory access in a single `core`-layer service that wraps the external `know` module. `flow` and `bridge` must not call `know` directly (D-006).

## Appetite
4h. 

## Open Questions

1. **Protocol completeness** — The existing `MemoryService` protocol covers decisions and tasks. Downstream steps (03 session runtime, 06 curation) will need to persist lessons, concepts, and session summaries. Should Step 02 define how those will be added later, or is that deferred entirely to each downstream step's S1?

2. **Appetite realism** — `know` has 9 atom types and a non-trivial API surface. Is 4h a realistic appetite for a wrapper + integration tests that is also extensible, or should the minimum viable slice be scoped even smaller?

## Handoff

```yaml
from_step: S1
to_step: S2
agent: nowu-constraints
status: READY_FOR_ARCH
```
