---
# Intake Brief
id: intake-2026-03-22-memory-integration
created: 2026-03-22
status: READY_FOR_ARCH
appetite: 8h
affected_modules: [core, know]
use_case_ids: [NF-01, NF-02, PK-03, XP-01]
---

## Problem Statement

The nowu framework has contract interfaces (Protocols) for memory operations but
no concrete implementation. Flow and bridge modules cannot persist decisions,
create tasks, recall context, or generate a today-view because there is no
integration layer connecting `core` to the external `know` package. Without this,
the entire pipeline from S5 onward is blocked — nothing survives a session boundary.

## Context

This is Step 02 of V1_PLAN.md. Step 01 (repo scaffold + contract baseline) is
complete. The MemoryService Protocol already exists in `core/contracts/memory.py`
with four methods: `record_decision`, `create_task`, `today_view`, `recall_context`.
The `know` package (v0.2.0) is available as an external dependency. D-006 mandates
using `know` as the system of record — no reimplementation allowed.

## Appetite

8 hours. This is the first real integration work — connecting two packages with
input validation, error handling, and integration tests against a temporary data
directory. If it takes longer, we cut scope to the two most critical methods
(record_decision + recall_context) and defer today_view/create_task.

## Open Questions

1. What is the current `know` public API surface? Has it changed since D-006
   was recorded? Need to verify compatibility with the Protocol.
2. How should `project_scope` be modeled — as a `know` tag, a namespace prefix,
   or a separate collection?
3. What retry/error strategy is appropriate? `know` uses SQLite — what failure
   modes are realistic (locked DB, corrupt index)?
4. Should `MemoryService` be stateless (pure function calls) or hold a
   connection/adapter reference?

## Handoff
```yaml
from_step: S1
to_step: S2
agent: nowu-constraints
status: READY_FOR_ARCH
```
