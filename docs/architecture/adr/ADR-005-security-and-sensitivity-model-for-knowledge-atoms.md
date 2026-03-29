---
id: ADR-005
status: PROPOSED
title: Security and sensitivity model for knowledge atoms
created: 2026-03-29
source: global-pass-2026-03-29 (ADR-F-005)
priority: CRITICAL — must be ACCEPTED before co-locating personal and business knowledge
---

# ADR-005 — Security and sensitivity model for knowledge atoms

## Status

PROPOSED

## Context

PK-06, AP-07, and RE-07 all require a sensitivity model for knowledge atoms. Without one, a generated report or a cross-project knowledge discovery could expose personal financial data, regulatory filings, or property records to unintended readers.

Today (Stage 1, solo developer): personal knowledge and framework-development knowledge already coexist in the same `know` instance. This is currently acceptable because there is only one user and no collaborators. However, Stage 2+ will add:

- Business domain knowledge (AP: product formulation, regulatory requirements)
- Real estate knowledge (RE: property records, financial projections)
- Potential collaborators who should not see all knowledge

The system boundary between containers requires clarification:
- `core` defines the policy contract (what is allowed)
- `know` enforces at query time (access-scoped queries)
- `bridge` checks policy before surfacing results to the user

This is a **security constraint**, not a preference. It must be ACCEPTED before any implementation co-locates PK-06 class atoms (personal knowledge) with AP or RE business knowledge in the same `know` instance.

**Priority:** Must be ACCEPTED before Stage 2 begins or before any AP/RE data is stored alongside personal knowledge.

## Decision

[HUMAN TO COMPLETE]

## Options Considered

**(A) Per-atom sensitivity tag + `know` query filter**
Each atom receives a `sensitivity` field (e.g. `public`, `private`, `confidential`). `bridge` reads the active user's clearance level and passes a filter to `know` queries. `core` defines the `SensitivityPolicy` Protocol that `bridge` must call before any query. `know` enforces the filter at query time. Fine-grained control; fits existing atom schema. Requires all existing and future atoms to have a sensitivity tag (migration needed for existing atoms).

**(B) Project-level visibility (all atoms in a project share sensitivity level)**
The sensitivity level is set at the project scope, not the atom level. All atoms in `project_scope="aperitif"` are `confidential`; all atoms in `project_scope="nowu"` are `internal`. Simpler to administer; no per-atom migration needed. Less flexible: a single "personal moment" captured in an AP project inherits the project's sensitivity level. Cross-project discovery (XP-01) must respect project-level visibility.

**(C) No enforcement in v1 — document as known accepted risk, defer to Stage 2**
Explicitly record that the current single-user, no-collaborator context makes enforcement unnecessary for Stage 1. Define a hard gate: before any AP or RE project is bootstrapped into `know`, or before any collaborator is onboarded, ADR-F-005 must be ACCEPTED with option A or B. Lowest engineering cost now; requires discipline to enforce the gate before Stage 2 proceeds.

## Consequences

[HUMAN TO COMPLETE]
