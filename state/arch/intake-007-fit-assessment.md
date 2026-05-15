---
artifact_type: FIT_ASSESSMENT
status: ACCEPTED
created_at: 2026-05-15
intake_id: intake-007
decision_id: D-027
---

# W27 Fit Assessment — AP Evidence vs Existing Contracts/Schemas

## Scope

This assessment maps AP-domain evidence needs (AP-01, AP-02, AP-06) against existing
nowu contracts/schemas only: `TaskSpec`, `DecisionRecord`, `SessionCheckpoint`, and
`MemoryService` protocol surface. No new contracts are proposed in this artifact.

## Coverage Matrix

| AP Need | Existing Contract/Schema | Fits? | Gap |
|---|---|---|---|
| AP-06 business decision structure | `DecisionRecord` (`title`, `rationale`, `risks`, `mitigations`, `use_case_ids`) | Partial | Missing explicit fields for `options[]`, `criteria[]`, evidence links, recommendation, chosen path, revisitation trigger. |
| AP-06 decision traceability | `TaskSpec.use_case_ids` | Yes | AP-06 can be linked directly through `use_case_ids`; no structural gap for linkage itself. |
| AP-01 regulatory requirement | No direct contract | No | No generic knowledge-item contract for requirement atoms (body/source/jurisdiction/deadline/confidence/status). `MemoryService` has no `create_atom` / `query_atoms` capability. |
| AP-01 dependency ordering | No direct contract | No | No relationship edge model and no dependency traversal/query operation in `MemoryService` (e.g., prerequisites, blockers, topological order). |
| AP-02 formulation versions | No direct contract | No | No first-class version chain semantics (`supersedes`, `superseded_by`, immutable version IDs, effective date) in current contracts or `MemoryService` methods. |
| AP-02 rationale per version | `DecisionRecord.rationale` | Partial | `rationale` field exists but semantics are decision-centric; not scoped to formulation outcomes, sensory results, process parameters, or batch test context. |
| Epistemic grades on AP knowledge | `SessionCheckpoint.checkpoint_grade` | Conceptual fit | Grade exists at session-checkpoint level, not at AP knowledge-item level; cannot assign confidence/grade per regulatory item/formulation/decision evidence node. |

## Contract-by-Contract Notes

### DecisionRecord (current 5-field shape)

- **Sufficient for:** high-level statement of decision title, rationale summary, explicit risks/mitigations, use-case linkage.
- **Insufficient for AP-06 evidence completeness:** cannot encode option table, weighted criteria scoring, evidence citations, recommendation vs final selection distinction, or revisit conditions.

### TaskSpec

- **Sufficient for:** tracing AP work items to `AP-06` using `use_case_ids` and preserving scope boundaries.
- **Limitation:** not an evidence container; does not persist decision analysis details.

### SessionCheckpoint

- **Sufficient for:** preserving workflow/session state with grade metadata.
- **Limitation:** `checkpoint_grade` represents session confidence, not confidence per AP domain artifact unit.

### MemoryService Protocol Surface

- **Sufficient for W27 artifact-only approach:** yes, because this intake validates representability in artifacts.
- **Insufficient for AP knowledge operations:** no explicit atom create/read/query by semantic fields; no relationship graph primitives; no version supersession operations.

## Three-Layer Fit Analysis

### 1) Python contract fit

- **Directly supported today:**
  - `DecisionRecord` carries AP-06 high-level decision intent (`title`, `rationale`, `risks`, `mitigations`, `use_case_ids`).
  - `TaskSpec.use_case_ids` supports AP traceability linkage.
  - `MemoryService` can support artifact-oriented flow checkpoints at a coarse level.
- **Not directly supported in contract fields:**
  - AP-01 requirement atoms (jurisdiction/body/deadline/provenance/dependency semantics).
  - AP-02 version lineage semantics (branching, effective dates, immutable identity, evidence linkage).
  - AP-06 full option/criteria/evidence/revisit structure as first-class contract members.

### 2) Artifact/template fit

- **Expressible via existing templates and artifact conventions:**
  - `templates/decision.md` shape (Context, Decision, Rationale, Alternatives, Consequences) maps to AP-06 S1-S4 decision proof sections.
  - `task-spec.md` and intake/task metadata preserve AP use-case trace links and execution scope.
  - Markdown artifacts can carry richer tables/lists (weighted scoring, dependency mini-graph, version chain narratives) beyond current Python contract fields.
- **Limit of this layer:**
  - Rich AP evidence is human-readable but convention-based; it is not machine-validated or strongly typed.

### 3) Future automation fit

- **Requires K3 for machine-queryable behavior:**
  - Generic AP knowledge atom CRUD/query and dependency traversal/reverse lookup.
  - Retrieval/comparison surface for AP-02 versions.
- **Requires W19 for domain extension formalization:**
  - Typed AP-specific entities/metadata patterns (regulation atoms, formulation versions, evidence links).
- **Requires K9 for robust version automation:**
  - First-class version lineage semantics (including branching), comparison workflows, and effective-date aware version identity.

## Fit Conclusion

1. **AP-06 is representable with supplementary artifact structure** layered on top of `DecisionRecord` semantics.
2. **AP-01 and AP-02 are only partially representable at artifact level** and are not contract-complete without future knowledge/relationship/versioning capabilities.
3. **D-027 (artifact-only validation) remains valid** for W27 because this phase asks for structural proof and gap surfacing, not protocol expansion.
