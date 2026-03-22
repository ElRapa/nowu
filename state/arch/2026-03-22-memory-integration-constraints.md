---
# Constraints Sheet
id: 2026-03-22-memory-integration-constraints
intake_id: intake-2026-03-22-memory-integration
created: 2026-03-22
status: READY_FOR_OPTIONS
c4_l1_update_needed: false
affected_modules: [core, know]
---

> **⚠️ STALE**: This document references `know` v0.2/v0.3 flat API (`know.init()`, `know.today()`, etc.).
> As of know v0.4.0, all operations are instance methods on `KnowledgeBase`.
> See `know/docs/adr/ADR-0005-class-based-api.md` and `nowu/docs/ARCHITECTURE.md` §5 for current API.
> The constraints reasoning is still valid; only the specific API signatures have changed.

## Fixed Constraints

### D-002: DDD Layer Architecture
**Source**: D-002 (ACCEPTED, system level)  
**Constraint**: Domain must not import from Infrastructure. All cross-module dependencies go through `core/contracts/*.py` Protocols.  
**Impact**: MemoryService implementation must live in `core/` (Application layer) and call `know` (external) via its public API only — no private imports, no direct DB access.

### D-006: Treat `know` as external memory SoR
**Source**: D-006 (ACCEPTED, system level)  
**Constraint**: Reuse existing `know` v0.2.0 through public API and `KnowAdapter`. No internal reimplementation in nowu.  
**Impact**: Must use ONLY the operations listed in `know.__all__`: `init`, `create_atom`, `get_atom`, `update_atom`, `query_atoms`, `add_connection`, `search`, `today`, `subgraph`. Cannot bypass or extend `know` internals.

### D-007: Modular monolith for v1
**Source**: D-007 (ACCEPTED, system level)  
**Constraint**: Integration-first modular monolith. All modules in one runtime.  
**Impact**: MemoryService will be a standard Python class, not a service interface with RPC. Initialization happens in-process.

### MemoryService Protocol already defined
**Source**: `core/contracts/memory.py` (Step 01 baseline)  
**Constraint**: Four methods are already specified:
- `record_decision(decision: DecisionRecord) -> str`
- `create_task(title, content, project_scope, tags) -> str`
- `today_view(project) -> dict[str, Any]`
- `recall_context(query, project, top_k) -> list[Any]`

**Impact**: Implementation must fulfill this exact interface. No signature changes allowed without updating the Protocol and all its consumers (flow, bridge).

### Python 3.11+, mypy --strict
**Source**: D-004 + project standards  
**Constraint**: TDD, 90%+ coverage, type-checked with `mypy --strict`, no bare `Any` types.  
**Impact**: MemoryService and all integration tests must be fully typed. Return types must be concrete, not `Any` unless justified.

## Flexible Constraints

### Project scoping model
**Status**: Open design choice  
**Options**: 
- A: Use `know` `project_scope` list field directly (atoms can belong to multiple projects)
- B: Use tags for project filtering
- C: Use atom ID prefixes (e.g., `nowu:decision:001`)

**Recommendation for S3**: Explore Option A (native `project_scope` field) as the path of least resistance — it's already in the `KnowledgeAtom` schema.

### Error handling strategy
**Status**: Open design choice  
**Failures to handle**:
- `RuntimeError` if `know.init()` not called
- `ValueError` if atom validation fails (empty title, grade >=4 without justification)
- SQLite locked DB (if two processes access `~/.know` simultaneously — rare in v1)

**Recommendation for S3**: Fail fast on initialization errors (don't catch), wrap validation errors with informative messages, defer DB lock handling to future (v1 is single-user).

### Stateful vs. stateless MemoryService
**Status**: Open design choice  
**Options**:
- A: Stateless — each method calls `know.init()` or assumes initialization elsewhere
- B: Stateful — MemoryService holds a reference to initialized `KnowAdapter`
- C: Hybrid — lazy initialization on first call

**Recommendation for S3**: Explore Option B (stateful with injected adapter) for testability — allows mocking the adapter in unit tests without touching global `know.init()`.

### Retry logic
**Status**: Deferred to post-v1 unless S3 finds a compelling use case  
`know` operations are synchronous and local (SQLite). Network-style retry logic is not needed for v1. If `know.create_atom()` fails, propagate the error to the caller — don't retry silently.

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| `know` v0.2.0 API has changed since D-006 was written | Medium | S3 must verify current API surface against Protocol requirements. Read `know/docs/API.md` and `know/__init__.py` exports. If mismatches exist, either adapt MemoryService or update the Protocol (Tier 3 gate). |
| `DecisionRecord` type may not map cleanly to `KnowledgeAtom` | Medium | S3 must design the translation layer. Specifically: `DecisionRecord` has `title`, `rationale`, `risks`, `mitigations`, `use_case_ids`. `KnowledgeAtom` has `title`, `content`, `tags`, `project_scope`, `epistemic_grade`. How do `risks` and `use_case_ids` map? |
| Integration tests require `know` to be installed | Low | `pyproject.toml` must list `know` as a dependency. Confirm `know` is installable from the sibling workspace directory (editable install: `uv pip install -e ../know`). |
| `today_view` signature returns `dict[str, Any]` — too vague | Medium | S3 must define the concrete shape of the dict (keys, value types). Consider introducing a `TodayView` dataclass to replace the `Any` type. |
| Multiple projects may call `know.init()` with different `data_dir` | Low | v1 assumes single `~/.know` directory for all projects. Scoping is via `project_scope` field, not separate DBs. Document this assumption in MemoryService docstring. |

## Assumptions

| Assumption | Validated |
|-----------|-----------|
| `know` v0.2.0 is installed and working in the sibling `../know/` directory | True (workspace structure confirms this) |
| `KnowAdapter` is part of `know`'s public API | True (verified in `know/__init__.py` line 39: `from know.adapter import KnowAdapter`) |
| `know.today()` returns a structured dict (not just a string) | Unknown — needs verification in S3 |
| `know.init()` is idempotent (safe to call multiple times) | Unknown — needs verification in S3 or testing |
| Integration tests can use a temporary `KNOW_DATA_DIR` | True (documented in `know` API: `data_dir` parameter) |
| `flow` and `bridge` do not yet exist (no consumers to break) | True (stubs only, no concrete usage yet) |

## Open Questions for S3

1. **`today_view` return shape**: What is the concrete structure of the dict returned by `know.today()`? Should we introduce a `TodayView` dataclass, or keep it as `dict[str, Any]` and document the shape in a docstring?

2. **`DecisionRecord` → `KnowledgeAtom` mapping**: How do we map:
   - `DecisionRecord.rationale` → `KnowledgeAtom.content`?
   - `DecisionRecord.risks` / `mitigations` → tags, or append to content?
   - `DecisionRecord.use_case_ids` → tags or connections?

3. **Initialization ownership**: Who calls `know.init()`? Should MemoryService do it lazily, or should it assume the caller (flow/bridge) has already initialized `know`?

4. **`recall_context` return type**: What is `list[Any]`? Should it be `list[KnowledgeAtom]`, `list[SearchResult]`, or something else? The Protocol says `Any` but the implementation should be concrete.

5. **Test isolation**: How do integration tests prevent state bleed between test cases when using a shared temp `KNOW_DATA_DIR`? Should each test use a unique subdirectory, or should we clear the DB between tests?

## C4 L1 Update

Not needed. No new external actors or system boundaries introduced. The integration stays within the existing system boundary (nowu ↔ know).

## Handoff
```yaml
from_step: S2
to_step: S3
agent: nowu-options
status: READY_FOR_OPTIONS
```
