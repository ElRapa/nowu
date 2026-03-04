# nowu Delivery Workflow

Date: 2026-03-04
Status: Active

This workflow defines how humans and AI agents execute work in `nowu` with consistent quality and low coordination overhead.

## 1) Roles

- Architect: frame architecture options and decisions.
- Shaper: convert goals into bounded executable tasks.
- Implementer: produce code/docs/tests for shaped tasks.
- Reviewer: validate against acceptance criteria, ADRs, and regressions.
- Curator: capture decisions/lessons/tasks into durable memory (`know`).

## 2) Workflow Loop (required)

1. Intake
- gather request, relevant use-case IDs, and affected modules
- load current context from `ARCHITECTURE.md`, `V1_PLAN.md`, `DECISIONS.md`

2. Architecture analysis
- define constraints, module boundaries, and failure modes
- identify assumptions that need validation

3. Design options
- produce 2-3 viable approaches
- include tradeoffs and migration implications

4. Evaluation and decision
- score options against delivery speed, modularity, reliability, and governance
- record the selected option and rationale in `DECISIONS.md` and/or `know`

5. Task shaping
- split into tasks sized for <=4h each
- specify in-scope, out-of-scope, dependencies, acceptance criteria, and test commands

6. Implementation
- execute one shaped task at a time
- avoid crossing module boundaries without an explicit decision update

7. Verify Before Reporting (VBR)
- run required tests/lint/checks
- compare outputs to acceptance criteria
- reject self-reported completion without proof

8. Review and approval routing
- Tier 1: auto-approve low-risk internal changes
- Tier 2: batch review queue (human periodic approval)
- Tier 3: explicit immediate human approval (high-impact actions)

9. Capture and close
- summarize decisions, facts, tasks, lessons
- persist to `know` (search first, deduplicate, then create/update/connect)

## 3) Approval Tiers

Tier 1 (auto):
- docs-only edits, test additions, non-breaking internal refactors

Tier 2 (batch):
- feature additions inside approved scope
- dependency changes with low operational risk

Tier 3 (block until human approves):
- destructive migrations
- policy/architecture reversals
- changes that alter data integrity or security posture

## 4) WAL and Session Rules

- Before every agent response in active implementation loops, update `soul/SESSION-STATE.md`.
- Keep WAL concise and actionable (current goal, decisions, next action, blockers).
- On session end, persist durable outcomes into `know` as decisions/lessons/tasks.

## 5) Artifacts Per Task

Every shaped task should produce:

1. task spec (scope, acceptance criteria, dependencies)
2. implementation diff
3. verification evidence (commands + outcomes)
4. decision updates (if architecture/policy changed)
5. knowledge capture summary

## 6) AI-centric Quality Rules

- Prefer explicit interfaces over implicit coupling.
- Prefer small reversible changes over large speculative rewrites.
- Keep prompt/context payloads focused (load only needed references).
- Use use-case IDs to justify scope and tests.
- If requirements are ambiguous, stop and resolve before coding.

## 7) Supporting Skills

The repository includes reusable skills for this workflow:

- `skills/nowu-architect`
- `skills/nowu-shaper`

Use them for architecture and shaping tasks to keep outputs consistent across sessions.

