# Artifact Templates

## Knowledge Artifact

```yaml
---
artifact_class: knowledge
artifact_type: GOAL | USE_CASE | ADR | SYNTHESIS | LESSON
id: [TYPE]-NNN
title: "[descriptive title]"
origin_altitude: STRATEGIC | PRODUCT | ARCHITECTURE | DELIVERY | EXECUTION
origin_phase: IDEA | PROBLEM | ANALYSIS | SYNTHESIS | OPTIONS | DECISION | EVALUATION | IMPLEMENTATION | VERIFICATION | LEARN
consumer_altitudes: [list of altitudes that may reference this]
epistemic_grade: SPECULATION | HYPOTHESIS | INFORMED_ESTIMATE | EVIDENCE_BASED | VERIFIED_FACT
grade_justification: "[one sentence explaining WHY this grade]"
status: ACTIVE | SUPERSEDED | DEPRECATED
created_at: YYYY-MM-DD
last_edited_at: YYYY-MM-DD
related_artifacts: []
promoted_from: null
promotes_to: null
relationships: []
---
```

### Field Rules

- `origin_altitude` + `origin_phase`: REQUIRED — where this artifact was created
- `consumer_altitudes`: which altitudes may reference this artifact
- `promoted_from`: set at creation when parent artifact is known
- `promotes_to`: set retroactively by curator during LEARN phase
- `relationships`: graph-readiness field — `[{edge_type, target_id, target_altitude, target_phase}]`, starts empty, populated by knowledge graph layer (v1.1+)
- `status`: ACTIVE (current), SUPERSEDED (replaced by newer), DEPRECATED (no longer valid)

---

## Workflow Phase Artifact

```yaml
---
artifact_class: workflow_phase
altitude: STRATEGIC | PRODUCT | ARCHITECTURE | DELIVERY | EXECUTION
phase: [one of 10 phases]
session_id: [uuid or identifier]
epistemic_grade: [appropriate for altitude — see tiered thresholds]
grade_justification: "[reasoning]"
---
```

### Notes

- Workflow phase artifacts are ephemeral (session-scoped), not indexed
- Once a decision is made, the winning option becomes a knowledge artifact (e.g., OPTIONS draft -> ADR)
- Naming: `{PHASE}-{ID}-{altitude}.md` (e.g., `OPTIONS-011-architecture.md`)
