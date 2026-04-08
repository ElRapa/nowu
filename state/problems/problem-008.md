---
id: problem-008
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-008

## Core Problem

The nowu framework delivers continuity, decision memory, and structured knowledge management for software development — but these same capabilities are not yet validated for the human's non-software work. The food business is managed in notes, spreadsheets, and memory: regulatory permits are scattered, formulation history is lost, business decisions are made in conversations and forgotten before the next meeting. The real-estate business runs on paper and institutional knowledge that lives in people's heads. The framework's value is available only in the one domain where the human already has the most tooling.

## Validated Personas

**Primary:** Raphael (the multi-project human) — operates a food & beverage business and a real-estate business alongside his software work; needs the same quality of continuity, reasoning traceability, and knowledge compounding in those domains.

## Confirmed Outcome Goals

1. Regulatory requirements for the AP business are tracked as living knowledge: every requirement has a source, a status, and its dependency on other requirements visible — the human can ask "what do I still need to do to legally sell this product?" and get an accurate, dependency-ordered answer.
2. Product formulations are version-controlled as knowledge: each version has its rationale, what was changed, what was tested, and why it was accepted or abandoned — recoverable even if the original device is lost.
3. Business and investment decisions in both the AP and RE domains carry the same traceable reasoning as architectural decisions in software: options generated, rationale recorded, chosen path and rejected alternatives preserved.
4. Current RE business processes are documented as structured knowledge before any digitalisation begins: steps, participants, inputs/outputs, and bottlenecks are captured and linked to each other.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| Non-software domains will benefit as much as software from the same framework | Needs investigation — this problem exists specifically to test this assumption. If AP and RE work requires substantial bespoke domain configuration, the 12-month "six projects" vision horizon is at risk. | This is an explicit assumption-test; problem-008 MUST surface findings at S9 capture for later P-cycle consideration |
| The framework can represent regulatory knowledge (permits, dependencies, deadlines) without a domain-specific schema extension | Needs investigation — regulatory requirements have freshness models, expiry, and inter-dependencies that differ from software ADRs. The P3 architecture pass must assess whether the existing knowledge atom model is sufficient. | Affects P3/S2: open architecture question |
| Decision capture overhead in non-software domains is manageable | Accepted as a real risk — AP-06 and RE-06 decisions happen in conversations (supplier meetings, property negotiations) rather than in structured sessions. Capture must work at conversation pace, not only in desk sessions. | Links to problem-006 (frictionless capture): AP and RE decision triggers often arrive away from a computer |

## Appetite

- [ ] Tiny (< 2 h)
- [ ] Small (< 1 day)
- [x] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** Five distinct outcome goals across two non-software domains. Each is individually Small, but the human's non-software work must benefit from the same continuity and decision memory as their software work — without bespoke infrastructure per domain. Validating that the framework is genuinely domain-agnostic makes this a Medium problem: the output is both delivered capability and an explicit answer to whether the framework scales across domains.

## Out of Scope (explicit)

1. Supply chain modelling and risk analysis for AP (AP-03 — v1.2 scope).
2. Business milestone planning and timeline tracking for AP (AP-05 — v1.2 scope).
3. Collaborator onboarding for AP or RE projects (AP-07 — v1.2 scope).
4. Property lifecycle tracking, stakeholder mapping, or digitisation prioritisation for RE (RE-02, RE-03, RE-04 — v1.2 scope).
5. Market intelligence capture for AP (AP-04 — v1.1 scope).
6. Investment decision analytics across multiple properties (beyond the first decision record for RE-06).
7. Report generation for external audiences (RE-07 — v1.2 scope).

## Success Criteria

1. The human can ask "what permits do I still need to legally sell the aperitif?" and receive a dependency-ordered answer from the nowu knowledge base — no consultation of external notes required.
2. Formulation version N can be retrieved with its full history: what changed from version N-1, the taste or cost outcome, and the reason for acceptance or abandonment.
3. At least one business decision in the AP domain and one investment decision in the RE domain are recorded with full traceable reasoning (options, rationale, chosen path, rejected alternatives) — retrievable six months later without context prompting.
4. Enough core RE business processes are documented as structured knowledge — with steps, handoffs, and identified bottlenecks — to confidently prioritise the first digitalisation sprint. The right number is whatever suffices to make that prioritisation decision; quantity is not the goal.
5. A structured retrospective note is produced at S9 answering: did the framework need domain-specific changes to serve AP and RE, and if so what? This feeds directly into the next pre-workflow cycle.

## Dependencies

Requires: problem-005 to be resolved first. The AP and RE projects must be bootstrapped as independent project contexts before domain-specific knowledge can be stored in them. The decision traceability capabilities used by AP-06 and RE-06 require problem-002 (decision memory) to be operational. The frictionless capture mechanism from problem-006 is recommended before AP and RE work begins in earnest (many observations arise away from a computer), but is not strictly required.

Requires: problem-002 to be resolved first (for AP-06 and RE-06 decision traceability).

## UC Coverage

- AP-01: Track Regulatory Requirements as Living Knowledge
- AP-02: Manage Product Formulation as Versioned Knowledge
- AP-06: Evaluate a Business Decision With Traceability
- RE-01: Inventory Existing Processes Before Digitalization
- RE-06: Support Long-Term Investment Decision Tracking
