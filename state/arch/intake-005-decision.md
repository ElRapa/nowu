---
id: intake-005-decision
intake_ref: intake-005
status: ACCEPTED
created: 2026-04-07
decision: "Option 1 — Multi-instance wrap"
supersedes: ~
new_decision_ref: ~
---

# Decision: intake-005 — `know` Coupling Model (D-006 / D-011 Resolution)

## 1. Decision Statement

Option 1 (multi-instance wrap) is adopted as the binding resolution of the D-006 / D-011
contradiction. nowu's `know` module instantiates one `KnowledgeBase(data_dir=project_dir)`
from the sibling library per managed project; `KnowAdapter` is refactored from a singleton
wrapper to a registry that holds N instances keyed by project identifier and implements
XP-01 cross-project federation as a fan-out loop across all live instances, merging results
in `know`-internal code. The sibling library remains the sole storage implementation —
no storage logic is added to nowu. D-006 retains ACCEPTED status; this decision appends a
binding corollary to D-006 that extends its instantiation pattern to cover the per-project
isolation model mandated by D-011. D-006 is NOT superseded.

---

## 2. ATAM Weighted Scoring Matrix

S4 applies ATAM criteria with weights 1–5 (favouring long-term health). H = 3 / M = 2 / L = 1.

| Criterion | Weight | Option 1 | Opt 1 Wtd | Option 2 | Opt 2 Wtd | Option 3 | Opt 3 Wtd |
|---|:---:|---|:---:|---|:---:|---|:---:|
| Simplicity | 3 | M(2) — registry non-trivial but bounded | 6 | M(2) — simple in nowu once upstream ships | 6 | L(1) — 27-UC storage reimplementation | 3 |
| Testability | 4 | M(2) — sibling lib is real but manageable dep | 8 | L(1) — provisional impl; hard to test until stable | 4 | H(3) — no external dep; full isolation | 12 |
| Modifiability | 4 | H(3) — KnowledgeStoreProvider Protocol isolates nowu from sibling internals | 12 | M(2) — Protocol in place but upstream coupling adds surface | 8 | H(3) — full schema control | 12 |
| Performance / Schedule | 5 | H(3) — unblocks intake-001 immediately; fan-out bounded at ≤ 20 projects | 15 | L(1) — intake-001 blocked until upstream ships; no timeline control | 5 | M(2) — unblocks immediately but 27-UC scope delays actual delivery | 10 |
| Migration cost (v2 path) | 4 | H(3) — per-`data_dir` isolation maps directly to XP-10 directory routing | 12 | M(2) — depends on upstream design; uncertainty unresolvable at S4 | 8 | H(3) — full control; schema risk during initial design | 12 |
| **Weighted total** | **20** | | **53** | | **31** | | **49** |

**Normalised (max = 60):** Option 1: 88% · Option 2: 52% · Option 3: 82%

### S3 Quality-Attribute Rescoring (S4 reclassifications)

S3 scored using four quality attributes. S4 re-evaluates two scores; others are unchanged.

| Quality Attribute | S3 Weight | Option 1 | Option 2 | Option 3 | S4 Reclassification |
|---|---|---|---|---|---|
| XP-01 satisfaction | 40% | 4 → **4** | **3 → 2** | 5 → **5** | Option 2: conditional FC-03/FC-06 satisfaction is structurally weaker than S3 scored; XP-01 cannot be confirmed satisfied until upstream adopts per-instance isolation. Score lowered from 3 to 2. |
| D-006 compatibility | 20% | 4 → **4** | 5 → **5** | 1 → **1** | No change. Option 1 requires corollary extension; S4 confirms 4 is correct for the residual ambiguity that S4 now resolves. |
| Implementation risk | 20% | 3 → **3** | **2 → 1** | 1 → **1** | Option 2: R2-1 (upstream cadence uncontrolled, HIGH) means the implementation risk is not MEDIUM — it is HIGH. Score lowered from 2 to 1 to match the risk tier. |
| v2 migration path | 20% | 5 → **5** | 3 → **3** | 4 → **4** | No change. |
| **S4 adjusted total** | | **4.00** | **2.60** (was 3.20) | **3.20** | Option 1 remains the clear winner. |

---

## 3. ATAM Sensitivity and Tradeoff Points

### Sensitivity Point SP-1 (HIGH)

Option 1's correctness on XP-01 is entirely sensitive to the fan-out merge strategy
implemented in `KnowAdapter`. A flawed deduplication algorithm or incorrectly ranked
merge of cross-project results will degrade XP-01 search quality silently — there is no
structural failure mode that would produce a test error; only semantic quality degrades.
The S5 task spec must include an explicit acceptance criterion for the merge strategy
(e.g., deterministic ranking, deduplication by atom id, stable sort across instances).

### Tradeoff Point TP-1 — Testability vs. Schedule

Option 3 scores H on testability (sibling library is fully removed; `know` tests are
self-contained). Option 1 scores M (sibling library is a real test dependency). The
tradeoff accepted: testability isolation is reduced from H to M in exchange for preserving
the delivery schedule (intake-001 unblocked) and avoiding a 27-UC storage reimplementation
that D-004's 90%+ coverage requirement would make unavoidable scope.

### Tradeoff Point TP-2 — D-006 Literal Compliance vs. Immediate Delivery

Option 2 satisfies D-006's original literal pattern (`KnowAdapter(kb)` singleton) most
cleanly. Option 1 requires extending that pattern with a corollary. The tradeoff accepted:
D-006 compatibility is H in Option 2 but extended (not violated) in Option 1, in exchange
for Option 2's Schedule score of L — indefinite blocking of intake-001 — which is
strategically unacceptable. Option 1's corollary extension is the minimal change to D-006
that makes the decision tractable.

---

## 4. S4 Judgment: Corollary vs. Supersession

**Ruling: COROLLARY. D-006 stands ACCEPTED.**

### Reasoning

**4.1 — The governing principle of D-006 is preserved in full.**

D-006's operative constraint is "No internal reimplementation in nowu." Every atom in
every project under Option 1 is stored and retrieved by a `KnowledgeBase` instance from
the sibling library. nowu adds no schema definitions, no SQLite DDL, no serialisation
logic. The sibling library is the storage system of record for all projects. The principle
is intact.

**4.2 — The singleton was an implicit assumption, not a stated principle.**

D-006 was written before D-011 existed. The per-project isolation model (one SQLite file
per project) did not exist as a binding constraint at D-006's authoring date. The
`KnowAdapter(kb)` singleton appeared because there was only one project context to
consider at the time. D-006 did not state "exactly one KnowledgeBase instance is binding";
it stated "use the sibling library's KnowledgeBase class." The number of instances is an
implementation detail of the instantiation strategy, not a stated principle.

**4.3 — The sibling library's own design supports multi-instance use.**

`KnowledgeBase(data_dir: Path)` is a regular class with no global/singleton database
state (confirmed by S2 API inspection). Multiple instances can coexist in the same process,
each scoped to a different `data_dir`. The library was designed to be multi-instantiable;
the singleton was nowu's usage pattern, not a constraint imposed by the library.

**4.4 — Supersession criteria are not met.**

A supersession is required when an original decision's LITERAL CONSTRAINT is directly
contradicted. D-006's literal constraint is "no internal reimplementation." Option 1 does
not reimplement storage. Changing the constructor signature of `KnowAdapter` from
`KnowAdapter(kb: KnowledgeBase)` to `KnowAdapter()` with lazy per-project instantiation is
an adapter implementation detail — the adapter is still wrapping the sibling library, just
more of it. This is categorically different from building a new storage layer.

**4.5 — A corollary is the correct instrument.**

A corollary is appropriate when the original decision's intent is preserved but its literal
form must be extended to cover a case it did not anticipate. That is exactly this situation:
D-011 introduced a per-project isolation constraint after D-006 was recorded; extending
D-006's instantiation pattern to cover that constraint is a clarification, not a
contradiction. D-013 is therefore NOT required.

---

## 5. Binding Corollaries

These corollaries are binding as of 2026-04-07 and extend D-006. They do not supersede
D-006; they specify how D-006 applies under D-011's per-project isolation model.

1. `KnowAdapter` holds a registry of `KnowledgeBase` instances, one per active project,
   keyed by project identifier; the singleton `KnowAdapter(kb)` pattern is replaced by
   lazy per-project instantiation (`KnowAdapter()` with `register_project(project_id,
   data_dir)` or equivalent).

2. The sibling library's `cross_project=True` flag is unused in nowu; XP-01 cross-project
   federation is implemented exclusively as a fan-out loop in `KnowAdapter`, querying each
   project's `KnowledgeBase` instance independently and merging results in nowu code.

3. Each `KnowledgeBase` instance is initialised with `data_dir` set to the project's
   isolated directory; this is the mechanism by which D-011's per-project SQLite isolation
   is satisfied — one instance = one `data_dir` = one `knowledge.db`.

4. `project_scope` tags written by the sibling library to individual atoms are treated as
   internal metadata by nowu; cross-project scope is expressed structurally (by which
   instance is queried), never by the `project_scope` field.

5. The `KnowledgeStoreProvider` Protocol in `core/contracts.py` is unchanged; all
   multi-instance complexity is encapsulated inside `know` and invisible to `flow`, `soul`,
   and `bridge`.
   
6. `know` is treated as an internal nowu boundary for all architectural purposes
   (ownership of federation, lifecycle, and contracts), while continuing to
   delegate storage implementation to the sibling `KnowledgeBase` library in v1.
   Future storage engines (for example a graph database) may be introduced behind
   the `know` boundary provided:
   - `KnowledgeStoreProvider` in `core/contracts.py` remains the sole persistence
     contract surface visible to other modules, and
   - the new storage engine fully satisfies ADR-0004 (per-project isolation +
     federation) and XP-01/XP-08 semantics.

---

## 6. Consequences

### Good
- intake-001 (Memory Integration Layer) is unblocked immediately.
- D-006's principle (sibling library = storage system of record) is preserved; no storage
  code is written in nowu.
- D-011 per-project SQLite isolation is fully satisfied by structural means (one instance
  per project), not by query-filter convention.
- XP-08 export is a directory copy of the project's `data_dir` — semantically complete by
  construction.
- v2 multi-user isolation (XP-10) is additive: directory routing inside `KnowAdapter`, no
  schema migration.

### Bad
- `KnowAdapter` registry management is non-trivial (R1-2). Instance lifecycle (create,
  cache, close) must be correct; stale handles are a resource leak.
- The sibling library at v0.4.0 has no formal API stability SLA (R1-3). A breaking change
  to `KnowledgeBase.__init__` or `search()` requires updating `KnowAdapter` with no
  automated version-gate preventing this.
- `project_scope` tags on atoms are now structurally redundant but still written by the
  sibling library. If not managed consistently, they become confusing metadata that does
  not reflect the instance-based isolation model.

### Review Trigger
- If the sibling library introduces a breaking API change to `KnowledgeBase` before v1
  ships, re-evaluate whether a formal version-pin ADR is needed.
- If XP-01 fan-out performance degrades at > 15 active projects (threshold monitoring),
  consider activating D-011's `federation-index.db` fallback without waiting for v1.1.
- If `KnowAdapter` instance lifecycle management produces resource leaks in integration
  tests, escalate to an explicit `KnowAdapter.close()` / context manager pattern before
  S8 review.

---

## 7. Contradiction Check Against D-001–D-012

| Decision | Status | Assessment |
|---|---|---|
| D-001 — File-based memory | ACCEPTED | Not affected. |
| D-002 — DDD layer architecture | ACCEPTED | **SATISFIED.** `core/contracts.py` `KnowledgeStoreProvider` Protocol unchanged; `core` remains I/O-free. Multi-instance complexity lives in `know`. |
| D-003 — 5-module structure | ACCEPTED | **SATISFIED.** No sixth module introduced. |
| D-004 — TDD non-negotiable | ACCEPTED | **SATISFIED.** Registry + fan-out is bounded scope; test coverage is achievable under existing constraints. |
| D-005 — Dedicated agents per step | ACCEPTED | Not affected. |
| D-006 — Treat `know` as external memory (storage) | ACCEPTED | **CLARIFIED by this decision's corollaries.** Singleton becomes registry; principle preserved. D-006 status remains ACCEPTED. |
| D-007 — Modular monolith for v1 | ACCEPTED | **SATISFIED.** All `KnowledgeBase` instances run in-process; no network, no IPC. |
| D-008 — Integration slices | ACCEPTED | Not affected. |
| D-009 — VBR + approval tiers | ACCEPTED | Not affected. |
| D-010 — v1 scope (NF focus + XP-01, XP-08) | ACCEPTED | **SATISFIED.** XP-01 and XP-08 remain in scope and are deliverable under Option 1. |
| D-011 — Per-project SQLite isolation | ACCEPTED | **SATISFIED.** One `KnowledgeBase` instance per project = one `data_dir/knowledge.db` per project. Federation fan-out inside `know` as required. |
| D-012 — Artifact-based soul↔flow coupling | ACCEPTED | Not affected. |

**No contradictions found with any binding decision (D-001–D-012).**
