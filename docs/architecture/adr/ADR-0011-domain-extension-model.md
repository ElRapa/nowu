---
id: ADR-0011
title: Domain Extension Model for Knowledge Atoms
date: 2026-05-15
status: PROPOSED
epistemic_grade: HYPOTHESIS
superseded_by: ~
source_synthesis: SYNTHESIS-001
source_themes: [T2, T5, T6]
source_ucs: [AP-01, AP-02, AP-06, RE-01, RE-06]
depends_on: [ADR-0001, ADR-0008, ADR-0009, ADR-0010]
---

# ADR-0011: Domain Extension Model for Knowledge Atoms

## Status

PROPOSED (HYPOTHESIS grade) — Derived from cross-domain evidence in intake-007 (AP) and
intake-008 (RE), plus W28 systemic classification. This ADR addresses GAP-003 and GAP-005
as a design hypothesis for KI-4 implementation in `../know`, without changing `core/contracts/`.

## Context

W28 classified GAP-003 and GAP-005 as systemic (not AP-only):

- **GAP-003:** Decision evidence chains in AP-06 and RE-06 exceed the current first-class
  `DecisionRecord` shape.
- **GAP-005:** AP and RE both need a formal domain extension mechanism for atom typing,
  instead of ad hoc artifact conventions.

ADR-0008 establishes `know` atoms as canonical knowledge units and explicitly anticipates
domain-specific typing. ADR-0001 and current import boundaries require that cross-module
integration stays behind boundaries; `core` is contracts-only and must not become a domain
extension implementation surface.

Therefore, this ADR defines a **bridge/configuration-level extension model** and concrete
KI-4 requirements for `../know`, while keeping existing `core/contracts/` unchanged in W19.

## Decision

nowu adopts a **Domain Extension Model** with three layers:

1. **Domain Type Registry (in `../know`, delivered by KI-4):**
   A runtime registry for domain atom types and payload schemas.
2. **Bridge Domain Mapping Adapter (in `bridge/`):**
   Maps workflow/artifact content into registered domain atom types using configuration.
3. **Decision Evidence Chain Linker (artifact + atom references):**
   Captures structured links between decision records and domain evidence atoms without
   expanding `core` contracts in this ADR.

### Binding Scope Rule

- **No changes to `core/contracts/` are introduced by ADR-0011.**
- Extension behavior is implemented in `bridge` adapters and `../know` registry/config.
- `core` remains stable while KI-4 proves the extension model.

## Consequences

**Positive:**

- GAP-005 is addressed with formal, reusable extension points for AP and RE.
- GAP-003 is addressed by explicit decision→evidence chain linking semantics.
- AP and RE can evolve domain vocabularies without framework-level rewrites.
- Maintains ADR-0001 boundary discipline and current `core` immutability.

**Negative:**

- Bridge adapters must maintain mapping config quality and schema versioning discipline.
- Registry misuse (type drift, uncontrolled aliases) can degrade query consistency.

**Neutral:**

- This is a HYPOTHESIS ADR: concrete KI-4 implementation may refine naming/details,
  but must preserve the extension architecture and boundary constraints defined here.

## Extension Points

### Extension Point 1: Domain Type Declaration (configuration)

Each domain declares atom types in configuration consumed by the KI-4 registry.

Example declaration model:

```yaml
domain: ap
types:
  - name: ap.regulation_requirement
    base_kind: fact
    required_fields: [authority, jurisdiction, effective_date, dependency_refs]
  - name: ap.formulation_version
    base_kind: concept
    required_fields: [formula_code, supersedes, rationale, cost_profile]
```

Equivalent RE example:

```yaml
domain: re
types:
  - name: re.process_step
    base_kind: task
    required_fields: [process_id, actor, handoff_to, input_refs, output_refs]
  - name: re.investment_assumption
    base_kind: decision
    required_fields: [assumption_metric, horizon, confidence_band, outcome_link_refs]
```

### Extension Point 2: Bridge Mapping Profiles

`bridge` provides mapping profiles that transform workflow artifacts into domain atoms.
Profiles are selected per project/domain and validated against the KI-4 registry before write.

### Extension Point 3: Decision Evidence Chain Manifest

For GAP-003, each decision capture can include a machine-readable manifest that links a
decision atom to option, criterion, score, evidence, and review-trigger atoms.

Minimal chain shape:

```yaml
decision_atom_id: "dec-..."
domain: "ap|re"
links:
  - role: option
    atom_id: "..."
  - role: criterion
    atom_id: "..."
  - role: scored_evidence
    atom_id: "..."
  - role: revisitation_trigger
    atom_id: "..."
```

This preserves current `DecisionRecord` compatibility while enabling richer evidence chains.

## AP + RE Examples

### Example A — AP-06 evidence chain (intake-007)

AP-06 decisions (e.g., packaging option tradeoff) include options, weighted criteria,
scoring evidence, and revisitation triggers. Under this ADR:

- decision summary remains in existing workflow decision artifact,
- option rows become `ap.decision_option` atoms,
- evidence entries become `ap.evidence_node` atoms,
- trigger conditions become `ap.review_trigger` atoms,
- all are connected through the decision evidence chain manifest.

### Example B — RE-06 long-horizon investment tracking (intake-008)

RE-06 decisions include assumptions, rationale, confidence, and projected-vs-actual
outcome links over long horizons. Under this ADR:

- assumption records become `re.investment_assumption` atoms,
- projected outcomes become `re.projection_metric` atoms,
- later observations become `re.actual_outcome` atoms,
- links preserve assumption→projection→actual lineage for retrospectives.

### Example C — AP-01 regulatory dependency representation

`ap.regulation_requirement` atoms capture authority and dependency references so blocking
queries can be executed by relationship traversal rather than markdown-only interpretation.

### Example D — RE-01 process handoff representation

`re.process_step` atoms encode actor, handoff, and I/O references, allowing process
inventory and bottleneck analysis to be queried as typed graph data.

## Downstream KI-4 Requirements (for `../know`)

KI-4 must implement a domain atom type registry and decision-evidence link API compatible
with ADR-0008 atom semantics and this ADR's bridge/config extension model.

Required concrete surfaces (names may vary only if semantically equivalent):

```python
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class DomainAtomTypeSpec:
    domain: str
    type_name: str
    base_kind: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]
    schema_version: str

@dataclass(frozen=True)
class DecisionEvidenceLink:
    decision_atom_id: str
    role: str
    target_atom_id: str
    metadata: dict[str, Any]

class DomainTypeRegistry:
    def register_type(self, spec: DomainAtomTypeSpec) -> None: ...
    def get_type(self, type_name: str) -> DomainAtomTypeSpec | None: ...
    def list_types(self, domain: str | None = None) -> list[DomainAtomTypeSpec]: ...
    def validate_payload(self, type_name: str, payload: dict[str, Any]) -> None: ...

class DecisionEvidenceStore:
    def link_evidence(self, link: DecisionEvidenceLink) -> str: ...
    def list_evidence_for_decision(self, decision_atom_id: str) -> list[DecisionEvidenceLink]: ...
```

Behavioral requirements:

1. Reject atom writes that declare unknown domain types.
2. Reject writes missing required fields for a declared type.
3. Preserve typed role labels on decision-evidence links (`option`, `criterion`,
   `scored_evidence`, `revisitation_trigger`, etc.).
4. Support query of full decision evidence chains for AP-06 and RE-06 classes of decisions.
5. Keep compatibility with generic atom operations from ADR-0008.

## Related

- addresses_gaps: GAP-003, GAP-005
- evidence: `state/arch/w28-gap-comparison.md`, `state/arch/intake-007-gap-register.md`
- intakes: `state/intake/intake-007.md`, `state/intake/intake-008.md`
- adrs: ADR-0001, ADR-0008, ADR-0009, ADR-0010
- blocked_work: K3 (contract shaping), KI-4 (know registry implementation), W20 (traceability)
