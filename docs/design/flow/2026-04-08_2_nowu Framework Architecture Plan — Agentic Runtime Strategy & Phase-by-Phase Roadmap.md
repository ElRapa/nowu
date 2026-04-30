# nowu Framework Architecture Plan — Agentic Runtime Strategy & Phase-by-Phase Roadmap
> **Purpose:** A strategic decision document for choosing, adopting, and evolving the orchestration runtime for nowu across four development phases. Every recommendation is grounded in nowu's vision (v2.0, approved 2026-03-31), the USE_CASES catalog (v2.3), and the current state of the agentic framework ecosystem (April 2026).
>
> **User clarification on Principle 0:** Conversations between AI-AI or human-AI are acceptable as the working medium, *provided* that artifacts capturing relevant decisions, state, and reasoning are produced at defined checkpoints. This relaxes strict "only files" orthodoxy while preserving the continuity requirement. The artifact is the long-term record, not necessarily every intermediate exchange.

***
## 1. Where nowu Is Today
nowu is currently in **Stage 1, v1-core, Step 02** (Memory Integration Layer in progress). The workflow runs in practice as a **prompt-based orchestration** approach: SKILL.md and agent prompt files (nowu-intake.md, nowu-decider.md, nowu-shaper.md, etc.) are loaded into GitHub Copilot in VS Code, and each step (S1–S9) is triggered manually by the human as a conversation. The human carries the orchestration burden — deciding when to move from S2 to S3, loading the right agent prompt, triggering the next step. Artifacts (SESSION-STATE.md, DECISIONS.md, PROGRESS.md, task specs) are the durable record produced by each conversation.

This approach is not wrong — it is the correct starting point. The current state confirms several important things:

1. **The artifact schema is solid.** The fact that DECISIONS.md, PROGRESS.md, and SESSION-STATE.md already work as session resumption artifacts means NF-01 has a viable implementation path without any framework code.
2. **The agent prompts are stable contracts.** nowu-intake.md through nowu-curator.md define clear inputs, outputs, and altitude constraints — exactly the interface definitions that programmatic orchestration will later expose.
3. **The human is the orchestrator.** This is appropriate for v1-core validation: understanding exactly what the system needs to do before deciding how to automate it.

The gap that is currently felt, and will grow, is the **manual orchestration tax**: the human must remember to load the right agent, trigger the next step, queue approvals, and route work. This is the bottleneck that programmatic orchestration is meant to remove — but it is not urgent to remove today.

***
## 2. The Core Architectural Question
The question is not "which framework?" — it is three nested questions:

1. **Should nowu build its own orchestration or adopt a framework?**
2. **If a framework, which one and when?**
3. **How does the transition happen without breaking the current working system?**

These questions are answered differently at each phase.

***
## 3. The Three Strategic Options
### Option A — Prompt-Native, Artifact-Governed (Stay in the Shell)
**What it is:** Continue developing nowu as a collection of SKILL.md files, agent prompts, and artifact schemas, executed via a coding shell (OpenCode / Claude Code). Programmatic orchestration is introduced only when a specific pain point demands it — and then written as thin custom Python scripts, not a framework adoption. Conversations happen freely; artifacts are the durable record at each gate.

**Architecture:**
```
Human / Coding Shell
      ↓  loads
SKILL.md + Agent Prompts (nowu-*.md files)
      ↓  produces
Typed Artifacts (SESSION-STATE.md, DECISIONS.md, task-spec.md, ...)
      ↓  read by
Next Agent / Human at next step
```

**When this works best:** v1-core through v1. When nowu is still primarily a workflow *design* problem, not a workflow *execution* problem.

**Benefits:**
- Zero framework overhead or learning curve
- The artifact schema IS the API — perfectly aligned with nowu's current architecture
- AI agents already know how to produce and consume markdown/JSON artifacts
- No risk of framework dependency that could constrain long-term design
- Consistent with the 85% of production agentic teams that build custom in-house rather than using frameworks[^1]
- Conversations between agents or between human and agent are fine — the artifact produced at the end of each step is the durable record
- Every SKILL.md iteration directly improves the product

**Risks:**
- NF-05 (tiered approval routing) and NF-01 (session resumption) become painful at scale without at least a minimal script layer
- The human orchestration tax grows with project count (will matter more at v1.1 with 6+ active projects)
- No built-in observability — logging, health metrics (NF-08), and work-ratio tracking (NF-14) must be custom-built
- XP-06 (multi-agent concurrency) is hard to achieve safely without framework primitives

**Risks of over-correction:** If you adopt a heavy framework now to "solve" orchestration problems you don't yet have, you will spend most of v1-core building framework plumbing instead of building the nowu workflow and knowledge model.

***
### Option B — LangGraph as the Orchestration Engine (Framework-First)
**What it is:** Introduce LangGraph as the S1–S9 pipeline orchestration layer in v1 or early v1.1, with PydanticAI as the typed agent node implementation and LlamaIndex as the `know` module. Agent conversations can still happen freely within each node; the graph manages state, gates, and transitions between nodes.

**Architecture:**
```
LangGraph StateGraph (S0 → S1 → ... → S9)
  ↓ nodes = PydanticAI agents (typed input/output schemas)
  ↓ checkpoints = human approval gates (interrupt/resume)
  ↓ shared state = thread_id context (NF-01 resumption)
  ↓ reads/writes ↓
LlamaIndex `know` module (episodic, semantic, procedural memory)
```

**When this works best:** v1.1 and beyond, when multiple projects are running concurrently and the human orchestration tax is genuinely creating lost velocity.

**Benefits:**
- LangGraph checkpointer solves NF-01 exactly: thread state is persisted per thread_id, resumption is automatic[^2][^3]
- Human-in-the-loop interrupt/resume is a first-class primitive — NF-05 tier model maps cleanly to interrupt conditions[^4][^5]
- Cyclic graph supports S4 option-retry, S6→S7→S6 VBR loops, S8 back-to-S5 rejection — things a linear DAG cannot express[^2]
- LangSmith provides observability out-of-the-box — NF-08 health metrics and NF-14 work-ratio are much easier to measure[^6]
- LangMem's procedural memory layer enables NF-06 (lessons feed back into agent instructions) without custom code[^7]
- 400+ companies in production, including Uber, LinkedIn, Cisco, JPMorgan — well-proven at scale[^8]

**Risks:**
- Steeper learning curve — graph theory basics required before it feels natural[^5]
- LangChain ecosystem coupling — the ecosystem is large and sometimes suffers from API instability between versions[^9]
- Orchestration overhead for simple tasks: a single-agent S2 discovery run has graph setup cost added to it
- Risk of premature framework adoption: building graph boilerplate before the workflow itself is stable enough to express as a graph
- LangSmith is proprietary observability (though optional); using it creates partial vendor dependency

**Critical caveat:** Do not start with LangGraph until the workflow is stable. A graph is a formalisation of a workflow that already works. If the workflow is still being designed (which it is, today), formalising it prematurely produces a fragile graph that must be rewritten when the workflow changes.

***
### Option C — Thin Custom Python Layer (Custom-First)
**What it is:** Write a minimal custom Python orchestration layer — a CLI or simple script that reads SESSION-STATE.md, triggers the right agent for the current step, writes checkpoints, and queues approvals. Use PydanticAI for individual agent nodes from the start. No graph framework; just plain Python with clear interfaces. Adopt frameworks selectively for specific sub-problems where they excel (LlamaIndex for `know`, Atomic Agents for tool components).

**Architecture:**
```
nowu-cli (thin Python orchestrator)
  ↓ reads SESSION-STATE.md → determines current step
  ↓ loads correct PydanticAI agent (typed input/output)
  ↓ writes artifact checkpoint to /state/
  ↓ queues human approvals (YAML-based approval queue)
  ↓ writes/reads ↓
LlamaIndex `know` module (selective adoption)
```

**When this works best:** From v1 onward, when there is a clear pain point in manual orchestration but LangGraph's full graph complexity is not yet warranted.

**Benefits:**
- Full control — no framework constraints on workflow shape
- Type-safe artifact production from day one via PydanticAI[^10]
- Consistent with the dominant production pattern: 85% of production agent teams build custom rather than using frameworks[^1]
- The thin orchestrator *is* nowu code — it directly implements NF-05, NF-01, NF-09 as Python functions, and every improvement is nowu learning from itself (NF-06)
- Easy migration path: each custom component can be replaced with a LangGraph node later (strangler fig) without rewriting the rest of the system[^11]
- No ecosystem lock-in — change model providers, add new agent types, or swap LlamaIndex for a different knowledge layer freely

**Risks:**
- Must build what frameworks provide for free: checkpointing, retries, observability, state serialisation
- Risk of the custom orchestrator becoming the "framework that wasn't designed as a framework" — accumulating technical debt as complexity grows
- NF-08 (health metrics), NF-14 (work ratio), and XP-06 (concurrency) require non-trivial custom instrumentation
- Slower path to v1.1 features compared to LangGraph adoption, if the custom layer is not designed for extensibility

***
## 4. Recommendation: A Phased, Strangler-Fig Strategy
The right answer is not Option A, B, or C exclusively — it is a **deliberate phase progression** that starts with Option A, introduces Option C elements at the right inflection point, and adopts Option B selectively for specific modules when the workflow is stable enough to formalise. The governing principle is: **formalise only what you have validated**.

This approach is called a **strangler fig migration**: the old system (prompt-based orchestration) continues to work in production while the new system (programmatic orchestration) is built alongside it and incrementally takes over. Each module that is replaced is tested, then cut over; the old path is only removed when the new one is confirmed working.[^11][^12]

***
## 5. Phase-by-Phase Architecture Plan
### Phase 0 — Now: Validated Prompt-Native (v1-core, Step 02–07)
**Duration:** Remaining v1-core steps (estimated 2–3 months)

**Architecture:** Option A — pure prompt-native

**What the system looks like:**

```
Human (orchestrator)
  ├── loads SKILL.md in OpenCode / Copilot Chat
  ├── runs nowu-intake → produces intake-brief.md
  ├── runs nowu-discovery → produces discovery-report.md  
  ├── runs nowu-options → produces options.md
  ├── approves option (gate) → runs nowu-decider → produces decision.md
  ├── runs nowu-shaper → produces task-spec.md
  ├── runs nowu-implementer (parallel or sequential)
  ├── VBR: tests run, nowu-reviewer checks
  ├── Human batch review (Tier 2 gate)
  └── nowu-curator → updates DECISIONS.md, lessons, PROGRESS.md
```

**What to build in this phase:**
- Complete the Memory Integration Layer (Step 02): robust SESSION-STATE.md schema + S0 resumption protocol
- Stabilise the artifact schemas (intake-brief, discovery-report, options, task-spec, decision-record) — these become the interfaces that programmatic orchestration will later consume
- Begin logging every step's input artifact → output artifact pair → this is the training data for NF-06 learning loop and NF-14 work-ratio tracking
- Do NOT introduce framework code yet — the workflow is not stable enough to formalise

**Key milestone:** When any step can be resumed from its input artifact alone, without reading previous conversation history. This is the prerequisite for programmatic orchestration.

**Build tools:** OpenCode as primary shell (LiteLLM routing, SKILL.md compatible, Copilot Enterprise auth); OMC for intensive parallel sessions; Claude Sonnet 4.6 for most steps; o3 for high-stakes options/decisions (S3, S4).

***
### Phase 1 — v1: Thin Orchestration Backbone (Month 4–6)
**Duration:** v1 milestone period (dogfooding with AP, RE projects)

**Architecture:** Option C — thin custom Python + selective PydanticAI

**The inflection point:** By v1, you will have two non-software projects active (AP, RE) alongside the NF project. Manually loading the right agent prompt for three concurrent projects, each at different steps, will become the primary friction point. This is when the human orchestration tax becomes the bottleneck.

**What the system looks like:**

```
nowu-cli (thin Python orchestrator — ~300 lines)
  ├── reads /state/{project}/SESSION-STATE.md
  ├── determines current step and next action
  ├── loads correct PydanticAI agent (typed schema)
  │     ├── IntakeBrief (Pydantic model)
  │     ├── DiscoveryReport (Pydantic model)
  │     ├── OptionsDoc (Pydantic model)
  │     ├── DecisionRecord (Pydantic model)
  │     ├── TaskSpec (Pydantic model)
  │     └── QualityReport (Pydantic model)
  ├── writes checkpoint artifact
  ├── checks tier classification → routes to approval queue
  ├── human reviews YAML approval queue (PK-05 today view)
  └── LiteLLM router: model selection per step type
```

**What to build:**
1. **nowu-cli v0.1** — a minimal `nowu run <project> <step>` command that reads state, calls the right agent, writes the output artifact, and stops for human approval at Tier 2/3 gates. No LangGraph, no graph DSL — just Python functions and a state file.
2. **PydanticAI agent nodes** for each S-step — replacing raw prompt calls with typed, validated agent invocations. The `TaskSpec` Pydantic model, for instance, forces `in_scope_files`, `acceptance_criteria`, and `validation_trace` fields to always be populated.[^10]
3. **LiteLLM router** — route S3/S4 (high-stakes options/decision) to o3, S6 (implementation) to Sonnet 4.6, S2 (discovery) to GPT-5.1 for web search. This is a simple dict config, not a framework feature.
4. **Approval queue** — a `pending-approvals.yaml` file read by `nowu review` command. Tier 1 items auto-proceed; Tier 2 items appear in queue; Tier 3 items halt the step. Human runs `nowu review` and approves/rejects items in batch.

**What NOT to build yet:** The LlamaIndex know module, LangGraph graph, cross-project discovery. These are v1.1 features. Build only what removes the v1 orchestration bottleneck.

**Dogfooding validation:** Run AP-01, AP-02, AP-06, RE-01, RE-06 through the nowu-cli. If the thin orchestrator can handle three concurrent projects without session contamination, the architecture is valid. If it cannot, you discover the gaps in v1 — not v2.

***
### Phase 2 — v1.1: LangGraph for Flow, LlamaIndex for Know (Month 7–12)
**Duration:** v1.1 milestone period (knowledge compounds across projects)

**Architecture:** Selective Option B adoption — LangGraph for `flow`, LlamaIndex for `know`

**The inflection point:** By v1.1, the workflow steps are validated and stable (six+ cycles through each step across multiple domains). The artifact schemas are not changing every two weeks. The nowu-cli has proven what the system needs to do. This is the correct moment to formalise: the graph expresses a workflow that already works.

**Migration path (strangler fig):** The nowu-cli's Python functions become LangGraph nodes one-by-one. The SESSION-STATE.md stays as the human-readable artifact; the LangGraph checkpointer becomes the machine-readable state alongside it. Old CLI path continues to work during transition.

**What the system looks like:**

```
┌─────────────────────────────────────────────────────────┐
│  BUILD LAYER                                             │
│  OpenCode + OMC → write nowu code via SKILL.md          │
└─────────────────────────────────────────────────────────┘
             ↓  produces / modifies
┌─────────────────────────────────────────────────────────┐
│  FLOW LAYER (LangGraph StateGraph)                       │
│  S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9     │
│  • Each node = PydanticAI agent (typed artifact schema)  │
│  • Human gates = LangGraph interrupt checkpoints         │
│  • NF-01: thread_id checkpointer = session resumption    │
│  • NF-05: interrupt conditions = tier classification     │
│  • NF-06: LangMem procedural store = lesson feedback     │
│  • LangSmith: observability → NF-08, NF-14              │
└─────────────────────────────────────────────────────────┘
             ↓  reads/writes
┌─────────────────────────────────────────────────────────┐
│  KNOW LAYER (LlamaIndex)                                 │
│  • Episodic: session logs, decision history              │
│  • Semantic: knowledge atoms (source, confidence, links) │
│  • Cross-project: PK-07 ingestion, XP-01 discovery      │
│  • RAG queries: PK-09 domain expertise on demand         │
│  • XP-11: role-appropriate views (human vs. agent lens)  │
└─────────────────────────────────────────────────────────┘
```

**What to build in this phase:**

1. **LangGraph StateGraph** for S0–S9, migrating from nowu-cli functions one step at a time. Start with S1 (Intake) and S4 (Decision gate) — these have the clearest node boundaries.
2. **LangMem procedural memory** — connect S9 (Curator) output to a procedural store that modifies agent system prompts. When the Shaper consistently produces over-scoped tasks, the next S5 invocation gets a tighter constraint in its system prompt. This is NF-06 operationalised.[^13]
3. **LlamaIndex `know` module** — start with document ingestion pipeline (PK-07) and in-project semantic search. Cross-project discovery (XP-01) comes after in-project retrieval is stable.
4. **Atomic Agents tool library** — individual tools (web search, file reader, code executor, knowledge atom writer) as Atomic Agent components callable from PydanticAI nodes.[^14][^15]

**What remains custom:** The `know` schema — the `KnowledgeAtom` data structure with `source`, `confidence_grade`, `provenance`, `relationships`, `decay_date` — is not provided by any framework. This must be custom, but it can be stored and retrieved via LlamaIndex.

***
### Phase 3 — v1.2–v2: Mature Stack + Shipment Preparation (Month 13–24)
**Duration:** v1.2 and v2 milestones

**Architecture:** Stable LangGraph + LlamaIndex core, with Haystack as the deployment layer for the v2 product

**What the system looks like:**

The v1.1 architecture is fundamentally sound for v1.2. The work in this phase is deepening and hardening:

- **XP-06 concurrency** — LangGraph parallel branches allow AP Implementer and RE Framer to run simultaneously. LlamaIndex handles concurrent reads; a write-coordination layer (Redis or SQLite WAL) handles concurrent atom updates.[^4]
- **XP-05 scale** — LlamaIndex with Qdrant or Weaviate as the vector backend replaces the initial in-memory or SQLite store as the atom count grows past 1,000+.
- **AP-03, AP-05, RE-02, RE-07** — domain-specific agents for supply chain, milestone tracking, property lifecycle, and report generation are added as new nodes in the LangGraph, reading from the LlamaIndex know layer.
- **PK-08 ubiquitous access** — a thin API wrapper around the nowu-cli enables mobile/voice capture that feeds the LlamaIndex ingestion pipeline asynchronously.

**Haystack entry point (v2):** When nowu is ready to ship as a product, Haystack provides the production deployment harness — Kubernetes-ready pipelines, multi-user request handling, visual pipeline editor for observability, enterprise RAG at scale. The LangGraph + LlamaIndex core can be wrapped as Haystack components without rewriting the agent logic. This is the appropriate moment to adopt Haystack — not earlier.[^16]

**Multi-user (XP-09, XP-10):** The v2 multi-user architecture requires the `know` module to support per-user knowledge isolation with cross-user sharing rules. This is a custom data governance layer on top of LlamaIndex — no existing framework provides it out of the box.

***
## 6. The "Build vs. Adopt" Question — Resolved
> *"Should we build everything ourselves with AI agents?"*

The answer is a three-part resolution:

**Build custom for:** the workflow logic (S0–S9 orchestration), the artifact schemas, the knowledge atom data model, the confidence/provenance/decay system, the tiered approval classifier, and the project isolation/cross-project discovery rules. These are the things that make nowu *nowu* — they are the product, not the infrastructure.

**Adopt frameworks for:** the things that are genuinely infrastructure-level and framework-neutral. LangGraph for stateful graph execution and human-in-loop checkpointing; PydanticAI for type-safe agent outputs; LlamaIndex for document ingestion and semantic retrieval; Atomic Agents for swappable tool components. These are solved problems — building them from scratch is not differentiation, it is overhead.[^2][^5][^10][^14][^17][^18]

**The 85% finding is important but not deterministic:** A survey of production agent teams found 85% build custom rather than using frameworks. But these teams are building agents for customer-facing products (chatbots, support agents, search systems) — their requirements for performance, predictability, and deployment scale differ from nowu's. nowu's primary requirement is continuity and compound learning across sessions, not sub-200ms response time or 1,000 concurrent users. The 85% finding should prompt caution about framework coupling, not a blanket rejection of frameworks.[^1]

**The guiding test:** At any given phase, if a framework requirement is forcing you to write code that serves the framework rather than the product, that is the signal to step back to a thinner abstraction. nowu eats its own dog food — if the framework is creating overhead that contradicts "if it feels like bureaucracy, we built it wrong," it is the wrong framework for that phase.

***
## 7. How to Replace / Migrate Agent Steps
The migration from prompt-based orchestration to programmatic orchestration follows the strangler fig pattern, applied at the step level:[^11][^12]

| Step | Current | v1 Target | v1.1 Target |
|---|---|---|---|
| S0 Resume | Human reads SESSION-STATE.md | `nowu status <project>` CLI command | LangGraph thread checkpointer |
| S1 Intake | Human loads nowu-intake.md, runs chat | `nowu run <project> intake` | LangGraph S1 node + interrupt |
| S2 Discovery | Human loads nowu-discovery.md | `nowu run <project> discovery` | LangGraph S2 node + LlamaIndex |
| S3 Options | Human loads nowu-options.md | `nowu run <project> options` | LangGraph S3 node + NF-13 debate |
| S4 Decision | Human approval + nowu-decider.md | YAML approval queue → auto-load | LangGraph interrupt + ADR write |
| S5 Shaping | Human loads nowu-shaper.md | `nowu run <project> shape` | LangGraph S5 + PydanticAI TaskSpec |
| S6 Implement | Human triggers implementer | `nowu run <project> implement` | LangGraph parallel branches |
| S7 VBR | Human triggers verifier | `nowu run <project> verify` | LangGraph S7 + sandbox test runner |
| S8 Review | Human loads nowu-reviewer.md | Batch review queue | LangGraph interrupt + ADR check |
| S9 Curator | Human loads nowu-curator.md | `nowu run <project> curate` | LangGraph S9 + LangMem procedural |

**Transition rule:** A step is only migrated when its artifact schema has been stable for two full cycles. Migrating a step whose schema is still evolving creates graph nodes that must be rewritten — this is the most common source of framework regret.

***
## 8. Guo et al. — What the Survey Says for nowu
The Guo et al. 2025 survey of LLM-empowered agentic software engineering synthesises findings from across the SWE-bench era. The key implications for nowu's architecture:

**Planning quality is the primary differentiator.** Agents that decompose tasks explicitly into bounded sub-tasks significantly outperform agents given broad objectives. nowu's S5 Shaping step (task specs with explicit `in_scope_files` and `acceptance_criteria`) is the correct architectural response — this is what nowu's design already does, and it should be preserved through any framework migration.

**Memory architecture drives long-run quality.** The survey identifies three memory types as critical: episodic (what happened in past sessions), semantic (world knowledge and facts), and procedural (how to perform tasks). nowu's NF-06 learning loop, XP-01 cross-project knowledge, and the `know` module map directly to these three memory types. The framework choice for the `know` module matters as much as the framework choice for the `flow` module — arguably more so for nowu's long-term value proposition.

**Multi-agent > single-agent for complex, multi-step tasks.** Specialised agents with constrained altitudes (Discovery does not touch Architecture; Architecture does not write code) consistently outperform single general-purpose agents given the same resources. nowu's altitude discipline is architecturally validated by the empirical literature.

**Human-in-the-loop improves reliability disproportionately.** Introducing human checkpoints at key decision points (not at every step) improves correctness more than doubling the compute budget on autonomous runs. nowu's tiered approval model (NF-05) is not a concession to manual overhead — it is a reliability architecture. The T3 gate before production merges is the single most impactful intervention available.

**Context management is more important than context size.** Agents with curated, step-specific context outperform agents with access to full project history. nowu's "scope ruthlessly" principle (Principle 2) and `in_scope_files` constraint in task specs are direct implementations of this finding. When migrating to LangGraph, ensure that each node receives only the context relevant to its altitude — not the full thread history.

***
## 9. Decision Summary
| Question | Answer | When | Why |
|---|---|---|---|
| Should nowu build custom orchestration or adopt a framework? | **Custom first, then selective adoption** | Phased | Workflow must stabilise before it can be formalised as a graph |
| When to introduce programmatic orchestration? | **v1 (Month 4–6)** | When 3+ concurrent projects make manual step-routing painful | The pain must be real before the solution is worth its overhead |
| Which framework for flow orchestration? | **LangGraph** | **v1.1 (Month 7–12)** | Best stateful graph, human-in-loop, cyclic support, LangMem integration |
| Which framework for agent nodes? | **PydanticAI** | **v1 (start with typed agents)** | Type-safe artifact schema enforcement, fast, composable |
| Which framework for know module? | **LlamaIndex** | **v1.1 (when ingestion is needed)** | Best RAG pipeline, memory types, cross-project semantic search |
| Which framework for agent components/tools? | **Atomic Agents** | **v1.1 (as tools are extracted)** | Swappable, atomic components, schema-aligned |
| Which framework for v2 deployment? | **Haystack** | **v2 (Month 13–24)** | Production deployment, multi-user, Kubernetes-ready |
| Should conversations (AI-AI, human-AI) be used? | **Yes, freely within steps** | All phases | Conversations are the working medium; artifacts are the durable record |
| When to fully replace the prompt-based system? | **Never replace — evolve** | Continuous | SKILL.md prompts remain the agent definition; the shell triggers them programmatically |

***
## 10. Specific Risks to Monitor
**Premature formalisation risk:** If you introduce LangGraph at v1-core before the workflow is stable, graph nodes will be rewritten every cycle. The cost of the rewrite is not just code — it is the time spent explaining graph changes to AI agents instead of building nowu features. **Watch for this signal:** if more than 20% of any week's work is modifying framework plumbing rather than workflow logic, the framework was adopted too early.

**Framework ceiling risk (CrewAI):** The v1-core prototyping stage sometimes tempts adoption of CrewAI for its fast setup. Based on documented experience, CrewAI hits a ceiling at 6–12 months when non-linear flows, custom gating, or knowledge graph requirements emerge — exactly the capabilities nowu requires for v1.1. If CrewAI is adopted for v1-core speed, budget a migration to LangGraph by Month 6. It is worth noting here: the prior report recommended CrewAI for rapid prototyping; given the current state (prompt-based system already working), there is no reason to introduce CrewAI at all. The prompt-based system is already beyond what CrewAI would deliver, at zero framework overhead.[^19]

**LangGraph ecosystem coupling risk:** LangChain/LangGraph has historically had API instability between minor versions. Pin versions explicitly. Use LangGraph's stable public API surface (StateGraph, interrupt, checkpointer) rather than internal utilities that may change.

**Knowledge graph underinvestment risk:** The greatest long-term risk to nowu is not choosing the wrong orchestration framework — it is underinvesting in the `know` module. The atomic knowledge model (every fact with source, confidence, relationships, decay) is the core differentiator of nowu vs. a generic agentic framework. LlamaIndex provides the infrastructure; the schema design and confidence-grading logic must be custom, well-designed, and built before v1.1. This is where nowu should concentrate its most careful design work.

**The clarification on Principle 0** — that conversations are acceptable as the working medium — is correct and important. The original strict interpretation creates unnecessary friction for exploratory and discovery work (NF-12, S3 option generation, S4 debates). What must never be relaxed is the requirement that each step produces an artifact at its gate point. The conversation is the workshop; the artifact is the deliverable that exits the workshop.

---

## References

1. [Measuring Agents in Production - arXiv](https://arxiv.org/html/2512.04123v1) - The survey covers system architecture, evaluation, deployment, and operational challenges through 47...

2. [LangChain vs. LangGraph: Great Orchestration Debate](https://atalupadhyay.wordpress.com/2026/02/25/langchain-vs-langgraph-great-orchestration-debate/) - An Agent is an LLM that has access to Tools. Instead of following a pre-defined chain, the Agent loo...

3. [Top 10 AI Agent Frameworks 2026: Complete Comparison](https://www.braincuber.com/blog/top-10-ai-frameworks-building-agents-2026-comparison) - Compare the top 10 AI agent frameworks in 2026. LangChain, CrewAI, AutoGen, LangGraph, and more. Rea...

4. [A Detailed Comparison of Top 6 AI Agent Frameworks in 2026 - Turing](https://www.turing.com/resources/ai-agent-frameworks) - AutoGen treats workflows as multi-agent conversations, while LangGraph models them as graphs with no...

5. [LangChain vs LangGraph: Which AI Agent Framework Wins in 2026?](https://www.folio3.ai/blog/langchain-vs-langgraph-ai-agent-framework) - Compare LangChain vs LangGraph for building AI agents. Learn key differences, use cases, architectur...

6. [LangChain Review 2026: Complete Framework Test & Real Results](https://hackceleration.com/langchain-review/) - (56)

7. [Best AI Agent Memory Frameworks 2026: Mem0, Zep, LangChain ...](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/) - Compare the 8 best AI agent memory frameworks in 2026 — Mem0, Zep, LangChain, Letta, and more. Archi...

8. [The Best Open Source Frameworks For Building AI Agents in 2026](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks) - Discover the top seven open source frameworks for building powerful AI agents with advanced reasonin...

9. [LangChain, LangGraph, or Custom? Choosing the Right Agentic ...](https://www.turgon.ai/post/langchain-langgraph-or-custom-choosing-the-right-agentic-framework) - CTO-level comparison of LangChain, LangGraph, and custom agent frameworks. Learn when to use each fo...

10. [Pydantic AI: Build Type-Safe LLM Agents in Python](https://realpython.com/pydantic-ai/) - Pydantic AI is a Python framework for building LLM agents that return validated, structured outputs ...

11. [Strangler Fig Pattern and Legacy System Migration Methods](https://www.altexsoft.com/blog/strangler-fig-legacy-system-migration/) - The strangler fig pattern is a method used to gradually replace a legacy system with a new one witho...

12. [The Strangler Fig Pattern | Enterprise UI - Steve Kinney](https://stevekinney.com/courses/enterprise-ui/strangler-fig-introduction) - In practice, Strangler Fig works best when business boundaries, code boundaries, deployment boundari...

13. [The 6 Best AI Agent Memory Frameworks You Should Try in 2026](https://machinelearningmastery.com/the-6-best-ai-agent-memory-frameworks-you-should-try-in-2026/) - LlamaIndex provides memory capabilities integrated with its data framework. This makes it particular...

14. [BrainBlend-AI/atomic-agents - GitHub](https://github.com/BrainBlend-AI/atomic-agents) - The Atomic Agents framework is designed around the concept of atomicity to be an extremely lightweig...

15. [What is the Atomic Agents Multi-Agent AI Framework? - Generative AI](https://generativeai.pub/an-in-depth-introduction-to-the-atomic-agents-multi-agent-ai-framework-b621f14df454) - Introducing Atomic Agents: A New Framework for Building Agentic AI with Modular Design · Before we s...

16. [Haystack Review 2026 | AI Infrastructure & MLOps Tool - AI Agents List](https://aiagentslist.com/agents/haystack) - Haystack's agentic AI framework allows developers to build sophisticated agent pipelines with functi...

17. [Agent Workflows: Multi-Step Orchestration for end-to-end automation](https://www.llamaindex.ai/workflows) - Master agent workflows to orchestrate GenAI apps. Create multi-step, async, and event-driven systems...

18. [Improved Long & Short-Term Memory for LlamaIndex Agents](https://www.llamaindex.ai/blog/improved-long-and-short-term-memory-for-llamaindex-agents) - In this article, we will walk through some of the core features of the new LlamaIndex memory compone...

19. [AI Agent Framework Comparison 2026: LangGraph vs CrewAI vs ...](https://www.stencilwash.com/blog/ai-agent-framework-comparison-2026) - Teams start with CrewAI, move fast, ship features. Then requirements grow. They need custom orchestr...

