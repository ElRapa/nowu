---
id: story-v1core-004-s002
source_epic: epic-v1core-004
source_problem: problem-008
source_use_cases:
  - AP-01
  - AP-02
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-004-s002 — AP Regulatory and Formulation Knowledge

## Story Statement

As Raphael (the multi-project human),
I want to query regulatory requirements for the aperitif business and receive a dependency-ordered answer, and to store and retrieve product formulation versions with full rationale and outcome history,
So that the AP project's most critical knowledge — what permits are still needed, and what was changed in each formulation and why — is preserved, traceable, and answerable from the knowledge base without consulting external notes.

## Appetite

Small — two complementary knowledge record types for the AP project: a regulatory requirements graph (with dependency ordering) and a versioned formulation record. Both use the same knowledge atom model; domain-specific schema extensions are an open question for P3.

## Acceptance Criteria

- **AC-001:** Given regulatory requirements for the AP business have been entered into the knowledge base, when Raphael asks "what permits do I still need to legally sell the aperitif?", then he receives a dependency-ordered answer from the knowledge base — with each outstanding requirement and its dependencies visible — and no external notes or spreadsheets are consulted.
- **AC-002:** Given a product formulation version exists in the knowledge base, when Raphael retrieves it, then the record shows: what was changed from the previous version, the taste or cost outcome, and whether the version was accepted or abandoned and why — recoverable even without access to the original creation device.
- **AC-003:** Given a new formulation version is recorded, when the record is written, then it carries a link to the prior version — so the complete formulation history is navigable as a version chain, not a flat list.

## Out of Scope (story-level)

1. Supply chain modelling or risk analysis for AP (AP-03 — v1.2 scope).
2. Market intelligence capture for AP (AP-04 — v1.1 scope).
3. Business milestone planning and timeline tracking for AP (AP-05 — v1.2 scope).
4. Domain-specific reporting for external audiences (RE-07 / AP — v1.2 scope).

## Architecture Signals

- Likely touches: know (knowledge atom storage; dependency-graph query; version chain representation)
- Likely touches: core (AP project context; regulatory requirement schema; formulation version schema)
- Likely touches: soul (regulatory query response generation; formulation history retrieval)
- May require: a freshness or status field on regulatory requirement atoms (e.g., "pending", "obtained", "expired") to support dependency-ordered gap queries
- Unknown whether: the existing knowledge atom model supports inter-atom dependency relationships (required for regulatory dependency ordering) without schema extension — P3 must resolve this

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | AP-01 | Raphael (multi-project human) | "What permits do I still need?" answered from knowledge base with dependency ordering — no external notes required |
| AC-002 | AP-02 | Raphael (multi-project human) | Formulation history retrievable with full version rationale — change, outcome, and accept/abandon reason all present |
| AC-003 | AP-02 | Raphael (multi-project human) | Complete formulation history navigable as a version chain — not a flat undifferentiated list |
