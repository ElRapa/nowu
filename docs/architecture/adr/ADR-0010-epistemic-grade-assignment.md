---
id: ADR-0010
title: Epistemic Grade Assignment & Propagation
date: 2026-05-07
status: PROPOSED
epistemic_grade: HYPOTHESIS
superseded_by: ~
source_synthesis: SYNTHESIS-001
source_themes: [T4, T2, T8]
source_ucs: [NF-15, NF-16, NF-11, PK-04, PK-05, PK-09, XP-04, AP-01, AP-04, RE-05]
depends_on: [ADR-0008]
---

# ADR-0010: Epistemic Grade Assignment & Propagation

## Status

PROPOSED (HYPOTHESIS grade) — Derived from SYNTHESIS-001 Theme T4 (Epistemic Awareness).
Depends on ADR-0008 (atom schema defines where grades live). Will be validated through
first S1-S9 intake. D-015 establishes the tiered enforcement policy; this ADR defines
the grade semantics, assignment rules, propagation, and decay.

## Context

SYNTHESIS-001 identifies T4 (Epistemic Awareness) as a pervasive theme spanning 10+ UCs
across all domain categories. D-015 already establishes the 5-level epistemic grade scale
and tiered enforcement (Level 0: syntax check → Level 1: advisory → Level 2: blocking).

What D-015 does NOT define:
- **Who assigns grades** — producing agent, reviewing agent, or human?
- **How grades propagate** — a decision based on HYPOTHESIS inputs: what grade does it get?
- **When grades decay** — how is domain-aware staleness applied?
- **Composite grading** — what's the grade of an options sheet with mixed-grade options?
- **Behavioral impact** — how should agents weight different grades in reasoning?

The `know` module already implements the 5-level `EpistemicGrade` enum, confidence ranges
per grade, justification requirements for high grades, and auto-downgrade logic in the
curator. This ADR formalizes how nowu's workflow adopts and extends those semantics.

## Decision

### Grade Vocabulary (Canonical — from `know/ontology.json`)

| Grade | Level | Confidence Range | Requires Justification | Typical Decay |
|-------|-------|-----------------|----------------------|---------------|
| `SPECULATION` | 1 | 0.10–0.30 | No | fast |
| `HYPOTHESIS` | 2 | 0.30–0.50 | No | medium |
| `INFORMED_ESTIMATE` | 3 | 0.50–0.70 | No | medium |
| `EVIDENCE_BASED` | 4 | 0.70–0.90 | **Yes** | slow |
| `VERIFIED_FACT` | 5 | 0.90–1.00 | **Yes** | slow |

The `know` module's `EpistemicGrade` IntEnum (1–5) and `ontology.json` confidence ranges
are the single source of truth. nowu workflow artifacts use the same labels.

### Assignment Rules

**Principle: The producing agent assigns the initial grade. The reviewer may adjust.**

| Producer | Max Assignable Grade | Justification |
|----------|---------------------|---------------|
| Any agent (S1–S7) | `INFORMED_ESTIMATE` (3) | Agents cannot self-certify beyond this |
| Reviewer agent (S8) | `INFORMED_ESTIMATE` (3) | Reviewer validates, does not promote |
| Human (S4/S5 gates, reviews) | `VERIFIED_FACT` (5) | Human judgment is the highest authority |
| Curator (S9) | No change — records only | Curator captures, does not re-grade |
| `know` curator (automated) | Downgrade only | Auto-decay; never auto-promotes |

**Default grades by artifact type:**

| Artifact | Default Grade | Why |
|----------|--------------|-----|
| Intake brief (S1) | `HYPOTHESIS` | Unvalidated problem statement |
| Constraints sheet (S2) | `HYPOTHESIS` | Analysis without verification |
| Options sheet (S3) | `HYPOTHESIS` | Generated alternatives, unselected |
| Decision (S4) | `INFORMED_ESTIMATE` | Human-approved choice with reasoning |
| Task spec (S5) | `INFORMED_ESTIMATE` | Human-approved decomposition |
| Implementation (S6-S7) | `EVIDENCE_BASED` (if VBR passes) | Tests + verification = evidence |
| Review report (S8) | `INFORMED_ESTIMATE` | Review is judgment, not proof |
| Capture record (S9) | Inherits from reviewed artifact | Reflects final reviewed grade |
| Hypothesis ADR | `HYPOTHESIS` | Untested architectural decision |
| SYNTHESIS | `HYPOTHESIS` | Cross-cutting analysis, pre-validation |

### Propagation Rules

**Principle: Uncertainty compounds. A composite artifact inherits the LOWEST grade of
its inputs, unless the composition process itself adds evidence.**

1. **Derived artifacts inherit minimum input grade:**
   A decision (S4) based on an `INFORMED_ESTIMATE` constraints sheet and a `HYPOTHESIS`
   options sheet inherits `HYPOTHESIS` — unless the decision process itself adds evidence
   (e.g., human judgment elevates it to `INFORMED_ESTIMATE`).

2. **Promotion requires new evidence, not just time:**
   - `HYPOTHESIS` → `INFORMED_ESTIMATE`: requires 2+ S1-S9 intakes validating the hypothesis
   - `INFORMED_ESTIMATE` → `EVIDENCE_BASED`: requires passing implementation + VBR + review
   - `EVIDENCE_BASED` → `VERIFIED_FACT`: requires human attestation with justification
   - Promotion of ADRs: per D-017, `HYPOTHESIS` → `INFORMED_ESTIMATE` after 2 intakes,
     → `EVIDENCE_BASED` after 5+.

3. **Grade can never increase without explicit action:**
   No artifact or atom silently becomes more trusted. Every promotion is a recorded event
   with a justification trail.

### Decay Rules

**Principle: Trust degrades with time. Domain context determines the rate.**

Decay is managed by the `know` curator's auto-downgrade logic:

| Decay Rate | Half-Life | Example Content |
|-----------|-----------|----------------|
| `fast` | 30 days | Market data (AP-04), current prices (RE-02), ephemeral notes |
| `medium` | 90 days | Project decisions, technical analysis, process documentation |
| `slow` | 365 days | Regulatory knowledge (AP-01), architectural decisions, verified facts |

**Decay mechanics:**
- When `now - last_verified > half_life`: grade downgrades by 1 level
- `VERIFIED_FACT` → `EVIDENCE_BASED` → `INFORMED_ESTIMATE` (floor: never below `INFORMED_ESTIMATE` via auto-decay)
- `SPECULATION` and `HYPOTHESIS` do not auto-decay (they're already low-trust)
- Re-verification by human or agent resets `last_verified` and may restore grade

**Domain-aware decay (T5):**
- Decay rates are assigned per `KnowledgeType` in `ontology.json` (e.g., `fact` defaults
  to `medium`, `ephemeral` to `fast`)
- Project configuration may override defaults for domain-specific knowledge
  (e.g., food regulations decay faster than physics constants)

### Behavioral Impact

**Principle: Agents must acknowledge grades in reasoning. They must not treat all inputs
as equally trustworthy.**

Rules for agents consuming graded inputs:

1. **Flag uncertainty:** When an agent's output depends on `SPECULATION` or `HYPOTHESIS`
   inputs, it must note this in its output artifact.

2. **Prefer higher-grade sources:** When contradictory information exists at different
   grades, the higher-grade source wins unless the lower-grade source provides explicit
   counter-evidence (XP-04: conflict resolution).

3. **Grade-appropriate actions:** Agents should not make irreversible decisions based on
   `SPECULATION` inputs. Tier 2/3 approval gates exist precisely for this.

4. **Composite grading disclosure:** When producing an artifact from mixed-grade inputs,
   the output must list its input grades in metadata (e.g., `input_grades: [HYPOTHESIS, INFORMED_ESTIMATE]`).

### Enforcement Levels (from D-015)

| Level | Stage | Enforcement |
|-------|-------|-------------|
| 0 | v1-core | Syntax check only: `grade` field exists in frontmatter |
| 1 | v1 | Advisory warnings when grade < expected for artifact type |
| 2 | v1.1 | Blocking: cannot pass S4/S5 gates if inputs below threshold |

At v1-core (now), enforcement is Level 0. The ADR defines semantics so agents follow
them voluntarily. Automated enforcement comes later.

## Rationale

1. **Pervasive need:** 10+ UCs across all domains require confidence tracking. Without
   formal rules, every agent applies ad-hoc judgment about trustworthiness.

2. **Existing implementation:** `know` already has the enum, confidence ranges, justification
   requirements, and auto-decay. This ADR codifies how the workflow layer uses those primitives.

3. **Compound uncertainty:** Without propagation rules, a decision built on speculation
   looks as trustworthy as one built on verified facts. The "inherit minimum grade" rule
   makes uncertainty visible.

4. **Decay prevents false confidence:** A fact verified in 2024 should not carry `VERIFIED_FACT`
   indefinitely. Domain-aware decay (AP-01: regulations change, AP-04: market shifts)
   ensures the system actively questions stale information.

## Consequences

**Positive:**
- Every artifact carries explicit trust level — no implicit assumptions
- Agents have clear rules for assignment, propagation, and consumption
- Human review effort is focused on high-impact grade promotions
- Auto-decay prevents silent knowledge rot

**Negative:**
- Grade assignment adds a decision to every artifact creation step
- Propagation rules add complexity to composite artifacts
- Default grades may feel bureaucratic for trivial outputs (mitigated by R2 risk:
  agents auto-assign up to INFORMED_ESTIMATE, no human needed for routine work)

**Neutral:**
- v1-core enforcement is syntax-only — the rules exist but aren't blocking
- Grade labels match `know`'s vocabulary exactly — no translation layer needed

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Formal grade rules with propagation (recommended) | Clear, auditable, compound uncertainty visible | More rules for agents to follow | **Selected** — T4 theme requires it |
| Binary trust (trusted/untrusted) | Simple | Loses the granularity that makes NF-15 and PK-04 possible | Too coarse for 10+ UCs requiring nuanced confidence |
| No propagation (grades on leaves only) | Simpler, fewer rules | Composite artifacts carry no trust signal; humans must reconstruct | Defeats the purpose — the composite IS what humans review |
| Agent self-certification to VERIFIED_FACT | Fewer human gates | Agents cannot verify real-world facts (AP-01 regulations, RE-02 property data) | Unsafe — human attestation required for highest trust level |

## Related

- synthesis: SYNTHESIS-001 (Theme T4)
- arch_vision: docs/architecture/ARCHITECTURE-VISION.md (Principle P5)
- decisions: D-015 (epistemic grades with tiered enforcement)
- adrs: ADR-0008 (grades live on atoms — depends on atom schema)
- depends_on: ADR-0008
- depended_on_by: ADR-0007 (continuity state carries grades), ADR-0009 (orchestration
  routes by grade at gates), ADR-0012 (traceability includes grade metadata)
