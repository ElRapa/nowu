# AI Coding Agent Systems & Agentic Frameworks — nowu Guide (v2)

> **Scope:** This report evaluates both (A) coding-agent shells — the tools you *use day-to-day* to build nowu — and (B) Python agentic orchestration frameworks — the potential *runtime engine inside* nowu. Every evaluation is anchored to nowu's vision: a continuity-layer for the multi-project human, with a durable atomic knowledge graph, gated 9-step workflow, cross-session memory, and a 24-month trajectory toward infrastructure status.

***

## nowu's Critical Requirements (from Vision v2.0 + USE_CASES v2.3)

Before comparing anything, it is important to derive a requirements matrix from nowu's actual documents. The frameworks are only useful insofar as they serve these needs.

| Requirement | Source UC | Why it matters |
|---|---|---|
| **Artifact-as-API** — agents talk through files, not conversations | Principle 0 | Silent conversation failures vs. visible artifact failures |
| **Cross-session continuity** — pick up from last verified checkpoint | NF-01, NF-10 | Core value proposition: "project that compounds vs. resets" |
| **Gated approvals** — tiered human-in-loop without full blocking | NF-05 | T1 auto-proceed, T2 batch, T3 halt |
| **Altitude discipline** — discovery ≠ architecture ≠ implementation | NF-03, NF-04 | Agents must not bleed across layers |
| **Atomic knowledge graph** — every fact has source, confidence, relationships | PK-01 to PK-09, XP-01 | Memory infrastructure across all projects |
| **Multi-project isolation + cross-project discovery** | XP-01, NF-07 | nowu must simultaneously isolate AP/RE/NF projects and connect them semantically |
| **Non-software domain support** | AP-01, RE-01 | Regulatory, supply chain, real estate — not just code |
| **Session-to-session learning** — lessons feed back into prompts | NF-06 | "Using nowu improves nowu" |
| **LiteLLM model routing** | Your stack | Claude Sonnet/Opus 4.x, GPT-5.1/5.2, o3 all in play |
| **Provider-agnostic, open formats** | Principle: not a walled garden | Portable artifacts, no vendor capture |

***

## Part A — Coding Agent Shells (Build Tools)

*These are the tools you open a terminal or IDE and use to write and evolve nowu itself. Evaluation focuses on how well they fit nowu's artifact-first, SKILL.md-loading, gated-step workflow.*

### Comparison Matrix

| Tool | SKILL.md / Custom Instructions | Hooks / Pre-step | Multi-agent / Parallel | LiteLLM / Custom Model | File-based State | Non-code Projects | Cost & Auth for Your Stack |
|---|---|---|---|---|---|---|---|
| **Claude Code** | ✅ Native `.claude/skills/` | ✅ `tool.execute.before` hooks | ✅ via sub-agents | ⚠️ API key only (no subscription routing) | ✅ Native | ✅ Works anywhere | Anthropic API credits |
| **OpenCode** | ✅ `.opencode/skills/`, `.claude/skills/` compatible | ✅ Hooks system | ✅ Primary + subagents | ✅ LiteLLM provider built in | ✅ Native | ✅ Works anywhere | GitHub Copilot Enterprise auth supported |
| **oh-my-claudecode (OMC)** | ✅ 32+ agents, execution modes | ✅ Autopilot/Swarm modes | ✅ tmux parallel workers | ❌ Claude-only | ✅ via CLAUDE.md | ✅ | Claude subscription / API |
| **oh-my-codex (OmX)** | ✅ Forked from OMC for Codex CLI | ✅ | ✅ Multi-agent teams via tmux | GPT/Codex only | ✅ | ✅ | OpenAI API |
| **Codex CLI App** | ⚠️ AGENTS.md only | ⚠️ Limited | ⚠️ Parallel via worktrees | ✅ GPT-5.x native | ✅ | ✅ | OpenAI account |
| **Aider** | ⚠️ `.aider.conf.yml` | ❌ No hooks | ❌ Single agent | ✅ LiteLLM | ✅ Git-native | ⚠️ Code only | Any provider |
| **Cline / Roo Code** | ✅ `.clinerules`, custom modes | ⚠️ Limited | ✅ Roo: parallel tasks | ✅ LiteLLM | ✅ | ⚠️ IDE-bound | Any provider |
| **MetaGPT** | ✅ SOP-defined roles | ✅ SOP pipeline | ✅ Software company roles | ✅ LiteLLM | ✅ | ❌ Software only | Any provider |
| **GitHub Copilot Workspace** | ⚠️ Plans only | ❌ | ❌ Single-agent | ✅ Copilot Enterprise | ❌ Browser | ⚠️ | ✅ Your subscription |

### oh-my-claudecode / oh-my-codex in Detail

**oh-my-claudecode (OMC)** is the most feature-complete overlay for Claude Code. It ships 32+ specialised agents — including Sisyphus (orchestration), Prometheus (planning), Atlas (implementation), and Librarian (research) — and five execution modes including Autopilot and Swarm. Agents detect your model family at runtime and switch prompts accordingly (Claude gets full mechanics; GPT gets a compact principle-driven version). The tmux-based parallel execution is a genuine capability for running S6 implementation agents concurrently. The hard constraint: it is Claude-only, which matters less when Claude Sonnet 4.6 is already your primary model.

**oh-my-codex (OmX)** is a fork of OMC explicitly for Codex CLI, announced February 2026 as "same multi-agent orchestration, now for Codex CLI". It inherits the `$ralph`, `$deep-interview`, `$ralplan`, and `$team` skill vocabulary from OMC, adding structured persistent state management for session resumption — highly relevant to NF-01. OmX operates as a workflow harness that wraps Codex as an execution engine, adding guardrails, structured clarification phases, and team spawning rather than replacing the underlying model. With 12,000+ stars shortly after launch, active development is confirmed.

**Recommendation for building nowu (2026 stack):** OpenCode as primary shell (LiteLLM + Copilot Enterprise + Claude-compatible SKILL.md), with OMC for intensive Claude-centric sessions requiring Swarm-mode parallelism. OmX is worth adopting if you want Codex CLI as an implementation worker in your agent team.

***

## Part B — Agentic Orchestration Frameworks (Runtime Engine)

*These are Python (or TypeScript) libraries that could power nowu's internal `flow` orchestration module — the engine that runs S1–S9, manages state, enforces gates, and accumulates the knowledge graph. This is a build decision, not a use decision.*

### The Two-Dimension Clarification

Most evaluations of these frameworks treat them as alternatives. For nowu, the distinction is:

- **Coding shells** (Part A) = what you run to write the nowu codebase
- **Orchestration frameworks** (Part B) = what the nowu codebase *uses internally* to run its pipeline

These are orthogonal choices. You can write nowu using OpenCode while its internal orchestration is powered by LangGraph.

***

### Framework Deep Dives

#### LangGraph

LangGraph won the "stateful, multi-step workflow" market segment in 2026. Its graph model — nodes are Python functions, edges are conditional transitions — maps naturally to nowu's S1–S9 pipeline, where each step is a named state with explicit entry/exit conditions. The checkpointer serialises the full graph state per thread ID, enabling exact-point resumption across sessions — which directly satisfies NF-01.

Human-in-the-loop is a first-class primitive: nodes can pause, await approval, and resume without losing state. This covers NF-05's tiered approval model. The **LangMem SDK** (built on LangGraph's persistent StateGraph store) supports three memory types: episodic (past interactions), semantic (world facts), and — uniquely — *procedural memory*, where agents update their own system-prompt instructions from accumulated feedback. That procedural layer directly enables NF-06 ("learn from past mistakes") without custom plumbing.

**Strengths for nowu:** NF-01 (resumption), NF-02 (ADR enforcement as a graph node), NF-05 (human gates), NF-06 (procedural memory), XP-01 (cross-project discovery with Mem0/cognee semantic layer)

**Weaknesses:** Verbose boilerplate; tightly coupled to LangChain ecosystem; medium setup time (~150ms vs PydanticAI's ~50ms); graph state is memory-heavy at scale

**Best fit for nowu:** `flow` orchestration module (S1–S9 as a StateGraph), persistent session state, and the knowledge-atom retrieval layer once XP-01 is in scope.

***

#### CrewAI

CrewAI uses a "team of specialists" metaphor: agents are defined with role, goal, backstory, and allowed tools, then combined into crews with sequential or hierarchical task execution. LiteLLM integration is native, enabling routing across your full model stack. Its long-term memory uses ChromaDB for persistence across runs.

The 6–12 month ceiling is well-documented: teams start fast but hit constraints when needing non-linear flows, dynamic agent spawning, or custom orchestration patterns — at which point a rewrite typically begins. For nowu's S1–S9 gated pipeline with conditional S4 retries and S8 validation loops, that ceiling would likely arrive around v1.1.

**Strengths for nowu:** Fastest path to a working P0-S9 crew; LiteLLM works out of the box; good for v1-core prototyping; role abstraction aligns with nowu's altitude discipline concept

**Weaknesses:** Opinionated design limits custom gating; not suitable for the knowledge graph layer; long-term memory is ChromaDB-only (no semantic knowledge graph); hits walls with non-linear flows

**Best fit for nowu:** Rapid v1-core prototyping of the S1–S9 agent crew. Not a long-term foundation for v1.1+ features requiring atomic knowledge and cross-project semantic memory.

***

#### AutoGen / Microsoft Agent Framework

Microsoft consolidated AutoGen and Semantic Kernel into **Microsoft Agent Framework**, released in public preview October 2025 with GA targeted for Q1 2026. AutoGen won the "multi-agent collaboration" segment — scenarios where agents debate, critique, or parallelise work. The framework inherits Semantic Kernel's thread-based state management, built-in A2A protocol support, and MCP integration. AutoGen's `human_input_mode=ALWAYS` provides human-in-loop for every turn; `TERMINATE` allows fully autonomous runs.

For nowu, the conversation-driven model is the core tension. Principle 0 states "artifacts are the API — broken conversations fail silently and leave nothing behind." AutoGen/Agent Framework's conversation-passing model can produce this exact failure mode if agents don't also write durable artifacts at every step. The framework is more appropriate if nowu were to implement a cross-agent debate pattern (e.g., multiple options for NF-13) rather than the core step-gated pipeline.

**Strengths for nowu:** NF-13 (multi-option debate), multi-agent collaboration with specialised critics, MCP and A2A protocol support for future interop, enterprise reliability from Semantic Kernel foundations

**Weaknesses:** C#-native heritage; conversation-driven (conflicts with Principle 0); Python SDK less mature; overhead for nowu's structured pipeline

**Best fit for nowu:** Option-generation debate nodes within LangGraph (called from an Agent Framework sub-process), or later when XP-09/XP-10 requires enterprise multi-user workflows.

***

#### PydanticAI

PydanticAI is a Python-first, type-safe agent framework where all inputs, outputs, and tool parameters are validated using Pydantic models. It is significantly lighter than LangGraph (~50ms setup vs ~150ms) and excels at structured output tasks. Human-in-the-loop tool approval is a first-class feature — specific tool calls can be flagged for approval based on arguments, conversation history, or user preferences. It supports MCP and A2A protocols natively.

For nowu, PydanticAI is the ideal choice for individual agent nodes rather than the orchestration layer. An NF-04 Quality Agent that validates task output against typed acceptance criteria schemas, or a PK-09 Research Agent that returns structured `KnowledgeAtom` objects, benefits directly from PydanticAI's type safety. The multi-agent gap is real — it does not have built-in role-based delegation or agent handoffs — but this is solved by composing PydanticAI agents as nodes within a LangGraph flow.

**Strengths for nowu:** Type-safe knowledge atom construction, structured output for all S1–S9 artifacts, faster execution per step, cleaner developer experience for Python-familiar teams

**Weaknesses:** No built-in multi-agent orchestration; no role-based delegation; not designed for complex graph flows

**Best fit for nowu:** Individual agent implementations (discovery agent, quality agent, research agent, curator) called as nodes within a LangGraph StateGraph. **PydanticAI + LangGraph is the strongest combination for nowu.**

***

#### Atomic Agents

Atomic Agents is built on the LEGO metaphor: every component (agent, tool, context provider) is single-purpose, reusable, composable, and predictable. Each agent has explicit input/output Pydantic schemas, and chaining is done by aligning those schemas — swapping one search tool for another requires no other code changes. It is built on Instructor for provider-agnostic LLM calls, making it compatible with any provider via OpenAI-compatible API (including your LiteLLM endpoint).

The philosophy aligns strongly with nowu's "right role, right task" principle and altitude discipline. Where it differs from PydanticAI is in its explicit atomicity constraint: every component is designed to be independently replaceable, which matches nowu's vision of swappable agents at each step. However, Atomic Agents lacks the stateful graph orchestration of LangGraph — it is a component library, not an orchestrator.

**Strengths for nowu:** Modular component design aligns with S1–S9 altitude discipline; easy agent replacement without pipeline refactoring; schema-first design for artifact-as-API; lightweight

**Weaknesses:** No built-in state persistence; no human-in-loop checkpointing; needs an orchestration layer on top (could be LangGraph)

**Best fit for nowu:** Agent component library for individual steps, composable with LangGraph orchestration. Especially good for the knowledge-atom tools in the PK layer.

***

#### MetaGPT

MetaGPT simulates a full software company: Product Manager, Architect, Project Manager, Engineer, and QA Engineer roles collaborate via SOPs and an assembly-line paradigm. Given one-line requirements, it outputs PRDs, data structures, APIs, tests, and code. It achieves 85.9% on HumanEval. LiteLLM is supported.

For nowu, MetaGPT is simultaneously the most and least relevant framework. It is the most relevant conceptually — its SOP-enforced role separation and artifact-producing assembly line is exactly the pattern nowu is trying to generalise beyond software. It is the least relevant practically — it is hardwired to software development roles and has no mechanism for non-software domains like AP (food business) or RE (real estate). The knowledge graph, cross-session memory, and atomic knowledge atom layers are absent. MetaGPT's architecture is best understood as a specific nowu configuration for the software domain — not a foundation for the full multi-domain system.

**Strengths for nowu:** Reference architecture for SOP-driven multi-role agent collaboration; good inspiration for NF-03 scoping and NF-04 quality agents

**Weaknesses:** Hardwired to software development; no cross-session knowledge graph; no human approval gates; no multi-domain support; architecture is not extensible to AP/RE/PK project types

**Best fit for nowu:** Study as a reference for the NF software pipeline; not a runtime dependency.

***

#### LlamaIndex

LlamaIndex is a developer-first agent framework built around RAG (Retrieval-Augmented Generation), structured data pipelines, and event-driven workflows. Its **Workflows** abstraction enables multi-step, async, event-driven pipelines that can launch, pause, and resume statefully. The memory system supports short-term (token-limited chat buffer), long-term (vector stores like Qdrant/Weaviate), and vector memory blocks that flush to semantic search when the token limit is reached.

For nowu, LlamaIndex is the most compelling choice for the **knowledge atom layer** (PK group use cases). When Raphael ingests a food regulation document (PK-07), asks a domain-specific question (PK-09), or surfaces connections across projects (XP-01), those are RAG + semantic search tasks — exactly LlamaIndex's strength. It is not the right choice for the S1–S9 orchestration pipeline (LangGraph is stronger there), but as the knowledge infrastructure layer, it is purpose-built.

**Strengths for nowu:** PK-07 (document ingestion), PK-09 (domain expertise on demand), XP-01 (cross-project discovery), XP-11 (knowledge graph in role-appropriate format), best-in-class long-term memory management

**Weaknesses:** Not a workflow orchestrator; less suited to the S1–S9 procedural pipeline; different ecosystem from LangGraph (though compatible)

**Best fit for nowu:** Knowledge infrastructure layer — the `know` module. Use alongside LangGraph for orchestration and PydanticAI for individual agent nodes.

***

#### Haystack (deepset)

Haystack is a production-ready, component-based AI pipeline framework with a visual editor, multimodal support, cloud-agnostic Kubernetes-ready pipelines, and enterprise support. Its agent model composes Chat Generators, Tool classes, and ToolInvoker components in a Pipeline. Multi-agent orchestration is supported by wrapping an agent as a ComponentTool of another agent.

Haystack's primary strength is enterprise RAG and NLP pipeline deployment — it is the most production-hardened framework for taking a prototype to a scalable service. For nowu v2 ("infrastructure, not just a tool"), Haystack becomes relevant. For nowu v1-core, it introduces too much enterprise overhead and diverges from nowu's current Python-first, Git-native, local-first architecture.

**Strengths for nowu:** XP-05 (scale without degrading performance), XP-09/XP-10 (multi-user, company-operating-system), visual pipeline editor for observability, Kubernetes-ready

**Weaknesses:** Over-engineered for solo/small-team v1; enterprise overhead; not LangChain-ecosystem compatible; steeper learning curve than alternatives

**Best fit for nowu:** v2 deployment layer when nowu ships as a service or installable product.

***

### oh-my-opencode Specialised Agents

The **Oh My Opencode** harness (separate from OmX) packages OpenCode with 11 specialised agents — Sisyphus (orchestration), Prometheus (planning), Atlas (implementation), Librarian (research), and others — using LSP + AST-Grep for IDE-quality refactoring and a Hashline edit tool that eliminates stale-line errors. Built-in MCPs include Exa (web search), Context7 (official docs), and Grep.app. Agents auto-detect your model family (Claude vs GPT) and switch prompts accordingly. This is the closest third-party approximation of nowu's own specialised-agent vision, and serves as both a build tool and an architectural reference for how to assign prompts to model families.

***

## Part C — Synthesis: Recommended Architecture for nowu

### The Two Roles Are Orthogonal

| Role | Recommendation | Reasoning |
|---|---|---|
| **Day-to-day build tool** | OpenCode (primary) + OMC (intensive Claude sessions) | LiteLLM routing, SKILL.md compatible, Copilot Enterprise auth, no model lock-in |
| **S1–S9 pipeline orchestration** | **LangGraph StateGraph** | Stateful graph, human gates, procedural memory via LangMem, replay/audit |
| **Individual agent implementations** | **PydanticAI** as nodes inside LangGraph | Type-safe artifact construction, structured knowledge atoms, clean Python |
| **Knowledge graph / `know` module** | **LlamaIndex** | RAG, document ingestion, cross-project semantic search, best memory management |
| **Agent component library** | **Atomic Agents** | Swappable tool/agent components for each S-step |
| **Multi-option debate (NF-13)** | AutoGen / Agent Framework | Structured debate pattern for decision-point option generation |
| **v2 scalable deployment** | Haystack | When nowu ships as multi-user infrastructure |

### The Three-Layer Stack

```
┌──────────────────────────────────────────────────────────────────────────┐
│  BUILD LAYER (shells)                                                     │
│  OpenCode / OMC  →  write nowu code, load SKILL.md, invoke sub-agents   │
└──────────────────────────────────────────────────────────────────────────┘
             ↓  produces / modifies
┌──────────────────────────────────────────────────────────────────────────┐
│  FLOW LAYER (LangGraph StateGraph)                                       │
│  P0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 → S9                     │
│  Each node = a PydanticAI agent producing a typed artifact               │
│  Human gates = LangGraph checkpoints awaiting approval                   │
│  Session state = persisted via thread_id checkpointer                    │
└──────────────────────────────────────────────────────────────────────────┘
             ↓  reads/writes
┌──────────────────────────────────────────────────────────────────────────┐
│  KNOW LAYER (LlamaIndex + Atomic Agents tools)                           │
│  Episodic memory (what happened) → session logs, decisions               │
│  Semantic memory (world facts)   → knowledge atoms, regulatory data      │
│  Procedural memory (how-to)      → SOPs, lessons, skill improvements     │
│  Cross-project discovery         → vector store + graph relationships    │
└──────────────────────────────────────────────────────────────────────────┘
```

### Use Case Coverage by Framework

| Use Case | Primary Framework | Supporting Framework |
|---|---|---|
| NF-01 Resume after context loss | LangGraph checkpointer | Session-STATE.md artifact |
| NF-02 Enforce architectural decisions | PydanticAI (typed ADR schema) + LangGraph gate | — |
| NF-03 Scope without creep | PydanticAI (TaskSpec schema) | Atomic Agents (scoping tool) |
| NF-04 Self-assess quality | PydanticAI (QualityReport schema) | LangGraph (VBR node) |
| NF-05 Route approvals | LangGraph (interrupt/checkpoint) | — |
| NF-06 Learn across sessions | LangMem procedural memory | LlamaIndex (episodic capture) |
| NF-07 Bootstrap new project | LangGraph (project init flow) | — |
| NF-10 Maintain thread | LangGraph thread state | LlamaIndex session summary |
| NF-12 Explore vague idea | PydanticAI (framer agent) | — |
| NF-13 Generate multiple options | AutoGen debate pattern | LangGraph conditional branch |
| PK-01 Fast capture | LlamaIndex (quick ingest) | Atomic Agents (capture tool) |
| PK-07 Ingest documents | LlamaIndex RAG pipeline | — |
| PK-09 Domain expertise on demand | LlamaIndex + web search tool | PydanticAI (structured result) |
| XP-01 Cross-project discovery | LlamaIndex (semantic search + graph) | LangGraph (trigger node) |
| XP-06 Multi-agent concurrency | LangGraph (parallel branches) | CrewAI (if early-stage only) |
| AP-01 Track regulatory requirements | LlamaIndex (living knowledge) | PydanticAI (confidence-graded atom) |

***

## Part D — Evaluation Table

| Framework | Best fit for nowu | When to use | Avoid when | LiteLLM? |
|---|---|---|---|---|
| **LangGraph** | `flow` orchestration | S1–S9 pipeline, human gates, session resumption | You need a fast prototype without graph complexity | ✅ |
| **PydanticAI** | Individual agent nodes | Type-safe artifact generation, structured output | You need full multi-agent orchestration | ✅ |
| **LlamaIndex** | `know` module | RAG, document ingestion, cross-project discovery | You only need the S1–S9 flow (no knowledge layer) | ✅ |
| **Atomic Agents** | Tool/agent components | Swappable components per step, atomicity | You need stateful orchestration across steps | ✅ |
| **CrewAI** | v1-core prototyping | Fastest multi-agent crew to production | You need non-linear flows or a knowledge graph | ✅ |
| **AutoGen / MS Agent Framework** | NF-13 debate nodes | Multi-agent option generation, enterprise A2A | Core pipeline orchestration | ✅ |
| **MetaGPT** | Reference only | Studying SOP-driven software agents | Non-software domains (AP, RE, PK) | ✅ |
| **Haystack** | v2 deployment | Multi-user scaled deployment as a service | Solo v1-core development | ✅ |
| **oh-my-codex (OmX)** | Build tool (coding shell) | Codex CLI team orchestration | You need Claude as primary model | OpenAI only |
| **oh-my-claudecode (OMC)** | Build tool (coding shell) | Claude-heavy parallel sessions, Swarm mode | You need model diversity in build tool | Claude only |
| **OpenCode** | Build tool (primary) | All sessions — provider-agnostic, SKILL.md, Copilot Enterprise | — | ✅ |

***

## Part E — Strategic Considerations

### Why CrewAI is not the long-term foundation

nowu's v1.2 milestone requires active projects in software, food business, and real estate — all with a shared, queryable knowledge base. CrewAI's memory layer is ChromaDB-backed (semantic similarity) but has no knowledge graph with explicit entity relationships, confidence grades, or conflict detection (XP-04). NF-06's procedural memory (lessons feed back into agent behaviour) is not supported. Building toward the 24-month "company operating system" vision on a framework with a known 6–12 month ceiling is a deliberate technical debt choice.[^1]

### Why the PydanticAI + LangGraph combination is strong

nowu's Principle 0 states "artifacts are the API." PydanticAI enforces that principle at the code level: every agent interaction produces a typed, validated output model — a `TaskSpec`, `ADRRecord`, `KnowledgeAtom`, `QualityReport`. LangGraph then routes those artifacts through the pipeline as first-class graph state, with human gates, replay capability, and persistent thread context. The combination gives nowu's architecture the type discipline it needs without sacrificing the workflow control that LangGraph provides.

### The knowledge graph is the hardest part

Neither LangGraph nor PydanticAI provides the atomic knowledge graph that nowu v1.1 requires (XP-11: "query knowledge graph in role-appropriate format"). LlamaIndex provides the best off-the-shelf foundation for this — document ingestion, entity extraction, vector search, and graph relationships — but building the full nowu `know` layer with confidence grades, provenance tracking, conflict detection (XP-04), and decay (PK-04) will require custom work on top of any framework. This is by design: nowu's vision explicitly states that the knowledge layer must be "inspectable, portable, and yours."[^1]

### On Semantic Kernel / Microsoft Agent Framework

Semantic Kernel and its successor Microsoft Agent Framework are primarily C#/.NET-oriented, with Python SDKs that lag behind in maturity. For a Python-native, Git-artifact-first system like nowu, the overhead of the Microsoft ecosystem is not justified unless you are targeting Azure enterprise deployments — relevant for XP-10 ("run a small company on nowu") but not for v1-core.

### On LangChain vs LangGraph

LangChain's founder has acknowledged that "the framework era is ending" — LlamaIndex itself is pivoting toward agent SDKs. LangGraph is the production-stable successor to the LangChain chain pattern and should be adopted directly rather than routing through LangChain abstractions. The two are compatible but using raw LangGraph avoids the LangChain deprecation risk.

***

## Appendix: Framework Release Status (April 2026)

| Framework | License | Primary Language | Stars (approx.) | Status |
|---|---|---|---|---|
| LangGraph | MIT | Python | 15,000+ | GA, actively developed |
| PydanticAI | MIT | Python | 8,000+ | GA (v0.x, stabilising) |
| CrewAI | MIT | Python | 25,000+ | GA, enterprise tier added |
| AutoGen / Agent Framework | MIT | Python / C# | 40,000+ AutoGen | Public preview (GA Q1 2026) |
| LlamaIndex | MIT | Python | 40,000+ | GA, mature |
| Haystack | Apache-2.0 | Python | 18,000+ | GA, enterprise tier |
| Atomic Agents | MIT | Python | 5,000+ | Active, stable |
| MetaGPT | MIT | Python | 48,000+ | GA |
| oh-my-claudecode | MIT | TypeScript | 10,000+ | Active |
| oh-my-codex (OmX) | MIT | TypeScript | 12,000+ | Active (Feb 2026 fork) |

---

## References

1. [vision.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/2b094027-efc2-4303-9dc6-56fa01e7c64a/vision.md?AWSAccessKeyId=ASIA2F3EMEYERBOTJ3YA&Signature=ncYFDuoSsCkeK8DVL70Zj63WD6A%3D&x-amz-security-token=IQoJb3JpZ2luX2VjECsaCXVzLWVhc3QtMSJHMEUCIQCqXCdq2TMzrHrHDKx9mbn6C83xGu3mVu%2BP2E2%2FGBmCzQIgFmyNpGrADWoHVIGfgpPScEIa2uSrPB%2FBSt%2FACZ5Zsu8q%2FAQI9P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDDuJ8GDjCTZ%2BHu%2BeZCrQBMtftXe%2BzFXgp%2FGKQiUY4DeBj7pJ%2FF9lzgPaZ0yc5IZHcq31x32Z0xC9dtSuWyBYP3bk7P%2F37suXa6wif0T6syqjo8%2BlV7iR87Lzm1Vu0F%2F9xxG9MdvpuK%2FsY5X7VdHNeRHHxK8fqv4ohGISkHyvBw5tHnSRCnmu9%2FB0bzXrhLjKnFdqpIIiqA2Pfh2gT4nfIbZBWGnFFa3oOZfhDm%2B8fMroyMmqfDNBx16tvHW5VgIKespXvFfc008pMZoyah8%2B1S5L7Oq1vP0SL%2Bm%2ByPbb17IhfNnFSNgASdQW7UJZaRrKOWQ%2FDR01SXFDe2%2B%2ByA%2B7Fb8xu4HMNvSRohgFBFWrIzEiaJzcFaYBPV1jkBcZZ001h0W0ZXBf%2BkcWcUv2ep7%2F6AEqLAUlOMsktl1PgNUdenpiRZWahtL5ik%2B2iPiwj3NZDMcNw53g%2Bv81BHxLuYMeM3s3k%2FYf7eUiJzDn6fURZNUU7meQ5rFGqqRw2%2BvUj3npdgO3Ntmwf%2BjXxRIrNP54SideLMGf3TXQDxky%2FwYo6PMJ0MLVTZh7t6n%2FXfxgPAjb2%2F2ECVf5b5qcxAYs6Q5lhoioKVZwULA7Tikva5rK0ojHjhdUCCavBFBW62IAH9U%2B%2FUul72Px9mdIqaSUGoOl5KwIvCGzsLNnIaZ6qK9FKzKe4%2F5vEmcy95%2F9vsJvS3hI5ZyTEW5v6%2FUlpbQ8iG9GVoV9xwUaF5%2BXTzSfVRS7BP%2BI2OI79%2Fo25hLhczdwi0ZUqzHILbmU1DMWp5I9UllzwlHNqD9awQDT47XUTmSY3pcw3%2FjWzgY6mAGxmlBrvo9k%2FXY1MfAWWxsC0xmCqbnaaNgH7Q3iC4jKe1wOa7onAHSM%2B4HNeO5pyp7pOat7POaw%2F43LaGSJNKrBVQh55d7t04%2BYUGeAoQrY2PvCh5ieMsaF1NfEVfxJNZ4Rg2O5JEejoCOUmxWrC0L4vAvqqzFpamjA%2BJKtsQk5%2Fsci21faF4WvzSdDcMcJJXGIZKMip4CIMQ%3D%3D&Expires=1775618610) - ---
last_updated: 2026-03-31
last_approved: 2026-03-31
status: APPROVED
version: 2.0
stage: 1
produc...

