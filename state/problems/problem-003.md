---
id: problem-003
source_idea: idea-v1core
source_discovery: disc-v1core
created: 2026-04-07
status: APPROVED
authored_by: perspective-interview@P1.2
reviewed_at:
---

# Problem Statement: problem-003

## Core Problem

AI agent work that should be bounded frequently expands into adjacent concerns, produces unverified claims of completion, and blocks human attention at the wrong moments. Without active scope enforcement, quality self-assessment, and tiered routing of approvals, the human either micro-manages the pipeline (high friction) or loses confidence in its output (low trust). Neither is compatible with a 90–99% AI-handled workflow.

## Validated Personas

**Primary:** Raphael (the multi-project human) — needs the pipeline to handle execution without requiring his attention for every step, while halting reliably when his input genuinely matters.
**Secondary:** AI agents (shaper, implementer, reviewer) — must operate within clear boundaries and self-verify before claiming work is complete.

## Confirmed Outcome Goals

1. Every piece of work is bounded before execution starts: explicit scope, explicit exclusions, and acceptance criteria that an agent can verify independently.
2. The pipeline verifies actual output (tests pass, criteria met) before representing work as done — the human never encounters broken or incomplete work in their review queue.
3. Human attention is held precisely for high-stakes decisions; low-risk, verified work flows through without interruption.

## Flagged Assumptions (resolved)

| Assumption | Resolution | Impact |
|---|---|---|
| Scope creep is primarily an AI agent failure, not a human one | Partially accepted — agents expand scope opportunistically, but underdefined task specs are also a cause. Mitigation: the shaping step (NF-03) must produce explicit boundaries that serve as the enforcement input, not just guidance. | Affects design: task spec is a contract, not a suggestion |
| Self-assessment can catch real failures without running actual tests | Rejected — self-report is insufficient. VBR protocol must run actual tests in a verifiable environment. | Confirms NF-04 design: actual execution required, not agent self-evaluation |

## Appetite

- [ ] Tiny (< 2 h)
- [ ] Small (< 1 day)
- [x] Medium (2-3 days)
- [ ] Large (up to 1 week)

**Rationale:** Three workflow mechanics must be implemented and integrated: shaping (NF-03), verification (NF-04), and approval routing (NF-05). Each is tractable alone; together they define the complete execution pipeline from shaped task to reviewed output.

## Out of Scope (explicit)

1. Health metrics and framework performance tracking (NF-08 — that is v1.1 scope).
2. Automated tier-classification learning from past approval history — manual tier rules are sufficient for v1-core.
3. Concurrency or multi-agent conflict resolution (XP-06 — that is v2 scope).
4. Non-technical task verification (documentation, diagrams) — VBR scope is code-producing tasks only.

## Success Criteria

1. Every task entering execution has a defined scope (what's in, what's out, measurable acceptance criteria) — and the implementer agent never touches files outside the declared scope.
2. Only verified-passing work reaches the human review queue — agents claiming completion without passing the VBR protocol are recycled, not forwarded.
3. At mid-day, the human can review and approve a batch of 5 queued items in under 15 minutes, with Tier 3 items (merges, breaking changes) having halted automatically at the correct boundary.

## Dependencies

Requires: problem-001 to be resolved first. Scope enforcement requires knowing where the last verified boundary was; approval routing requires persisted state of what is pending. The shaping step also references prior decisions, which connects to problem-002, but problem-003 can be started in parallel with problem-002 since it does not depend on decision records being in place — it creates its own task-level records.

## UC Coverage

- NF-03: Scope a Piece of Work Without Scope Creep
- NF-04: Self-Assess Quality Without Human Intervention
- NF-05: Route Approvals Without Blocking Progress
