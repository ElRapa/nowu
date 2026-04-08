---
id: story-v1core-001-s003
source_epic: epic-v1core-001
source_problem: problem-006
source_use_cases:
  - PK-01
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-001-s003 — Frictionless Structured Capture

## Story Statement

As Raphael (the multi-project human),
I want to record a thought using a structured template in under 2 minutes, with the result automatically project-linked and findable,
So that valuable observations captured away from a desk or mid-task do not require categorisation effort at capture time and are not lost.

## Appetite

Small — one structured capture flow with a minimum-field template. The async enrichment pipeline and multi-interface access are explicitly deferred; only the desktop CLI path with a lightweight template is in scope.

## Acceptance Criteria

- **AC-001:** Given Raphael has a thought to capture, when he initiates capture from the CLI, then a structured template is presented, the minimum required input is a single field (the thought itself), and all other fields are optional — so the full capture interaction completes in under 2 minutes.
- **AC-002:** Given a capture is submitted, when Raphael later searches across that project's records, then the captured item is findable by its content without any additional categorisation step having been required at capture time.
- **AC-003:** Given a capture is submitted within the context of an active project, when the capture record is written, then it carries a project link to that project — automatically, with no manual routing step.

## Out of Scope (story-level)

1. Multi-interface capture (voice, mobile, remote) — that is PK-08, deferred to v1.
2. Asynchronous enrichment or automatic evaluation of captured signals — deferred to v1.1.
3. Cross-project capture routing without a known active project context.
4. Knowledge decay, archival, or expiry of capture records.

## Architecture Signals

- Likely touches: bridge (CLI capture entry point)
- Likely touches: core (capture record schema; project-linking convention)
- Likely touches: soul (structured template rendering)
- May require: a minimum-field capture schema that supports optional enrichment fields without schema breakage
- Unknown whether: project-linking is resolved at capture time by convention (current project) or requires an explicit context signal

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | PK-01 | Raphael (multi-project human) | Captured in under 2 minutes — single required field, all others optional |
| AC-002 | PK-01 | Raphael (multi-project human) | Findable without additional action — searchable by content immediately after capture |
| AC-003 | PK-01 | Raphael (multi-project human) | Project-linked automatically at capture time — no manual routing step |
