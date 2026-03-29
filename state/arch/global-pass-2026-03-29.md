---
id: global-pass-2026-03-29
status: PROPOSED
agent_version: gap-analyst@1.0
generated_at: 2026-03-29T00:00:00Z
trigger: "No prior GAP has ever run. Stage 1, Step 02 in progress. Validate architecture against accumulated decisions D-003/D-006/D-008/D-009 and full UC catalog before further steps ship."
gap_scope: FULL_RESET
product_stage_at_time: Stage 1 — v1 core (Step 02 of 7 in progress)
---

# Global Architecture Pass — 2026-03-29

## Why This GAP Was Run

No Global Architecture Pass has ever been executed for the nowu project. Stage 1
is actively in progress (Step 02 — Memory Integration Layer underway, Step 01 —
Repo and Contract Baseline complete). Decisions D-003, D-006, D-008, and D-009
have accumulated since project bootstrap without a cross-cutting architectural review.

Neither `docs/architecture/context.md` nor `docs/architecture/containers.md` exist.
The architecture is currently documented only in `docs/ARCHITECTURE.md` §4. This pass
produces the full C4 L1 and L2 baseline from which dedicated `context.md` and
`containers.md` can be authored.

The UC catalog (`docs/USE_CASES.md`) contains 36 use cases across 5 domains. This
pass verifies that every ACTIVE v1 UC has a clear container owner, and that CANDIDATE
UCs do not require new containers before v1 exits.

---

## UC-to-Container Matrix

All 36 use cases from `docs/USE_CASES.md`. Stage column: **Active-v1** (in scope for
Stage 1 v1), **Candidate** (not blocking v1; long-term fit verified).

| UC-ID | Title | Stage | Natural Container | Gap / Risk |
|---|---|---|---|---|
| NF-01 | Resume Work After Context Loss | Active-v1 | `soul` (WAL append) + `flow` (session open/resume) | WAL schema and the trigger for syncing to `know` needs a formal ADR (→ ADR-F-002) |
| NF-02 | Track and Enforce Architectural Decisions | Active-v1 | `core` (policy contracts) + `flow` (nowu-reviewer enforcement at S8) | Existing D-002 covers principle; machine-parseable ADR format not yet decided (→ ADR-F-?) |
| NF-03 | Scope Work Without Scope Creep | Active-v1 | `flow` (nowu-shaper, `in_scope_files` in task spec) | No gap — shaping is operationally active |
| NF-04 | Self-Assess Quality Without Human Intervention | Active-v1 | `flow` (VBR gate, hook-driven) | No gap — TDD constraint (D-004) + VBR hook in `flow` |
| NF-05 | Route Approvals Without Blocking Progress | Active-v1 | `bridge` (approval queue in `soul/pending/`) + `flow` (tier classification) | Approval queue schema and lifecycle not formally ADR'd (→ ADR-F-003) |
| NF-06 | Learn From Past Mistakes Across Sessions | Active-v1 | `flow` (nowu-curator, S9) + `know` (pattern atom storage) | Pattern detection logic and lesson persistence mechanism not designed (→ ADR-F-007) |
| NF-07 | Bootstrap a New Project Using the Framework | Active-v1 | `bridge` (`nowu bootstrap <project>` CLI) + `know` (project_scope isolation) | Project isolation model not formally ADR'd (→ ADR-F-004) |
| NF-08 | Measure and Visualize Framework Health | Candidate | `bridge` (report trigger/CLI) + `know` (metrics atoms) | No container currently collects metrics; health agents are a workflow workaround, not a code path (→ ADR-F-006) |
| NF-09 | Ensure Every Deliverable Traces Back to a Use Case | Active-v1 | `flow` (nowu-reviewer, S8 `validation_trace` check) + `core` (trace spec) | No gap — activated at S8 and described in `V1_PLAN.md` exit criteria |
| AP-01 | Track Regulatory Requirements as Living Knowledge | Candidate | `know` (atoms w/ `project_scope=["aperitif"]`) + `bridge` (CLI capture) | Domain adapters (AP context) are data, not code — uses existing project_scope isolation; NOT BLOCKING v1 |
| AP-02 | Manage Product Formulation as Versioned Knowledge | Candidate | `know` (versioned atoms + connections) | Version history via `kb.get_atom_versions()` — capability exists; NOT BLOCKING v1 |
| AP-03 | Model Supply Chain Relationships and Risks | Candidate | `know` (connection graph) | Relationship atoms are an existing `know` primitive; NOT BLOCKING v1 |
| AP-04 | Capture Market Intelligence Over Time | Candidate | `know` (atoms with temporal metadata) + `bridge` | Confidence decay model not yet in `know` v0.4.0 — deferred to PK-04 resolution; NOT BLOCKING v1 |
| AP-05 | Plan and Track Business Milestones | Candidate | `know` (TASK atoms + dependency connections) | Dependency-aware milestone tracking needs TASK atom enhancement in `know` — out of v1 scope |
| AP-06 | Evaluate a Business Decision with Traceability | Candidate | `flow` (S3-S4 decision workflow) + `know` (DECISION atoms) | Existing workflow (nowu-decider, S4) is the natural home — no gap |
| AP-07 | Onboard a Collaborator Into the Project Context | Candidate | `bridge` (role-scoped report generation) or `dash` (future) | No report-generation capability in `bridge` yet; role scoping requires sensitivity model (→ ADR-F-005) |
| RE-01 | Inventory Existing Processes Before Digitalization | Candidate | `know` (process atoms, narrative + structured) | Process documentation is knowledge atom data; NOT BLOCKING v1 |
| RE-02 | Track Property Data Across Lifecycle Stages | Candidate | `know` (atoms tagged by lifecycle stage, connections) | Lifecycle-stage tagging is a convention, not a schema — needs documented pattern before RE project starts |
| RE-03 | Capture Stakeholder Relationships and Constraints | Candidate | `know` (relationship atoms) | Existing `know` connection primitives cover this; NOT BLOCKING v1 |
| RE-04 | Prioritize Digitalization by Impact and Feasibility | Candidate | `know` + `flow` (S3-S4 multi-criteria decision) | Existing decision workflow applies; NOT BLOCKING v1 |
| RE-05 | Detect Inconsistencies Across Property Records | Candidate | `know` (contradiction detection service) | Contradiction detection is not in `know` v0.4.0 — overlaps XP-04; needs `know` enhancement or new `core` service |
| RE-06 | Support Long-Term Investment Decision Tracking | Candidate | `know` (DECISION atoms + outcome linkage) | Financial projection schema not defined — deferred; NOT BLOCKING v1 |
| RE-07 | Generate Reports for Different Audiences | Candidate | `bridge` (report command) or `dash` (future) | Audience-specific filtering requires sensitivity model (→ ADR-F-005); natural long-term home is `dash` |
| PK-01 | Capture a Thought Before It's Lost | Active-v1 | `bridge` (fast-capture command, minimal friction) + `know` (atom storage) | Capture UX step in Step 05 bridge; no gap in architecture |
| PK-02 | Surface Relevant Knowledge Without Being Asked | Candidate | `flow` (proactive surfacing trigger) + `know` (semantic search) | Push mechanism not designed; pull (human-triggered) is already possible via `know`; NOT BLOCKING v1 |
| PK-03 | Maintain a "Today" View Across All Projects | Active-v1 | `bridge` (today command) + `know` (`query_atoms` + date filter) | Step 05 bridge is the implementation home; architecture supports it |
| PK-04 | Let Knowledge Decay and Clean Up Gracefully | Candidate | `know` (decay / stale-atom model) + `flow` (curator periodic pass) | Decay model not in `know` v0.4.0 API; needs design before Stage 2 |
| PK-05 | Build Understanding Incrementally Over a Topic | Candidate | `know` (synthesis + confidence model) | Synthesis is not in current `know` API; requires know enhancement or new `core` synthesis service |
| PK-06 | Protect Sensitive Personal Knowledge | Candidate | `core` (security policy Protocol) + `know` (access-scoped queries) | **CRITICAL GAP**: No container owns this. No security model exists. Must be resolved via ADR before Stage 2 or before any AP/RE data is stored alongside personal knowledge. (→ ADR-F-005) |
| XP-01 | Discover Connections Across Projects Automatically | Active-v1 | `know` (`subgraph()` + `search()`) | `know` v0.4.0 has search and subgraph — capability exists; operational use validated |
| XP-02 | Maintain Consistent Terminology Across Projects | Candidate | `know` (namespace / project-scoped glossary) | Namespace model not in `know` v0.4.0; needs design before multi-project confusion grows |
| XP-03 | Transfer Lessons Learned Between Projects | Candidate | `flow` (curator, lesson generalization) + `know` (cross-scope atoms) | Generalization logic not designed (→ ADR-F-007); NOT BLOCKING v1 |
| XP-04 | Handle Conflicting High-Confidence Knowledge | Candidate | `know` (conflict detection) + `flow` (curator escalation) | Contradiction detection not in `know` v0.4.0; needed before trustworthy cross-project recall at scale |
| XP-05 | Scale the Knowledge Base Without Degrading Performance | Candidate | `know` (infrastructure) | SQLite + JSON ceiling not assessed; NOT BLOCKING v1, but should be evaluated at Stage 2 transition |
| XP-06 | Allow Multiple Agents to Work Without Conflicts | Candidate | `know` (concurrency) + `core` (intent protocol) | Serialized writes assumed for v1 (solo developer); concurrency model needed before multi-agent parallel work |
| XP-07 | Adapt the Framework to a New Domain Without Rewriting | Candidate | `know` (extensible atom types) + `bridge` (project init) | Governed by D-010 scope decision; extensibility test when first non-NF project onboards |

---

## L1 Context — Changes Required

**Current state:** No `docs/architecture/context.md` exists. The ARCHITECTURE.md §4
documents the module map but does not define the system boundary or external actors at
the C4 L1 level.

**Delta to be authored in `context.md`:**

The **nowu System** boundary includes all Python source modules (`core`, `flow`, `bridge`,
`soul`) and the workflow artifact layer (`state/`, `docs/`, `.claude/`). It does NOT
include `know` — that is an external system consumed through a defined API.

External actors and systems that must appear in the L1 diagram:

| External Actor / System | Role | Direction | Notes |
|---|---|---|---|
| **Developer (Human)** | Primary user. Triggers workflows via CLI + VS Code; approves Tier 2/3 decisions | → nowu System (commands + approvals) | Primary persona is Raphael; secondary is small-team lead |
| **AI Agent (Claude / Copilot)** | Co-producer. Operates every S1–S9 step; writes code and artifacts | ↔ nowu System (reads state, writes artifacts) | Not a monolith — multiple specialised agents per step (D-005) |
| **`know` package (external)** | System of record for all durable knowledge, tasks, decisions, lessons | nowu System → know (API calls via KnowledgeBase + KnowAdapter) | Sibling repo, v0.4.0; access contract defined in D-006 |
| **Git / Version Control** | Stores code artifacts and Markdown state as the source of truth for code | nowu System → Git (commits, history) | Not owning decision memory — that is `know`'s role |
| **File System** | Passive state medium (WAL, Markdown artifacts, `soul/` identity files, `state/` workflow state) | ↔ nowu System (read/write) | No external service dependency — by design (D-001) |
| **VS Code / IDE** | Interaction environment for agents; loads `.claude/rules/`, `.github/copilot-instructions.md` | → nowu System (context loading, agent invocation) | Implicit today; if nowu becomes a standalone tool, this changes |

**Not yet present but implied by CANDIDATE UCs:**

| Actor | Required By | Needed When |
|---|---|---|
| External Domain Data Sources (Philippines FDA, permit APIs, property registries) | AP-01, RE-01 | Stage 2+, when AP/RE projects actively onboard |
| Collaborators / External Users | AP-07, RE-07, NF-07 | Stage 3 (framework product horizon) |
| AI Provider API (Claude API, Copilot API) | All agent-driven steps | Currently implicit through IDE; becomes explicit if nowu ships as a standalone tool |

**Recommendation:** These future actors should be reflected in `context.md` as dashed/future
system relationships today, so the boundary is clear when Stage 2 begins.

---

## L2 Containers — Analysis

### Existing containers: assessment

The five containers defined in `docs/ARCHITECTURE.md` §4.1 are assessed here.
`know` is treated as an external system (bounded by D-006), not an internal container.

| Container | Still Valid? | Responsibility Update Needed? | Notes |
|---|---|---|---|
| `core` | Yes | Minor: explicitly own the validation_trace Protocol and future security policy contract | Currently owns "domain contracts + MemoryService"; needs to also explicitly own the security policy Protocol when ADR-F-005 is resolved |
| `flow` | Yes | Minor: explicitly own pattern-detection coordinator logic (NF-06, XP-03) alongside the session/VBR pipeline | Steps 03–04 pending; architecture is sound |
| `bridge` | Yes | Minor: explicitly own the approval queue lifecycle, fast-capture UX, and today-view assembly | Step 05 pending; the responsibility as stated is accurate but the approval queue schema needs an ADR (ADR-F-003) |
| `soul` | Yes | Minor: clarify that soul owns WAL conventions and identity governance docs, but does NOT own business logic | Scaffold exists; WAL contract needs ADR (ADR-F-002) |
| `know` (external) | Yes | N/A — external system; API contract is defined in D-006 | Critically: no internal `know` reimplementation is permitted; any new `know` capability (decay, synthesis, contradiction detection) requires either contributing to the `know` project or wrapping in a `core` service |

**Conclusion:** The 5-container split (plus external `know`) is valid and sufficient for all
ACTIVE v1 use cases. No container change is needed before Stage 1 completes.

---

### Proposed new containers (if any)

**Proposal 1: `dash` — Visualization and Reporting UI**

- Already mentioned in `docs/ARCHITECTURE.md` §4.1 as "out of scope v1"
- Triggered by: NF-08, AP-07, RE-07 (report generation for different audiences)
- This GAP confirms the existing scoping decision: `dash` is not needed for v1
- **Required before this container can be created:** An ADR formalizing its scope (what it may/may not import), its dependency chain (reads from `bridge` or `core`, never `flow` internals), and the stage trigger (→ ADR-F-008)

**No other new containers are proposed for v1.** All CANDIDATE UCs map to data patterns or
`know` enhancements — they do not require new top-level modules. Domain-specific UCs
(AP-01..AP-07, RE-01..RE-07) use `know` project_scope isolation as the partitioning
mechanism, which is implemented data-side, not code-side.

---

### Containers with blurred responsibilities

| Container A | Container B | Overlap | Recommended Resolution |
|---|---|---|---|
| `flow` (curator, S9) | `know` (knowledge storage) | Learning from mistakes (NF-06): is the pattern detection logic a `flow` concern (when to detect) or a `know` concern (how to store/retrieve patterns)? | Resolve via ADR-F-007: `flow` owns the detection trigger and escalation logic; `know` owns the storage and recall of lessons. Detection algorithm lives in `flow`. |
| `bridge` (approval queue) | `soul` (pending/ directory) | Approval queue items are stored under `soul/pending/` but managed by `bridge` logic | The storage location (`soul`) is distinct from the management logic (`bridge`). Keep as-is but make explicit in ADR-F-003 that `soul/pending/` is `bridge`'s write area in `soul`. |
| `core` (security policy Protocol) | `know` (access-scoped queries) | Sensitivity model (PK-06): who enforces access — the Protocol in `core` or `know` at query time? | Resolve via ADR-F-005: `core` defines the policy contract (what is allowed); `know` enforces it at query time; `bridge` checks policy before surfacing results to the user. |

---

## ADR Candidates

Decisions that are currently recorded informally in `docs/DECISIONS.md` or implied by
`docs/ARCHITECTURE.md` but have not been lifted to a formal `docs/architecture/adr/*.md`
with options evaluated and PROPOSED/ACCEPTED status. All existing D-NNN entries should be
considered for ADR formalisation — the list below identifies those with the highest
architectural consequence or the most active open questions.

| # | Title | Decision Needed | Options to Consider | Why It Matters |
|---|---|---|---|---|
| ADR-F-001 | know API boundary and version contract | Exactly which `know` APIs are permitted in each nowu module; how to handle `know` version upgrades; whether nowu pins a `know` version | (A) Pin exact `know` version, explicit upgrade gate; (B) Use a compatibility shim in `core` that abstracts `know` API changes; (C) Declare `know` a first-class dependency with a shared changelog | D-006 records the reuse decision but not the boundary rigor. A breaking `know` API change today would cascade unpredictably through multiple `nowu` modules. |
| ADR-F-002 | WAL + session summary atom strategy | When and how `soul/SESSION-STATE.md` WAL entries are synced to `know` as summary atoms; what the WAL schema is; what constitutes a valid checkpoint | (A) Sync every session end; (B) Sync on every significant event (checkpoint after each role step); (C) WAL-only with periodic batch sync | V1_PLAN Step 03 cites this decision but no formal ADR exists. An incorrect WAL schema cannot be migrated cheaply once sessions accumulate. |
| ADR-F-003 | Approval queue storage format and lifecycle | The schema for items in `soul/pending/`; what states an item can be in; when items expire or are pruned; how `bridge` reads and writes them | (A) YAML files (one-per-item, matches Markdown-as-state principle D-001); (B) A single JSON queue file in `soul/`; (C) `know` TASK atoms as the queue (no separate files) | V1_PLAN Step 05 assumes `soul/pending/` without defining the contract. A poor schema here makes approval review slow and audit trails incomplete. |
| ADR-F-004 | Cross-project isolation model | How `know` project scopes are bootstrapped, named, and kept isolated; whether cross-project connections are opt-in or opt-out; what happens when a project is archived | (A) `project_scope` tag on all atoms, no hard isolation (current assumption); (B) Separate `KnowledgeBase` instances per project (strong isolation); (C) `project_scope` with explicit cross-project link table | D-007 and NF-07 assume project_scope partitioning but never specify the invariants. If isolation is weak, AP/RE knowledge could bleed into NF framework decisions. |
| ADR-F-005 | Security and sensitivity model for knowledge atoms | How knowledge atoms are classified by sensitivity; who can read/query them; how sensitivity is enforced in `bridge` and `know` | (A) Per-atom sensitivity tag + `know` query filter; (B) Project-level visibility (all atoms in a project share sensitivity level); (C) No enforcement in v1 — document as known gap and defer to Stage 2 | PK-06, AP-07, RE-07 all require this. Without a model, a generated report or cross-project discovery could expose personal financial data. This is a security issue, not just a feature gap. Must be resolved before any personal + business knowledge is co-located. |
| ADR-F-006 | Health metrics collection architecture | How NF-08 health metrics are collected; whether health is a `flow` subsystem, a `bridge` command, or an agent-only workflow; where metrics atoms live | (A) Agent-only (health-sweep as a VS Code agent, no code path — current state); (B) `bridge health` command that queries `know` for structured metrics; (C) A metrics-collection hook in `flow` that writes health atoms after each session | Currently, health is only operational at the agent-workflow level. For NF-08 to be verifiable by machine (NF-09), it needs a code path. |
| ADR-F-007 | Pattern detection and lesson persistence mechanism | How recurring patterns are detected; whether lessons are `know` atoms, `flow` rules, or prompt injections; how the curator (S9) populates and applies them | (A) Lessons as `know` DECISION atoms with `type=lesson`, surfaced at next session start; (B) Lessons as additions to `.claude/rules/` files (prompt-level); (C) Hybrid — lessons to `know`, critical structural lessons to `.claude/rules/` | NF-06 and XP-03 depend on this. "Learning" that lives only in Markdown prompts is not machine-verifiable. The storage choice also determines whether lessons survive a full re-clone. |
| ADR-F-008 | `dash` scope, dependencies, and activation trigger | What `dash` is allowed to import; whether it reads from `bridge` or `core` directly; at which product stage it is created | (A) `dash` reads from `core` contracts only (never `flow`); (B) `dash` is a `bridge` output command, not a separate module; (C) `dash` emerges only as a Stage 3 artefact, blocked by a formal stage gate | ARCHITECTURE.md §4.1 marks `dash` as "🔮 out of scope v1" but does not define the container boundary. If `dash` is built without a defined boundary, it will import from `flow` internals and create coupling that prevents future event-driven evolution (a path explicitly preserved by D-007). |

---

## Constraints for P3 (effective immediately)

These apply to all P3 Architecture Bootstrap runs after this GAP is accepted.

1. **No new top-level module without a superseding ADR to D-003.** The 5-module structure
   (`core`, `flow`, `bridge`, `soul`, `know`-external) is validated for all ACTIVE v1 use
   cases and must not be extended without a formal decision.

2. **`know` is the only permitted durable state store.** No module may open its own database,
   write its own structured index, or persist structured in-memory state between sessions
   outside of `soul/SESSION-STATE.md` (WAL, governed by ADR-F-002) and `soul/pending/`
   (approval queue, governed by ADR-F-003). File-system Markdown artifacts remain valid
   as workflow state (D-001).

3. **All cross-module API surfaces must be declared as Protocols in `core/contracts/`
   before any code is written against them.** A contract file is the gate between shaping
   (S5) and implementation (S6). S6 may not begin without a merged contract.

4. **Domain-specific UCs (AP, RE, PK) must be implemented through `know` project_scope
   isolation — not through new modules.** Adding a new domain does not justify a new
   top-level module; it justifies a new project_scope value and possibly a new `bridge`
   command. This constraint may only be relaxed by an ADR that supersedes D-003 and
   resolves ADR-F-004.

5. **ADR-F-005 (security model) must be ACCEPTED before any implementation that co-locates
   personal knowledge (PK-06 class atoms) with business knowledge (AP/RE) in the same
   `know` instance.** This is a security constraint, not a preference.

6. **`dash` may not be scaffolded until ADR-F-008 is ACCEPTED and the product is at
   Stage 2 or later.** A `dash/` directory appearing in the repo before this gate is an
   architecture violation.

7. **The linear role pipeline (D-009) is fixed for Stage 1.** P3 may not propose a
   DAG-based orchestrator or parallel agent execution for any Stage 1 epic. This decision
   may be revisited at the Stage 1 → Stage 2 transition.

8. **All new public functions in `core`, `flow`, and `bridge` must have corresponding
   tests written before implementation (D-004, TDD constraint).** A P3 architecture
   bootstrap that produces a task spec without explicit acceptance criteria and test
   stubs is incomplete. S6 may not begin.

---

## What Stays the Same

The following aspects of the architecture are explicitly validated by this pass and
must not be changed without a superseding ADR:

- **5-module structure** (`core`, `flow`, `bridge`, `soul`, external `know`). All ACTIVE
  v1 use cases are accommodated within this structure without additions.
- **DDD layering** (Domain → Application → Infrastructure → Interface, D-002). The
  constraint that domain code must not import from infrastructure is not renegotiable.
- **Markdown-as-state** (D-001). No external service, no internal database. `know` is
  the only structured persistence layer and it is explicitly external.
- **`know` v0.4.0 as system of record** (D-006). No internal reimplementation. Access
  only via `KnowledgeBase` + `KnowAdapter` instance methods.
- **Integration-first modular monolith** (D-007). Single Python runtime; contracts
  allow future event-driven evolution but do not require it in v1.
- **TDD non-negotiable** (D-004). 90%+ coverage enforced. VBR gate blocks commits.
- **Dedicated agent per workflow step** (D-005). 8 agents, each scoped to exactly the
  context its step requires. No shared "architect" agent across steps.
- **v1 UC priority** (D-010). NF-01..NF-07, PK-01, PK-03, XP-01 are the implementation
  mandate. All other UCs are direction, not blocked work.

---

## Open Questions for Human

1. **`know` version pinning (→ ADR-F-001):** The `know` package is an active sibling
   project. When `know` ships v0.5.0, does nowu upgrade immediately, maintain a
   compatibility shim, or pin indefinitely? This needs a policy before `know` changes
   the API that MemoryService wraps in Step 02.

2. **Security model timing (→ ADR-F-005):** PK-06 is marked Candidate, implying it
   is not blocking v1. However, the gap is present today: personal knowledge and
   framework-development knowledge already coexist in the same `know` instance. Is this
   acceptable for Stage 1 (solo developer, single user, no collaborators)? If yes,
   this needs to be explicitly documented as a known accepted risk, with a hard gate
   at Stage 2 before AP or RE data is added.

3. **Contradiction detection ownership:** RE-05 and XP-04 both require contradiction
   detection in the knowledge base. This is either a `know` enhancement (submitted
   upstream to the `know` project) or a `core` service that wraps `know` queries with
   conflict-detection logic. Which path does the human prefer? The answer determines
   where this work appears in the backlog.

4. **Health as code vs. health as agents (→ ADR-F-006):** The current health-check
   system (health-sweep, health-vision, etc.) is entirely agent-driven, producing
   Markdown reports. For NF-08 to be machine-verifiable (NF-09 requirement), health
   signals must eventually have a code path. Should this be designed as a future
   `bridge health` command, or is the current agent-only approach acceptable through
   all of Stage 1?

5. **Domain data co-location:** AP and RE projects will store domain-specific knowledge
   (regulatory requirements, property data, financial projections) in the same `know`
   instance as framework-level decisions and personal knowledge. The project_scope
   mechanism partitions reads. But: are there backup, export, or compliance scenarios
   where domain data must be separable? If so, ADR-F-004 needs to model that before
   the first AP or RE project is bootstrapped into `know`.

6. **Lesson storage channel (→ ADR-F-007):** After S9 curator runs, where do lessons
   learned actually land? If they go into `.claude/rules/` files (prompt-level), they
   affect agent behavior but are not machine-verifiable. If they go into `know` atoms,
   they are verifiable but require agents to actively query them at session start.
   The hybrid path (C) in ADR-F-007 is the most powerful but most complex. What is
   the acceptable complexity level for Stage 1?

---

## Recommended Next Steps

1. Human reviews this proposal and marks `status: APPROVED` or raises objections.
2. Human authors formal ADRs for each ADR candidate above, prioritised:
   - **Immediate (before Step 03 ships):** ADR-F-002 (WAL schema), ADR-F-001 (know version contract)
   - **Before Step 05 ships:** ADR-F-003 (approval queue), ADR-F-004 (project isolation)
   - **Before Stage 2 begins:** ADR-F-005 (security model), ADR-F-007 (lessons channel)
   - **At Stage 2 gate:** ADR-F-006 (health metrics), ADR-F-008 (dash scope)
3. Human (or gap-writer agent) authors `docs/architecture/context.md` from the L1 context
   section above, and `docs/architecture/containers.md` from the L2 container analysis.
4. Human updates `state/arch/gap-trigger.md`: set `status: CLOSED`.
5. Run `/health-check architecture` against the new `containers.md` to verify consistency.
