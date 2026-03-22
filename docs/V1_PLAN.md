# nowu v1 Plan

Date: 2026-03-22
Status: Rebased on `know` v0.4.0 (class-based `KnowledgeBase` API)
Workflow: 9-step cycle with VS Code agents operational (see `docs/WORKFLOW.md`)

## 1) v1 Objective

Deliver a usable `nowu` core that can:

- recover and continue sessions reliably (`NF-01`)
- enforce architectural and quality gates (`NF-02`, `NF-04`)
- shape and execute bounded work (`NF-03`)
- route approvals safely (`NF-05`)
- bootstrap and run at least one additional project context (`NF-07`)
- leverage `know` for task queries and cross-project recall (`PK-03`, `XP-01`)
- ensure every deliverable traces back to a use case (`NF-09`)

## 2) Delivery Strategy

Use incremental vertical slices. Every step is executed via the **9-step S1–S9 workflow** (Intake → Capture) with dedicated VS Code agents.

Each feature must be traceable from code → test → acceptance criterion → use case ID (`NF-09`).
Detailed task specs, acceptance criteria, and done-criteria are produced by S5 Shaping — not stored here.

See `docs/WORKFLOW.md` for the full reference.
Dedicated VS Code agents run each step. See `docs/WORKFLOW.md` for the full reference.

## 3) Steps and Mini-plans

> **Note**: Each step is executed via the S1–S9 workflow (see `docs/WORKFLOW.md`).
> The mini-plans below record the **pre-decided direction only** — settled design choices
> that S2–S5 agents should treat as constraints, not re-litigate.
> Detailed task specs, acceptance criteria, and done-criteria are produced by S5 Shaping.

## Step 01 - Repo and Contract Baseline ✅ Done
Use cases: `NF-01`, `NF-02`, `NF-03`

Design options:
- A: flat layout — all source in `src/nowu/`, no sub-packages
- B: per-module packages — `src/nowu/core/`, `src/nowu/flow/`, `src/nowu/bridge/`, etc.

Decision: **B** — each module maps to a VS Code agent context and enforces the import boundary rules at the filesystem level.

## Step 02 - Memory Integration Layer
Use cases: `NF-01`, `NF-02`, `PK-03`, `XP-01`
**Status**: ⏳ Next

Design options:
- A: call `kb.*` / `KnowAdapter` directly from `flow` and `bridge` wherever memory is needed
- B: `core/memory_service.py` wrapper around `KnowledgeBase` + `KnowAdapter`

Decision: **B** — centralizes retries, validation, and project scoping in one place.

Key orientation for S2:
- `core/memory_service.py` implements the existing `MemoryService` protocol
- Required operations: `record_decision`, `create_task`, `recall_context`, `task_overview`
- Must use `KnowledgeBase(kb)` + `KnowAdapter(kb)`, never raw `kb.*` calls from `flow`/`bridge`
- Integration tests use a temp `KNOW_DATA_DIR`

## Step 03 - Session Runtime and WAL
Use cases: `NF-01`, `NF-04`

Design options:
- A: write-ahead log (WAL) only — append events to `soul/SESSION-STATE.md`, replay on resume
- B: WAL + mirrored session summary atom in `know` — same WAL, but also persist a summary atom after each session

Decision: **B** — the `know` atom provides structured recall and cross-session auditability; WAL alone is hard to query.

Key orientation for S2:
- `flow/session.py` state model + WAL writer to `soul/SESSION-STATE.md`
- Resume logic reads `soul/SESSION-STATE.md` on startup
- Session-end: summarize events → write lesson/decision atoms via `MemoryService`

## Step 04 - Session Role Sequencer (`flow/orchestrator.py`)
Use cases: `NF-02`, `NF-03`, `NF-04`

> The *development workflow* role pipeline (structured handoff artifacts, agent-per-step,
> S1–S9 cycle) is already fully operational via the VS Code agent system.
> This step covers the **runtime role sequencer** only.

Design options:
- A: fixed linear sequence (Intake → Constraints → Options → Decision → Shape → Implement → VBR → Review → Capture)
- B: configurable DAG allowing parallel or skipped steps

Decision: **A** — linear is sufficient for v1 and far simpler to test; DAG adds complexity without a current use case.

Key orientation for S2:
- Implements `RoleOrchestrator` protocol from `core/contracts/session.py`
- Enforces per-transition guards: reject if `SessionSnapshot` is missing required fields

## Step 05 - Bridge CLI and Approval Routing
Use cases: `NF-05`, `PK-03`, `NF-07`

Design options:
- A: thin CLI pass-through — forward commands to `flow`, no approval modeling
- B: policy-aware CLI with approval queue — classify actions by tier, store pending approvals as objects in `soul/pending/`

Decision: **B** — approvals must be auditable and resumable; a pass-through loses the tier decision and requires manual re-evaluation after interruption.

Key orientation for S2:
- `bridge/cli.py` commands: `continue`, `status`, `today`, `approve`, `bootstrap`
- Tier classification rules (Tier 1/2/3) in `bridge/`
- Pending queue lives in `soul/pending/`

## Step 06 - Learning and Curation Loop
Use cases: `NF-06`, `PK-04`, `XP-04`

Design options:
- A: batch-only — curator runs once per sprint, processes all accumulated signals
- B: lightweight continuous signals — detect patterns on session end, curator reviews periodically with pre-filtered input

Decision: **B** — batch-only delays feedback; continuous signal detection is cheap and surfaces issues earlier, while the curator gate controls noise.

Key orientation for S2:
- Pattern detection sources: reviews, repeated failures, repeated edits
- Contradiction scan via `know` connections + epistemic grades
- Lessons/tasks persisted back to `know` for follow-up

## Step 07 - Project Bootstrap and Cross-project Context
Use cases: `NF-07`, `XP-01`, `XP-03`

Design options:
- A: manual setup — human creates `soul/`, config files, and initial `know` atoms by hand
- B: `nowu bootstrap <project>` command seeds atoms (concept, decision, task types) and generates required files with `project_scope=[project]`

Decision: **B** — manual setup is error-prone and undocumented; a bootstrap command encodes the correct starting state and is testable.

Key orientation for S2:
- `nowu bootstrap <project>` seeds concept/decision/task atoms with `project_scope=[project]`
- Cross-project recall uses explicit link confirmation (no silent merging)

## 4) Exit Criteria for v1

1. At least one non-framework project is bootstrapped and actively used.
2. Session recovery works after forced interruption.
3. Approval tiers are enforced with auditable queue state.
4. Role pipeline runs with structured handoffs and VBR checks.
5. Core decisions and lessons are persisted in `know` with links.
6. Every merged task spec carries a complete `validation_trace` (code → test → AC → use case ID).

## 5) Out of Scope for v1

- Full web dashboard implementation
- Multi-user collaboration model
- External webhook ecosystem
- Domain-complete automation for all AP/RE use cases

