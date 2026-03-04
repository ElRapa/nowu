# nowu Architecture

Version: 1.1
Date: 2026-03-04
Status: Active draft for implementation kickoff

## 1) Problem and Target

`nowu` is an AI-first framework for running multi-project work with durable memory, structured decision-making, and reliable execution loops.

The key constraint is that `know` already exists (v0.2.0) and should be reused as the memory substrate, not rebuilt.

### Primary v1 use-case focus

`USE_CASES.md` is directionally broad (35 use cases). v1 should focus on the core framework capabilities that unblock everything else:

- `NF-01`: resume work after context loss
- `NF-02`: track and enforce architecture decisions
- `NF-03`: scope work without scope creep
- `NF-04`: self-assess quality (Verify Before Reporting)
- `NF-05`: route approvals by risk tier
- `NF-06`: learn from recurring mistakes
- `NF-07`: bootstrap a new project safely
- `PK-01`, `PK-03`: fast capture and unified today view
- `XP-01`: cross-project discovery

## 2) Architecture Drivers

1. `know` is the system-of-record memory layer.
2. AI agents are the primary producers of change, so interfaces must be explicit and testable.
3. Recovery must be deterministic after crashes/context loss.
4. Governance must be cheap: approvals and ADR checks should be automatic where possible.
5. The system must stay modular so new domains can be added without core rewrites.

## 3) Candidate Architectures

### Option A: Integration-first modular monolith (recommended)

- Single Python runtime with clear module boundaries.
- Modules communicate through Python contracts.
- `know` is consumed via `KnowAdapter`/public API.
- Durable state in `know` + `soul/SESSION-STATE.md` WAL.

Pros:
- Fastest delivery for solo + AI development.
- Lowest operational overhead.
- Strong local debugging and testability.

Cons:
- Runtime coupling inside one process.
- Horizontal scaling limits (acceptable for current scope).

### Option B: Event-driven orchestrator with internal command bus

- Modules interact through an event bus and append-only domain events.
- Strong auditability and replay semantics.

Pros:
- Excellent traceability and evolution path.
- Good decoupling between producers/consumers.

Cons:
- Higher complexity before value is proven.
- More cognitive load for AI agents during early implementation.

### Option C: Early microservice split

- `flow`, `bridge`, and future `dash` as separate services with RPC/queues.

Pros:
- Strong runtime isolation and independent deployability.

Cons:
- Heavy operational burden.
- Slower iteration and higher failure surface for a greenfield framework.

### Weighted evaluation (1-5, higher is better)

| Criterion | Weight | Option A | Option B | Option C |
|---|---:|---:|---:|---:|
| Delivery speed (solo + AI) | 25 | 5 | 3 | 1 |
| AI-agent implementation reliability | 20 | 5 | 3 | 2 |
| Modularity/extensibility | 20 | 4 | 5 | 5 |
| Operational simplicity | 15 | 5 | 3 | 1 |
| Governance/traceability | 20 | 4 | 5 | 4 |
| **Weighted total** | **100** | **4.65** | **3.80** | **2.55** |

Decision: choose Option A now, while designing contracts that allow a gradual move toward Option B patterns where needed.

## 4) Selected High-level Architecture

### 4.1 Module map

| Module | Responsibility | Owns | Depends on |
|---|---|---|---|
| `know` (external package) | Durable knowledge graph, search, task/today view, versions, subgraph context | `~/.know` data | none |
| `soul` | Human-authored identity and governance docs (`VISION`, `AGENTS`, WAL conventions) | markdown policies | none |
| `core` (new) | Domain contracts and use-case level services for nowu | interfaces, policies | `know`, `soul` |
| `flow` (new) | Session runtime, role pipeline (Architect/Shaper/Implementer/Reviewer/Curator), VBR loop | session lifecycle | `core`, `know`, `soul` |
| `bridge` (new) | CLI/API entrypoints, approval queue interactions, project bootstrap commands | user interaction layer | `flow`, `core`, `know` |
| `dash` (later) | Visualization and reporting UI | presentation only | `bridge` or `core` |
| `skills` (new in repo) | Reusable role skills for AI agents (`nowu-architect`, `nowu-shaper`) | workflow knowledge | none |

### 4.2 Data ownership and boundaries

- Only `know` persists structured memory.
- `flow` and `bridge` do not write to private DB tables; they use `know` API calls.
- `soul/SESSION-STATE.md` is the WAL for in-flight session continuity.
- Long-term decisions/tasks/lessons live in `know` atoms, scoped by project.

### 4.3 Runtime interaction (user perspective)

1. User invokes `nowu` from CLI (`bridge`).
2. `flow` opens/resumes session and writes WAL checkpoint.
3. `flow` asks `know` for relevant context (`today`, `search`, `subgraph`).
4. Role-specific logic runs (Architect/Shaper/Implementer/Reviewer).
5. Actions, tasks, decisions, lessons are persisted to `know`.
6. Reviewer/VBR gate decides pass, retry, or escalation.
7. Session summary is captured back into `know`.

### 4.4 Runtime interaction (framework-as-user perspective)

The framework uses itself:

- `nowu` project decisions are stored in `know` with `project_scope=["nowu"]`.
- Each external project gets its own scope (for example `aperitif`, `real-estate`).
- Cross-project links are explicit (`related_to`, `supports`, `refines`) after discovery.
- Planning and delivery loops consume these atoms just like any other project.

## 5) know Usage Contract (v1)

Use only public `know` APIs and `KnowAdapter`.

Required operations for nowu modules:

- Initialization: `know.init(data_dir=...)`
- Persist knowledge: `know.create_atom(...)`, `know.update_atom(...)`
- Link knowledge: `know.add_connection(...)`
- Query/retrieval: `know.query_atoms(...)`, `know.search(...)`, `know.today(...)`
- Context extraction: `know.subgraph(...).to_prompt(...)`
- Audit/history: `know.get_atom_versions(...)`

Guidance:

- Use `ACTION` atoms for reusable behavior contracts.
- Use `TASK` atoms for planned execution items.
- Use `DECISION` atoms for architecture and policy choices.
- Grade conservatively; grades >=4 require justification.

## 6) AI-centric Engineering Principles

1. Design for deterministic handoffs: every step emits machine-checkable artifacts.
2. Keep tasks small: target <=4h per implementation atom.
3. Use bounded contracts before code generation.
4. Make verification non-optional (tests, lint, acceptance criteria).
5. Capture decisions/lessons into `know` after each substantial cycle.

## 7) Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Embedding cold-start in `know` can slow first run | slower UX | warm-up command and lazy semantic fallback |
| Planning drift across many docs | inconsistency | single source docs (`ARCHITECTURE.md`, `V1_PLAN.md`, `WORKFLOW.md`) + ADR capture |
| Agent overreach/scope creep | wasted cycles | strict shaping templates and in/out scope per task |
| Concurrency conflicts at scale | stale/locking behavior | start with serialized writes and add intent/locking policy in phase 2 |

## 8) Non-goals for v1

- Full dashboard product (`dash`) implementation
- Multi-user auth/permissions model
- Distributed microservice deployment
- Domain-specific deep features for every AP/RE/PK use case

