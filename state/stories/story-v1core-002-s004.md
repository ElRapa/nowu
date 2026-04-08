---
id: story-v1core-002-s004
source_epic: epic-v1core-002
source_problem: problem-003
source_use_cases:
  - NF-04
created: 2026-04-08
status: APPROVED
---

# Story: story-v1core-002-s004 — Verified-Before-Reporting Quality Gate

## Story Statement

As Raphael (the multi-project human),
I want work to be reported as complete only after actual tests have passed in a verifiable environment,
So that I never encounter broken or unverified work in my review queue, and I can trust that agent self-reports of completion are backed by real evidence.

## Appetite

Small — the VBR gate is a protocol step inserted between implementation completion and human review. It runs the test suite in a real environment and cycles back to the implementer if tests fail. No new verification infrastructure is required; the existing test runner is the verification environment.

## Acceptance Criteria

- **AC-001:** Given an agent submits work as complete, when the VBR protocol runs, then it executes the project's tests in an actual runtime environment and produces a verifiable pass/fail result — not an agent self-assessment.
- **AC-002:** Given the VBR protocol produces a failing result, when the failure is recorded, then the work is returned to the implementer with the specific failure details — and it is not forwarded to the human review queue until a subsequent VBR run produces an all-passing result.
- **AC-003:** Given the VBR protocol produces a passing result, when the work is forwarded to the human review queue, then the review artifact includes the VBR pass evidence (test output summary) — Raphael can confirm verification occurred without re-running tests himself.

## Out of Scope (story-level)

1. Verification of non-code deliverables (documentation, diagrams, decision records) — VBR scope is test-producing work only.
2. Automated remediation or self-healing of failing tests.
3. Performance, load, or security testing — functional correctness only.
4. Health metrics and cycle-time tracking for VBR (NF-08 — v1.1 scope).

## Architecture Signals

- Likely touches: flow (S7 VBR step — test execution and cycle-back protocol)
- Likely touches: bridge (test runner invocation; result capture)
- May require: a structured VBR result artifact that carries the pass/fail summary and is attached to the review submission
- Unknown whether: VBR is a discrete workflow step (S7) or an inline check within the implementation step (S6)

## Validation Trace

| AC | UC-ID | Persona | Success Criterion |
|---|---|---|---|
| AC-001 | NF-04 | AI agent (quality) | VBR executes actual tests in a real environment — not agent self-evaluation |
| AC-002 | NF-04 | Raphael (multi-project human) | Failing VBR cycles back to implementer — human never receives unverified work |
| AC-003 | NF-04 | Raphael (multi-project human) | VBR pass evidence attached to review submission — Raphael can confirm verification without re-running |
