# nowu v1 Plan

Date: 2026-03-22
Status: Rebased on `know` v0.4.0 (class-based `KnowledgeBase` API)

## 1) v1 Objective

Deliver a usable `nowu` core that can:

- recover and continue sessions reliably (`NF-01`)
- enforce architectural and quality gates (`NF-02`, `NF-04`)
- shape and execute bounded work (`NF-03`)
- route approvals safely (`NF-05`)
- bootstrap and run at least one additional project context (`NF-07`)
- leverage `know` for task queries and cross-project recall (`PK-03`, `XP-01`)

## 2) Delivery Strategy

Use incremental vertical slices. Every step contains:

1. architecture analysis
2. design options
3. evaluation and decision
4. detailed implementation plan
5. implementation + verification

## 3) Steps and Mini-plans

## Step 01 - Repo and Contract Baseline
Use cases: `NF-01`, `NF-02`, `NF-03`

Architecture analysis:
- define package/module boundaries (`core`, `flow`, `bridge`, `soul`)
- define what remains external (`know`)

Design options:
- A: flat module layout under one package
- B: per-module package with explicit interface files

Evaluation and decision:
- choose B for clearer agent boundaries and easier ownership

Detailed implementation plan:
1. create Python workspace scaffold and `pyproject.toml`
2. add interface contracts (`core/contracts/*.py`)
3. add architecture compliance tests (import boundaries)

Implementation + verification:
- tests: scaffold tests + boundary checks
- done when modules import cleanly and boundaries are enforced

## Step 02 - Memory Integration Layer
Use cases: `NF-01`, `NF-02`, `PK-03`, `XP-01`

Architecture analysis:
- identify required `know` operations and failure modes
- define session-to-knowledge write policy

Design options:
- A: direct `kb.*` calls everywhere (where `kb` is a `KnowledgeBase` instance)
- B: `core/memory_service.py` wrapper around `KnowledgeBase` + `KnowAdapter`

Evaluation and decision:
- choose B to centralize retries, validation, and project scoping

Detailed implementation plan:
1. implement `MemoryService` with typed methods (`record_decision`, `create_task`, `recall_context`, `task_overview`)
2. add input validation for grades/scope/tags
3. add integration tests against a temp `KNOW_DATA_DIR`

Implementation + verification:
- tests cover create/search/link/query/subgraph calls
- done when flow/bridge can use memory service without raw `kb.*` calls

## Step 03 - Session Runtime and WAL
Use cases: `NF-01`, `NF-04`

Architecture analysis:
- define minimal durable session state for crash recovery
- define what is WAL-only vs persisted to `know`

Design options:
- A: markdown WAL only
- B: markdown WAL + mirrored session summary atom

Evaluation and decision:
- choose B for auditability and recovery confidence

Detailed implementation plan:
1. implement `flow/session.py` state model + WAL writer
2. implement resume logic from `soul/SESSION-STATE.md`
3. implement session-end summarization contract

Implementation + verification:
- tests for resume, append events, interrupted sessions
- done when a killed session can restart and propose next action correctly

## Step 04 - Role Pipeline (Architect/Shaper/Implementer/Reviewer)
Use cases: `NF-02`, `NF-03`, `NF-04`

Architecture analysis:
- define role handoff artifacts and required invariants

Design options:
- A: free-form prompt handoffs
- B: structured role payloads (`analysis`, `options`, `decision`, `task_spec`, `verification`)

Evaluation and decision:
- choose B to reduce ambiguity and improve automated checks

Detailed implementation plan:
1. define payload schemas
2. implement pipeline orchestrator in `flow/orchestrator.py`
3. add automatic rejection for missing acceptance criteria

Implementation + verification:
- tests for handoff completeness and failure recycling
- done when each role output can be consumed without human cleanup

## Step 05 - Bridge CLI and Approval Routing
Use cases: `NF-05`, `PK-03`, `NF-07`

Architecture analysis:
- map command surface to user intents (`continue`, `status`, `today`, `approve`, `bootstrap`)

Design options:
- A: thin pass-through CLI
- B: policy-aware CLI with approval queue metadata

Evaluation and decision:
- choose B so approvals become explicit, auditable objects

Detailed implementation plan:
1. implement CLI commands in `bridge/cli.py`
2. implement tier classification rules (Tier 1/2/3)
3. implement pending queue representation in `soul/pending/`

Implementation + verification:
- CLI integration tests (golden output + state transitions)
- done when approvals can be batched safely and low-risk work stays unblocked

## Step 06 - Learning and Curation Loop
Use cases: `NF-06`, `PK-04`, `XP-04`

Architecture analysis:
- define pattern detection sources (reviews, failures, repeated edits)
- define contradiction detection thresholds

Design options:
- A: periodic batch-only curator
- B: lightweight continuous signals + periodic curator review

Evaluation and decision:
- choose B for earlier feedback with controlled noise

Detailed implementation plan:
1. implement recurring pattern detector from task/review events
2. implement contradiction scan using `know` connections + grades
3. persist lessons/tasks for follow-up

Implementation + verification:
- tests with synthetic repeated-failure datasets
- done when framework surfaces reusable lessons and conflict alerts

## Step 07 - Project Bootstrap and Cross-project Context
Use cases: `NF-07`, `XP-01`, `XP-03`

Architecture analysis:
- define project namespace model and safety boundaries

Design options:
- A: manual project setup only
- B: bootstrap command that creates project seed atoms + files

Evaluation and decision:
- choose B to make onboarding repeatable and low-friction

Detailed implementation plan:
1. implement `nowu bootstrap <project>`
2. seed project concept/decision/task atoms
3. add cross-project recall command with explicit link confirmation

Implementation + verification:
- end-to-end test: create project, capture knowledge, discover cross-project item, link safely
- done when a new project can be started in one command with isolated scope

## 4) Exit Criteria for v1

1. At least one non-framework project is bootstrapped and actively used.
2. Session recovery works after forced interruption.
3. Approval tiers are enforced with auditable queue state.
4. Role pipeline runs with structured handoffs and VBR checks.
5. Core decisions and lessons are persisted in `know` with links.

## 5) Out of Scope for v1

- Full web dashboard implementation
- Multi-user collaboration model
- External webhook ecosystem
- Domain-complete automation for all AP/RE use cases

