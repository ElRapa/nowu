# Idea: `know` as a Semantic Code Property Graph

> Status: FUTURE — target v2+
> Origin: Research into CPG and C4, conversation 2026-03-15

## The Concept
When `know` stores typed atoms with typed edges, it becomes a lightweight
semantic CPG — queryable at any abstraction level.

## Atom Types (mapping to C4 levels)
- `VISION` → L1 (upper diamond)
- `USE_CASE` → L1 (upper diamond)
- `DECISION` → Equator (with `level` field)
- `MODULE` → L2
- `PROTOCOL` → L3 (interface/contract)
- `CLASS` → L3
- `FUNCTION` → L4
- `TEST` → L4

## Edge Types
- `DRIVES` (DECISION → MODULE): this decision created this module boundary
- `IMPLEMENTS` (CLASS → PROTOCOL): this class implements this protocol
- `CALLS` (FUNCTION → FUNCTION): call graph
- `FLOWS_TO` (VARIABLE → FUNCTION): data flow (PDG-style)
- `TESTS` (TEST → FUNCTION): test covers this function
- `DEPENDS_ON` (MODULE → MODULE): C4 L2 dependency edge

## Query Power
```python
# C4 L2 view — which modules does `flow` depend on?
know.subgraph(from_atom="MODULE:flow", edge_types=["DEPENDS_ON"], depth=1)

# Validation trace — what use case drives this function?
know.path(from_atom="FUNCTION:recover", to_atom="USE_CASE:*")

# Impact analysis — what breaks if MemoryService changes?
know.dependents(atom="PROTOCOL:MemoryService", edge_types=["IMPLEMENTS", "CALLS"])
```

## Migration Path
v1: Files as atoms (today) — `know` stores file references, not code structure
v2: Module atoms — MODULE, PROTOCOL nodes, DEPENDS_ON edges (from contracts/)
v3: Component atoms — CLASS, FUNCTION nodes from AST parsing
v4: Full CPG — CALLS + FLOWS_TO edges from CFG/PDG analysis

## Why Not Full CPG Now
Tools like Joern or Fraunhofer CPG library are powerful but heavyweight.
The AST-based architecture tests already give 80% of the boundary enforcement
value with 5% of the complexity. Build the graph incrementally as `know` matures.
