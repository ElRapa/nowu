---
id: story-v1core-002-s005
source_epic: epic-v1core-002
source_problem: problem-003
source_use_cases:
  - NF-05
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s005 — Tiered Approval Routing

## Story Statement

As Raphael (the multi-project human),
I want work to be automatically routed by tier — Tier 1 flowing through without interruption, Tier 2 batching for my periodic review, and Tier 3 halting immediately for my decision — with routing determined by predefined rules rather than agent discretion,
So that my attention is reserved for decisions that genuinely require it and I can process a batch of queued items efficiently.

## Appetite

Small — tiered routing applies a classification rule to each work item at the point it is ready for handoff. The rules themselves are human-defined; the routing mechanism reads the classification and acts accordingly. No ML-based tier learning is in scope.

## Acceptance Criteria

- **AC-001:** Given a work item is ready for handoff and its tier has been classified by the predefined rules, when the routing step runs, then: Tier 1 items are forwarded automatically without interrupting Raphael; Tier 2 items are queued for batch review; Tier 3 items halt the pipeline and surface an immediate notification to Raphael.
- **AC-002:** Given 5 Tier 2 items have accumulated in the review queue, when Raphael opens the batch review view, then he can evaluate and approve or reject all 5 items in under 15 minutes — each presented with enough context to decide without re-reading source artifacts.
- **AC-003:** Given a Tier 3 item is identified (merge, breaking change, or other predefined Tier 3 trigger), when the routing step runs, then the pipeline halts at that item, no subsequent work in the same cycle proceeds, and Raphael receives a prompt with the specific Tier 3 trigger identified.

## Out of Scope (story-level)

1. Automated tier-classification learning from past approval patterns — manual tier rules are the v1-core mechanism.
2. Concurrent pipeline management across multiple active Tier 3 halts.
3. Tier reclassification by the agent without human authorisation.
4. Health dashboards or metrics for routing accuracy (NF-08 — v1.1 scope).

## Architecture Signals

- Likely touches: flow (handoff step — tier classification read and routing decision)
- Likely touches: bridge (halt notification for Tier 3; batch review presentation for Tier 2)
- Likely touches: core (tier classification rules as a persistent, human-editable configuration)
- May require: a tier field on every work item's handoff artifact, set at shaping time (S5)
- Unknown whether: Tier 2 batching requires a persistent queue or is assembled on demand from the persisted state of pending items

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-05 | System / Raphael (multi-project human) | Tier routing determined by predefined rules — Tier 1 auto-proceeds, Tier 2 batches, Tier 3 halts immediately |
| AC-002 | NF-05 | Raphael (multi-project human) | 5 Tier 2 items reviewable in under 15 minutes |
| AC-003 | NF-05 | Raphael (multi-project human) | Tier 3 halts correctly — pipeline does not proceed until Raphael resolves the halt |
