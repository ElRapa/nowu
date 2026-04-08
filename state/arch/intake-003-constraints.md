---
id: intake-003-constraints
intake: intake-003
status: READY_FOR_OPTIONS
created: 2026-04-06
agent: nowu-constraints@S2
arch_pass_ref: global-pass-2026-04-06
---

# Constraints Sheet — intake-003: Cross-Project Knowledge Architecture and DB Session Pattern

## Fixed Constraints (Non-Negotiable)

1. **`core` may not perform I/O.** The global-pass L2 container definition is explicit: `core` is "a Python module — no I/O." A `DatabaseProvider` defined in `core` must be a Protocol or abstract type only. Any concrete connection implementation lives in the module that owns the data. Source: D-002 (DDD layer rule: domain must not import from infrastructure), global-pass container definition for `core`.

2. **All cross-module communication goes through `core/contracts.py` — no direct imports.** Whatever Q5 answer is chosen, `know` must not be called by `flow`, `soul`, or `bridge` via anything other than a protocol defined in `core/contracts.py`. A session factory that other modules reach into `know` to access directly would violate this. Source: D-002, P3 constraint 4.

3. **No sixth module may be created for federation.** The cross-project search layer required for XP-01 must live inside `know`. A "federation" container is not permitted without a superseding ADR and Tier 3 approval. The five-module ceiling applies. Source: D-003, P3 constraint 1.

4. **All persistence must be local and SQLite-based.** Cloud databases and SaaS backends are ruled out through v1.2. The only off-SQLite alternative acknowledged in the GAP (ADR-A option B) still requires SQLite for search. Option C of ADR-D (Markdown primary) does not eliminate SQLite. Source: D-001, P3 constraint 5.

5. **`know` is the sole persistent store for knowledge atoms.** No other module may implement its own atom storage. Q5 is only about how `know`'s own connections are managed — not a licence for `flow` or `soul` to own SQLite files for knowledge. Source: D-006.

6. **XP-01 cross-project semantic search must be achievable in v1-core.** The isolation model chosen by ADR-D must support cross-project queries at v1-core — not deferred to v1.1. Whichever option S3 recommends must include a concrete description of how XP-01 is served without a storage migration. Source: D-010, global-pass UC matrix (XP-01 = v1-core, assigned to `know`), P3 constraint 7.

7. **XP-08 portable per-project export must be achievable in v1.1.** The ADR-D choice must not create a situation where exporting a single project requires a full DB schema migration or cherry-picked row filtering that risks orphaning relational data (cross-project connection edges). Source: global-pass UC matrix (XP-08 = v1.1, assigned to `know`).

8. **ADR-D must be ACCEPTED before any `know` storage implementation begins.** No intake that scopes `know`'s storage layer may proceed past S4 until ADR-D is recorded in DECISIONS.md. This applies retroactively to intake-001 (Memory Integration Layer), which references XP-01. Source: P3 constraint 7, global-pass "ADR-D: CANDIDATE — URGENT".

9. **Q5's answer follows directly from ADR-D's answer.** Per-project SQLite files (Option B) structurally implies per-module DB ownership — each project file is `know`'s file alone, and there is nothing for `core` to share. A shared `core` session factory is only structurally coherent under Option A (single shared DB). S3 must not treat Q1 and Q5 as independent decisions. Source: intake-003 problem statement, global-pass Q5.

---

## Flexible Parameters (S3 may choose)

1. **Federation implementation strategy.** If Option B (per-project files) is chosen, S3 may propose either (a) query-time fan-out across N SQLite files, or (b) a materialized cross-project index file updated on every write. Both satisfy XP-01 at v1-core scale; they differ in read latency vs. write overhead. Neither requires a new module.

2. **DatabaseProvider Protocol scope.** If a `DatabaseProvider` Protocol is defined in `core/contracts.py`, S3 may scope it to `know` only or make it a general-purpose persistence contract that any data-owning module implements. The protocol definition itself does not violate the "no I/O in core" constraint as long as `core` does not provide a concrete implementation.

3. **Connection management approach within `know`.** Single connection per project file, WAL-mode with concurrent readers, or a lightweight connection pool — all are open. This is an implementation detail inside `know`'s boundary and does not affect the inter-module contract.

4. **Active-project context passing.** How the active project identifier is passed to `know` at runtime (constructor argument, context variable, initialization call) is unconstrained. S3 may propose any pattern that keeps the decision inside `know`'s public surface.

5. **SQLite schema internals.** Table names, column names, and index strategy are fully open. Constraints 6 and 7 above impose behavioral requirements (XP-01 queryability, XP-08 exportability) but do not prescribe any particular schema shape.

6. **Schema migration tooling.** Alembic, versioned SQL scripts, or manual migration functions are all acceptable. No existing decision constrains this choice.

---

## Key Risks for S3 to Address

1. **[HIGH] XP-08 export correctness is structurally at odds with Option A (single shared DB).** A single SQLite file with `project_id` makes per-project export a filter + schema rebuild. Cross-project relationship edges (atoms that link entities in two projects) cannot be cleanly split without semantic loss. S3 must model what a correct XP-08 export produces under Option A — including what happens to cross-project edges — before recommending it. Mitigation direction: if Option A is recommended, S3 must define the edge-ownership rule and show that XP-08 can be implemented without orphaning data.

2. **[MEDIUM] Federation query performance for XP-01 under Option B is unknown at reasonable project counts.** If the human operates 10+ projects, a fan-out semantic search across 10+ SQLite files at query time may be unacceptably slow on a laptop. S3 must include a performance assumption (e.g., "acceptable at ≤ 20 projects for v1-core") and model the materialized-index alternative as the fallback. Without this, the federation layer's scope cannot be estimated at S5.

3. **[MEDIUM] Concrete I/O leaking into `core` if Q5 is answered carelessly.** The most natural naive implementation — `core` opens a SQLite connection and hands it to modules — directly violates D-002 and the global-pass container definition. If S3 recommends a `DatabaseProvider` in `core`, the options sheet must specify that only a Protocol type lives in `core`, and must name where the concrete factory is implemented. Mitigation direction: implementation is in `know`; `core/contracts.py` holds only the Protocol.

4. **[MEDIUM] Option A creates migration debt toward XP-10 (v2 multi-user).** A shared SQLite DB with `project_id` makes row-level per-user isolation at v2 significantly harder to add without a breaking schema migration. S3 should include a one-paragraph migration-from-A-to-B assessment so the human can factor this into the Option A recommendation. This is a known risk flagged in the intake itself.

5. **[LOW] Implicit expansion of a `core` session factory to non-`know` modules.** If a `DatabaseProvider` contract is added to `core/contracts.py` and framed generically, future implementers may assume `flow` or `soul` can also acquire a DB session through it — silently expanding `core`'s scope. S3 should either scope the Protocol name explicitly to `know` (e.g., `KnowledgeStoreProvider`) or include a governance note in the options sheet specifying that the Protocol is `know`-only unless a new ADR expands it.

---

## Constraint Summary for Options Agent

S3 is constrained to a two-option decision space: per-project SQLite files with an internal federation layer (Option B), or a single shared SQLite with `project_id` namespacing (Option A) — both implemented entirely within `know` and callable only via `core/contracts.py` protocols, with no I/O permitted in `core` itself. Q5 (core DB session factory vs. per-module ownership) is not an independent decision: it resolves as a corollary of whichever ADR-D option is chosen, and S3 must pair each ADR-D option with its corresponding Q5 answer. The primary risks S3 must model are XP-08 export correctness under Option A and federation performance under Option B; both must be addressed with concrete assumptions before a recommendation is made.

---

## Assumptions

- `arch_pass_divergences`: No pre-workflow arch-pass exists for intake-003. Constraints derived cold from global-pass-2026-04-06 (PROPOSED) P3 bindings and existing DECISIONS.md entries D-001 through D-010.
- XP-01 (v1-core) and XP-08 (v1.1) UC descriptions in USE_CASES.md v2.2 are taken as authoritative and verified by S1 (s1_validated_at: 2026-04-06).
- The global-pass-2026-04-06 status is PROPOSED, not ACCEPTED. All P3 bindings referenced here are treated as directionally binding for this spike — they reflect the same architectural logic as the accepted decisions (D-002, D-003) they extend. If the global-pass is rejected or significantly revised before ADR-D is recorded, these constraints must be revisited.
- No `docs/ARCHITECTURE.md` and no `docs/architecture/containers.md` exist yet. The global-pass is the sole C4 L2 reference.

## Open Questions Passed to S3

1. **ADR-D option selection (Q1).** S3 must produce an options sheet that evaluates Option A and Option B against fixed constraints 6 and 7 (XP-01 and XP-08 requirements), including the migration-to-v2 assessment noted in risk 4.
2. **Q5 resolution.** S3 must pair each ADR-D option with its Q5 answer and show why the pairing is internally consistent.
3. **Federation performance threshold.** S3 must state an explicit project-count assumption for Option B's federation performance before recommending it.

## c4_l1_update_needed

false — this spike does not introduce a new external actor or system boundary. The C4 L1 diagram in the global-pass is unaffected. The C4 L2 `know` container description (currently says "per-project SQLite" reflecting Option B directionally) will require a one-line update once ADR-D is accepted.
