---
id: goal-003
title: "Compounding Knowledge"
status: proposed
parent_vision_horizon: "12 Months — Knowledge compounds across projects"
created: 2026-04-29
linked_epics:
  - epic-v1core-004
retired_reason:
---

# Goal Brief: goal-003 — Compounding Knowledge

## Outcome Goal

**Linked Horizon:** "12 Months — Knowledge compounds across projects"
**Desired Change:** Knowledge accumulates within each project and starts to connect usefully across them. The framework serves non-software domains with the same traceability, continuity, and decision memory it provides for software. Someone else could pick up any project from the artifacts alone.
**Success Signals:**
- Cross-project connections the human would never find themselves are surfaced actively, not on demand
- At least two non-software projects are running with the same artifact fidelity as software projects
- A project can be handed off to someone who was not the original builder, using only the stored artifacts
**Non-Goals:** This goal does not address the 24-month "company operating system" horizon — it does not include shipping the framework externally, collaboration layers, or data governance. It also does not address making individual cycles faster.

## Solution Shape

**Form:** A shared, queryable knowledge base that spans projects plus verified domain extension to non-software work
**Key Capabilities:**
- Active surfacing of cross-project connections from the accumulated artifact store
- Domain-neutral artifact structure that works for software, AP, and RE projects without separate formats
- Knowledge base queryable by humans and AI agents alike
- Proof-of-domain validation: at least two non-software projects running end-to-end through the workflow
**Main Tradeoffs:** Accepting that the cross-project connection surfacing in v1 is coarse — pattern-based rather than deep semantic — in order to deliver something real at the 12-month mark. Deferring fine-grained ontology and knowledge graph construction.
**Sequencing Notes:** Depends on goals 001 and 002 being stable; the knowledge base is only as good as the artifacts being fed into it. Non-software domain validation requires live projects running through a working workflow.
**Epic Seeds:** Knowledge That Compounds, Domain Extension
