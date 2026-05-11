---
artifact_type: INTAKE_BRIEF
intake_id: intake-001
status: READY_FOR_S1
created_at: 2026-05-10
workflow_mode: A
use_case_ids: [NF-01]
affected_modules: [core, flow]
appetite: small
priority: high
source: docs/ROADMAP-003.md (W4)
---

# Intake Brief: Resume Work After Context Loss

## Problem Statement

When an AI session ends abruptly, critical context is lost. The user must manually reconstruct what was happening, losing momentum. This problem affects both agents and humans, leading to inefficiency and frustration.

## Use Cases

- **NF-01: Resume Work After Context Loss**
  - **Stage Target**: v1-core
  - **Actor**: Any AI agent and Multi-Project Human
  - **Situation**: A new session starts after an abrupt end. Context is missing.
  - **Need**: Reconstruct enough context to continue productive work seamlessly.
  - **Success**: Agents propose the correct next action; humans resume without re-orientation.
  - **Failure**: Agents restart or contradict prior work; humans lose trust.

## Acceptance Criteria

1. Agents must read persisted state, identify the last verified checkpoint, and propose the correct next action.
2. Humans must receive a clear signal of where things stand to confidently resume direction.
3. No hallucination of progress or contradictions with prior decisions.

## Affected Modules

- **core**: Session contracts, `SessionStore` protocol.
- **flow**: Session orchestration, pipeline state.

## Appetite

Small. This is scoped as the first S1-S9 cycle to validate the workflow, not to build the full continuity engine.

## Context

This is the first S1-S9 intake per W4, selected because NF-01 is a v1-core UC in the critical path. It addresses the most fundamental user pain point (context loss) and exercises `core` and `flow` modules.