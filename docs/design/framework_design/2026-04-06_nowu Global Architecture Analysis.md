# nowu Global Architecture Analysis

## Executive Summary

Based on a deep analysis of `vision.md` (v2.0), `USE_CASES.md` (v2.2, 47 UCs), the Guo et al. 2025 survey of LLM-empowered software engineering, the Palantir Ontology comparison, and an audit of current design documents (ARCHITECTURE.md v1.3, containers.md, DECISIONS.md, 6 ADRs), three architecture options are proposed, evaluated via ATAM, and compared against the existing design. The verdict: the current architecture is directionally correct and more sophisticated than most comparable frameworks, but it has three structural gaps that must be closed. A targeted evolution — not a rewrite — is recommended.

***

## 1. Vision & Use-Case Architecture Drivers

### What the Vision Demands

The nowu vision v2.0 defines five non-negotiable architectural properties:[^1]

1. **Continuity as infrastructure** — sessions must always pick up without manual re-orientation (NF-01, NF-10).
2. **Atomic knowledge graph** — every fact, decision, lesson, and idea is a discrete unit with provenance, confidence grade, and relationships. The same graph is rendered differently for humans vs. AI agents — "same data, different lenses."[^1]
3. **Artifacts as the primary API** — agents communicate through version-controlled files, not conversations. A broken artifact breaks visibly; a broken conversation fails silently.[^1]
4. **Self-building** — nowu must run its own development using itself, with 90–99% AI work ratio at 6 months. This means the architecture must be maximally legible to AI agents — structured, bounded, and testable.[^1]
5. **Multi-project, local-first, no walled garden** — all data is portable, inspectable, and user-controlled.[^1]

### What the Use Cases Demand

The 47 UCs across NF, AP, RE, PK, and XP groups reveal five architectural requirements:[^2]

- **Resumption protocol** (NF-01, NF-10): structured session state that any agent or human can read cold and resume from.
- **Decision enforcement** (NF-02): architectural decisions must be machine-checkable at review time.
- **Learning loop** (NF-06, XP-03): pattern detection and lesson transfer must be automatic — not passive documentation.
- **Cross-project federation** (XP-01, XP-11): semantic discovery across project boundaries without blurring project isolation.
- **Tiered approval** (NF-05): Tier 1 auto-proceed / Tier 2 batch / Tier 3 block, with the human only seeing high-value gates.

The use-case distribution is notable: `know` owns 27 of 47 UCs (57%) — meaning the knowledge layer is the center of gravity, not the workflow orchestrator.[^2]

***

## 2. What State-of-the-Art Says

### Guo et al. 2025 — Agent-Based Software Engineering

The survey of 150+ papers identifies four core agent capabilities that must be architecturally provided:[^3]

| Capability | What it requires architecturally |
|---|---|
| Planning & Decomposition | Hierarchical task structures; staged pipelines with explicit handoffs |
| Reasoning & Self-Refinement | Generate-test-revise loops; sandbox execution; VBR gates |
| Memory Mechanisms | Tiered memory: volatile short-term (session) + persistent long-term (knowledge graph) |
| Tool Augmentation | Explicit tool registry; Agent-Computer Interface (ACI) with bounded commands |

Critically, Guo et al. identify **hierarchical cognitive architecture** as the path beyond token-limit scalability — moving from flat token sequences to Code Property Graphs and tiered memory systems. They also flag the **evaluation crisis**: agents optimized for benchmark pass-rates produce code that fails in production due to security flaws and technical debt. The solution is lifecycle-aware benchmarking and verified acceptance criteria — exactly what NF-04 (VBR) and NF-09 (traceability) address.[^3]

For AI-creatable systems specifically, the survey emphasizes that **process-oriented training data** (trajectories, not snapshots) and **self-evolving architectures with continuous learning** are the frontier. An architecture designed to be built by AI agents must expose deterministic handoffs, small bounded tasks, and machine-checkable contracts at every seam.[^3]

### Spotify's "Honk" — Production AI Engineering

Spotify's Honk (built on Claude Code + Slack ChatOps) demonstrates the reference production pattern: AI handles full-stack feature development, database migrations, API endpoints, testing, and deployment; engineers approve or reject. The architecture that enables this is not a monolith or a microservice cluster — it is a **ChatOps + CI/CD integration layer** where the AI operates through the same interfaces as a human developer (Slack, git, deployment pipelines). The lesson for nowu: the human-facing interaction surface must be a first-class architectural concern, not an afterthought.[^4][^5][^6]

### oh-my-codex / claw-code / openclaw

**oh-my-codex v2** establishes the pattern of "a default path from a vague prompt to a durable multi-worker runtime" — a concept directly analogous to nowu's intake-to-implementation cycle. The key architectural pattern: a **role roster** (Architect, Implementer, Reviewer) with explicit handoff contracts in `AGENTS.md`.[^7][^8]

**claw-code** (Python + Rust) models a full agent stack as distinct layers: API client → runtime → tools → commands → plugins → compatibility harness → CLI. The plugin pipeline is the critical innovation: every capability is a plugin that implements a known interface, making the system composable and AI-creatable at the component level.[^9]

**openclaw** uses a **Gateway + Skills ecosystem** where skills are distributed via ClawHub, the framework has persistent memory and messaging integration, and the perception-action loop is the primary execution primitive. This maps directly to nowu's vision of cross-platform interaction (PK-08).[^10]

### DDD for Agentic Codebases

The key insight from applying DDD to agentic systems: **bounded contexts prevent "prompt spaghetti"**. Each agent needs a ubiquitous language for consistent tool inputs/outputs, stable port/adapter contracts, and CI evaluation gates that keep agents honest. These are not nice-to-haves — they are the reason agentic systems remain maintainable at scale.[^11]

### Clean Architecture

The dependency rule (infrastructure → domain, never domain → infrastructure) is what makes a codebase AI-implementable: agents can generate infrastructure layers independently because the domain layer has no hidden assumptions about how it will be called. The current nowu design follows this correctly via `core/contracts.py` — but incompletely, as discussed below.[^12][^13]

***

## 3. Three Architecture Options

### Option A: Refined Modular Monolith with Pluggable Pipelines

This is an evolution of the current architecture — same 5-module structure, but with three targeted fixes:

**Structure:**
```
core/       (contracts, domain models — I/O-free)
  └── contracts.py  (KnowledgeStoreProvider, AdapterProtocol, PipelineStep)
flow/       (pipeline orchestrator)
  └── pipelines/    (each pipeline as a registered, discoverable unit)
  └── steps/        (S1-S9, P0-P4 as pluggable PipelineStep implementations)
soul/       (AI analytical reasoning — artifact-coupled)
know/       (atomic knowledge graph, per-project SQLite + federation)
bridge/     (CLI + messaging adapters)
  └── adapters/     (CLI, Telegram, future: voice/HTTP)
```

**Key changes from current:**
- Pipeline steps become registered `PipelineStep` protocol implementations (discoverable by AI agents)
- `soul` gets an explicit Skills registry: `soul/skills/` directory of bounded analytical capabilities
- `flow` and `soul` coupling gets a lightweight sentinel contract (`soul_manifest.yaml`) so S3 can validate soul outputs without filesystem path coupling
- `bridge` adapter protocol (ADR-0002) is formally ratified and moved from PROPOSED to ACCEPTED

**AI-agent buildability:** High. Agents see small, bounded protocol implementations. The pipeline step registry acts like an MCP tool manifest — agents can enumerate what pipelines exist and what each step does.[^3]

***

### Option B: Knowledge-Centric Event-Sourced Architecture

Reframe `know` as the source of truth for ALL state — not just knowledge atoms, but also session events, pipeline transitions, and approval decisions. `flow` and `soul` become event consumers and producers.

**Structure:**
```
core/       (contracts, domain events, projections)
know/       (event store + projection engine + knowledge graph)
  └── events/       (append-only event log per project)
  └── projections/  (derived views: session state, today view, health metrics)
  └── atoms/        (knowledge atoms with confidence grades)
flow/       (event-driven pipeline — subscribes to events, emits new events)
soul/       (analytical projections — reads event log, writes derived insights as atoms)
bridge/     (event emitter for user actions; projection reader for display)
```

**Key changes from current:**
- Session state is not a WAL file — it is an event projection from `know`
- "Artifacts as the API" becomes "events as the API" — every state change is an append-only event
- Soul does not need one-cycle staleness — it processes events as they arrive (or in batch)
- Cross-project federation becomes event federation (query across multiple event logs)
- Export (XP-08) is event log slice + projection snapshot

**AI-agent buildability:** Medium. Event-sourced architectures are well-understood but require agents to understand projection semantics — which is non-trivial to implement correctly without errors.[^3]

***

### Option C: Agent Mesh with Capability Registry (Microkernel)

Inspired by openclaw's Gateway + Skills pattern and the plugin pipeline architecture of claw-code. The microkernel holds minimal routing logic; all capabilities are registered plugins.

**Structure:**
```
core/       (kernel contracts, capability registry, message bus)
  └── registry.py   (AgentCapability protocol + discovery)
  └── bus.py        (in-process message bus for agent coordination)
capabilities/       (each nowu capability as an independent plugin)
  └── session/      (NF-01 — session resumption)
  └── decisions/    (NF-02 — ADR enforcement)
  └── scoping/      (NF-03 — scope management)
  └── quality/      (NF-04 — VBR gate)
  └── knowledge/    (all PK + XP + AP + RE UCs)
  └── learning/     (NF-06, XP-03 — pattern detection, lesson transfer)
  └── orientation/  (NF-10 — today view, thread maintenance)
bridge/     (adapter layer — same as Option A)
```

**Key changes from current:**
- No `flow`, `soul`, `know` modules — replaced by capability plugins registered with the kernel
- The 8 workflow agents (S1-S9) become capability invocations, not hardcoded pipeline steps
- Each capability exposes a `manifest.yaml` (discoverable by AI agents) with inputs, outputs, dependencies
- The message bus replaces filesystem artifact coupling for soul↔flow-equivalent coordination

**AI-agent buildability:** Very high for individual capabilities (each plugin is small and bounded). Very low for the kernel and bus (complex coordination logic). The bus introduces race conditions and failure modes that require sophisticated error handling.[^3]

***

## 4. ATAM Evaluation

### Quality Attribute Scenarios

The following utility tree scenarios drive the evaluation:

| QA | Scenario | Priority | Source |
|---|---|---|---|
| **AI-buildability** | An AI agent implementing NF-03 can do so without reading any other module's source | Critical | Vision (self-building) |
| **Modifiability** | A new pipeline step (e.g., NF-15) can be added without touching existing steps | High | D-003, NF-07 |
| **Resumability** | After a crash mid-S5, S3's options artifact is still valid for the next cycle | Critical | NF-01 |
| **Knowledge integrity** | XP-04 conflict detection catches contradicting atoms with high confidence | High | XP-04 |
| **Performance** | XP-01 cross-project search across 20 projects returns in <200ms | Medium | XP-05 |
| **Portability** | XP-08 project export is semantically complete without external ID resolution | High | XP-08 |
| **Ubiquity** | PK-08 Telegram capture works when the local CLI is not running | High | PK-08 |
| **Observability** | NF-08 health metrics are computed without modifying flow or soul source | Medium | NF-08 |

### ATAM Scoring

| Quality Attribute | Weight | Option A | Option B | Option C |
|---|---:|---:|---:|---:|
| AI-buildability | 25 | 4 | 3 | 4 |
| Modifiability | 20 | 4 | 4 | 5 |
| Resumability | 20 | 5 | 5 | 3 |
| Knowledge integrity | 15 | 4 | 5 | 3 |
| Performance at scale | 10 | 4 | 3 | 4 |
| Portability / export | 5 | 5 | 5 | 4 |
| Ubiquity (PK-08) | 5 | 5 | 4 | 4 |
| **Weighted total** | **100** | **4.30** | **4.05** | **3.85** |

### Tradeoff Points and Sensitivity Analysis

**Option A sensitivity points:**
- `know`'s 27-UC load is a risk concentration. If `know` needs to be split (e.g., for v2 multi-user), it is a bounded internal refactor — all callers use `KnowledgeStoreProvider` protocol.
- Soul's one-cycle artifact staleness (ADR-0006) is a structural tradeoff: NF-13 options are always from the previous cycle. This is bounded and detectable, but not zero-latency.
- Pipeline steps as hardcoded implementations (current state) limit discoverability. The fix (registering steps as protocol implementations) is low-risk and high-value.

**Option B tradeoff points:**
- Event sourcing solves the soul staleness problem but introduces projection complexity. Agents implementing projections must understand event ordering and idempotency — a non-trivial constraint that increases implementation error surface.[^3]
- The "artifacts as the API" principle is weakened: events are harder to inspect than Markdown files. Debuggability and agent resumption (NF-01) depend on projection correctness, not readable files.
- Event sourcing is the right long-term pattern for XP-09 (multi-user, v2), but premature at v1-core.

**Option C tradeoff points:**
- The in-process message bus introduces failure modes (message ordering, delivery guarantees) that are not present in Option A's artifact model. Guo et al. explicitly flag this as over-engineered for single-user systems.[^3]
- The capability registry requires the kernel to be correct before any capability can be built. This is a critical-path dependency that serializes early AI-agent work — the opposite of what a self-building system needs.
- The microkernel pattern is ideal for a framework that ships as a product to other developers (v2 vision), but premature for a personal tool in Stage 1.

### Risk Themes

**Option A risks:**
- R1: `know` complexity overload at v1.1+ if 27 UCs accumulate without internal decomposition. Mitigation: internal sub-packages (`know/atoms/`, `know/federation/`, `know/graph/`) with clean interfaces.
- R2: soul artifact staleness causes NF-13 failure if soul's S9 subprocess fails repeatedly. Mitigation: the sentinel file mechanism in ADR-0006 catches this; a retry option can be added without architecture change.

**Option B risks:**
- R3: Projection bugs silently corrupt derived state (session view, health metrics). Mitigation: snapshot testing of projections — but this adds significant test complexity for early-stage work.
- R4: Event log growth without compaction strategy. Mitigation: event compaction at S9 curator step — but this is net-new complexity not in current scope.

**Option C risks:**
- R5: Message bus race conditions between concurrent capability invocations. Mitigation: require sequential execution — but this eliminates the parallelism benefit that justifies Option C's complexity.
- R6: Capability manifest proliferation: 47 UCs become 47 capabilities, each with a manifest. AI agents building individual capabilities cannot easily understand system-wide state without the kernel. The complexity is distributed rather than eliminated.

***

## 5. Recommendation: Option A — Refined Modular Monolith

**Option A is recommended** — not as-is, but with three targeted changes that address the structural gaps identified through this analysis.

### Why Option A

The "artifacts are the API" principle is not an implementation convenience — it is the primary mechanism by which AI agents can build nowu without human coordination. Every artifact is a durable, inspectable, version-controlled handoff point. Event sourcing (Option B) weakens this; the bus (Option C) eliminates it. Option A preserves it while fixing its current weaknesses.[^1]

Spotify's Honk demonstrates that the human-as-approver model works in production with a clean interaction layer — not with a complex event bus. Guo et al. confirm that for single-agent systems and small teams, a staged pipeline with explicit handoffs outperforms distributed architectures in implementation reliability.[^6][^3]

### The Three Required Changes

**Change 1: Ratify and complete the missing ADRs (immediate)**

ADR-0002 (bridge adapter protocol) and ADR-0003 (LLM client architecture) are both PROPOSED. These are critical-path blockers: nothing that touches `bridge` or LLM configuration can be safely implemented until they are ACCEPTED. The S4 decision session for ADR-0002 must happen before PK-01 or PK-03 implementation begins.

**Change 2: Register pipeline steps as discoverable protocol implementations (v1-core)**

Currently, flow's pipeline steps are hardcoded implementations inside `flow`. This means an AI agent adding a new step (e.g., NF-15 in a future cycle) must navigate `flow`'s internals. The fix: define a `PipelineStep` protocol in `core/contracts.py` and register each step (S1-S9, P0-P4) as an implementation. Steps become an enumerable, discoverable list — like an MCP tool manifest. This change is low-risk (internal to `flow`) and high-value (directly improves AI-buildability for every future NF use case).

**Change 3: Decompose `know` internally before v1.1 (v1 gate)**

`know` owns 57% of all use cases. Even with clean external contracts, this concentration creates implementation risk: any AI agent working on, say, XP-11 (knowledge graph queries) must navigate the same module that implements AP-01 (regulatory requirements) and PK-06 (sensitivity tags). The fix is not a new module — it is internal sub-packages:

```
know/
  atoms/        (CRUD, confidence, temporal metadata)
  graph/        (relationships, cross-project discovery)
  sensitivity/  (PK-06 foundation for AP-07, RE-07, XP-10)
  ingestion/    (PK-07 pipeline)
  federation/   (XP-01 fan-out query layer)
  export/       (XP-08 portable snapshot)
```

This does not change `know`'s external API — all callers continue to use `KnowledgeStoreProvider`. It makes AI-agent implementation of individual know sub-features tractable without knowledge of the entire module.

***

## 6. The Right Final Architecture

Combining the recommendation above with the current design, the target architecture for nowu is:

### C4 Level 1 — System Context (unchanged)

```
Raphael → nowu (local Python CLI)
nowu → LLM API (outbound only)
nowu → External Documents (PK-07 ingestion)
nowu ↔ Telegram (PK-08 remote interface, v1+)
```

### C4 Level 2 — Containers (refined)

| Container | Responsibility | UCs | Change from current |
|---|---|---|---|
| `core` | Contracts, domain models, PipelineStep protocol, AdapterProtocol, KnowledgeStoreProvider | 0 (infra) | Add `PipelineStep` protocol |
| `flow` | Step-registered pipeline orchestrator; session state; approval routing; VBR gate | 9 | Steps as `PipelineStep` implementations |
| `soul` | AI analytical reasoning; artifact-coupled via sentinel contract | 7 | Add `soul_manifest.yaml` sentinel |
| `know` | Atomic knowledge graph; internal sub-packages | 27 | Internal decomposition (no API change) |
| `bridge` | Typer CLI + AdapterProtocol implementations (CLI, Telegram) | 4 | ADR-0002 → ACCEPTED |

### Import Graph (unchanged, now fully ratified)

```
flow   → core
soul   → core
know   → core
bridge → core, flow (contracted API), know (contracted API)
```

### What Does NOT Change

- **5-module structure** — lean, correct, appropriate for Stage 1-2[^14]
- **Artifact-based soul↔flow coupling (ADR-0006)** — the artifact staleness tradeoff is correct and bounded[^15]
- **Per-project SQLite with federation (ADR-0004)** — the design defect in Option A (single shared DB) is correctly avoided[^16]
- **TDD with VBR gate (D-004)** — the Guo et al. survey confirms test-driven refinement as the primary quality mechanism for agent-based SE[^3]
- **Tiered approval model (D-009)** — the Spotify Honk pattern: human approves, AI executes[^6]
- **8 dedicated agents per workflow step (D-005)** — context isolation per step prevents the "context bleed" failure mode documented in multi-agent collaboration research[^3]
- **Local-first, no cloud** — correct for Stage 1; evolution path to v2 multi-user is additive[^17]

***

## 7. Existing Design Audit

### What Is Good

**Structurally sound and validated by state-of-the-art:**

- **The 5-module structure with `core` as contracts-only** is a clean implementation of the Dependency Inversion Principle. Clean Architecture literature confirms: domain layer knowing nothing about infrastructure is what makes a codebase AI-implementable. ADR-0001 enforces this statically via import-linter.[^13][^12]
- **Artifact-based soul↔flow coupling (ADR-0006)** is the right tradeoff for a local, single-user system. The event bus alternative (rejected in ADR-0006) would add race conditions and delivery-guarantee complexity that the Guo et al. survey explicitly flags as over-engineered at this scale.[^15][^3]
- **Per-project SQLite with federation (ADR-0004)** solves the XP-08 export requirement correctly. The single-DB alternative was correctly identified as a design defect (not a tradeoff).[^16]
- **8 dedicated agents per step (D-005)** aligns with the multi-agent specialization pattern validated by MASAI, AgileCoder, and MAGIS in Guo et al. — specialized agents outperform generalists for bounded cognitive tasks.[^3]
- **TDD with 90%+ coverage + VBR gate (D-004)** is directly supported by Guo et al.'s emphasis on test-driven refinement as the primary quality mechanism in agent-based SE, and by Spotify's approve/reject human role.[^6][^3]
- **Tiered approval model (D-009)** correctly separates the human's cognitive load from agent execution. The Tier 1/2/3 classification mirrors the ChatOps human-in-the-loop patterns used by Honk.[^5]
- **The knowledge atom model with confidence grades** maps precisely to the Palantir Ontology "primitive" model: Data (nouns) + Logic (reasoning) + Action (verbs) + Security (scoping). nowu has the first three through `know`; sensitivity tags are the security layer.[^18]
- **`soul` redesign to AI analytical reasoning** (containers.md) is the correct evolution away from "governance docs module" (ARCHITECTURE.md v1.3). This separation of analytical intelligence from pipeline orchestration is a best practice validated by the MASAI architecture in Guo et al..[^3]

### What Is Bad / Needs Fixing

**Critical issues:**

1. **ARCHITECTURE.md is stale** — version 1.3 (March 2026) still defines `soul` as "Human-authored identity and governance docs (VISION, AGENTS, WAL conventions)." This directly contradicts containers.md (April 2026) which defines `soul` as "AI-powered analytical reasoning." Any AI agent reading ARCHITECTURE.md will build the wrong `soul`. This document must be updated to reflect the April 2026 global-pass decisions before any `soul` implementation work begins.

2. **ADR-0002 and ADR-0003 are PROPOSED** — these are not nice-to-have ratifications. ADR-0002 (bridge adapter protocol) is on the critical path for PK-01, PK-03, and NF-10, all of which are v1-core. ADR-0003 (LLM client architecture) is needed before any LLM-calling code can be written in `flow` or `soul`. The delay creates a window where AI agents may implement incompatible LLM client patterns.

3. **No `PipelineStep` protocol in `core`** — pipeline steps are implemented inside `flow` without a discoverable contract. This directly impairs AI-agent buildability (Guo et al. key finding: tool augmentation requires explicit tool contracts ). An AI agent cannot enumerate available pipeline steps or safely add a new one without reading `flow`'s internals.[^3]

4. **`know` has no internal structure** — 27 UCs in a flat module creates a navigation problem for AI agents. When implementing XP-11 (knowledge graph queries in role-appropriate format), an agent must understand the entire `know` module to avoid breaking AP-01 or PK-06. The sub-package decomposition described in Section 6 is the fix.

**Moderate issues:**

5. **NF-10 (Maintain the Thread) is assigned to `bridge`** — but the UC description makes clear that the orientation artifact requires reading from both session state (`flow` artifacts) and knowledge atoms (`know`). `bridge` can be the presenter, but the orientation computation belongs in a dedicated step in `flow` or as a `soul` analytical task. The current assignment conflates presentation (bridge's job) with computation.

6. **D-001 (File-Based Memory Architecture) has not been reviewed since `know` became operational** — the review trigger says "When `know` MemoryService is operational." `know` v0.4.0 is operational. D-001 should be reviewed and either superseded by a richer memory architecture ADR or explicitly confirmed as complementary.

7. **No explicit skill/capability discovery mechanism** — unlike openclaw (ClawHub skills) or claw-code (plugin pipeline with manifests), nowu has no way for an AI agent to ask "what can this system do right now?". The `PipelineStep` protocol registry fixes this for flow; a parallel `SoulCapability` registry should be added for soul's analytical functions.[^9][^10]

**Minor issues:**

8. **`dash` module is still in ARCHITECTURE.md as a future placeholder** — it should either be explicitly deferred to v2 with a note in the roadmap, or removed from the architecture document to avoid confusion. The containers.md correctly omits it; ARCHITECTURE.md should be consistent.

9. **ADR-0005 (Telegram) is PROPOSED** — this is lower urgency since PK-08 is v1 (post v1-core), but the Telegram dependency should be finalized before v1-core is declared stable, so v1 scoping can proceed without an ADR gap.

***

## 8. What You Should Have as the Final Architecture

The final architecture is **Option A — Refined Modular Monolith**, with the following concrete action list:

### Immediate (before any v1-core implementation)
1. **Update ARCHITECTURE.md** to reflect the April 2026 global-pass soul redefinition. Mark v1.3 as superseded.
2. **Ratify ADR-0002** (bridge adapter protocol: Typer + AdapterProtocol in core) via S4 decision.
3. **Ratify ADR-0003** (LLM dual client: flow + soul each instantiate independently from `LLMClientConfig`) — it is already resolved as an ADR-0006 corollary; it needs the ACCEPTED stamp.
4. **Add `PipelineStep` protocol to `core/contracts.py`** and register the S1-S9 and P0-P4 steps as implementations.

### At v1-core completion (before v1 scoping)
5. **Decompose `know` into internal sub-packages** (atoms, graph, sensitivity, ingestion, federation, export) without changing the external `KnowledgeStoreProvider` API.
6. **Review D-001** (file-based memory) for compatibility with `know` operational status.
7. **Ratify ADR-0005** (Telegram) to unblock PK-08 v1 scoping.
8. **Clarify NF-10 ownership** — define whether orientation computation is a `flow` step or a `soul` analytical task, with `bridge` as presentation-only.

### At v1.1 (before domain projects scale)
9. **Add `SoulCapability` registry** in `soul/` analogous to the `PipelineStep` registry in `flow`. Each soul analytical function (options generation, pattern detection, drift analysis, work ratio, conflict detection) becomes a discoverable `SoulCapability` implementation.
10. **Add `soul_manifest.yaml` sentinel** to replace the implicit filesystem path coupling between `soul` and `flow`. The manifest declares which artifacts soul will write; `flow` reads the manifest rather than hard-coding state file paths.

The resulting architecture correctly implements:
- DDD layer boundaries (D-002) with static enforcement[^12]
- Agent-based SE best practices (Guo et al.): planning decomposition via registerable pipeline steps, memory via tiered atoms+WAL, tool augmentation via discoverable protocols[^3]
- Palantir Ontology pattern: atomic knowledge primitives with confidence grades, action verbs (approval tiers), security scoping (sensitivity model)[^18]
- Spotify Honk production model: human as approver, AI as executor, ChatOps interface (Telegram) as interaction layer[^6]
- Clean Architecture dependency rule, DDD bounded contexts, artifacts-as-API[^13][^11]
- claw-code / openclaw plugin composability without the operational overhead of a full plugin bus[^10][^9]

---

## References

1. [vision.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/7bafbece-9150-43b8-ae94-89896dad79cb/vision.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=dUpL4V1qtt1yhtxeIbgPaLXB8Oo%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - ---
last_updated: 2026-03-31
last_approved: 2026-03-31
status: APPROVED
version: 2.0
stage: 1
produc...

2. [USE_CASES.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/16494219-33d0-4eb0-a477-d4d9fc4d4968/USE_CASES.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=bwt3WA9ga8C96x%2BPFAOnyAfiSVk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - ---
version: 2.2
generated_by: use-case-agent@2.2
generated_at: 2026-04-06
based_on_vision: v2.0 (ap...

3. [Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LL.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/e45b316d-ee86-4e38-8088-1989c65a02c1/Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LLM-Empowered-Agentic.pdf?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=tm6YUFg%2FMrBiVtwSchgphw0iH60%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic ...

4. [Spotify CEO: AI now writes and deploys code, engineers only review](https://indianexpress.com/article/technology/tech-news-technology/sporify-ai-vibe-coding-developers-review-10530446/) - ... tools to accelerate development. ... Soderstorm say that they are now using an internal AI tool ...

5. [Spotify's AI System 'Honk' Automates Development Tasks - LinkedIn](https://www.linkedin.com/posts/andresveraf_spotify-says-its-best-developers-havent-activity-7428084939327344640-ZOoz) - How Developers can Adapt to AI Changes · AI Coding Tools and Their Impact on Developers · Benefits o...

6. [Spotify's Engineers Stop Coding as Honk AI Takes Over ...](https://www.thehansindia.com/tech/spotifys-engineers-stop-coding-as-honk-ai-takes-over-development-workflow-1048135) - As AI tools grow more capable and more deeply embedded in corporate workflows, Spotify's experiment ...

7. [oh-my-codex (OMX) v2 - GitHub](https://github.com/staticpayload/oh-my-codex) - Codex-native orchestration for builders who want one default path from a vague prompt to a durable m...

8. [oh-my-codex/AGENTS.template.md at master - GitHub](https://github.com/staticpayload/oh-my-codex/blob/master/AGENTS.template.md) - 2. EXECUTIVE ARCHITECTURE · Codebase structure and organization · Choice of libraries and frameworks...

9. [Claw Code Launches as Open-Source AI Coding Agent Framework ...](https://newclawtimes.com/articles/claw-code-open-source-ai-coding-agent-framework-72000-github-stars-launch/) - An open-source project called Claw Code launched today as an AI coding agent framework built in Pyth...

10. [Comprehensive Guide to OpenClaw GitHub Setup Instructions and ...](https://skywork.ai/skypage/en/openclaw-github-setup-ai-agent/2038581106300502016) - Discover OpenClaw: free, open‑source AI agent framework. Learn GitHub setup, compare with NanoClaw, ...

11. [From Prompt Spaghetti to Bounded Contexts: DDD for Agentic ...](https://gitnation.com/contents/from-prompt-spaghetti-to-bounded-contexts-ddd-for-agentic-codebases) - This presentation shows how Domain-Driven Design (DDD) turns agentic coding from “prompt spaghetti” ...

12. [ADR-0001-module-boundary-enforcement.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/76d0d9f2-72a9-4dd2-bcab-62873ffe937c/ADR-0001-module-boundary-enforcement.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=lERGUBURiQVpE8AUx0mPU41VRxI%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - ---
id: ADR-0001
title: Module Boundary Enforcement
date: 2026-04-06
status: ACCEPTED
superseded_by:...

13. [Clean Architecture and Domain-Driven Design in Practice 2025](https://wojciechowski.app/en/articles/clean-architecture-domain-driven-design-2025) - Complete guide to Clean Architecture and Domain-Driven Design: application layers, Bounded Contexts,...

14. [ARCHITECTURE.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/f6e6a3a5-81e2-4c5e-973e-3537e5146d13/ARCHITECTURE.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=e1Ry7NzBVBrE3XmV3194pyrqicw%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - # nowu Architecture

Version: 1.3
Date: 2026-03-22
Status: Active — scaffold complete, Step 02 (Memo...

15. [ADR-0006-soul-flow-integration-pattern.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/b09e0db5-d913-4d77-9343-03401115c0a1/ADR-0006-soul-flow-integration-pattern.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=f9xiyoVncGSIsDsOFchhXsEAr30%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - ---
id: ADR-0006
title: Soul–Flow Integration Pattern — Artifact-Based Coupling with S9 Subprocess
d...

16. [ADR-0004-database-isolation-model.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/01150881-f611-4e5c-bd65-aefac4c5266b/ADR-0004-database-isolation-model.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=FAWA%2B4LCOnzlNxDEC8HsN%2BDaxKk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - ---
id: ADR-0004
title: Database Isolation Model — Per-Project SQLite with Federation
date: 2026-04-...

17. [context.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/6f9ad4b0-b0b1-4db3-b650-c1766ffb0eaa/context.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=x%2FM2dX4LEnz9lzAj7SBdOEaQ6%2Fw%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - ---
version: 1.0
generated_from: global-pass-2026-04-06
status: DRAFT
last_gap_check: 2026-04-06
---...

18. [nowu_palantir_guo_et_al_comparison.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/6693d3f8-e4b4-4d6e-895e-c1ca51b8d317/nowu_palantir_guo_et_al_comparison.md?AWSAccessKeyId=ASIA2F3EMEYEYXUCQAD2&Signature=6AKg0aYXt6dpDTyLiBFNo2rUzRY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAUaCXVzLWVhc3QtMSJIMEYCIQCz5vqz%2BUa3zZPD%2FVdSmMA%2B3F2%2B3YfAC%2FSQqgC4BrvNtAIhAOkT5UC1FLr8tIspudZFGfiVu4bKzChV6oYx4v64b9%2FRKvwECM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMNjk5NzUzMzA5NzA1Igy%2BG%2BG2yu1nqBXw7SQq0ARVWwRAaWtSOC9pN7sd%2BJW7oueO%2Fr2RfhwEj2J1mqalKhkOfRZm7nz0juSLW6Sci4%2Fty8xOujuaY7Q3ln0YYwinUFulpBLzGZqtuEwrC%2BgWkq4NhIktYVe%2F6EEb3qK93lw%2BOcINbcz5A%2B2NArs9l3azfDxBNhnHiPxcqIvlrgkD%2BYq79Q3nERkykWjbqqsooBKy2SpKD3CY685iYs0Q8zXOC1Nr5Nj2PZcCsse1OaVoe7iqv8EA%2Fwpk0%2FSVOexOVGIgW0uzsaTRy7Fzx64sEgu4UGC6DJ4hk1dFU8o5ZUF%2BANuhL0UjQw7AvuldH2E45hQu%2F3gV0WYK3AQQHlL5UnWwQw6wdVVO2Ah3V9iZqVF%2FXOA3jRRCcDy7ZtbLZTMbWuydxD636J2RZYsTZhzezyOe615SiybW%2FNuk58iI9PoF9OKxplCELx2fPX7XMHYX7uyWtzRrCC%2BV1%2BkVId99FSWNYqvMAHOaluDHw8IztmHin3RIZL59xg5ApoI%2BWws%2BcxmiM5Pn0Sf%2Bso6ufit5koiZNkImNDQfVgy1yQ3mlorbdaxr8dL09wsKzDRdZQ57GsM9n%2FgQghu%2BzD4mQ%2Fs8%2FGR5MgIFK%2FjdgRxQAZ5EYi3haCjvHsCYGnv0pg93o9pnDIra8SDzkJSHU%2FQX6L%2BOvmTLTcCsOgS0Fsz8RMEH0lj6KpkkLIU4TT6v8RfQMr38PGmtA9hLRNW2IsTzom8jk%2BsZQAH14fbCHKEYMUQZEKTyMbcvqc%2B1yQG1%2FqV31JR4Ic0vXrdAEw8AeldmDMfG%2F2WbMKDZzs4GOpcBA6ZOZy0CptUc%2Fxci6G%2FLZYZSJxS6cKFRhZnnqJ6TGOgpuTRuExbEYQNSFLKv3JVlmcJG8W898Y15LWGPgYSx2BYeadbFdjTlGU2XmDNBE2XR6TddclrBwREvG2QeMg6SzFHiaVIpfkzK4pTBZb8z5zqORnnJDGZkf6t1aYBhJ51Ev7mGccPcTMLOEJlo1zMxG4zkx6nVmg%3D%3D&Expires=1775483507) - The nowu framework does not need a major overhaul. Both Palantirs Ontology architecture and the Guo ...

