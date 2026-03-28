---
last_updated: 2026-03-26
status: ACTIVE
version: 1.1
workflow_level: Above C4
stage: 1
---

# nowu v1 Plan

> **Lifecycle:** Read at P0 (idea alignment, decomposition), P0.UC (use-case-agent), and
> S1 (nowu-intake). Updated by human after each completed step or stage transition.
> Health checks (health-goals, health-use-cases) verify active work aligns with this file.
> Run `/health-check goals` whenever this file changes.

---

## 1. v1 Objective

Deliver a usable `nowu` core that:

- Recovers and continues sessions reliably after any interruption (NF-01)
- Enforces architectural and quality gates (NF-02, NF-04)
- Shapes and executes bounded work within defined appetite (NF-03)
- Routes approvals safely with an auditable tier model (NF-05)
- Bootstraps and runs at least one additional project context (NF-07)
- Leverages `know` for task queries and cross-project recall (PK-03, XP-01)
- Ensures every deliverable traces back to a use case (NF-09)

**Current step:** Step 02 - Memory Integration Layer (In Progress)

---

## 2. Delivery Strategy

Every step is executed via the S1-S9 implementation workflow (Intake to Capture).
Where a step is substantial enough to warrant it, a pre-workflow run (P0-P4) produces
the intake brief that feeds S1. See Section 7 for pre-workflow routing guidance per step.

Each feature must be traceable: code > test > AC > use case ID (enforced at S8, NF-09).
Detailed task specs and ACs are produced at S5 Shaping - not stored here.

Architectural decisions per step are recorded in docs/DECISIONS.md.
Full S1-S9 reference: docs/WORKFLOW-DETAILED.md.

---

## 3. Steps

Mini-plans record pre-decided direction only - design choices that S2-S5 agents
treat as constraints and do not re-litigate. Detailed task specs and ACs are produced
by S5 Shaping.

### Step 01 - Repo and Contract Baseline (Done)

Use cases: NF-01, NF-02, NF-03

Decision: Per-module packages (src/nowu/core/, src/nowu/flow/, src/nowu/bridge/,
src/nowu/soul/, src/nowu/know/) over flat layout. Each module maps to an agent context
and enforces import boundaries at the filesystem level (D-003).

---

### Step 02 - Memory Integration Layer (In Progress)

Use cases: NF-01, NF-02, PK-03, XP-01

Decision: core/memory_service.py wrapper around KnowledgeBase + KnowAdapter (D-006).
Centralizes retries, validation, and project scoping. Direct kb.* calls from flow/bridge
are prohibited - all memory access goes through MemoryService.

---

### Step 03 - Session Runtime and WAL

Use cases: NF-01, NF-04

Decision: WAL + mirrored session summary atom in `know` (over WAL-only, D-008).
WAL appends events to soul/SESSION-STATE.md; a summary atom is persisted to `know` after
each session for structured recall and cross-session auditability.

---

### Step 04 - Session Role Sequencer (flow/orchestrator.py)

Use cases: NF-02, NF-03, NF-04

Note: The development workflow role pipeline (S1-S9 with dedicated agents) is already
fully operational. This step covers the runtime role sequencer only.

Decision: Fixed linear sequence over configurable DAG (D-009). Linear is sufficient
for v1 and far simpler to test; DAG adds complexity without a current use case.

---

### Step 05 - Bridge CLI and Approval Routing

Use cases: NF-05, PK-03, NF-07

Decision: Policy-aware CLI with approval queue over thin pass-through. Approvals must be
auditable and resumable. Pending approvals stored in soul/pending/.

---

### Step 06 - Learning and Curation Loop

Use cases: NF-06, PK-04, XP-04

Decision: Lightweight continuous signals over batch-only. Detect patterns on session end;
curator reviews periodically with pre-filtered input.

---

### Step 07 - Project Bootstrap and Cross-project Context

Use cases: NF-07, XP-01, XP-03

Decision: `nowu bootstrap <project>` command over manual setup. Encodes the correct
starting state as a testable command; manual setup is error-prone and undocumented.

---

## 4. Exit Criteria for v1

1. At least one non-framework project is bootstrapped and actively used.
2. Session recovery works after forced interruption (tested with a real crash).
3. Approval tiers are enforced with auditable queue state.
4. Role pipeline runs with structured handoffs and VBR checks.
5. Core decisions and lessons are persisted in `know` with links.
6. Every merged task spec carries a complete validation_trace (code > test > AC > UC-ID).

---

## 5. Product Stage Map

This plan covers Stage 1 - v1 core framework.

| Stage | Label | Description | Exit gate |
|-------|-------|-------------|-----------|
| 0 | Seed | Vision defined, repo exists, contracts baseline | Step 01 done |
| 1 | v1 core | All 7 steps done, exit criteria met | current |
| 2 | v1.1 reliability | Health metrics, wider dogfooding, performance | NF-08 at scale |
| 3 | Framework product | Installable, public docs, first external users | XP-07 satisfied |
| 4 | Platform / SaaS | Multi-user, managed service, billing | v2.0 vision |

Stage transitions are human-gated and require:
1. All exit criteria for the current stage passing.
2. An updated docs/vision.md (with last_approved refreshed).
3. A new docs/USE_CASES.md pass via use-case-agent for the next stage.

---

## 6. Out of Scope for v1

- Full web dashboard or UI
- Multi-user collaboration model
- External webhook ecosystem
- Domain-complete automation for AP/RE use cases
- SaaS multi-tenancy

---

## 7. Pre-Workflow Routing by Step

Each remaining step should be initiated through the pre-workflow (P0-P4):

| Step | Size | Recommended pre-workflow mode |
|------|------|-------------------------------|
| 02 - Memory Integration | New capability in existing module | STANDARD |
| 03 - Session Runtime + WAL | New capability in soul, affects core | FULL |
| 04 - Role Sequencer | New module (flow/orchestrator) | FULL |
| 05 - Bridge CLI | New module (bridge), new approval model | FULL |
| 06 - Curation Loop | Extension of existing S9 patterns | STANDARD |
| 07 - Bootstrap command | New capability, cross-module | FULL |

The mini-plan direction above is pre-decided architecture and feeds into P3 as constraints
- it does not replace the pre-workflow story mapping and readiness assembly.
