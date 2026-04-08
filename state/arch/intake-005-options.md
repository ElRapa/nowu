---
id: intake-005-options
intake_ref: intake-005
status: READY_FOR_DECISION
created: 2026-04-07
recommended_option: "1"
---

# Options Sheet: `know` Coupling Model — D-006 / D-011 Resolution Spike

## Restated Decision Question

D-006 (ACCEPTED) says nowu reuses the sibling `know` library through a single
`KnowAdapter(kb)` wrapping one `KnowledgeBase` instance, with no internal
reimplementation in nowu. D-011 (ACCEPTED) requires per-project SQLite isolation and a
federation query layer inside nowu's `know` module. The sibling `KnowledgeBase` is a
per-instance class with a single-database scope; it has no built-in multi-instance
federation. These two decisions cannot both be literally true at the same time. The
question S4 must answer is: which of three coupling models reconciles this contradiction
— and does the chosen model require a superseding D-013, or only a clarifying corollary
appended to D-006?

**Key fact surfaced by S2:** The sibling library's `cross_project=True` flag does NOT
implement multi-file federation. It is a query filter within one `KnowledgeBase`
instance's single SQLite database, using `project_scope: list[str]` as an atom tag.
This is structurally identical to D-011's rejected Option A. Using the sibling library
in its current form for XP-01 would violate D-011.

---

## Option 1 — Multi-instance wrap (one `KnowledgeBase` per project in nowu)

### Description

nowu's `know` module instantiates one `KnowledgeBase(data_dir=project_dir)` per managed
project. `KnowAdapter` is refactored from a singleton wrapper to a registry: it holds N
`KnowledgeBase` instances keyed by project identifier, creates/retrieves instances lazily
on project activation, and implements XP-01 federation by fanning out search calls across
all live instances and merging results. The sibling library remains the storage
implementation for every atom — nowu adds no storage logic. `core`'s
`KnowledgeStoreProvider` Protocol is unchanged; multi-instance complexity is fully
encapsulated inside `know`. The `project_scope` field on atoms is set to a single-value
tag (the project id) on write; `cross_project=True` is unused (it would only search within
one project's database, not across them). Fan-out for XP-01 is nowu-owned orchestration.

UC coverage: XP-01 federation delivered by the nowu fan-out layer. XP-08 export is a
directory copy of the project's `data_dir` — guaranteed by isolation structure. PK-02
through PK-07 handled by the sibling library's existing atom CRUD API, unchanged.

### Constraint Satisfaction

| Constraint | Verdict | Notes |
|---|---|---|
| FC-01 — core I/O-free | SATISFIED | `core/contracts.py` Protocol unchanged; no I/O at core level |
| FC-02 — cross-module calls via contracts | SATISFIED | `KnowledgeStoreProvider` boundary unaffected; fan-out hidden inside `know` |
| FC-03 — one SQLite file per project | SATISFIED | One `KnowledgeBase` instance per project = one `data_dir/knowledge.db` per project |
| FC-04 — federation inside `know`, not a new module | SATISFIED | Fan-out loop lives inside `know`'s adapter; no new module |
| FC-05 — D-006 no-reimplementation | SATISFIED WITH COROLLARY | Sibling library is still the storage engine; `KnowAdapter` changes from singleton to registry — clarifying corollary needed, not full supersession |
| FC-06 — XP-08 export = file copy | SATISFIED | Each project's `data_dir` is a standalone directory; export is a directory copy |
| FC-07 — five-module structure | SATISFIED | No new module introduced |
| FC-08 — modular monolith, no distributed storage | SATISFIED | All `KnowledgeBase` instances run in-process |

Variable constraint affected: **VC-03** — `KnowAdapter(kb)` signature changes to
`KnowAdapter(registry)`. This is a D-006 clarification, not a supersession, if S4 agrees
that instantiation-strategy ownership is not "reimplementation" under D-006.

### Scoring

| Quality Attribute | Weight | Raw Score (1–5) | Weighted |
|---|---|---|---|
| XP-01 satisfaction | 40% | 4 | 1.60 |
| D-006 compatibility | 20% | 4 | 0.80 |
| Implementation risk | 20% | 3 | 0.60 |
| v2 migration path | 20% | 5 | 1.00 |
| **Total** | | | **4.00** |

**XP-01 (4/5):** Per-project isolation is structurally native; XP-08 file-copy guaranteed.
Fan-out must be manually implemented — correctness depends on nowu's merge strategy.

**D-006 (4/5):** Storage not reimplemented; registry change needs clarifying corollary but
not supersession — if S4 agrees. One point deducted for the ambiguity S4 must resolve.

**Risk (3/5):** MEDIUM. `KnowAdapter` registry is non-trivial (R1-2). `project_scope`
redundancy must be managed consistently (R1-1). Sibling API stability has no formal SLA
(R1-3). Scope is bounded — no storage logic written, only orchestration.

**v2 path (5/5):** Per-`data_dir` isolation maps directly to XP-10 (directory routing for
multi-user) — additive inside `know`, no schema migration.

**Sensitivity point:** Fan-out merge strategy correctness is the highest-risk implementation
detail; a flawed strategy degrades XP-01 search quality silently.

### Applicable Risks from S2

- R1-1 (MEDIUM): `project_scope` tags become redundant; must be populated consistently.
- R1-2 (MEDIUM): `KnowAdapter` constructor changes from singleton to registry; lifecycle
  management of N instances is non-trivial.
- R1-3 (MEDIUM): Sibling API stability at v0.4.0 has no formal SLA.

---

## Option 2 — Contribute federation upstream to the sibling `know` project

### Description

nowu authors a multi-instance federation capability in the sibling `know` library and
merges it there before consuming it in nowu. The sibling library would expose a new API
(e.g., `KnowledgeFederation([kb1, kb2, ...])`) that performs cross-instance fan-out
internally. nowu then consumes this API via `KnowAdapter`. D-006 is satisfied cleanly
once the sibling library ships the feature. Both projects share the same maintainer, so
this is a sequencing question, not a governance question — but the work must be designed
and implemented in the sibling library's context first, blocking nowu's intake-001 for
the duration. The federation model chosen in the sibling library must adopt per-instance
isolation (not `project_scope` tagging on a shared DB) to satisfy FC-03 and FC-06.

### Constraint Satisfaction

| Constraint | Verdict | Notes |
|---|---|---|
| FC-01 — core I/O-free | SATISFIED | `KnowledgeStoreProvider` Protocol unchanged |
| FC-02 — cross-module calls via contracts | SATISFIED | Boundary unaffected |
| FC-03 — one SQLite file per project | CONDITIONAL | Satisfied only if upstream adopts per-instance isolation |
| FC-04 — federation inside `know`, not a new module | SATISFIED | Federation in sibling library; `know` consumes it |
| FC-05 — D-006 no-reimplementation | SATISFIED | Sibling library implements federation; nowu does not |
| FC-06 — XP-08 export = file copy | CONDITIONAL | Requires per-instance isolation in upstream design |
| FC-07 — five-module structure | SATISFIED | No new module |
| FC-08 — modular monolith | SATISFIED | Sibling library remains in-process dependency |

### Scoring

| Quality Attribute | Weight | Raw Score (1–5) | Weighted |
|---|---|---|---|
| XP-01 satisfaction | 40% | 3 | 1.20 |
| D-006 compatibility | 20% | 5 | 1.00 |
| Implementation risk | 20% | 2 | 0.40 |
| v2 migration path | 20% | 3 | 0.60 |
| **Total** | | | **3.20** |

**XP-01 (3/5):** FC-03/FC-06 satisfaction is conditional on upstream design choice. If
sibling adopts shared-DB federation (the model D-011 rejected), both constraints break.

**D-006 (5/5):** Cleanest satisfaction of D-006 as written. No supersession needed.

**Risk (2/5):** HIGH. intake-001 serialized behind upstream work. Federation API must be
stable before nowu can write consuming code. Even same-maintainer cannot eliminate delay.

**v2 path (3/5):** Depends entirely on upstream design choice; uncertainty unresolvable at S3.

### Applicable Risks from S2

- R2-1 (HIGH): Sequencing delay; intake-001 blocked until sibling federation ships.
- R2-2 (MEDIUM): Federation API contract must stabilize before nowu consuming code.
- R2-3 (LOW): D-006 version reference must be updated on first consumption.

---

## Option 3 — Decouple from sibling: nowu builds its own storage layer

### Description

nowu's `know` module implements per-project SQLite files directly (using Python `sqlite3`
or SQLAlchemy). Sibling library storage layer abandoned. `KnowAdapter` reimplemented from
scratch. D-006 is unambiguously superseded — S4 must issue D-013 before this option is
valid. nowu owns all 27 UCs' storage implementation, all storage tests, and all schema
evolution. The sibling library may still supply domain type schemas (`KnowledgeAtom`,
`EpistemicGrade`) but not storage — a fragile partial dependency (R3-3).

### Constraint Satisfaction

| Constraint | Verdict | Notes |
|---|---|---|
| FC-01 — core I/O-free | SATISFIED | `KnowledgeStoreProvider` Protocol can still be pure |
| FC-02 — cross-module calls via contracts | SATISFIED | Boundary unaffected |
| FC-03 — one SQLite file per project | SATISFIED | nowu controls schema and file layout |
| FC-04 — federation inside `know` | SATISFIED | Fan-out inside nowu's `know` module |
| FC-05 — D-006 no-reimplementation | VIOLATED — requires D-013 | Hard gate; S4 must supersede D-006 |
| FC-06 — XP-08 export = file copy | SATISFIED | nowu controls file layout |
| FC-07 — five-module structure | SATISFIED | No new module |
| FC-08 — modular monolith | SATISFIED | All storage in-process |

### Scoring

| Quality Attribute | Weight | Raw Score (1–5) | Weighted |
|---|---|---|---|
| XP-01 satisfaction | 40% | 5 | 2.00 |
| D-006 compatibility | 20% | 1 | 0.20 |
| Implementation risk | 20% | 1 | 0.20 |
| v2 migration path | 20% | 4 | 0.80 |
| **Total** | | | **3.20** |

**XP-01 (5/5):** Maximum design control; D-011 semantics guaranteed; XP-08 by construction.

**D-006 (1/5):** Unambiguous supersession required. Not a clarification.

**Risk (1/5):** VERY HIGH. 27 UCs include complex storage: graph relationships (AP-03,
XP-03), TTL decay (PK-04), versioning (AP-02), ingestion pipeline (PK-07) — all currently
tested by the sibling library. D-004 (90%+ TDD) makes full reimplementation non-negotiable
scope for a solo + AI team.

**v2 path (4/5):** Maximum schema control but higher risk of early schema errors.

### Applicable Risks from S2

- R3-1 (HIGH — blocking): D-006 violation without D-013 is a hard gate.
- R3-2 (HIGH): 27 UC storage scope is severe for solo + AI team.
- R3-3 (MEDIUM): Type-only reuse of sibling library is a fragile half-dependency.

---

## Weighted Ranking

| Option | XP-01 (×0.4) | D-006 (×0.2) | Risk (×0.2) | v2 path (×0.2) | **Total** |
|---|---|---|---|---|---|
| **1 — Multi-instance wrap** | 4 → 1.60 | 4 → 0.80 | 3 → 0.60 | 5 → 1.00 | **4.00** |
| 2 — Contribute upstream | 3 → 1.20 | 5 → 1.00 | 2 → 0.40 | 3 → 0.60 | 3.20 |
| 3 — Decouple / replace | 5 → 2.00 | 1 → 0.20 | 1 → 0.20 | 4 → 0.80 | 3.20 |

Option 1 is the clear winner. Options 2 and 3 tie at 3.20 with inverted strength/weakness profiles.

---

## S3 Recommendation

**Recommend Option 1 — Multi-instance wrap.**

Strongest reason: the only option that satisfies FC-03 (per-project isolation), FC-06
(XP-08 file-copy), and XP-10 v2 migration path with certainty — while still using the
sibling library for all atom storage as D-006 intends, without blocking intake-001 (Option
2's risk) or requiring D-013 (Option 3's hard gate). `KnowAdapter` registry complexity
(R1-2) is bounded and manageable. Fan-out is nowu-owned orchestration, not storage
reimplementation.

---

## Open Question for S4

**Does D-006's `KnowAdapter(kb)` singleton-to-registry transition constitute:**
- **(a) A clarifying corollary** — D-006 absorbs it; storage is still the sibling library;
  nowu adds instantiation strategy and fan-out orchestration only. No supersession.
- **(b) A superseding change** — adapter shape is structurally different from D-006's
  literal `KnowAdapter(kb)`; a D-013 is warranted.

S3 reads this as (a): D-006's intent was "do not rewrite the storage layer," and Option 1
satisfies that intent precisely. S4 must declare which interpretation is binding — the output
format differs: amendment corollary vs. full D-013 entry in DECISIONS.md.