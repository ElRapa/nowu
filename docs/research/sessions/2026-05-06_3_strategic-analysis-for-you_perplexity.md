# Strategic Analysis: nowu Workflow Evolution & Next Steps
**Date:** 2026-05-06  
**Context:** Response to pre-workflow pain points, triage needs, and altitude model questions

---

## Executive Summary

**Your core insight is correct:** The altitude problem isn't about lacking altitude labels—it's about **S1-S9 agents being implementation-focused when the workflow needs strategic thinking**.

The pre-workflow pain you experienced (jumping use-cases→epics without global view, missing pieces, patchwork features) is a **well-documented failure mode** in software development research. You independently rediscovered:

1. **The Systems Engineering Zigzag** — Requirements and architecture must co-evolve, not cascade linearly
2. **Shape Up's Shaping Track** — Strategic work must happen BEFORE implementation commits
3. **Lean Startup's Build-Measure-Learn vs. Big Design Upfront** — The tension between iteration and planning

**The research validates your direction** but suggests a **different implementation path** than Sisyphus's 55-file migration.

---

## Pain Point Analysis: What You Actually Experienced

### The Problem in Your Words

> "Jumping from use-cases to epics. Not having a global-view. [...] jumping to an Epic trying to implement a small Use-Case will lead to patch-work of miss-aligned features and a code-mess."

**This is altitude drift.** You tried to go from PRODUCT (use cases) directly to DELIVERY (epics) without ARCHITECTURE synthesis.

**Research name for this:** "Premature decomposition" (Boehm 1988), "Requirements cascade without architectural validation" (Bass et al. 2021).

### Why S1-S9 Didn't Prevent It

**S1-S9 as currently conceived assumes:**
- The architecture is already decided (modules exist, contracts are stable)
- An intake can be scoped to a single epic
- Implementation can proceed linearly: intake → constraints → options → decide → shape → implement → verify

**Reality of early-stage development:**
- Architecture emerges FROM use cases, not before them
- You don't know how to scope until you synthesize cross-cutting themes
- The first 5 use cases will force 3 architectural pivots

**The altitude model addresses this** by making ARCHITECTURE synthesis an explicit phase BEFORE delivery scoping.

---

## The Altitude Solution: What It Actually Solves

### What Altitudes Give You (That Linear S1-S9 Doesn't)

1. **Explicit "Where am I now?" markers** — An agent knows if it's doing strategic, architectural, or implementation work

2. **Forcing functions for upward promotion** — "This UC has architectural implications" becomes a machine-checkable flag that triggers SYNTHESIS

3. **Preventing downward bleeding** — A PRODUCT/PROBLEM artifact that contains module names fails validation

4. **Cross-artifact reasoning** — "I have 3 approved UCs with state management concerns. Run architectural synthesis BEFORE next epic."

### The Balance You're Seeking

Your quote:
> "Where is the balance between full spec up-head and we define as we go. Both have their pros and cons."

**Research has answered this.** The framework is called **"Just-In-Time" (JIT) specification** or **"Spec-Driven Iteration"** (Martinelli 2026).

**The pattern:**[cite:561]
- Write specs (use cases, constraints, architectural decisions) BEFORE code
- Keep specs SHORT (1-2 pages, markdown, version-controlled)
- Update specs EVERY TIME you learn something new
- Specs are living artifacts, not paperwork

**Comparison:**

| Waterfall | JIT Spec (nowu model) | Pure Agile |
|---|---|---|
| Big upfront scope | Small upfront scope | No written scope |
| Late validation | Continuous validation | Continuous validation |
| Specs written once | Specs updated per iteration | No specs (code is truth) |
| Changes expensive | Changes start in specs | Changes start in code |

**The nowu altitude model is JIT spec.** You write PRODUCT/PROBLEM, then ARCHITECTURE/OPTIONS, then DELIVERY/SHAPE incrementally—but each altitude's spec stabilizes BEFORE the next altitude starts implementation.

---

## Triage: The Missing Capability

### Your Need

> "The 'what should we do next'? (what is important or blocking or having the biggest leverage or will define something with a lot of dependencies? triage?)"

**This is the #1 gap in your current workflow model.** Neither S1-S9 nor P0-P4 has a triage step.

### What Triage Means in Product Development

Triage in software = **Intake → Assessment → Routing**[cite:563]

- **Intake:** What's the request? (UC, bug, constraint, idea)
- **Assessment:** What altitude does this belong to? What's the impact? What's blocking on this?
- **Routing:** Where in the workflow does this go? (STRATEGIC, ARCHITECTURE, or DELIVERY intake queue)

**Priority frameworks for assessment:**[cite:573][cite:577][cite:582]

1. **RICE (Reach × Impact × Confidence / Effort)** — Best for product features with measurable reach
2. **Value vs. Effort Matrix** — 2×2 grid: Quick Wins, Major Projects, Fill-Ins, Thankless Tasks
3. **Impact/Urgency Matrix** — 2×2 grid: Do First (high/high), Schedule (high/low), Delegate (low/high), Drop (low/low)
4. **Reversibility × Consequence** — Jeff Bezos's framework: Type 1 (irreversible + consequential) vs. Type 2 (reversible + inconsequential) decisions

**For nowu specifically:**

You need **Impact × Altitude Assessment**:

```
High Impact, STRATEGIC altitude     → P0 (Vision/Goal revision)
High Impact, ARCHITECTURE altitude  → Trigger SYNTHESIS or emergency ADR
High Impact, DELIVERY altitude      → P3 (Intake queue, prioritized)
Low Impact, any altitude            → Backlog or reject
Blocking                            → Preempt current cycle, emergency intake
High leverage (defines dependencies)→ ARCHITECTURE synthesis
```

### Where Triage Fits in Your Workflow

**Option A: Triage as a pre-step to every altitude's IDEA phase**

```
User submits request → Triage → Routes to appropriate altitude's IDEA phase
```

- STRATEGIC/IDEA if it's a portfolio/vision concern
- PRODUCT/PROBLEM if it's a user pain point
- ARCHITECTURE/PROBLEM if it's a constraint or integration issue
- DELIVERY/IDEA if it's a feature request with clear scope
- EXECUTION/IDEA if it's a bug or code smell

**Option B: Triage as a separate agent that runs daily/weekly**

```
Triage Agent reviews:
- Unprocessed intake queue
- Problem statements flagged with architectural_implications: true
- Circuit breaker alerts (altitude violations, epistemic grade drift)
- Health metrics from S9/GAP

Outputs: Priority-ranked list of next intakes + recommended altitude/phase entry point
```

**Recommendation:** Start with Option B. Run triage manually for first 3-5 cycles, then automate.

---

## The Four Critical Deficits

### 1. Artifacts/Knowledge Management

**Your question:** Is markdown good for now? Shall we introduce Obsidian as interim?

**Research answer:** Markdown is correct for nowu's stage. Obsidian is optional but synergistic.[cite:562][cite:567][cite:575]

**Why markdown works:**[cite:567]

- LLMs are trained on markdown — it's their native format
- Git-trackable, diffable, human-readable
- Iterates faster than databases (domain expert can edit .md, no engineering needed)
- Observability: when agent makes error, you can READ the exact file it consumed

**When markdown stops working:**[cite:562][cite:567]

- Knowledge base grows to thousands of documents (selective injection becomes retrieval problem → need vector DB)
- Knowledge is highly relational with complex interdependencies → need knowledge graph
- Multi-user concurrent editing → need collaborative database

**You're not there yet.** With ~20 use cases, ~8 problems, ~6 intakes, ~5 ADRs, markdown is optimal.

**Obsidian's value for nowu:**[cite:575][cite:580]

- **Graph view** shows cross-references (UC-001 links to problem-003 links to ADR-0004)
- **Dataview plugin** queries frontmatter metadata (show all ARCHITECTURE/OPTIONS artifacts with epistemic_grade < INFORMED_ESTIMATE)
- **Canvas** for visual workflow/architecture mapping
- **Templater plugin** generates artifacts from templates with dynamic frontmatter

**Recommendation:** Keep markdown. Add Obsidian vault as the human UI for browsing/navigating artifacts. AI agents still read/write markdown files directly.

**Structure:**

```
nowu-repo/
  state/
    products/
      product-001.md
    problems/
      problem-001.md
    usecases/
      uc-001.md
    architecture/
      adr-0001.md
      options-001.md
      synthesis-001.md
    delivery/
      intake-001.md
      shape-001.md
    execution/
      session-state.md
  .obsidian/           ← Obsidian config (graph view settings, templates)
```

Obsidian treats `state/` as its vault root. Git ignores `.obsidian/` if you don't want to commit view settings.

### 2. Triage / "What Should We Do Next?"

**See Triage section above.** Implement as:

**Immediate:** Manual priority matrix (Impact × Altitude) after every GAP cycle

**v1:** Triage Agent that reads:
- Unprocessed items in `state/ideas/`
- Architectural implications flags in approved UCs
- Circuit breaker alerts
- Health metrics from last GAP

Outputs: `state/triage/triage-YYYY-MM-DD.md` with ranked next actions

**Framework to use:** RICE or Impact/Urgency Matrix[cite:573][cite:574][cite:577]

### 3. General AI Assistant

**Your need:** "As the system is getting more and more complex a general AI-assistant would be helpful."

**This is exactly what your altitude model enables.** The altitude/phase coordinates let a general assistant route queries correctly.

**Architecture:**

```
User: "Why did we decide SQLite per-project instead of shared DB?"

General Assistant:
  1. Detects this is ARCHITECTURE/DECISION query
  2. Searches state/architecture/ for relevant ADRs
  3. Finds ADR-0004 (altitude: ARCHITECTURE, phase: DECISION)
  4. Extracts decision rationale + tradeoffs from ADR
  5. Returns: "ADR-0004: Per-project isolation for bounded failure. Tradeoff: Federation complexity."
```

**Key capability:** The assistant can answer "where are we in the workflow?" by reading session state + latest artifacts.

**User:** "What's blocking v1-core launch?"  
**Assistant:** Reads `state/delivery/v1-core-readiness.md`, sees intake-003, intake-005 are not VERIFIED. Returns: "2 intakes pending VBR. Blocker: intake-003 AC3 (cross-project query <200ms) fails on 3-project federation test."

**Implementation:**

- LangGraph state machine with "query router" node
- Router classifies query type (artifact lookup, workflow position, decision history, blocker analysis)
- Routes to specialized subgraph (search agent, triage agent, retrospective analyzer)
- Uses markdown knowledge files (state/ artifacts + agent definitions) as RAG corpus

**Do NOT build this until after S1-S9 proves itself.** The general assistant needs stable artifact structure to query.

### 4. Deep Built-In Researcher on Solutions/Options

**This is the S3 (Options) agent but altitude-aware + research-augmented.**

**Current S3 problem:** It writes 2-4 architectural options from reasoning, not from researching comparable systems.

**What you need:** Options agent that:

1. Takes ARCHITECTURE/PROBLEM as input
2. **Searches for comparable solutions** (GitHub repos, academic papers, framework docs)
3. Extracts architectural patterns from 3-5 comparable systems
4. Synthesizes 2-4 architectural options grounded in real systems
5. Writes ARCHITECTURE/OPTIONS with citations + tradeoffs

**This is exactly AFLOW's Research → Exploration pattern**[cite:555][cite:557][cite:569]

**AFLOW methodology:**[cite:557]

- Generate initial workflow from blank template
- Test on validation set, collect failure cases
- Search academic papers + code repos for patterns that address failure modes
- Extract modular operators (Generate, Review, Test, Revise)
- Recombine operators into new workflows
- Iterate until performance plateaus

**For nowu:** Your Options agent should work the same way.

**Example:**

Input: ARCHITECTURE/PROBLEM-007 (cross-project knowledge invisible)

Research phase:
- Search: "cross-project knowledge management architecture"
- Find: Obsidian's shared vaults, Notion's workspace model, Roam's graph database, LogSeq's graph + pages
- Extract patterns:
  1. Shared vault with project namespaces (Obsidian)
  2. Centralized workspace with project views (Notion)
  3. Graph database with project tags (Roam)
  4. Hybrid: Local files + global index (nowu's current direction)

Synthesis phase:
- Generate 3 architectural options based on extracted patterns
- Compare tradeoffs (isolation, query complexity, migration path)
- Write ARCHITECTURE/OPTIONS-007.md with citations to researched systems

**This is S3 + web search + pattern extraction.** Build it as an enhanced S3, not a separate agent.

---

## DeepAgent / LangGraph Question

**Your question:** Should we introduce DeepAgents on LangGraph?

**Short answer:** Not yet. But LangGraph is the right choice when you do build the orchestration layer.

### What DeepAgents Is

**DeepAgents** = LangChain's "agent harness" built on LangGraph runtime[cite:565]

- Same core tool-calling loop as other agent frameworks
- Built-in tools and capabilities (web search, code execution, memory)
- Uses LangGraph for durable execution, streaming, human-in-the-loop
- Treats agents as a toolkit, not a structure

**LangGraph** = State machine orchestration for multi-agent workflows[cite:560][cite:576][cite:581]

- Models workflows as explicit state machines with typed state
- Conditional branching, checkpointing, human approval gates
- Full async support, LangSmith observability
- Native subgraph support (each altitude could be a subgraph)

**CrewAI** (alternative) = Role-based team orchestration[cite:576][cite:581]

- Models workflows as teams with roles, goals, tasks
- Sequential, hierarchical, or consensual processes
- Faster prototyping, less control
- No built-in checkpointing

### Research Recommendation

**LangGraph vs. CrewAI:**[cite:576][cite:581]

Use **LangGraph** when you need:
- Checkpointing (resume after failure)
- Human approval gates (P4 betting table, S8 VBR review)
- Complex conditional routing (S3 generates 4 options, S4 picks best, S5 adapts shape based on choice)
- Compliance/audit trails (who approved what, when)

Use **CrewAI** when you need:
- Fast prototyping of role-based workflows
- Linear or hierarchically supervised execution
- Simpler mental model (agents = people with roles)

**For nowu:** LangGraph is the correct choice because:

1. **You need checkpointing** — P0-P4 pre-workflow can span days; S1-S9 workflow must resume after VBR rejection
2. **You need approval gates** — P4 betting table, S4 decision recording, S8 VBR
3. **You need conditional routing** — S3 OPTIONS → S4 DECISION → S5 SHAPE needs to adapt based on decision
4. **You're building enterprise-grade structure** — The 5-altitude model with circuit breakers is compliance-oriented

### When to Introduce LangGraph

**Not in Package 1.** Wait until:

1. S1-S9 agents prove they can complete 3 intakes end-to-end (even if run manually)
2. You hit one of these pain points:
   - Agent fails mid-workflow, loses all context → need checkpointing
   - Human wants to intervene between S4 and S5 → need approval gate
   - S6-S8 loop runs 5 times, context window explodes → need state compression
3. You have stable artifact structure (altitude/phase coordinates, frontmatter schema)

**Then:** Implement LangGraph orchestration layer that treats S1-S9 agents as nodes in a state machine.

**Pattern:**

```python
from langgraph.graph import StateGraph

workflow = StateGraph()
workflow.add_node("S1_intake", nowu_intake_agent)
workflow.add_node("S2_constraints", nowu_constraints_agent)
workflow.add_node("S3_options", nowu_options_agent)
workflow.add_node("S4_decision", nowu_decision_agent)
workflow.add_node("S5_shape", nowu_shaper_agent)
workflow.add_node("S6_implement", nowu_implementer_agent)
workflow.add_node("S7_review", nowu_reviewer_agent)
workflow.add_node("S8_vbr", nowu_vbr_agent)
workflow.add_node("S9_curator", nowu_curator_agent)

# Conditional routing: S8 VBR fail → loop back to S6
workflow.add_conditional_edges(
    "S8_vbr",
    should_continue_to_s9_or_retry,  # Python function
    {"continue": "S9_curator", "retry": "S6_implement"}
)

# Human approval gate at S4
workflow.add_node("human_approval_s4", human_approval_gate)
workflow.add_edge("S4_decision", "human_approval_s4")
workflow.add_edge("human_approval_s4", "S5_shape")

workflow.set_entry_point("S1_intake")
```

**This is the endgame architecture.** But don't build it until S1-S9 agents exist and work.

---

## Modular Altitude-Phase-Agent/Skills Question

**Your question:** Did we still stick with the modular altitude-phase-agent/skills?

**Answer:** Yes, with refinements.

### The Modular Concept

**Agent** = Prompt + tool access + altitude/phase declaration

**Skill** = Reusable knowledge file (markdown) that teaches agents how to perform a capability

**Workflow** = Sequence of agents operating at appropriate altitudes

**This is still correct.** The modularity lets you:

- Reuse agents across altitudes (Options agent works at PRODUCT, ARCHITECTURE, DELIVERY)
- Compose skills (Research skill + Options skill = research-augmented options agent)
- Test agents independently (unit test: "Does Options agent generate ≥2 alternatives?")

### Refinement from Research

**AFLOW insight:**[cite:555][cite:557][cite:569] Operators (Generate, Review, Test, Revise) are **modular building blocks** that compose into workflows.

**Your agents SHOULD map to operators:**

| Operator | nowu Agent | Altitude Range | Skill(s) |
|---|---|---|---|
| Intake | nowu-intake | PRODUCT, ARCHITECTURE, DELIVERY | intake.md, constraint-elicitation.md |
| Explore | nowu-options | PRODUCT, ARCHITECTURE, DELIVERY | research.md, options-generation.md |
| Decide | nowu-decider | All altitudes | decision-recording.md, rationale-capture.md |
| Shape | nowu-shaper | ARCHITECTURE, DELIVERY | scope-definition.md, acceptance-criteria.md |
| Generate | nowu-implementer | ARCHITECTURE, DELIVERY, EXECUTION | code-generation.md, adr-writing.md |
| Review | nowu-reviewer | ARCHITECTURE, DELIVERY, EXECUTION | review-checklist.md, quality-gates.md |
| Verify | nowu-vbr | DELIVERY, EXECUTION | vbr-protocol.md, test-execution.md |
| Curate | nowu-curator | All altitudes | knowledge-capture.md, lesson-extraction.md |
| Reflect | (GAP agents) | RETROSPECTIVE | pattern-detection.md, health-analysis.md |

**Key insight:** Same agent (nowu-options) + different skill file (architecture-options.md vs. delivery-options.md) = altitude-specific behavior.

**This is how you avoid phase-altitude locking.** The agent is modular; the skill file specializes it.

---

## Revised Implementation Roadmap

### Stage 0: Validate S1-S9 Core Loop (1-2 weeks)

**Goal:** Prove the workflow can complete ONE intake end-to-end.

**Scope:**
- Implement S1, S3, S4, S5, S6, S8, S9 agents (skip S2, S7 for MVP)
- Minimal frontmatter: just `agent`, `date`, `intake_id`
- NO altitude enforcement
- Run manually: human triggers each step, reviews output, approves next step

**Success criteria:**
- Intake-007 completes S1→S3→S4→S5→S6→S8→S9
- Artifacts produced: INTAKE, OPTIONS, DECISION, SHAPE, IMPLEMENTATION, VERIFICATION, LEARN
- Human can read artifacts and understand what happened

**Failure = stop here, redesign workflow before adding altitude complexity**

### Stage 1: Add Altitude Awareness (1 week)

**Goal:** Agents declare their altitude/phase, artifacts validate consistency.

**Scope:**
- Add 4-field frontmatter: `altitude`, `phase`, `epistemic_grade`, `grade_justification`
- Agents declare altitude range in their definition file
- Verification: `verify-artifact.py` checks altitude/phase consistency

**Success criteria:**
- Run intake-007 again, agents correctly label their output altitude
- Altitude drift detector catches if nowu-implementer tries to write STRATEGIC/DECISION

**Defer:** 55-file migration, SYNTHESIS, circuit breakers

### Stage 2: Add Triage (1 week)

**Goal:** Prioritize the queue before starting next intake.

**Scope:**
- Implement Triage Agent (manual RICE scoring or Impact/Urgency matrix)
- Outputs: `state/triage/triage-YYYY-MM-DD.md` with ranked next actions
- Human reviews triage output, picks next intake

**Success criteria:**
- Triage correctly routes: architectural synthesis, delivery intake, or strategic goal revision
- No more "jumping from UCs to epics without global view"

### Stage 3: Add SYNTHESIS (1-2 weeks)

**Goal:** Detect cross-cutting architectural themes BEFORE delivery scoping.

**Scope:**
- Implement SYNTHESIS phase (trigger: ≥2 UCs with `architectural_implications: true`)
- Extract architectural signals (state, contracts, QA, dependencies)
- Cluster UCs into themes (≥2 UCs per theme)
- Recommend ADRs

**Success criteria:**
- Run SYNTHESIS on existing 10 approved UCs
- Detects: knowledge management theme, state isolation theme, LLM client theme
- Human confirms: matches ADR-0004, ADR-0003

### Stage 4: Add Research-Augmented Options Agent (1-2 weeks)

**Goal:** Options grounded in real systems, not just reasoning.

**Scope:**
- Enhance nowu-options agent with web search
- Search for comparable systems, extract patterns
- Cite sources in OPTIONS artifact

**Success criteria:**
- Generate OPTIONS for new ARCHITECTURE/PROBLEM
- Output includes citations to 3-5 comparable systems (GitHub, papers, framework docs)

### Stage 5: LangGraph Orchestration (2-3 weeks)

**Goal:** Automated workflow execution with checkpointing + approval gates.

**Scope:**
- Define LangGraph state machine for S1-S9
- Add conditional routing (S8 fail → S6 retry)
- Add human approval gates (S4, S8)
- Add checkpointing (resume after failure)

**Success criteria:**
- Run intake-007 fully automated
- Human approves at S4 (decision gate) and S8 (VBR gate)
- Workflow resumes after overnight pause

### Stage 6: General AI Assistant (1-2 weeks)

**Goal:** Query interface over workflow state + artifact history.

**Scope:**
- LangGraph query router (classify: artifact lookup, workflow position, blocker analysis)
- Markdown RAG corpus (state/ artifacts + agent definitions)
- Natural language interface

**Success criteria:**
- "What's blocking v1-core?" → returns actual blockers from delivery state
- "Why SQLite per-project?" → returns ADR-0004 rationale
- "Where are we in intake-007?" → returns current phase + next agent

---

## Key Insights for Sisyphus

1. **The altitude model is correct** — It addresses real pain (UC→epic jumping without architecture synthesis). Research validates it (SYSMOD zigzag, Shape Up shaping track, JIT specification).

2. **The implementation order is wrong** — Sisyphus's Package 1 (55-file migration before S1-S9 works) is backwards. AFLOW ran 6,300 workflows THEN extracted operators. You should run 3 intakes THEN add altitude metadata.

3. **Phase multi-altitude flexibility must be restored** — Your original concept (idea-004) was correct: IMPLEMENTATION happens at ARCHITECTURE, DELIVERY, and EXECUTION. Sisyphus locked phases to single altitudes. Revert to your concept.

4. **Triage is the missing primitive** — Neither S1-S9 nor P0-P4 has a "what should we do next?" step. Add Triage Agent (Impact × Altitude assessment) BEFORE Stage 3.

5. **Markdown is correct for your stage** — Don't introduce a database yet. Obsidian is optional but synergistic (graph view, dataview queries).

6. **LangGraph is the right choice** — But defer until S1-S9 agents exist. You need checkpointing + approval gates, which rules out CrewAI.

7. **Research-augmented Options agent is critical** — Your "deep built-in researcher" need = S3 agent + web search + pattern extraction from comparable systems. Build this as enhanced S3 in Stage 4.

8. **DeepAgents is an agent harness, not an orchestration framework** — It's a toolkit. You need orchestration (LangGraph), not just better agents.

9. **Epistemic grades are novel and validated** — Keep them. No comparable mechanism in AFLOW, MASAI, or other frameworks.

10. **SYNTHESIS phase addresses Guo et al.'s multi-hypothesis gap** — Keep it, but defer to Stage 3 (after S1-S9 works).

---

## Recommendations

**Immediate (this week):**
- Accept that altitude model is correct for your pain point
- Reject Sisyphus's 55-file Package 1 as premature
- Implement Stage 0 roadmap: S1-S9 MVP with minimal metadata

**Next 2-3 weeks:**
- Stage 1 (altitude awareness)
- Stage 2 (triage)

**Month 2:**
- Stage 3 (SYNTHESIS)
- Stage 4 (research-augmented options)

**Month 3:**
- Stage 5 (LangGraph orchestration)
- Stage 6 (general AI assistant)

**Do NOT introduce:**
- Database (markdown is correct for <1000 artifacts)
- DeepAgents harness (you need orchestration, not toolkit)
- CrewAI (LangGraph's checkpointing is mandatory for your approval gates)

**Do introduce:**
- Obsidian vault (optional, human UI only)
- Triage agent (critical missing primitive)
- Research augmentation for Options agent (Stage 4)

---

## The Core Trade-Off: Your Instinct Is Right

Your quote:
> "Where is the balance between full spec up-head and we define as we go."

**The research answer:** JIT specification (Just-In-Time spec-driven iteration)[cite:561]

- Write SHORT specs (1-2 pages markdown) BEFORE code
- Update specs EVERY TIME you learn something new
- Specs are living artifacts, not paperwork

**This is exactly what the altitude model enables.** You write:
- PRODUCT/PROBLEM before ARCHITECTURE/OPTIONS
- ARCHITECTURE/OPTIONS before ARCHITECTURE/DECISION
- ARCHITECTURE/DECISION before DELIVERY/SHAPE
- DELIVERY/SHAPE before EXECUTION/IMPLEMENTATION

But each artifact is SHORT, FOCUSED, and UPDATED per iteration.

**You're not doing waterfall.** You're doing spec-driven iteration with explicit altitude boundaries.

**The mistake Sisyphus made:** Treating the altitude model as a comprehensive taxonomy to be implemented all at once (55 files, 3-tier verification). That IS waterfall.

**What you should do:** Treat the altitude model as a **navigation framework**. Agents use it to answer "where am I?" and "what comes next?" But you build incrementally, validating at each stage.

**Lean Startup principle applies:**[cite:578][cite:583]

BUILD (S1-S9 MVP) → MEASURE (does it complete 3 intakes?) → LEARN (where did altitude drift occur?) → BUILD (add altitude metadata)

Not: SPEC (55-file migration) → BUILD (implement agents) → HOPE (it works)

**Your instinct to add steps incrementally as you discovered gaps** was correct. The altitude model gives those steps NAMES and COORDINATES. But you don't implement all 50 altitude/phase combinations upfront—you implement the traversal path you actually use (S1-S9 zigzag), then expand.

**Trust your instinct. Your pain point is real. The altitude solution is validated. The implementation path must be incremental.**
