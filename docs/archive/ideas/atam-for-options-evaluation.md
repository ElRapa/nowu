# Idea: Lightweight ATAM for S3 Options Evaluation

> Status: INCORPORATED into nowu-options.md and nowu-decider.md
> Origin: Research into architecture evaluation methods, 2026-03-15

## The Problem with "Best Option Wins"
Simple pros/cons lists produce decisions that feel subjective. When an agent
recommends Option A, the human can't tell if it was reasoned or guessed.
Disagreements are unresolvable because there's no shared scoring basis.

## ATAM (Architecture Tradeoff Analysis Method)
Developed by SEI at Carnegie Mellon. Key concepts:
- **Quality Attribute Scenarios**: concrete measurable goals (e.g., "system
  recovers from crash in <5 seconds")
- **Sensitivity Points**: architectural decisions that strongly affect one QA
- **Tradeoff Points**: decisions that improve one QA at cost of another
- **Risk/Non-Risk**: identified through scenario analysis

## Simplified ATAM for nowu (no full workshop needed)
In S3 (Options), the agent:
1. Identifies quality attributes that matter for this decision
   (default: simplicity, testability, modifiability, performance, migration cost)
2. Weights each 1-5 based on what matters most here
3. Scores each option H(3)/M(2)/L(1) per QA
4. Computes weighted total
5. Flags sensitivity and tradeoff points

In S4 (Decision), the decider:
1. Uses the scored matrix to recommend
2. Records tradeoff points in D-NNN (permanent record of what was sacrificed)
3. Uses tradeoff points at S8 Validation: "did we accept the expected tradeoff
   and is it acceptable in the actual implementation?"

## Why This Matters for AI Agents
Without a scoring method, the decider agent would "recommend" based on
whatever framing the options designer used — easily biased by how options
are described. A weighted matrix forces explicit quality attribute reasoning
and produces a justifiable, auditable decision record.

## Full ATAM for Future
For major architectural decisions (new module, new external system):
consider running a proper ATAM session with utility trees and scenario
prioritisation. Document as a dedicated ADR.
