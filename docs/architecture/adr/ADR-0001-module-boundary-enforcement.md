---
id: ADR-0001
title: Module Boundary Enforcement
date: 2026-04-06
status: ACCEPTED
superseded_by: ~
source_arch_pass: global-pass-2026-04-06
---

# ADR-0001: Module Boundary Enforcement

## Status

ACCEPTED — The architectural constraint is already operative under D-002 and D-003; this ADR formalises it as a numbered decision with explicit consequences.

## Context

nowu is structured as five modules: `core`, `flow`, `soul`, `know`, and `bridge`. Without
an explicit boundary rule, modules accumulate direct imports from each other over time,
creating coupling that is hard to detect and harder to undo. D-002 (DDD layer architecture)
and D-003 (5-module structure) both state that cross-module calls must go through
`core/contracts.py` — but neither formalises what the legal import graph looks like, what
the enforcement mechanism is, or what the consequences of violation are.

This decision must be ratified before any story that spans more than one module is shaped,
to ensure implementers have a clear rule to check against.

## Decision

ACCEPTED — The architectural constraint is already operative under D-002 and D-003; this ADR formalises it as a numbered decision with explicit consequences.

Recommended direction (derived from D-002, D-003, and global-pass-2026-04-06 P3 constraint 4):

All cross-module communication must go through types and protocols defined in `core/contracts.py`. This includes shared boundary contracts such as `KnowledgeStoreProvider`, `AdapterProtocol`,
`LLMClientConfig`, and future step-level protocols such as `PipelineStep`.

The legal import graph is:

```
flow   → core
soul   → core
know   → core
bridge → core, flow (via contracted API), know (via contracted API)
```

Direct Python imports between `flow`, `soul`, `know`, and `bridge` are forbidden. The
only permitted file-level coupling is `soul` reading/writing artifacts in `state/` paths
owned by `flow` — this is a filesystem dependency, not a Python import.

`bridge` is the only module permitted to import from `flow` and `know` — and only
through their contracted API surfaces, not from internal submodules.

## Rationale

The "artifacts are the API" principle requires that modules remain independently
deployable and testable. Direct cross-module imports short-circuit this by embedding
hidden assumptions about the importing module's internal structure. Routing all calls
through `core/contracts.py` Protocols ensures that changing a module's internals never
silently breaks a caller's assumptions.

## Consequences

**Positive:**
- Domain layer is testable in isolation without instantiating infrastructure modules.
- Each module can evolve its internals without breaking cross-module contracts.
- Import violations are statically detectable (e.g., via `import-linter` or `ruff`).

**Negative:**
- Protocol boilerplate in `core/contracts.py` grows with the API surface of each module.
- Adding a new cross-module capability requires updating `core` first (gatekeeping friction).

**Neutral:**
- `bridge` is permitted to import from `flow` and `know` because it is the integration
  layer; this is the only asymmetry in the import graph.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Direct imports allowed between any modules | Less boilerplate; faster initial development | Coupling accumulates silently; refactoring becomes exponentially harder | Violates D-002 and the testability constraint |
| Event bus for all cross-module calls | Fully decoupled; asyncable | Adds an in-process event bus dependency; overkill for a single-user CLI tool | Over-engineered for v1; deferred to post-v2 if scale requires it |
| `core/contracts.py` as Protocol boundary (recommended) | Statically typed; enforced by mypy; human-readable | Protocol boilerplate required for each new API surface | **Selected** |

## Related

- arch_pass: global-pass-2026-04-06
- decisions: D-002, D-003
- containers: all (`core`, `flow`, `soul`, `know`, `bridge`)
