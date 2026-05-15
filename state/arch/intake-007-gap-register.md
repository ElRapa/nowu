---
artifact_type: GAP_REGISTER
status: ACCEPTED
created_at: 2026-05-15
intake_id: intake-007
decision_id: D-027
---

# W27 Gap Register + Claim Boundary — intake-007

## Part 1: Summary Matrix

| gap_id | affects_uc | affects_ac | missing_capability | workaround_used_in_w27 | target_work_item | severity |
|---|---|---|---|---|---|---|
| GAP-001 | AP-01, AP-02, AP-06 | AC-2, AC-5 | `MemoryService` has no generic atom CRUD/query surface (`create_atom`, `query_atoms`, field-level retrieval), so AP evidence cannot cross nowu's contract boundary into machine-queryable persistence. | W27 kept AP knowledge in Markdown artifacts only (`state/arch/*`) with manual trace references. | K3 | HIGH |
| GAP-002 | AP-01 | AC-2, AC-5 | No relationship/graph traversal primitives in `MemoryService` for dependency edges and ordered traversal. | AP-01 dependency order represented manually via Markdown dependency lists and Mermaid graph. | K3, K13 | HIGH |
| GAP-003 | AP-06 | AC-3, AC-5 | `DecisionRecord` has only 5 fields (`title`, `rationale`, `risks`, `mitigations`, `use_case_ids`); full AP-06 evidence chain (options, criteria, scoring, evidence catalog, revisitation) is not first-class. | AP-06 used supplementary artifact sections around (not inside) the contract shape. | W19, W20 | HIGH |
| GAP-004 | AP-02 | AC-2, AC-5 | No versioning/supersedes semantics in `MemoryService`; version lineage cannot be traversed or compared programmatically. | AP-02 version chain captured as explicit `supersedes` narrative fields in Markdown only. | K9 | HIGH |
| GAP-005 | AP-01, AP-02 | AC-1, AC-5 | No domain extension model to formally declare AP-specific atom types (e.g., regulation, formulation, evidence node). | W27 encoded AP-specific structures as ad hoc artifact conventions without formal type declaration. | W19 | MEDIUM |
| GAP-006 | AP-01 | AC-2, AC-5 | No automated staleness/freshness alert capability for regulatory knowledge currency. | AP-01 included source/confidence notes and manual renewal-frequency reminders only. | K13 | HIGH |
| GAP-007 | AP-01 | AC-2, AC-5 | Decay semantics discrepancy: ADR-0010 specifies `MEDIUM=90d` while know-side implementation baseline is `MEDIUM=180d`; confidence decay calibration is inconsistent. | W27 treated confidence levels as static artifact annotations, without runtime decay enforcement. | ADR-0010 maintenance | MEDIUM |

## Part 2: Detailed Gap Cards

### GAP-001 — Missing generic knowledge atom CRUD/query boundary
- **Description:** W27 can represent AP knowledge in artifacts, but cannot persist/retrieve those units as first-class machine-queryable atoms through the existing contract boundary.
- **Evidence from W27:** `intake-007-fit-assessment.md` notes no direct contract for AP-01/AP-02 knowledge items and no `create_atom`/`query_atoms` capability in `MemoryService`.
- **Current workaround:** Artifact-only storage in Markdown with human-readable IDs and links.
- **What needs to happen:** Add generic atom creation/read/query capabilities at the contract surface used by nowu.
- **Owner (target work item):** K3.

### GAP-002 — Missing relationship graph traversal
- **Description:** Dependency representation exists textually, but there is no contract capability to traverse prerequisite/blocker relationships programmatically.
- **Evidence from W27:** `intake-007-ap01-mini-graph.md` states no automated dependency traversal, no blocked-item query, and no reverse dependency lookup.
- **Current workaround:** Manual dependency ordering via lists and Mermaid edges.
- **What needs to happen:** Provide relationship-edge modeling and traversal/query operations for dependency chains.
- **Owner (target work item):** K3, K13.

### GAP-003 — DecisionRecord evidence-chain limits
- **Description:** The current 5-field `DecisionRecord` supports high-level decision capture but not the full AP-06 decision evidence chain.
- **Evidence from W27:** `intake-007-ap06-proof.md` and `intake-007-fit-assessment.md` identify missing first-class structure for options, criteria, weighted scoring, evidence links, chosen-path distinction, and revisitation triggers.
- **Current workaround:** AP-06 proof used supplementary sections for criteria tables, scoring, evidence catalog, and trigger thresholds.
- **What needs to happen:** Standardize extended decision-evidence structure while preserving existing decision linkage semantics.
- **Owner (target work item):** W19, W20.

### GAP-004 — Missing version-chain semantics and traversal
- **Description:** Version lineage can be written in artifacts, but supersession semantics and version-to-version impact traversal are not available at the contract/persistence layer.
- **Evidence from W27:** `intake-007-ap02-mini-version-chain.md` records explicit `supersedes` narrative and notes lack of automated diff/comparison or machine-traceable change history.
- **Current workaround:** Manual version chain and rationale narrative in Markdown.
- **What needs to happen:** Add first-class version lineage semantics and programmatic chain traversal/comparison support.
- **Owner (target work item):** K9.

### GAP-005 — No formal domain extension model for AP atom types
- **Description:** AP-specific entities are representable as free-form artifact sections, but not as formally declared domain-extension types.
- **Evidence from W27:** `intake-007-fit-assessment.md` shows no direct contract for AP requirement/formulation atom shapes; `intake-007-ap02-mini-version-chain.md` references domain extension standardization need.
- **Current workaround:** W27 used consistent naming/section conventions without formalized extension contracts.
- **What needs to happen:** Define a domain extension model that can declare AP-specific atom/evidence types and metadata patterns.
- **Owner (target work item):** W19.

### GAP-006 — No automated regulatory freshness/staleness detection
- **Description:** Regulatory knowledge can be documented with confidence/source fields, but there is no automated freshness monitoring for evolving rules.
- **Evidence from W27:** `intake-007-ap01-mini-graph.md` explicitly identifies absence of automated staleness alerts when guidance changes.
- **Current workaround:** Manual source verification and periodic human review cues in artifact notes.
- **What needs to happen:** Add freshness/staleness monitoring and alerting tied to regulatory knowledge items.
- **Owner (target work item):** K13.

### GAP-007 — Decay semantics mismatch for MEDIUM confidence
- **Description:** Confidence-decay policy and implementation baseline are misaligned, creating uncertainty in medium-confidence calibration.
- **Evidence from W27:** W27 AP-01 evidence uses `confidence_level` as a key field; D-027 gap synthesis surfaced ADR-0010 vs know baseline mismatch (`MEDIUM=90d` vs `180d`).
- **Current workaround:** Confidence levels were treated as static labels in W27 artifact evidence.
- **What needs to happen:** Align runtime decay semantics with ADR policy (or formally update policy) so confidence interpretation is consistent.
- **Owner (target work item):** ADR-0010 maintenance.

## Part 3: Claim Boundary

### What W27 Proved

- Flow can process AP-domain intake artifacts without AP-specific workflow logic changes (T5 validated at workflow level).
- AP-06 business decision structure maps to the same S1-S9 decision pattern used by NF-02 (workflow/template shape reuse, domain content differs).
- AP-01 regulatory requirements can be represented as structured artifacts with explicit dependency references.
- AP-02 formulation versions can be represented with version chains (`supersedes`) and rationale narratives.
- No bespoke AP management system was created; AP evidence stayed inside existing nowu artifact/workflow structures (AC-4 satisfied).

### What Remains Blocked

- AP knowledge cannot be persisted/retrieved as first-class machine-queryable atoms through nowu's current contract boundary (**GAP-001 → K3**).
- Dependency traversal and blocker computation remain manual rather than automated (**GAP-002 → K3/K13**).
- Decision evidence chain completeness for AP-06 requires supplementary structure beyond `DecisionRecord` (**GAP-003 → W19/W20**).
- Version comparison, lineage traversal, and impact analysis are not programmatically available (**GAP-004 → K9**).
- Regulatory freshness monitoring is manual, not automated (**GAP-006 → K13**).
- AP-specific domain typing is convention-based, not formally declared (**GAP-005 → W19**).

## AC Evidence Matrix

| AC | Verdict | Evidence File | Evidence Section | Notes |
|---|---|---|---|---|
| AC-1: AP knowledge expressible in existing structures | PROVED | All 4 evidence artifacts | Full artifacts | Ad hoc Markdown conventions used for AP-01/AP-02; canonical templates reused for AP-06 |
| AC-2: Dependencies/versioning representable conceptually | PROVED (conceptual) | ap01-mini-graph, ap02-mini-version-chain | Dependency graph, version chain | Automation gaps documented in gap register |
| AC-3: AP-06 structurally equivalent to NF-02 | PARTIAL | ap06-proof | NF-02 crosswalk table | Core decision shape (S1-S4) maps cleanly; supplementary sections needed for full evidence chain |
| AC-4: No bespoke AP system created | PROVED | All artifacts | Scope verification | All work in state/arch/; no src/ or tests/ changes |
| AC-5: Blocking gaps documented with traceability | PROVED | gap-register | Summary matrix + gap cards | 7 gaps documented with work item ownership |

## Part 4: Cross-References

- Task spec: `state/tasks/task-013-w27-gap-register-and-claim-boundary.md`
- Evidence: `state/arch/intake-007-fit-assessment.md`
- Evidence: `state/arch/intake-007-ap06-proof.md`
- Evidence: `state/arch/intake-007-ap01-mini-graph.md`
- Evidence: `state/arch/intake-007-ap02-mini-version-chain.md`
- Intake AC baseline: `state/intake/intake-007.md`

**No `src/` or `tests/` changes were required for this evidence run.**
