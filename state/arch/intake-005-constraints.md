---
id: intake-005-constraints
intake_ref: intake-005
status: READY_FOR_OPTIONS
created: 2026-04-07
arch_pass_ref: ~
---

# Constraints Sheet: intake-005 — `know` Internal vs. External (D-006 Resolution Spike)

> Mode D (Architecture Only) spike. No implementation in scope. Output feeds S3 options evaluation only.
> No pre-workflow arch-pass exists for intake-005. Constraints derived cold.

---

## 1. Fixed Constraints

Constraints that cannot be changed without a superseding ACCEPTED decision or ADR. S3 must
treat these as hard walls — options that violate them are invalid absent a new ADR.

**FC-01 — DDD layer boundary: `core` must be I/O-free (D-002, ADR-0004 Q5 corollary)**
`core/contracts.py` defines `KnowledgeStoreProvider` as a pure Python Protocol with no
database library imports and no I/O of any kind. This is binding. Any option that causes
`core` to import SQLite libraries, instantiate database connections, or hold file handles
violates D-002 and ADR-0004 simultaneously. All three options (Option 1, 2, 3) must
preserve a `core`-level Protocol boundary; the concrete implementation must live in `know`.

**FC-02 — All cross-module calls go through `core/contracts.py` (D-002, D-003, ADR-0001)**
`flow`, `soul`, and `bridge` may not import from `know`'s internals. They may only call the
`KnowledgeStoreProvider` Protocol defined in `core`. This constraint applies regardless of
whether `know` internally wraps the sibling library, contributes upstream, or reimplements
its own storage. The public-facing API shape must remain `KnowledgeStoreProvider`-conformant
under all three options.

**FC-03 — Per-project SQLite isolation: one file per project (D-011, ADR-0004, ACCEPTED)**
D-011 Option B is ACCEPTED. Per-project SQLite files are binding. Any option that causes
nowu's `know` module to maintain a single shared SQLite across all projects (i.e., reverts
to D-011 Option A semantics) contradicts a binding ACCEPTED decision. This rules out a
naive single-instance adoption of the sibling `KnowledgeBase` class pointed at a single
`data_dir` serving all projects.

**FC-04 — Federation query layer must be `know`-internal, not a new module (D-011, ADR-0004)**
D-011 explicitly states: "A federation query layer inside `know` — not a new module — fans
out XP-01 cross-project queries." Creating a separate `federation` module, a `federation`
package under `core`, or any top-level module other than the five defined in D-003 violates
this constraint. All three options must implement or delegate fan-out within `know`.

**FC-05 — D-006 "no reimplementation" constraint (D-006, ACCEPTED — possibly to be superseded)**
D-006 states: "Reuse the existing sibling project `know` (v0.4.0) through `KnowledgeBase`
class API and `KnowAdapter(kb)`. No internal reimplementation in nowu." This is an ACCEPTED
binding decision. Option 3 (decouple/replace) explicitly contradicts D-006 as written and
cannot be evaluated as valid unless S4 produces a superseding decision (D-013 or equivalent).
Options 1 and 2 must be evaluated for whether they satisfy D-006 or merely approximate it.
The spike's primary output is whether D-006 stands, is clarified, or is superseded.

**FC-06 — XP-08 export must be a file-copy (D-011, ADR-0004, ACCEPTED)**
D-011 rationale explicitly chose Option B to ensure "a full project export for XP-08 is a
file copy — semantically complete by design, with no edge-ownership rules or stub
references." Any option that reintroduces cross-project edge-ownership ambiguity (e.g.,
atoms tagged with multi-project `project_scope` where a single export cannot be cleanly
bounded) breaks the XP-08 semantic guarantee. This constraint directly bears on whether the
sibling library's `project_scope` tagging model can satisfy XP-08 or whether per-instance
isolation is required.

**FC-07 — Five-module structure is fixed; no new top-level module (D-003, ACCEPTED)**
D-003 defines five modules: `core`, `flow`, `soul`, `know`, `bridge`. No sixth module may
be created for federation, storage abstraction, or sibling-library integration without a
superseding decision. All implementation, wherever the storage logic ultimately lives,
must fit within `know` (for storage and federation) and `core` (for contracts).

**FC-08 — Modular monolith for v1; no distributed storage (D-007, ACCEPTED)**
D-007 mandates an integration-first modular monolith for v1. Approaches that require network
calls, separate processes, or inter-process communication for knowledge storage queries are
out of scope for v1. The sibling `know` library is a local in-process dependency; it must
remain so under Options 1 and 2.

---

## 2. Variable Constraints

Real constraints that could be relaxed by a superseding ACCEPTED decision. S3 must note
which option requires relaxation of which variable constraint.

**VC-01 — D-006 "no reimplementation" (D-006, candidate for supersession)**
D-006 is the primary variable constraint. It can be superseded by S4 producing D-013.
- Option 1 (multi-instance wrap): likely satisfies D-006 without supersession; the sibling
  library is still the storage implementation. Whether "owning the instantiation pattern"
  constitutes reimplementation is a judgment S3 must surface.
- Option 2 (contribute upstream): clearly satisfies D-006 once the upstream library ships
  the federation capability; risk is the dependency on sibling project development cadence.
- Option 3 (decouple/replace): unambiguously supersedes D-006. S4 must issue D-013 before
  Option 3 is valid. S3 must evaluate whether the benefits justify a binding supersession.

**VC-02 — Sibling library version lock (operational, not formally decided)**
D-006 references v0.4.0. There is no formal version-lock ADR, but the intent of D-006 is
to consume the sibling library at a specific version. If Option 2 is chosen (contribute
upstream), nowu must consume a newer version of the sibling library — the version reference
in D-006 becomes stale. S4 would need to either update D-006's version reference or
supersede it, and a `pyproject.toml` dependency constraint must be updated accordingly.

**VC-03 — KnowAdapter wrapper pattern (D-006 corollary, not separately decided)**
D-006 specifies `KnowAdapter(kb)` as the coupling pattern. Under Option 1 (multi-instance),
`KnowAdapter` would wrap multiple `KnowledgeBase` instances instead of one — the adapter
interface persists but its internal implementation changes significantly. Under Options 2
and 3 the adapter's shape changes further. This is a variable constraint because it is
derived from D-006 and moves with it; no separate ADR governs adapter implementation.

---

## 3. Key Risks

### Option 1 — Multi-instance wrap (one `KnowledgeBase` per project)

**R1-1: Semantic risk — `project_scope` becomes redundant but harmful (MEDIUM)**
The sibling library uses `project_scope: list[str]` for multi-project tagging within one
database. If nowu instantiates one `KnowledgeBase` per project, `project_scope` is
structurally redundant — each instance is already scoped by its `data_dir`. However, the
sibling library may still write `project_scope` tags internally, and the `cross_project=True`
search API queries all atoms in a single database — which in a per-instance model is just
one project's atoms. XP-01 fan-out must be implemented in nowu's `know` module, not via
`cross_project=True`. S3 must verify that `cross_project=True` is either unused or benign
in the multi-instance model.

**R1-2: `KnowAdapter` must manage a dynamic registry of instances (MEDIUM)**
`KnowAdapter(kb)` was designed for a single `KnowledgeBase` instance. Under multi-instance,
the adapter must hold a registry of instances keyed by project identifier, create new
instances lazily (or eagerly at project bootstrap), and fan out search calls. This changes
the adapter's constructor signature and lifecycle management significantly. It is not
reimplementation of storage, but it is non-trivial wrapper complexity.

**R1-3: Sibling library API stability at v0.4.0 (MEDIUM)**
v0.4.0 has no stated semantic versioning guarantee in this workspace. If the sibling library
changes `KnowledgeBase.__init__` or `search()` signatures between now and nowu's
implementation, multi-instance wrapping breaks silently. No formal API stability contract
exists.

**R1-4: Fan-out query performance under ≤ 20 project threshold (LOW for v1-core)**
D-011 accepts bounded fan-out at ≤ 20 projects. Under multi-instance wrap, each fan-out
query opens N SQLite connections in the Python process. This is likely acceptable at ≤ 20
but must be validated. Connection pooling per instance is an implementation concern for S6,
not a constraint for S3 — but S3 must note the performance bound.

### Option 2 — Contribute federation upstream

**R2-1: Upstream development cadence is uncontrolled (HIGH)**
Option 2 requires the sibling `know` project to accept and implement multi-instance
federation. The sibling project's backlog, design preferences, and review process are
outside nowu's decision scope. This intake cannot compel the sibling project. If the
sibling project declines the feature or delays it, intake-001 remains blocked indefinitely.
This is the dominant risk for Option 2.

**R2-2: API contract for federation must be agreed across two projects (MEDIUM)**
Contributing upstream requires agreement on the federation API shape before nowu can write
its consuming code. Until the sibling library ships and stabilizes the feature, nowu's
`know` module implementation is provisional. This creates a dependency that is hard to
express in `pyproject.toml` and harder to test.

**R2-3: D-006 version reference becomes stale immediately (LOW)**
Consuming an upgraded sibling library version requires updating D-006 or superseding it.
This is procedurally straightforward but must not be forgotten — leaving a stale version
reference in a binding decision is a documentation correctness risk.

### Option 3 — Decouple / replace sibling library

**R3-1: D-006 violation without supersession (HIGH — blocking)**
Option 3 is architecturally invalid without a S4-issued superseding decision. This is not
a risk to mitigate — it is a hard gate. S3 must evaluate Option 3 under the assumption
that S4 will issue D-013 superseding D-006. If S3 cannot make a strong case for D-013,
Option 3 must be rejected in S3's evaluation.

**R3-2: Reimplementation scope risk — 27 UCs require significant storage capability (HIGH)**
`know` owns 27 UCs including atom versioning (AP-02), relationship graph (AP-03, XP-03),
sensitivity tagging (PK-06), TTL and decay (PK-04), ingestion pipeline (PK-07), and export
(XP-08). Reimplementing atom storage from scratch carries significant scope and maintenance
risk for a solo + AI team.

**R3-3: Schema and serialisation reuse ambiguity (MEDIUM)**
D-006 could be partially preserved by treating the sibling library as a source of domain
types only (`KnowledgeAtom`, `EpistemicGrade`, etc.) without using its storage layer.
Whether this constitutes "no reimplementation" is ambiguous — taking types but not storage
is a partial dependency that may create its own coupling problems without providing the
library's tested storage implementation. S3 must assess whether type-only reuse is a
meaningful middle ground or an unstable half-measure.

**R3-4: Test ownership of the storage layer shifts entirely to nowu (MEDIUM)**
Under Option 3, nowu owns all storage tests. Under Options 1 and 2, the sibling library's
test suite covers the storage implementation. This is a test maintenance cost increase
under Option 3 that D-004 (TDD, 90%+ coverage) makes unavoidable.

---

## 4. Sibling `know` API Surface Summary

Based on the pre-surfaced code inspection of `/Users/Raphael.Weidemann/Projects/know/` at v0.4.0.
S3 may use this summary directly without re-reading source.

**`KnowledgeBase(data_dir: Path)`**
Instantiable class. Each instance manages its own SQLite file at `data_dir`. Multiple
instances can coexist in the same process, each pointed at a different `data_dir`. There is
no global/singleton database state.

**Atom CRUD**
`KnowledgeBase` provides create, read, update, and delete operations for knowledge atoms.
Each atom carries: content, `project_scope: list[str]` (multi-project tag), `EpistemicGrade`
confidence classification, temporal metadata, and relationship references.

**`project_scope: list[str]`**
A multi-project tag on each atom within a single `KnowledgeBase` instance. In the library's
native (single-instance) usage model, this is the mechanism for isolating and querying atoms
by project within one shared SQLite file. In a per-instance model (Option 1), this field is
structurally redundant — all atoms in an instance implicitly belong to one project by virtue
of being in that instance's `data_dir`.

**`search(query, cross_project=False)`**
`cross_project=True` removes the `project_scope` filter and queries all atoms in the
instance's single SQLite database. In the library's native single-instance model, this
achieves "search everything" across all tagged projects. In a multi-instance model (Option
1), `cross_project=True` queries all atoms within one instance's database — which is just
one project. XP-01 federation in the multi-instance model cannot rely on this flag; it
requires nowu to fan out across instances manually.

**`KnowAdapter(kb: KnowledgeBase)`**
Adapter wrapper around a single `KnowledgeBase` instance. Provides the interface expected
by D-006 as the boundary through which nowu modules interact with the `know` library.
Current signature requires exactly one `KnowledgeBase` instance. Multi-instance usage would
require a constructor change (`KnowAdapter` taking a registry rather than a single `kb`).

**No built-in federation layer**
The sibling library at v0.4.0 has no multi-instance federation. Cross-database fan-out is
not implemented. `cross_project=True` operates within a single database, not across
multiple `data_dir` instances.

**Stable in practice, no formal SLA**
v0.4.0 has been in use for nowu planning. No semantic versioning guarantee or stability
commitment exists in the sibling project's documentation.

---

## 5. Questions S3 Must Answer

**Q1: Does Option 1 satisfy D-006 as written?**
D-006 says "no internal reimplementation in nowu." Using the sibling library for all atom
storage while nowu owns the instantiation strategy and fan-out orchestration is not storage
reimplementation — but it is pattern ownership. S3 must determine whether D-006's intent is
"do not rewrite the storage layer" (Option 1 satisfies) or "do not own any knowledge
persistence logic whatsoever" (Option 1 may not satisfy, requiring D-006 clarification).

**Q2: Is `project_scope` tagging on atoms a liability in the multi-instance model?**
Under Option 1, atoms in a per-project `KnowledgeBase` instance will still carry
`project_scope` tags — either empty, set to a single value, or potentially inconsistent.
Does the sibling library enforce population of `project_scope`? If so, nowu must supply a
value. If the field is populated inconsistently, does it create confusion in XP-11
(role-appropriate query rendering) or XP-05 (performance at scale)? S3 must surface this
as a semantic coherence concern.

**Q3: Is Option 2 gated by the sibling project's decision process?**
The intake notes that both projects share a workspace but are separate codebases. S3 must
determine: is there a known contribution process for the sibling `know` project? Is the
maintainer (also Raphael Weidemann) able to unilaterally add federation to the sibling
library? If yes, Option 2 collapses to a sequencing question (implement in sibling first,
then consume), not a governance question. This changes Option 2's risk profile significantly.

**Q4: Does Option 3 (type-only reuse) constitute reimplementation under D-006, and does it
deliver sufficient benefit to justify D-013?**
If Option 3 uses only `KnowledgeAtom`, `EpistemicGrade`, and schema types from the sibling
library — but implements its own SQLite layer — it still imports from the sibling library.
S3 must evaluate: (a) whether this is a meaningful split (stable types, replaceable
storage), (b) whether the sibling library's types are stable enough to serve as a contract
boundary, and (c) whether the net benefit over Option 1 justifies the cost of a superseding
D-013 and full storage ownership.

**Q5: Which option best positions nowu for XP-08 export semantics?**
D-011 guarantees XP-08 export = file copy. Under Option 1 (multi-instance), this holds
because each project IS a separate `data_dir`; export is trivially a copy of that directory.
Under Option 2 (same), provided the upstream library adopts per-instance semantics. Under
Option 3 (own storage), this is a design responsibility nowu must explicitly discharge.
S3 must confirm that the chosen option preserves the ADR-0004 semantic guarantee cleanly.

**Q6: What does D-006's `KnowAdapter(kb)` mean when `kb` is potentially a registry of N instances?**
D-006 names `KnowAdapter(kb)` as the coupling mechanism. If `kb` becomes a multi-instance
registry, does the adapter still satisfy D-006's intent? Or must D-006 be amended to
acknowledge `KnowAdapter(registry)` as the new form? S3 should assess whether this is a
clarification (same decision, updated detail) or a substantive change requiring D-013.

**Q7: Under Option 1, how does `nowu know` expose the `KnowledgeStoreProvider` Protocol to
callers when fan-out is required?**
`KnowledgeStoreProvider` in `core` defines `know`'s public API. Under multi-instance fan-out,
the `know` module must present a single conformant object to callers (via `core/contracts.py`)
while internally managing N instances. S3 must confirm that the Protocol boundary in `core`
remains stable and that the multi-instance complexity is fully hidden inside `know`.

---

## Arch-Pass Divergences

No pre-workflow arch-pass exists for intake-005. Constraints derived cold.

The D-011 "Review trigger" explicitly anticipated this spike: *"review D-006 ('No internal
reimplementation in nowu') for compatibility with `know`-as-internal-container — a
superseding ADR may be required."* This constraints sheet confirms the contradiction is real
and is not a false alarm. The contradiction arises because:

1. D-006 specifies a single `KnowAdapter(kb)` wrapping one `KnowledgeBase` instance.
2. D-011 requires per-project SQLite files with a federation query layer inside `know`.
3. The sibling library's `KnowledgeBase` is a per-instance class with no built-in
   federation — combining D-011's structural intent with D-006's literal text requires
   either (a) a clarification of D-006's scope, or (b) a superseding D-013.

The contradiction is structural, not interpretive. S4 cannot escape it by careful wording
alone — either D-006 is clarified with a binding corollary specifying how multi-instance
wrapping satisfies it, or D-006 is superseded.