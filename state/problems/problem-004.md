---
id: problem-004
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-004

## Core Problem

The framework accumulates session records and completed work, but neither improves its own behaviour from what it learns nor verifies that delivered work connects back to any stated goal. The same type of mistake recurs across sessions because no analysis runs. Work that was never needed gets delivered and accepted because no traceability check is enforced. The system grows more documented over time without growing more capable or more aligned.

## Validated Personas

**Primary:** Raphael (the multi-project human) — builds and runs the framework; needs it to self-improve so that using it longer produces measurably better outcomes.
**Secondary:** AI agents (curator, reviewer, shaper) — must both produce traceability evidence and consume it to improve future behaviour.

## Confirmed Outcome Goals

1. Every deliverable carries an unbroken link from code or output → acceptance criterion → use case ID, machine-verifiable at review time.
2. Recurring failure patterns in session history are detected and actively fed back into agent behaviour — not just documented.
3. The framework demonstrably improves over sessions: patterns identified early in the cycle are not repeated in later cycles.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| Session logs contain enough signal to detect patterns without additional instrumentation | Accepted — capture records (S9), review reports (S8), and VBR outputs (S7) collectively contain pattern-relevant data without additional logging. | Confirms design: learn from existing artifacts, not new infrastructure |
| Lessons fed back into agent memory will change behaviour | Needs investigation — the mechanism for feeding lessons into future agent prompts or constraints is not yet defined. This is the highest-risk open question; it **must be resolved during P3/S2 as a mandatory architecture question**, not deferred. P3 must evaluate existing approaches from external frameworks and research before proposing options: see Architecture Signal below. | Marks NF-06 implementation as requiring an explicit approach decision — if P3 does not answer this, the appetite inflates to Medium at S2 |

## Architecture Signal (P3 mandatory input)

Before shaping NF-06, P3 must survey existing approaches to agent memory and lesson feedback:

- **Guo et al. (2025)** — research on agent self-reflection and feedback loops; examine what "learning" mechanisms are tractable without a full training pipeline.
- **oh-my-claude / similar prompt-engineering frameworks** — review how persistent system prompt evolution and memory injection are handled in practice.
- **LangGraph** — examine its approach to persistent state, node-level memory, and cross-run knowledge; assess whether their patterns are reusable or instructive for nowu's architecture.

P3 must produce an explicit options comparison covering at least: (a) appended lesson block in system prompt, (b) structured memory store queried at agent startup, (c) constraint injection into task specs. The chosen approach becomes an ADR.

## Appetite

- [ ] Tiny (< 2 h)
- [x] Small (< 1 day)
- [ ] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** NF-09 (traceability) is already partially operational — task specs carry story_id and validation_trace fields. The main gap is enforcement at review time (S8). NF-06 (learning) is more open-ended but scoped to pattern detection from existing artifacts and a defined feed-back mechanism, not a full curriculum system. Together these are Small scope.

## Out of Scope (explicit)

1. Automated lesson application without human confirmation — any lesson learned must be reviewed before changing agent behaviour.
2. Health metrics dashboards (NF-08 — v1.1 scope).
3. Vision drift detection (NF-11 — v1.1 scope).
4. Cross-project lesson transfer (XP-03 — v1.1 scope).
5. Orphaned code detection via static analysis or linter integration — review-time check only in v1-core.

## Success Criteria

1. At review (S8), every acceptance criterion in a task spec has a traceable link to a UC-ID in USE_CASES.md — criteria without a traceable UC are flagged as blockers, not warnings.
2. After three or more sessions reveal the same failure type (e.g., a repeated scoping mistake, a recurring bug pattern), the pattern is surfaced in a capture record with an explicit reference to prior occurrences — and the next cycle shows evidence the agent incorporated it.
3. No orphaned feature is merged without a traceable use case ID — verified for 100% of deliverables in the first three cycles following implementation.

## Dependencies

Requires: problem-003 to be resolved first. Traceability enforcement (NF-09) runs at the S8 review step, which presupposes the task spec structure from problem-003 (NF-03/NF-04/NF-05). Pattern learning (NF-06) requires completed capture records from prior cycles — it cannot run until at least one full cycle has been captured.

## UC Coverage

- NF-06: Learn From Past Mistakes Across Sessions
- NF-09: Ensure Every Deliverable Traces Back to a Use Case
