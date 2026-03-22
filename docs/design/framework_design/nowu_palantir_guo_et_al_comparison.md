# Palantir Ontology & Guo et al. Survey: Evaluation for the nowu Framework
## Executive Summary
The nowu framework does **not** need a major overhaul. Both Palantir's Ontology architecture and the Guo et al. survey (150+ papers on agentic software engineering) validate the core design decisions already in place — multi-agent role specialization, persistent memory via `know`, WAL-based session state, approval tiers, and TDD-first development. However, they surface four concrete, adoptable improvements that would strengthen nowu without disrupting what already exists. This report maps every relevant concept from both sources onto the existing nowu architecture, flags what to adopt, and explicitly calls out what to leave alone.

***
## Source 1: Palantir's Ontology Architecture
### What It Is
Palantir's Ontology is the system at the heart of its enterprise platform. It models the complex, interconnected *decisions* of an organization — not simply data. It serves as a common interface for both humans and AI agents across all types of applications, enabling enterprises to steadily increase AI-driven automation.[^1][^2]

The Ontology integrates four primitives into a single coherent model:[^2]

| Primitive | What It Represents | Palantir Example |
|-----------|-------------------|-----------------|
| **Data** | Nouns — objects, properties, links unified from disparate sources | Flights, crew manifests, medical supplies |
| **Logic** | The reasoning behind actions — business rules, ML models, LLM functions | Scheduling optimizers, pricing models |
| **Action** | Verbs — transactions and multi-step updates written back to systems | Trigger purchase order, reallocate inventory |
| **Security** | Per-interaction permission scoping for humans and agents alike | Agent X can read orders but not approve shipments |

This fourfold model is then expressed through three conceptual layers: a **Language** (semantic objects, actions, and logic definitions), an **Engine** (the read/write infrastructure that materializes everything), and a **Toolchain** (SDKs and DevOps for building applications on top).[^2]
### What Makes It Relevant to nowu
The Ontology's core thesis is that knowledge must be paired with action to model decisions. Data objects ("nouns") must be complemented by "verbs" in order to model decisions — semantics paired with kinetics. This is directly relevant because nowu's `know` library currently stores knowledge atoms (nouns) but does not formally model what can be *done* with them (verbs).[^2]

Palantir also treats the ontology as a shared operational world between humans and AI agents. Every data integration, every piece of logic, and every feedback loop compounds into a single representation that all stakeholders interact with. nowu's `know` is already heading this direction — agents use the same `search`, `queryatoms`, and `today()` API that a human would use through CLI — but it hasn't formally declared itself as the shared operational interface.[^1][^3]

The security model is the biggest gap. Palantir enforces granular, per-action permissions at every tier — the ability to trigger a purchase order might have different permissions than the ability to run a scenario. nowu's approval tiers (Tier 1 auto, Tier 2 batch, Tier 3 blocking) are coarse by comparison.[^2]

***
## Source 2: Guo et al. Survey on Agentic Software Engineering
### What It Covers
This comprehensive survey reviews 150+ papers and proposes a taxonomy of LLM-powered software engineering along two dimensions: Solutions (prompt-based, fine-tuning-based, agent-based) and Benchmarks (code generation, translation, repair, and others). The agent-based solutions category is the most relevant to nowu, as it maps to exactly the kind of system being built.[^4]
### The Four Agent Capabilities (and How nowu Maps)
The survey identifies four core capabilities that define modern agentic SE systems:[^4]

| Capability | State of the Art | nowu Equivalent | Gap? |
|-----------|-----------------|-----------------|------|
| **Planning & Decomposition** | Multi-agent role specialization (MAGIS, AgileCoder, MASAI); staged pipelines; dynamic replanning | Framer → Shaper → Implementer → Reviewer pipeline; Shape Up-inspired scoping | **No gap.** nowu's pipeline is well-aligned with the static-pipeline approach used by MASAI and PatchPilot. Dynamic replanning could be added later. |
| **Reasoning & Self-Refinement** | Generate-test-revise loops (AutoCodeRover); human-in-the-loop (HULA, ROSE); multi-hypothesis (Nemotron-CORTEXA); formal verification (Alphaverus) | VBR protocol (verify before reporting); TDD-first; Reviewer agent | **Minor gap.** nowu lacks explicit multi-hypothesis generation (generating N candidate solutions and voting). Could add to Implementer agent. |
| **Memory Mechanisms** | Structural memory via knowledge graphs (LingmaAgent); working memory via on-demand retrieval (AutoCodeRover, BLAZE); dynamic evolving memory (EvoR); shared memory for multi-agent coordination (XpandA) | `know` library = structural long-term memory; SESSION-STATE.md = working memory; WAL protocol = context recovery | **Minor gap.** `know` doesn't yet serve as a *shared* memory for multi-agent coordination. Agents don't read/write to `know` during execution — only humans do currently. |
| **Tool Augmentation** | Agent-Computer Interfaces (SWE-agent); formal verifiers (Alphaverus); IDE integration (MarsCode); Language Server Protocol usage | Git, shell, file I/O via Copilot; planned CLI (`nowu` commands) | **No gap for v1.** Tool augmentation is inherently provided by the Copilot/VS Code environment. |
### The Scalability Challenge: "Project Amnesia"
The survey's most resonant finding for nowu is the concept of **project amnesia**: agents lose track of high-level architectural patterns, design conventions, and cross-module dependencies during extended tasks. Current mitigations like vector database retrieval fetch isolated snippets without comprehending the relationships that define a software architecture.[^4]

The recommended solution: **hierarchical cognitive architectures** that combine volatile short-term memory for immediate context with persistent long-term memory storing architectural knowledge and project conventions.[^4]

nowu already addresses this more directly than most systems in the survey — the WAL protocol + SESSION-STATE.md is the short-term working memory, `know` is the persistent long-term memory, and the `soul/` files (VISION.md, AGENTS.md) store architectural identity. The `know` library's three-layer search (exact → fuzzy → semantic) and typed connections already provide the structured representation the survey recommends.[^5][^6]
### Multi-Agent Coordination Gaps
The survey highlights that current multi-agent frameworks often rely on simple coordination mechanisms like sequential pipelines or centralized orchestration. True collective intelligence requires shared memory architectures, communication standards, conflict resolution algorithms, and role specialization that pairs complementary cognitive capabilities (e.g., a creative generator with a rigorous verifier).[^4]

nowu's Framer/Shaper/Implementer/Reviewer pipeline is sequential. This is actually *fine* for v1 — the survey notes that Agentless (a simple three-phase localization → repair → validation pipeline) can be sufficient for many tasks. But the survey flags that scaling to complex multi-project work requires richer coordination, which is where the recommended changes below come in.[^4]
### Continuous Learning and Knowledge Drift
A fundamental limitation of current LLM-based agents is their static nature — they cannot learn from new technologies, evolving best practices, or project-specific feedback after deployment. The survey recommends agents maintain versioned knowledge bases that track the evolution of APIs, best practices, and project conventions over time.[^4]

nowu's `know` curator already partially addresses this — the weekly review identifies stale atoms, risky atoms (high access but low confidence), and upgradeable atoms. But it doesn't yet handle *knowledge versioning* (tracking how an atom changed over time) or *feedback integration* (automatically learning from task outcomes).[^6][^7]
### Accountability and Audit Trails
The survey emphasizes that agents must generate verifiable audit trails explaining design rationale, cite sources for generated code, and trace decisions to specific origins. nowu's Decision Journal (ADRs) and activity logging in `know`'s SQLite database already address this. This is a validated strength.[^4][^5][^6]

***
## The Verdict: No Major Change, Four Medium Improvements
### What Is Already Right (Do Not Change)
These elements are validated by both Palantir and the survey:

- **Multi-agent role pipeline** (Framer → Shaper → Implementer → Reviewer) — matches MAGIS, AgileCoder, MASAI patterns[^4]
- **WAL protocol + SESSION-STATE.md** — directly combats "project amnesia"[^4]
- **VBR (Verify Before Reporting)** — matches the generate-test-revise self-refinement pattern[^4]
- **`know` as persistent knowledge layer** — JSON truth + SQLite index is structurally sound; three-layer search matches hierarchical cognitive architecture recommendations[^5][^6]
- **Decision Journal (ADRs)** — matches audit trail and provenance tracking requirements[^2][^4]
- **Approval tiers** — matches human-in-the-loop refinement pattern (HULA, ROSE)[^4]
- **TDD-first development** — validated as the most effective prompting paradigm for code generation[^4]
- **Epistemic grades on knowledge** — no equivalent exists in any surveyed framework; this is a genuine differentiator[^8]
- **Curator agent for knowledge maintenance** — addresses knowledge drift partially[^7]
### Improvement 1: Add "Action" as a First-Class Concept in `know`
**Source:** Palantir's fourfold model[^2]

**The problem:** `know` stores knowledge atoms (decisions, facts, concepts, tasks) but doesn't model what can be *done* with or *triggered by* that knowledge. A DECISION atom about "Use PostgreSQL" exists, but there's no formal link to the action "migrate database" or the logic "run migration script X."

**The change:** Add a new `KnowledgeType.ACTION` to the `know` ontology. Actions are atoms that describe executable operations — what they do, what they require, what permissions they need, and what other atoms they affect. Connect them to existing atoms via `IMPLEMENTS` or `TRIGGERS` connection types.

```
Atom: "Use PostgreSQL" (DECISION)
  ├── IMPLEMENTS → "Setup PostgreSQL Docker" (ACTION)
  ├── IMPLEMENTS → "Migrate SQLite to PostgreSQL" (ACTION)
  └── SUPPORTS → "Database benchmark results" (FACT)
```

**Impact:** Low implementation effort (add one enum value + convention). High value because it makes `know` a proper operational layer — agents can query "what actions are available for this decision?" This moves toward Palantir's "nouns + verbs" model without building a full action execution engine.

**Scope:** `know` repo only. No change to nowu's core framework.
### Improvement 2: Make `know` the Shared Agent Memory
**Source:** XpandA's centralized shared memory; Palantir's ontology as common interface[^4][^1][^2]

**The problem:** Currently, agents coordinate through files (SESSION-STATE.md, SHAPE.md, FRAMING.md). `know` is treated as a library that *humans* use to store knowledge, not as a runtime memory that agents read/write during task execution.

**The change:** In the `flow` module (the session/agent coordination layer), have each agent write its outputs and observations as `know` atoms during execution — not just to markdown files:

- **Framer** creates a `CONCEPT` atom for the framed problem and connects it to the originating `TASK`.
- **Shaper** creates `TASK` atoms for each scoped task and connects them via `DEPENDS_ON`.
- **Implementer** creates `DECISION` atoms for design choices made during coding.
- **Reviewer** creates `LESSON` atoms for review findings and connects them to the code atoms.

The existing markdown artifacts (FRAMING.md, SHAPE.md) can be *generated views* from these atoms, rather than the source of truth. This is exactly the "JSON truth, SQLite index" principle already in `know` — extended to agent workflow artifacts.

**Impact:** Medium effort (requires the `know_adapter` layer in nowu). High value because it means cross-project knowledge automatically accumulates — a design decision made in the aperitif project that is also relevant to real-estate digitalization becomes discoverable via `kb.search()`.
### Improvement 3: Add Knowledge Versioning to `know`
**Source:** Guo et al.'s continuous learning recommendation; Palantir's feedback loops[^4][^2]

**The problem:** When a `know` atom is updated (e.g., a DECISION changes from "Use SQLite" to "Use PostgreSQL"), the previous version is lost. The `know` atom only stores `createdat` and `updatedat`, with no history. The survey specifically recommends "versioned knowledge bases that track the evolution of APIs, best practices, and project conventions".[^4]

**The change:** Add a `versions` array to the atom JSON (or a `versions/` subfolder per atom). Each update creates a new version entry with a timestamp, the previous content, and optionally a reason for the change. The SQLite index tracks only the latest version; the JSON files preserve full history.

```json
{
  "id": "atom-abc123",
  "title": "Use PostgreSQL",
  "content": "Switched from SQLite after scale testing...",
  "versions": [
    {
      "version": 1,
      "timestamp": "2026-02-26T10:00:00",
      "title": "Use SQLite",
      "content": "Chosen for simplicity...",
      "changed_by": "human",
      "reason": "Initial decision"
    }
  ]
}
```

**Impact:** Low-medium effort. Enables the curator to detect *decision reversals* and flag them for review. Also enables "what changed since last week?" queries, which feed directly into the weekly health check.
### Improvement 4: Add Structured Prompting via Connection Graphs
**Source:** Guo et al.'s structured prompting findings — SynFix uses RelationGraphs, Codes uses multi-layer sketches, DRCodePilot uses "design first, then code"[^4]

**The problem:** When Copilot (the Implementer agent) starts a task, it reads SESSION-STATE.md and the task description. It does *not* receive a structured dependency graph showing how the current task relates to other atoms, decisions, and constraints in `know`.

**The change:** Before passing a task to the Implementer, the Shaper (or Orchestrator) queries `know` for all atoms connected to the task atom — decisions it `DEPENDS_ON`, facts that `SUPPORT` it, constraints that `CONTRADICT` other approaches — and formats this as a structured context block in the prompt:

```markdown
## Task Context (auto-generated from know)
### This task depends on:
- DECISION: "Use SQLite for know index" (grade: 4, confidence: 0.9)
- DECISION: "JSON files are source of truth" (grade: 5, confidence: 1.0)
### Related constraints:
- FACT: "SQLite FTS5 supports trigram tokenizer" (grade: 4)
### Known contradictions:
- (none)
### Connected actions:
- ACTION: "Run schema migration" (status: pending)
```

The survey found that providing structured context — especially dependency graphs and design rationales — significantly improves code generation quality compared to raw natural language. The DRCodePilot approach of formalizing a "design first, then code" plan by leveraging design rationales from issue logs directly maps to this pattern.[^4]

**Impact:** Medium effort (requires `know` query in the flow/bridge layer). High value because it directly addresses the "project amnesia" problem — agents receive architectural context, not just task descriptions.

***
## What NOT to Adopt
| Concept | Source | Why Skip (for now) |
|---------|--------|--------------------|
| Fine-grained per-action security | Palantir[^2] | Overkill for single-developer framework. Approval tiers are sufficient for v1. Revisit when multi-user. |
| Dynamic replanning (MCTS-based) | LingmaAgent[^4] | Adds massive complexity. Static pipeline is validated as sufficient by Agentless[^4]. |
| Multi-hypothesis generation + voting | Nemotron-CORTEXA[^4] | Expensive (multiple LLM calls per task). Add only if quality issues emerge. |
| Full action execution engine | Palantir's Action primitive[^2] | Adding ACTION as a knowledge type is enough. Building an execution engine is scope creep. |
| Formal verification tools | Alphaverus[^4] | Not applicable to a framework-level project. Relevant for safety-critical code only. |
| RL-based preference alignment | Guo et al.[^4] | Requires custom model training. nowu uses hosted LLMs via Copilot. |

***
## Mapping to nowu's Existing Architecture
```
┌─────────────────────────────────────────────────┐
│  USER INTERFACE LAYER (VS Code, CLI)            │
│  No change needed                               │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  APPLICATION LAYER (Orchestration & Routing)    │
│  + Improvement 4: Structured prompt generation  │
│    from know connection graphs before tasks     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  DOMAIN LAYER (Core Business Logic)             │
│  + Improvement 1: ACTION as knowledge type      │
│  + Improvement 2: Agents write to know directly │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  INFRASTRUCTURE LAYER (Persistence & Tools)     │
│  + Improvement 3: Version history on atoms      │
│  know repo: Add versions array to JSON schema   │
└─────────────────────────────────────────────────┘
```

***
## Implementation Priority
| Priority | Improvement | Where | Effort | When |
|----------|------------|-------|--------|------|
| 1st | Improvement 1: ACTION type | `know` repo | Low (1 enum + convention) | Next `know` PR |
| 2nd | Improvement 3: Versioning | `know` repo | Low-Med (JSON schema + update logic) | After Improvement 1 |
| 3rd | Improvement 2: Shared agent memory | `nowu` repo (flow module) | Medium (know_adapter layer) | When building `flow` |
| 4th | Improvement 4: Structured prompts | `nowu` repo (bridge module) | Medium (know query + prompt template) | When building `bridge` |

The first two can be done entirely within the `know` repo without touching nowu. The last two require the nowu modules (`flow`, `bridge`) that haven't been built yet — they'll be naturally incorporated during those phases.

***
## Conclusion
Both Palantir's enterprise ontology and the academic survey validate nowu's core architecture. The multi-agent pipeline, persistent knowledge layer, WAL protocol, decision journal, approval tiers, and TDD-first approach are all patterns that appear repeatedly across state-of-the-art research and production systems. The four recommended improvements — ACTION type, shared agent memory, knowledge versioning, and structured prompting from connection graphs — are additive changes that strengthen the existing foundation without requiring architectural restructuring. The framework is on the right track.

---

## References

1. [Agentic Operating System for the Enterprise | Palantir’s AIP Lead Jack Dobson at AIPCon 6](https://www.youtube.com/watch?v=SePXznjZ-1A) - Palantir’s customers operate in the most mission critical, sensitive and competitive environments - ...

2. [The Ontology system - Palantir](https://www.palantir.com/docs/foundry/architecture-center/ontology-system) - The Ontology is the system at the heart of Palantir’s architecture. The Ontology is designed to repr...

3. [Overview • Architecture center - Palantir](https://www.palantir.com/docs/foundry/architecture-center/overview) - Since its inception, Palantir's software has been shaped by our customers' most demanding missions. ...

4. [Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LL.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/122142d2-ff72-44be-b8ac-63f099624c26/Guo-et-al.-2025-A-Comprehensive-Survey-on-Benchmarks-and-Solutions-in-Software-Engineering-of-LLM-Empowered-Agentic.pdf?AWSAccessKeyId=ASIA2F3EMEYE7PNCTMQS&Signature=oe1Y369VPTv3qr7wk%2B0ARvM%2FE6I%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICugjAmUZ%2Feber%2BymqeIkrf557AKHhPoCHJCpA96QvPRAiEAikSeaYlNI37bscc2pJRE%2BIEDD33q%2FPVXaFM0KZhjor8q%2FAQIsf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDExFaYerEVPy7PPYeSrQBKqQ9X0vsPGlr4zG59uOoFZrf2sypKHzmHqOFTdI2Xp0TQnNSc1fP50%2FIE4dPnQU2sT3SphIXJrq8MSRuzWB1rxbDTsEbEDE%2FE0n%2FQwNXJjRp9FcESCI8PMZcM1XYIYSJDk%2BmBjB1LOMQG586%2FsyC7rumxJytFr8ZO5BpLaCRgIPn1qj63N69Az6ze7NcsmbJARZnm27oJLtSHihbDjGj0xBomkuUo0rRK893AyPo303ydy8hUQ0gnvHNeeEL41PG7mXRmI%2Bo03HSB354CDk8FSwjR4qM9O%2BWrskmxcrQlw7XoyaaclQMJjSe6keLKlpaZ78GTHcXEI5or%2BoDWq%2BuJ8R0VQSku%2Bb6V863JnhFwnUPmZA6wNJxLZlaSh%2B7HDAKPgYwqDS8hEemlFdParJPSFJhFxlmJc1zd8s0J8M%2FtcauvAz1XjtWNcX0%2F6MS3%2BbhvRQT7jI68LEp4%2Bm8kAW3yRSW7TcT%2FnZHVW8rMjy0QVc10t54Wv0dwkrlImgNXVwuwU2s9EQ5yB9KmxU9qqY5szcXfTsJCsSr2DCj4qznpecSqd8QQq7hO%2FuXNzfPsZG%2Fyi7RfLKQz0YOsU3DqJNGw6NrEWwHTqCaM0MgHx0MWkzr4MO3wjjiNx6c%2Bw6peY%2F26yWsfCRw9ED5xBWAuswXMCu2u0Q11vwC%2F4%2BYsN3uNCmp1EIrJfHAbJA%2BBYzb8mHReRmddzUg9cnRA4TGwRaOMdVHtjq0fpH9Lhm53Z2lBcout%2FxYYJNj3LiWmN7jmeJMXkrhoeVUwxEkTVTWGNbSnowucufzQY6mAEwDcHOVyLu2m74RrZoPfWG3nA7uuoM45VfRQoplCVryOhz9w1wxfqSlPWVahKW%2BNaV5sM2CW8PFegMjsutpN2pH1ss50ScstlAykfjyBoHHHsdVaP7xqp1GJtpLu%2B8GkWfvnXmr7tPGWy47PI353iV%2FivoJrN6jvwrOkJXJzpGTmaPxxjKpUPGH%2FZJ41oAzYPXIO1UdLtJ4g%3D%3D&Expires=1772615909) - A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic ...

5. [ARCHITECTURE.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/93aaa23a-36e1-43b9-b8a9-179b0d7284d5/ARCHITECTURE.md?AWSAccessKeyId=ASIA2F3EMEYE7PNCTMQS&Signature=%2BVjuk5XDzBLZy563jaGSsqOl7b4%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICugjAmUZ%2Feber%2BymqeIkrf557AKHhPoCHJCpA96QvPRAiEAikSeaYlNI37bscc2pJRE%2BIEDD33q%2FPVXaFM0KZhjor8q%2FAQIsf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDExFaYerEVPy7PPYeSrQBKqQ9X0vsPGlr4zG59uOoFZrf2sypKHzmHqOFTdI2Xp0TQnNSc1fP50%2FIE4dPnQU2sT3SphIXJrq8MSRuzWB1rxbDTsEbEDE%2FE0n%2FQwNXJjRp9FcESCI8PMZcM1XYIYSJDk%2BmBjB1LOMQG586%2FsyC7rumxJytFr8ZO5BpLaCRgIPn1qj63N69Az6ze7NcsmbJARZnm27oJLtSHihbDjGj0xBomkuUo0rRK893AyPo303ydy8hUQ0gnvHNeeEL41PG7mXRmI%2Bo03HSB354CDk8FSwjR4qM9O%2BWrskmxcrQlw7XoyaaclQMJjSe6keLKlpaZ78GTHcXEI5or%2BoDWq%2BuJ8R0VQSku%2Bb6V863JnhFwnUPmZA6wNJxLZlaSh%2B7HDAKPgYwqDS8hEemlFdParJPSFJhFxlmJc1zd8s0J8M%2FtcauvAz1XjtWNcX0%2F6MS3%2BbhvRQT7jI68LEp4%2Bm8kAW3yRSW7TcT%2FnZHVW8rMjy0QVc10t54Wv0dwkrlImgNXVwuwU2s9EQ5yB9KmxU9qqY5szcXfTsJCsSr2DCj4qznpecSqd8QQq7hO%2FuXNzfPsZG%2Fyi7RfLKQz0YOsU3DqJNGw6NrEWwHTqCaM0MgHx0MWkzr4MO3wjjiNx6c%2Bw6peY%2F26yWsfCRw9ED5xBWAuswXMCu2u0Q11vwC%2F4%2BYsN3uNCmp1EIrJfHAbJA%2BBYzb8mHReRmddzUg9cnRA4TGwRaOMdVHtjq0fpH9Lhm53Z2lBcout%2FxYYJNj3LiWmN7jmeJMXkrhoeVUwxEkTVTWGNbSnowucufzQY6mAEwDcHOVyLu2m74RrZoPfWG3nA7uuoM45VfRQoplCVryOhz9w1wxfqSlPWVahKW%2BNaV5sM2CW8PFegMjsutpN2pH1ss50ScstlAykfjyBoHHHsdVaP7xqp1GJtpLu%2B8GkWfvnXmr7tPGWy47PI353iV%2FivoJrN6jvwrOkJXJzpGTmaPxxjKpUPGH%2FZJ41oAzYPXIO1UdLtJ4g%3D%3D&Expires=1772615909) - know is a knowledge layer designed for agentic AI systems. It provides persistent, queryable, multi-...

6. [CODE_WALKTHROUGH.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/45aa6f53-0674-4c7f-a9ec-939cdd981dd5/CODE_WALKTHROUGH.md?AWSAccessKeyId=ASIA2F3EMEYE7PNCTMQS&Signature=vL2B7C3i7bU%2BZJrveQv9x6um6sg%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICugjAmUZ%2Feber%2BymqeIkrf557AKHhPoCHJCpA96QvPRAiEAikSeaYlNI37bscc2pJRE%2BIEDD33q%2FPVXaFM0KZhjor8q%2FAQIsf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDExFaYerEVPy7PPYeSrQBKqQ9X0vsPGlr4zG59uOoFZrf2sypKHzmHqOFTdI2Xp0TQnNSc1fP50%2FIE4dPnQU2sT3SphIXJrq8MSRuzWB1rxbDTsEbEDE%2FE0n%2FQwNXJjRp9FcESCI8PMZcM1XYIYSJDk%2BmBjB1LOMQG586%2FsyC7rumxJytFr8ZO5BpLaCRgIPn1qj63N69Az6ze7NcsmbJARZnm27oJLtSHihbDjGj0xBomkuUo0rRK893AyPo303ydy8hUQ0gnvHNeeEL41PG7mXRmI%2Bo03HSB354CDk8FSwjR4qM9O%2BWrskmxcrQlw7XoyaaclQMJjSe6keLKlpaZ78GTHcXEI5or%2BoDWq%2BuJ8R0VQSku%2Bb6V863JnhFwnUPmZA6wNJxLZlaSh%2B7HDAKPgYwqDS8hEemlFdParJPSFJhFxlmJc1zd8s0J8M%2FtcauvAz1XjtWNcX0%2F6MS3%2BbhvRQT7jI68LEp4%2Bm8kAW3yRSW7TcT%2FnZHVW8rMjy0QVc10t54Wv0dwkrlImgNXVwuwU2s9EQ5yB9KmxU9qqY5szcXfTsJCsSr2DCj4qznpecSqd8QQq7hO%2FuXNzfPsZG%2Fyi7RfLKQz0YOsU3DqJNGw6NrEWwHTqCaM0MgHx0MWkzr4MO3wjjiNx6c%2Bw6peY%2F26yWsfCRw9ED5xBWAuswXMCu2u0Q11vwC%2F4%2BYsN3uNCmp1EIrJfHAbJA%2BBYzb8mHReRmddzUg9cnRA4TGwRaOMdVHtjq0fpH9Lhm53Z2lBcout%2FxYYJNj3LiWmN7jmeJMXkrhoeVUwxEkTVTWGNbSnowucufzQY6mAEwDcHOVyLu2m74RrZoPfWG3nA7uuoM45VfRQoplCVryOhz9w1wxfqSlPWVahKW%2BNaV5sM2CW8PFegMjsutpN2pH1ss50ScstlAykfjyBoHHHsdVaP7xqp1GJtpLu%2B8GkWfvnXmr7tPGWy47PI353iV%2FivoJrN6jvwrOkJXJzpGTmaPxxjKpUPGH%2FZJ41oAzYPXIO1UdLtJ4g%3D%3D&Expires=1772615909) - This guide shows actual code from the project with explanations of the decisions. --- TITLE Architec...

7. [curator.py](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/a7c5d37a-5700-41b5-90bc-a5a95b5263f4/curator.py?AWSAccessKeyId=ASIA2F3EMEYE7PNCTMQS&Signature=N%2FOeHcoOUm96XmF615QSAeMUiKQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICugjAmUZ%2Feber%2BymqeIkrf557AKHhPoCHJCpA96QvPRAiEAikSeaYlNI37bscc2pJRE%2BIEDD33q%2FPVXaFM0KZhjor8q%2FAQIsf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDExFaYerEVPy7PPYeSrQBKqQ9X0vsPGlr4zG59uOoFZrf2sypKHzmHqOFTdI2Xp0TQnNSc1fP50%2FIE4dPnQU2sT3SphIXJrq8MSRuzWB1rxbDTsEbEDE%2FE0n%2FQwNXJjRp9FcESCI8PMZcM1XYIYSJDk%2BmBjB1LOMQG586%2FsyC7rumxJytFr8ZO5BpLaCRgIPn1qj63N69Az6ze7NcsmbJARZnm27oJLtSHihbDjGj0xBomkuUo0rRK893AyPo303ydy8hUQ0gnvHNeeEL41PG7mXRmI%2Bo03HSB354CDk8FSwjR4qM9O%2BWrskmxcrQlw7XoyaaclQMJjSe6keLKlpaZ78GTHcXEI5or%2BoDWq%2BuJ8R0VQSku%2Bb6V863JnhFwnUPmZA6wNJxLZlaSh%2B7HDAKPgYwqDS8hEemlFdParJPSFJhFxlmJc1zd8s0J8M%2FtcauvAz1XjtWNcX0%2F6MS3%2BbhvRQT7jI68LEp4%2Bm8kAW3yRSW7TcT%2FnZHVW8rMjy0QVc10t54Wv0dwkrlImgNXVwuwU2s9EQ5yB9KmxU9qqY5szcXfTsJCsSr2DCj4qznpecSqd8QQq7hO%2FuXNzfPsZG%2Fyi7RfLKQz0YOsU3DqJNGw6NrEWwHTqCaM0MgHx0MWkzr4MO3wjjiNx6c%2Bw6peY%2F26yWsfCRw9ED5xBWAuswXMCu2u0Q11vwC%2F4%2BYsN3uNCmp1EIrJfHAbJA%2BBYzb8mHReRmddzUg9cnRA4TGwRaOMdVHtjq0fpH9Lhm53Z2lBcout%2FxYYJNj3LiWmN7jmeJMXkrhoeVUwxEkTVTWGNbSnowucufzQY6mAEwDcHOVyLu2m74RrZoPfWG3nA7uuoM45VfRQoplCVryOhz9w1wxfqSlPWVahKW%2BNaV5sM2CW8PFegMjsutpN2pH1ss50ScstlAykfjyBoHHHsdVaP7xqp1GJtpLu%2B8GkWfvnXmr7tPGWy47PI353iV%2FivoJrN6jvwrOkJXJzpGTmaPxxjKpUPGH%2FZJ41oAzYPXIO1UdLtJ4g%3D%3D&Expires=1772615909)

8. [API.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/55ab1c8e-184a-4155-a2f6-7f44dfc39ae7/API.md?AWSAccessKeyId=ASIA2F3EMEYE7PNCTMQS&Signature=5rfRsjtAG4eM6LQGRjoV%2Fa9dfqI%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICugjAmUZ%2Feber%2BymqeIkrf557AKHhPoCHJCpA96QvPRAiEAikSeaYlNI37bscc2pJRE%2BIEDD33q%2FPVXaFM0KZhjor8q%2FAQIsf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDExFaYerEVPy7PPYeSrQBKqQ9X0vsPGlr4zG59uOoFZrf2sypKHzmHqOFTdI2Xp0TQnNSc1fP50%2FIE4dPnQU2sT3SphIXJrq8MSRuzWB1rxbDTsEbEDE%2FE0n%2FQwNXJjRp9FcESCI8PMZcM1XYIYSJDk%2BmBjB1LOMQG586%2FsyC7rumxJytFr8ZO5BpLaCRgIPn1qj63N69Az6ze7NcsmbJARZnm27oJLtSHihbDjGj0xBomkuUo0rRK893AyPo303ydy8hUQ0gnvHNeeEL41PG7mXRmI%2Bo03HSB354CDk8FSwjR4qM9O%2BWrskmxcrQlw7XoyaaclQMJjSe6keLKlpaZ78GTHcXEI5or%2BoDWq%2BuJ8R0VQSku%2Bb6V863JnhFwnUPmZA6wNJxLZlaSh%2B7HDAKPgYwqDS8hEemlFdParJPSFJhFxlmJc1zd8s0J8M%2FtcauvAz1XjtWNcX0%2F6MS3%2BbhvRQT7jI68LEp4%2Bm8kAW3yRSW7TcT%2FnZHVW8rMjy0QVc10t54Wv0dwkrlImgNXVwuwU2s9EQ5yB9KmxU9qqY5szcXfTsJCsSr2DCj4qznpecSqd8QQq7hO%2FuXNzfPsZG%2Fyi7RfLKQz0YOsU3DqJNGw6NrEWwHTqCaM0MgHx0MWkzr4MO3wjjiNx6c%2Bw6peY%2F26yWsfCRw9ED5xBWAuswXMCu2u0Q11vwC%2F4%2BYsN3uNCmp1EIrJfHAbJA%2BBYzb8mHReRmddzUg9cnRA4TGwRaOMdVHtjq0fpH9Lhm53Z2lBcout%2FxYYJNj3LiWmN7jmeJMXkrhoeVUwxEkTVTWGNbSnowucufzQY6mAEwDcHOVyLu2m74RrZoPfWG3nA7uuoM45VfRQoplCVryOhz9w1wxfqSlPWVahKW%2BNaV5sM2CW8PFegMjsutpN2pH1ss50ScstlAykfjyBoHHHsdVaP7xqp1GJtpLu%2B8GkWfvnXmr7tPGWy47PI353iV%2FivoJrN6jvwrOkJXJzpGTmaPxxjKpUPGH%2FZJ41oAzYPXIO1UdLtJ4g%3D%3D&Expires=1772615909) - Initialize the knowledge layer. Must be called before any other functions. Creates the data director...

