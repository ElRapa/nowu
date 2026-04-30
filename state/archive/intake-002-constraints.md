---
id: intake-002-constraints
intake_id: intake-002
created: 2026-04-06
status: READY_FOR_OPTIONS
arch_pass_ref: ~
reconstructed_at: 2026-04-08
reconstruction_note: >
  The original archived copy became text-corrupted during prior tooling output.
  This reconstructed archive preserves the decision-driving constraints used for
  intake-002 and points to canonical downstream decision artifacts.
---

# Constraints Sheet: intake-002 - Scoping and Data-Governance Principles

> No pre-workflow arch-pass - constraints derived cold.

---

## Affected Modules

| Module | Container (C4 L2) | Impact | Confidence |
|---|---|---|---|
| `core` | Contracts + MemoryService | Modify - sensitivity context must be expressible in the `MemoryService` protocol and enforcement checks must be possible before rendering. | HIGH |
| `know` (external) | Knowledge graph + embedding index | Constrained - current known API has no first-class sensitivity filter; any index-partition strategy may require sibling-library change. | HIGH |
| `flow` | Session runtime | Query consumer - receives filtered results through `core` contracts; must not bypass contract-level scoping. | HIGH |
| `bridge` | Interface layer | Rendering only - must present role-appropriate outputs, not perform authorization logic itself. | MEDIUM |
| `soul` | State and identity conventions | Indirect - must follow scoped retrieval rules when producing summaries or guidance artifacts. | MEDIUM |

---

## Fixed Constraints (Non-Negotiable)

1. **D-002 boundary remains binding:** cross-module interaction goes through `core/contracts.py`; no direct module bypass to apply ad hoc access rules.
2. **`core` stays I/O free:** policy and protocol definitions may live in `core`, but concrete database/session handling must not.
3. **Scoping enforcement must happen before role rendering:** XP-11 output format does not replace PK-06 access control.
4. **No new top-level module for this spike:** D-003 module structure remains in force unless superseded by a dedicated decision.
5. **Mode D output only:** this intake is architecture-only; no implementation shapes or code changes are in scope.

---

## Variable Constraints (S3/S4 Decision Space)

1. **Sensitivity granularity:** atom-level vs project-level vs hybrid tagging.
2. **Default sensitivity posture:** permissive default with explicit restriction vs restrictive default with explicit release.
3. **Visibility semantics for restricted knowledge:** invisible vs redacted tombstone vs metadata-only acknowledgement.
4. **Index-layer strategy:** post-retrieval filtering vs sensitivity-aware index partitioning.
5. **Scope context carrier:** explicit scope parameter vs session-context token vs typed request envelope.

---

## Key Risks to Evaluate in Options

1. **Leakage risk through retrieval similarity:** post-filtering can still leak existence patterns via ranking behavior.
2. **Over-restriction productivity risk:** restrictive defaults may degrade usability and suppress useful context.
3. **Schema-coupling risk with sibling `know`:** introducing sensitivity fields at storage level may force cross-repo coordination.
4. **Contract drift risk:** if `core` protocol and `bridge` rendering evolve separately, scoped output guarantees may break silently.

---

## Open Questions Passed to S3

1. What minimum sensitivity model satisfies PK-06 without making capture overhead unacceptable?
2. Where is the enforcement boundary in the retrieval pipeline so XP-11 stays a rendering concern, not a policy concern?
3. Which option preserves forward compatibility with sibling `know` while keeping D-002 and D-003 intact?

---

## Canonical Follow-On Artifacts

This archived constraints sheet fed the architecture-only decision chain for intake-002.
For binding outcomes, refer to:

- `state/intake/intake-002.md`
- `state/arch/intake-002-options.md` (if present)
- `state/arch/intake-002-decision.md` (if present)
- `docs/DECISIONS.md` (authoritative accepted decisions)
