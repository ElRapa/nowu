# GLOBAL-MODEL - C4 Model and Code Property Graph — nowu Reference

## C4 Model (primary — use today)

Simon Brown's C4 Model provides four zoom levels for software architecture.
Each level answers a different question and serves a different audience.

| Level | Name | Question | Audience | nowu Artifact |
|-------|------|----------|----------|---------------|
| L1 | System Context | What does the system do? Who uses it? | Stakeholders | ARCHITECTURE.md §1 |
| L2 | Container (Module Map) | How do modules interact? | Architect, Shaper | ARCHITECTURE.md §4.1 |
| L3 | Component | What files/classes exist? | Shaper, Implementer | contracts/ + file tree |
| L4 | Code | How does it work internally? | Implementer, Reviewer | source code itself |

**Which step uses which level:**
- S1-S2: L1 (system boundary, actors)
- S3-S4: L2 (module interactions, options)
- S5, S8: L3 (file/class map, review diff)
- S6-S7: L4 (code, tests, AST boundary check)

**Practical C4 for nowu v1:**
- L1: described in ARCHITECTURE.md §1 (human, no external systems yet)
- L2: the 5-module diagram in ARCHITECTURE.md §4.1 (update at S4/S9 if boundaries change)
- L3: `core/contracts/*.py` Protocol files ARE the component graph
- L4: `tests/unit/core/test_architecture.py` uses AST to enforce import boundaries

## Code Property Graph (future — via `know`)

A CPG merges three code representations into one queryable supergraph:
- **AST** (Abstract Syntax Tree): syntactic structure — what the code *says*
- **CFG** (Control Flow Graph): execution order — *when* things run
- **PDG** (Program Dependence Graph): data dependencies — *what flows where*

CPG enables cross-cutting queries impossible with any single representation,
e.g. "show all paths from user input to file write" or "what functions depend
on MemoryService?"

**Today (v1):** Lightweight CPG-adjacent — AST-based import boundary tests.
**Future (v2+):** `know` stores code atoms with typed edges (CALLS, FLOWS_TO,
IMPLEMENTS) enabling `kb.subgraph(from="MODULE:flow", depth=3)` to return
a queryable C4 L2 view without loading raw files.

## Why C4 Beats CPG for Visualisation

CPG is a machine analysis tool — it was never designed for human motivation.
C4's explicit L1→L4 zoom narrative, combined with the Octahedron model, gives
you the "filling pyramid" feeling that makes progress visible. Use C4 for all
diagrams and communications. Use CPG-style analysis only when `know` can serve it.

## Pyramid Fill-In Tracker

Track which C4 layers have been materialised per module:

| Module | L1 (boundary) | L2 (interactions) | L3 (contracts) | L4 (impl) |
|--------|--------------|-------------------|----------------|-----------|
| core   | ✅ | ✅ | ✅ (Step 01) | 🔄 in progress |
| flow   | ✅ | ✅ | 🔲 | 🔲 |
| bridge | ✅ | 🔲 | 🔲 | 🔲 |
| soul   | ✅ | 🔲 | 🔲 | 🔲 |
| know   | ✅ | 🔲 | 🔲 | 🔲 |

Update this table in S9 Capture after each completed task.
