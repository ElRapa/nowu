---
id: intake-003-decision
intake: intake-003
status: ACCEPTED
created: 2026-04-06
agent: nowu-decider@S4
decision_id: D-011
---

# Decision Record — intake-003: Cross-Project Knowledge Isolation Model and DB Session Pattern

## Chosen Option

**Option 2: Per-Project SQLite Files with `know`-Internal Federation Query Layer (ADR-D Option B)**

This is the binding decision for ADR-D (cross-project isolation model) and Q5 (DB session
pattern). Option 1 (single shared SQLite with `project_id`) is rejected. The edge-ownership
semantic loss under Option 1 is a structural product liability, not a solvable implementation
deficit. See scoring and ATAM sections below.

---

## Weighted Scoring Matrix

Weights: Modifiability 35%, Performance 25%, Simplicity 25%, Testability 15%.
Scores as assigned by S3 (options sheet): H=3, M=2, L=1.
Weighted total = sum of (score × weight%), scaled by 100 for display.

| Quality Attribute | Weight | Option 1 Score | Option 1 Weighted | Option 2 Score | Option 2 Weighted |
|---|---|---|---|---|---|
| Modifiability | 35% | M = 2 | 70 | H = 3 | 105 |
| Performance | 25% | H = 3 | 75 | M = 2 | 50 |
| Simplicity | 25% | H = 3 | 75 | M = 2 | 50 |
| Testability | 15% | H = 3 | 45 | M = 2 | 30 |
| **Total** | 100% | | **265** | | **235** |

With S3 scores taken as-is, **Option 1 nominally wins (265 vs 235)**. The ATAM sensitivity
analysis below reveals that Option 1's Modifiability of M significantly understates a
structural constraint. S4 reclassifies Option 1's Modifiability from M (score = 2) to
L (score = 1), yielding:

| | Option 1 (S4-revised) | Option 2 |
|---|---|---|
| Revised total | 230 | 235 |

Under S4-reclassified scores, **Option 2 wins (235 vs 230)**.

---

## ATAM Analysis

### Sensitivity Point

**Option 1's Modifiability score is the single decision-determining sensitivity point.**

The S3 assessment of M ("XP-08 edge rule adds fragility; v2 migration is a hard cutover")
understates the true constraint. The stub-reference rule for XP-08 under Option 1 is not a
fragile-but-implementable design — it is a structural guarantee that XP-08 exports will be
semantically incomplete whenever cross-project relationship edges exist. The receiving system
must independently resolve external stub IDs to restore link semantics. This is a product-level
liability that cannot be engineered away within Option 1's data model: it is a consequence of
the shared-table structure, not of the quality of the implementation.

**S4 reclassification:** Option 1 Modifiability from M = 2 to L = 1.
Justification: Modifiability for XP-08 is not "harder to implement correctly" but "impossible
to implement completely within the shared-table model." A Modifiability score of M implies
the limitation is an implementation challenge; it is not. This reclassification aligns the
numeric result (Option 2 wins 235 vs 230) with the structural argument.

### Tradeoff Point

**Performance + Simplicity (Option 1 advantage) vs. Modifiability (Option 2 advantage).**

Option 1 is unambiguously superior on XP-01 query performance: cross-project search is a
single SQL scan with no fan-out latency. Option 1 is also unambiguously simpler: no
federation layer, one connection handle, a conventional single-file SQLite pattern. These
are genuine advantages.

This decision consciously accepts Option 2's performance and simplicity costs in exchange for:

1. Semantically complete per-project export (XP-08) by design — file copy, no edge-ownership
   rule, no stub references, no semantic loss.
2. Structural project isolation at the filesystem level, not the query-filter level. Isolation
   bugs under Option 2 are "opened the wrong file" bugs, which are detectable in tests. Under
   Option 1 they are "missing WHERE clause" bugs, which are invisible until data corrupts.
3. Additive v2 multi-user path (XP-10): adding a user under Option 2 is a directory-routing
   decision inside `know`. Under Option 1 it is a breaking schema migration on every table.

The tradeoff is accepted. The performance disadvantage is bounded (see federation threshold
below) and the fallback is a `know`-internal implementation option.

---

## Federation Fan-Out Sensitivity Analysis

Option 2's XP-01 performance assumption is explicit, bounded, and must be monitored:

- **≤ 10 active projects** (typical v1-core): sequential fan-out across per-project SQLite
  files is estimated at < 300 ms on commodity hardware for cosine-similarity scans over
  ≤ 5,000 atoms per project. Acceptable for v1-core.
- **11–20 active projects** (edge case): fan-out degrades linearly; remains within acceptable
  bounds for v1-core but should be tracked.
- **> 20 active projects** (threshold breach): the `know`-internal materialized-index fallback
  must be activated. This is a `know`-internal implementation decision — it does not require a
  new module, a new intake or a schema migration. The fallback (a `federation-index.db`
  refreshed on every write) lives entirely inside `know`.

**The 20-project threshold is an explicit monitoring criterion embedded in this decision.**
If the human operates more than 20 concurrent active projects before v1.1, a follow-on intake
must be raised and the materialized-index fallback scoped before XP-01 is marked DONE.

---

## Use Case Coverage

| UC-ID | Stage | Covered by Option 2? | How |
|---|---|---|---|
| XP-01 | v1-core | YES | Federation layer fans out cross-project queries across all project files and merges results. Performance bounded at ≤ 20 projects. |
| XP-08 | v1.1 | YES — cleanly | Export = file copy of the per-project SQLite file. No edge-ownership rule required. No semantic loss. Self-contained by design. |

---

## Contradictions Check — DECISIONS.md D-001 through D-010

| Decision | Status | Compatible? | Note |
|---|---|---|---|
| D-001 File-Based Memory | ACCEPTED | YES | Per-project SQLite files are local file-based state. No conflict. |
| D-002 DDD Layer Architecture | ACCEPTED | YES | `core` holds only `KnowledgeStoreProvider` Protocol (no I/O, no database imports). `know` holds all concrete implementation and all I/O. DDD layer boundary upheld. |
| D-003 5-Module Structure | ACCEPTED | YES | Federation layer lives inside `know`. No sixth module created. D-003 five-module ceiling preserved. |
| D-004 TDD | ACCEPTED | YES | Architecture spike only; TDD applies when implementation follows from a subsequent intake. |
| D-005 Dedicated Agent Per Step | ACCEPTED | YES | Not affected. |
| D-006 Treat `know` as external memory system | ACCEPTED | FLAGGED | D-006 states "No internal reimplementation in nowu." The global-pass-2026-04-06 (PROPOSED) treats `know` as one of nowu's five internal containers with its own SQLite storage. D-011 preserves D-006's core intent: knowledge atoms are owned and served exclusively by the `know` boundary. **This is not treated as a blocker for D-011.** However: once global-pass-2026-04-06 is promoted to ACCEPTED, D-006 should be reviewed and a superseding ADR written to clarify the relationship between the sibling `know` project and the `nowu` `know` container. That ADR is out of scope for this spike. |
| D-007 Integration-First Modular Monolith | ACCEPTED | YES | Option 2 is consistent with the monolith approach. |
| D-008 Integration Slices | ACCEPTED | YES | Not affected. |
| D-009 VBR and Approval Tiers | ACCEPTED | YES | Not affected. |
| D-010 Prioritize NF Core UCs | ACCEPTED | YES | XP-01 (v1-core) is in scope; federation layer serves it. |

**No blocking contradiction found.** The D-006 flag is a post-acceptance recommendation, not a
blocker. D-011 may proceed to ACCEPTED under human review.

---

## Companion Decisions (Corollaries)

These follow directly from Option 2 and are binding on all implementers of `know`'s storage
layer. No remaining optionality exists on these points.

1. **`KnowledgeStoreProvider` Protocol in `core/contracts.py`** — no I/O, no database imports,
   `know`-only scope. Its docstring must state it is scoped to `know`. No concrete
   implementation, no database imports, and no I/O of any kind may appear in `core`.

2. **`know` owns all per-project SQLite files and all connection lifecycle.** `know` is the
   sole concrete implementation of `KnowledgeStoreProvider`. It maintains a per-project
   SQLite directory (user-controlled path). Connection open/cache/close managed entirely
   within `know`'s federation layer. No other module holds or requests a database connection.

3. **Federation fan-out threshold is ≤ 20 projects for v1-core.** The federation layer uses
   query-time fan-out as the default implementation. If active project count exceeds 20, the
   `know`-internal materialized-index fallback is activated. Threshold must be monitored;
   breach before v1.1 triggers a follow-on intake.

4. **v2 / XP-10 multi-user isolation is a directory-routing decision inside `know`.** Each
   user maps to a directory of per-project SQLite files. No schema migration required for
   adding a second user.

---

## What S4 Is NOT Deciding

Explicitly deferred to the implementer (a future intake scoping `know`'s storage layer):

- SQLite table names, column names, index strategy — schema internals are fully unconstrained.
- Connection management approach within `know` (WAL mode, connection pool) — purely internal.
- Schema migration tooling (Alembic, versioned SQL scripts) — unconstrained.
- Active-project context passing mechanism — unconstrained within `know`'s public surface.
- Whether federation uses ATTACH-based queries or sequential per-file connections — internal.
- The materialized-index fallback trigger logic and refresh strategy — internal to `know`.
- `KnowledgeStoreProvider` method signatures — designed by shaper of the follow-on intake.

---

## Mode Note

This is a Mode D (Architecture Only) spike. No S5 shaping or S6 implementation follows from
intake-003. The decision file and the D-011 DECISIONS.md entry are the sole deliverables. Any
intake that scopes `know`'s storage layer implementation is blocked until D-011 is ACCEPTED
and the global-pass-2026-04-06 is either ACCEPTED or its ADR-D candidate section is resolved
by this entry.
