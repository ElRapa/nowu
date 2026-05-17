---
artifact_type: SESSION_LEARNINGS
session: "W19 ADR-0011 domain extension model"
created_at: 2026-05-15
session_type: "architecture"
source_artifacts:
  - docs/architecture/adr/ADR-0011-domain-extension-model.md
  - state/arch/w28-gap-comparison.md
  - state/arch/intake-007-gap-register.md
  - state/intake/intake-007.md
  - state/intake/intake-008.md
  - docs/architecture/adr/ADR-0008-knowledge-atom-model.md
  - docs/architecture/adr/ADR-0009-orchestration-protocol.md
  - src/nowu/core/contracts/memory.py
  - src/nowu/core/boundaries.py
purpose: "Capture architecture learnings from defining the AP/RE domain extension hypothesis for KI-4"
---

# Session Learnings: W19 Domain Extension Model

## What Was Done

- Read W28 systemic gap evidence and confirmed GAP-003/GAP-005 apply to both AP and RE.
- Wrote ADR-0011 as PROPOSED/HYPOTHESIS with explicit extension points and boundary-safe scope.
- Defined AP+RE examples including AP-06 and RE-06 decision-evidence chain linkage.
- Specified concrete KI-4 registry requirements and signatures for `../know`.
- Kept extension mechanism at bridge/config + know registry layer with no `core/contracts/` changes.

## Decisions Made

### D-SESS-W19-01: Keep domain extension out of core contracts in W19

**Decision:** Domain extension is formalized at bridge mapping + know registry layers; `core/contracts/` remains unchanged in ADR-0011.
**Context:** GAP-005 requires formal extension, but ADR-0001 boundaries and current `core` stability constraints prohibit direct domain-specific contract expansion at this step.
**Why it matters:** This preserves boundary integrity while unblocking KI-4 with an implementable extension model.

### D-SESS-W19-02: Treat decision evidence chains as link manifests, not DecisionRecord expansion

**Decision:** GAP-003 is addressed through decision→evidence chain linking semantics and typed roles rather than immediate `DecisionRecord` field growth.
**Context:** AP-06 and RE-06 both exceed current decision shape; an adapter/registry approach enables richer modeling without immediate core churn.
**Why it matters:** K3/W20 can evolve contract and traceability surfaces later from a validated extension pattern rather than speculative upfront expansion.

---

## Process Insights

### Insight 1: Systemic gap classification sharply improves ADR specificity

**Observation:** Using W28 side-by-side AP/RE evidence prevented AP-biased design and forced extension points that work for both domains.
**Type:** workflow-process
**Implication:** For cross-domain ADRs, require explicit dual-domain references in Context and Examples sections.

### Insight 2: Bridge/config-first extension is the safest hypothesis path

**Observation:** Extension via bridge mapping profiles and know registry satisfies GAP-005 without violating ADR-0001 import boundaries.
**Type:** domain-insight
**Implication:** Prefer adapter-layer extension when domain variability is high and core contracts must remain stable.

### Insight 3: Concrete KI-facing signatures reduce ADR ambiguity

**Observation:** Adding method/type signatures in the ADR made KI-4 requirements actionable while still keeping HYPOTHESIS-grade flexibility.
**Type:** workflow-process
**Implication:** For implementation-blocking ADRs, include minimum concrete interfaces and behavior rules.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Solving systemic extension gaps by ad hoc domain markdown conventions

**Temptation:** Continue AP/RE modeling with narrative-only structures because it is fast and requires no schema decisions.
**Reality:** This reproduces GAP-005 and keeps decision evidence chains non-queryable, delaying K3/KI-4 and weakening cross-domain reuse.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| ADR-0011 | `docs/architecture/adr/ADR-0011-domain-extension-model.md` | PROPOSED | Define domain extension model and KI-4 requirements addressing GAP-003/GAP-005 |
| Session learnings | `state/learnings/session-2026-05-15-w19-domain-extension.md` | DONE | Capture decisions and reusable process insights from W19 |

## What Should Happen Next

1. Shape KI-4 implementation tasks directly from ADR-0011 registry and link requirements.
2. Use ADR-0011 as input to K3/W20 so contract and traceability updates align with extension semantics.
3. Validate AP-06 and RE-06 chains end-to-end with prototype bridge mapping profiles before promoting this ADR grade.
