---
id: story-v1core-004-s003
source_epic: epic-v1core-004
source_problem: problem-008
source_use_cases:
  - AP-06
  - RE-06
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-004-s003 — AP and RE Decision Traceability in Practice

## Story Statement

As Raphael (the multi-project human),
I want at least one AP business decision and one RE investment decision recorded using the same decision-recording mechanism as software ADRs — with options, rationale, chosen path, and rejected alternatives preserved,
So that I can retrieve either decision six months later and understand the full reasoning without re-doing the original analysis, and so that the framework's decision memory capability is validated as genuinely domain-agnostic.

## Appetite

Small — this story applies the decision-recording capability delivered by story-v1core-002-s001 to two real non-software domain decisions. The mechanism already exists; the scope here is the first real use of it in AP and RE, confirming domain-agnostic applicability.

## Acceptance Criteria

- **AC-001:** Given the AP project is bootstrapped and a real business decision arises (e.g., a supplier choice, a pricing decision, a regulatory strategy choice), when the decision is recorded using the framework's decision mechanism, then the record contains: options considered, chosen path with rationale, rejected alternatives with reasons, and conditions at the time.
- **AC-002:** Given the RE project is bootstrapped and a real investment decision arises (e.g., a property acquisition, a renovation scope choice, a financing strategy), when the decision is recorded using the same framework mechanism, then the record contains: options considered, chosen path with rationale, rejected alternatives with reasons, and conditions at the time.
- **AC-003:** Given both an AP decision and an RE decision have been recorded, when either is retrieved 6 months later (simulated by retrieval in a new session without context), then the full reasoning — options, rationale, chosen path, rejected alternatives — is readable without consulting external notes, meeting notes, or conversation history.

## Out of Scope (story-level)

1. Domain-specific decision templates with custom fields for AP or RE — the same schema as software decisions is used.
2. Analytics across multiple decision records for either domain.
3. Automated condition-change detection that prompts decision review (NF-11 — v1.1 scope).
4. Decision enforcement by a reviewer for AP or RE decisions — enforcement applies only within the workflow pipeline for code-producing tasks.

## Architecture Signals

- Likely touches: core (decision record retrieval in AP and RE project contexts; namespace isolation per project)
- Likely touches: soul (decision agent invoked in non-software domain context — must not assume software framing)
- Likely touches: flow (decision recording step applied to AP and RE project cycles)
- May require: the decision agent's options-generation prompt to be domain-agnostic — not anchored to ADR or software-specific framing
- Unknown whether: the same decision record schema satisfies both software ADR and business/investment decision types, or whether a thin wrapper is needed — this story must surface a finding at S9 capture

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | AP-06 | Raphael (multi-project human) | AP business decision recorded with options, rationale, chosen path, and rejected alternatives |
| AC-002 | RE-06 | Raphael (multi-project human) | RE investment decision recorded with options, rationale, chosen path, and rejected alternatives |
| AC-003 | AP-06, RE-06 | Raphael (multi-project human) | Both decisions retrievable 6 months later without context prompting — full reasoning preserved |
