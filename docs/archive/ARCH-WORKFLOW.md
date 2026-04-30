# Architecture Workflow – Implementation Notes

## Scope

Goal: implement extended P3 (architecture phase) and related artifacts
for the nowu pre-workflow, as described in the v3 architecture report.

## New agents

- .claude/agents/qa-elicitation.md
  - Input: problem-NNN, vision.md, quality.md, story-NNN-*.md
  - Output: state/arch/NNN-qa-scenarios.md

- .claude/agents/architecture-design.md
  - Input: problem-NNN, story-NNN-*.md, NNN-qa-scenarios.md,
           NNN-constraint-check.md, bounded-context-NNN.md?,
           docs/architecture/*
  - Output: state/arch/arch-pass-NNN.md

- .claude/agents/atam-lite.md
  - Input: arch-pass-NNN.md, NNN-qa-scenarios.md,
           docs/architecture/containers.md?, docs/architecture/risks.md?
  - Output: state/arch/NNN-atam-lite.md

## New architecture docs

- docs/architecture/quality.md      # QA scenarios registry
- docs/architecture/crosscutting.md # logging, auth, error handling, etc.
- docs/architecture/runtime.md      # C4 Dynamic diagrams for key flows
- docs/architecture/deployment.md   # C4 Deployment
- docs/architecture/risks.md        # risk register

## Runner wiring (pre-workflow)

For FULL / BOOTSTRAP modes, P3 should run:

- P3.0: domain modeling (if Epic/Product mode) → bounded-context-NNN.md
- P3.1: constraint-check (existing)
- P3.2: qa-elicitation → NNN-qa-scenarios.md
- P3.3: architecture-design (ADD 3.0) → arch-pass-NNN.md
- P3.4: atam-lite → NNN-atam-lite.md
- P3.5: ADRs (human)
- P3.6: update docs/architecture/*.md

Lite / Standard modes: skip P3.0–P3.4 as per mode rules.

## S1–S9 small changes

- S2 (constraints): if present, load docs/architecture/crosscutting.md
  and state/arch/NNN-atam-lite.md.
- S4 (decision): add “QA Scenario Impact” table to decision.md.
- S8 (review): verify implementation respects crosscutting.md.
- S9 (curator): update docs/architecture/risks.md with new risks/mitigations.
