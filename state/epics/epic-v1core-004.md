---
id: epic-v1core-004
source_problem: problem-007, problem-008
created: 2026-04-08
status: APPROVED
agent_version: story-mapper@2.3 (enriched)
parent_goal: goal-003  # Compounding Knowledge — accumulates within and across projects (TBD: idea-006)
generated_at: 2026-04-08T00:00:00Z
---

# Epic: epic-v1core-004 — Knowledge That Compounds

## Epic Summary

This epic delivers the two capabilities that turn the framework from a personal productivity tool into a compounding knowledge system: active surfacing of cross-project connections that the human would never find themselves (problem-007), and verified proof that the framework serves non-software domains — AP and RE — with the same traceability, continuity, and decision memory it provides for software (problem-008). Together they make the 12-month "six active projects, compounding knowledge base" vision horizon achievable rather than aspirational.

This epic is the v1-core probe of Discovery Theme 4 (Knowledge That Compounds Across Projects) and Theme 7 (AI as Expertise Bridge), and explicitly tests whether the nowu framework is genuinely domain-agnostic or software-only in practice. The AP and RE stories are not nice-to-haves — they are the assumption-test that determines whether the 12-month vision horizon is on track.

## Vision & Discovery Alignment

- **Vision (12 months):** "At least six projects are active across different domains… each one compounding on the others… The knowledge base is genuinely richer than the sum of individual projects." This epic delivers the first cross-project surfacing capability (XP-01) and the first non-software domain validation (AP + RE).
- **Vision (Guiding Principles):** "Every domain I work in should benefit from the same quality of continuity and reasoning traceability." AP-01, AP-02, AP-06, RE-01, and RE-06 are the concrete test of this principle against real non-software work.
- **Discovery Theme 4 (Knowledge Compounds):** Directly addressed by XP-01. The cross-project connection surfacing turns siloed project knowledge into a compounding shared resource.
- **Discovery Theme 7 (AI as Expertise Bridge):** Addressed by AP-01 and AP-02 — the framework must handle regulatory requirements and formulation history with the same fidelity it handles ADRs and code decisions.
- **Discovery Assumption 3 (Domain-agnostic framework):** This epic is the explicit assumption test. The S9 retrospective note for problem-008 is a first-class epic output.

## Use Case Mapping

| UC-ID | Description | Covered by |
|---|---|---|
| XP-01 | Discover Connections Across Projects Automatically | story-v1core-004-s001 |
| AP-01 | Track Regulatory Requirements as Living Knowledge | story-v1core-004-s002 |
| AP-02 | Manage Product Formulation as Versioned Knowledge | story-v1core-004-s002 |
| AP-06 | Evaluate a Business Decision With Traceability | story-v1core-004-s003 |
| RE-06 | Support Long-Term Investment Decision Tracking | story-v1core-004-s003 |
| RE-01 | Inventory Existing Processes Before Digitalization | story-v1core-004-s004 |

### v1-core Slice Only

For this epic, each UC is scoped to its v1-core slice:

- **XP-01:** Cross-project connection surfacing uses entity-overlap or semantic similarity (approach decided at P3 — see problem-007 Architecture Signal). Suggestions are dismissible, never interrupting. v1-core measures signal-to-noise via dismissal rate. No automated lesson transfer, no permanent cross-project links.
- **AP-01 / AP-02:** Regulatory requirements and formulations are stored as knowledge atoms with standard fields (source, status, rationale). No domain-specific schema extensions unless P3 determines the existing atom model is insufficient (open architecture question — see problem-008).
- **AP-06 / RE-06:** Business and investment decisions use the same ADR-style structure as software decisions. No bespoke decision types.
- **RE-01:** Process documentation uses the standard knowledge atom format. Scope is discovery of existing processes, not redesign or optimisation.

**Key prior art for P3 (mandatory):** Review `know` library (Projects/know) — ADR-0001, ADR-0003, ADR-0004, `adapter.py`, `NOWU_KNOW_USAGE_CONTRACTS.md` — before designing the XP-01 detection layer.

## Story Index

| Story ID | Title | Appetite | Priority |
|---|---|---|
| story-v1core-004-s001 | Cross-Project Connection Discovery | Small | Must |
| story-v1core-004-s002 | AP Regulatory and Formulation Knowledge | Small | Must |
| story-v1core-004-s003 | AP and RE Decision Traceability in Practice | Small | Must |
| story-v1core-004-s004 | RE Process Documentation as Structured Knowledge | Small | Should |

### Story Success Bounds (v1-core)

- **story-v1core-004-s001 (Cross-Project Discovery):** Delivers a surfacing mechanism that proposes connections across projects when the human is in a relevant context; Raphael can act on, link, or dismiss each. It does not create permanent links, transfer lessons automatically, or guarantee coverage across all possible entity types.
- **story-v1core-004-s002 (AP Regulatory + Formulation):** Delivers regulatory requirements as structured knowledge (source, status, dependencies) and product formulations as versioned records with rationale. It does not include supply chain modelling, market intelligence, or milestone tracking.
- **story-v1core-004-s003 (AP + RE Decision Traceability):** Delivers at least one end-to-end decision record for each domain using standard ADR-style structure. Proves the mechanism works; does not build a decision analytics layer.
- **story-v1core-004-s004 (RE Process Documentation):** Delivers structured process records sufficient to prioritise the first digitalisation sprint. Scope is documentation and discovery, not process redesign or stakeholder mapping.

## Out-of-Scope for v1-core (for this Epic)

- No automated cross-project lesson transfer (XP-03: v1.1).
- No permanent or structural cross-project links — surfacing only, human-confirmed.
- No domain-specific schema extensions beyond what the standard atom model requires — unless P3 finds it necessary (open question).
- No supply chain modelling, milestone planning, or market intelligence for AP (AP-03, AP-04, AP-05: v1.2).
- No property lifecycle tracking, stakeholder mapping, or digitisation prioritisation for RE beyond RE-01 (RE-02, RE-03, RE-04: v1.2).
- No report generation for external audiences (RE-07: v1.2).
- No investment analytics across multiple RE properties — one traceable decision record is the v1-core target.

## Scope Hammer Log

| Dropped Story | Reason |
|---|---|
| Automated cross-project lesson transfer | XP-03 is v1.1 scope. Surfacing connections (XP-01) must prove useful and non-noisy before automated transfer is appropriate — transfer without quality signal is high-risk. |
| Supply chain modelling for AP | AP-03 is v1.2 scope. The food business is still in early regulatory and formulation phase; supply chain modelling is premature before the product is closer to legal operation. |
| AP business milestone planning and tracking | AP-05 is v1.2 scope. Milestones are only meaningful once the formulation and regulatory baseline is established — which this epic lays, not extends. |
| Property lifecycle tracking and stakeholder mapping for RE | RE-02, RE-03, RE-04 are v1.2 scope. Process documentation (RE-01) must establish the knowledge foundation before lifecycle and stakeholder overlays are worth building. |
| Investment decision analytics across multiple RE properties | problem-008 explicitly defers this. One traceable investment decision record is the right v1-core target; analytics require a history that does not yet exist. |
| Report generation for external audiences | RE-07 is v1.2 scope. The RE knowledge base must exist and prove accurate before external-facing reports are a viable output. |

## Assumption Probes & Tensions

This epic is explicitly testing:

- **Assumption 3 (Domain-agnostic framework):** The AP and RE stories are the direct test. The mandatory S9 retrospective note (problem-008 SC-5) must answer: did the framework need domain-specific changes, and if so what? This feeds directly into the next pre-workflow cycle.
- **Assumption (Cross-project signal quality):** XP-01's dismissal-rate metric (target: < 70% dismissed over first month) tests whether the detection mechanism produces useful signal or noise. If dismissal is high, the detection approach chosen at P3 may need revision.
- **Assumption (know library fitness):** P3 must assess whether the existing `know` implementation is sufficient for XP-01, or whether it needs extension. The outcome becomes a binding P3 architecture decision.

Key tensions monitored:

- **Tension F (Connection surfacing vs. workflow interruption):** XP-01 suggestions must be relevant enough to act on but must never disrupt the current project's flow. We watch for: user reports of distraction, high dismissal rate, or suggestions arriving at wrong moments.
- **Tension G (Standardisation vs. domain fit):** Using ADR-style records for AP regulatory requirements and RE investment decisions tests whether standard structure is genuinely flexible. We watch for: fields that feel forced, required context that the standard format cannot hold, or the human reverting to external notes for domain-specific data.
- **Tension H (Breadth of domain coverage vs. depth of value):** Covering both AP and RE in v1-core tests breadth; the risk is that neither domain gets deep enough treatment to be genuinely useful. We watch for: the human still using external tools for AP or RE work after v1-core is delivered.

## Epic Appetite

Total: 4 Small — fits within 2 implementation cycles (cross-project knowledge cycle + domain dogfooding cycle)
