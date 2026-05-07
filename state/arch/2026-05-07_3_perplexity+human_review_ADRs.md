<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# For the session-state/checkpoints. With that approach we only have one session. What if we have multiple open. One for general assistant. one for Implementation, etc. Should we change our approach ADR-0007?

ADR-0008:
Will the docs (like architecture) be a atom at some point?

And in general:
We create artifacts in one go. Our workflow is doing the option creation and decision, etc on other altudues. Should we add that? Maybe our quality would increase here.

Excellent questions. All three touch on real architectural tensions. Here are direct answers:

***

## Q1: Multiple Concurrent Sessions — Should ADR-0007 Change?

**Short answer: YES — ADR-0007 needs refinement, but the core two-layer checkpoint design is correct.**

### The Problem

ADR-0007 assumes **one active session at a time** with a single `checkpoint-latest.json`. But you're right — the actual usage pattern will be:

- **Session A**: "General assistant" — answering questions, orienting you, surface-level help
- **Session B**: "Implementation session" — running S1-S9 intake cycles, making architectural changes
- **Session C**: "Research/exploration" — NF-12 vague idea exploration, no-commitment mode

These sessions have **different lifecycle requirements**:

- Session A is **always active** — it's your daily entry point (PK-03 "today view")
- Session B is **task-bounded** — starts at S1, ends at S9 capture, checkpoints every step
- Session C is **ephemeral** — may never reach S1, might be abandoned without capture


### What Should Change in ADR-0007

**Add a `session_type` field to the checkpoint schema**:

```yaml
SessionCheckpoint:
  session_id: str
  session_type: SessionType  # NEW: ASSISTANT | INTAKE | EXPLORATION | ARCHITECTURE
  ...
```

**Storage changes**:

```
state/sessions/
  ├── assistant/                    # One persistent session
  │   └── checkpoint-latest.json
  ├── intake-001/                   # Task-bounded, archived after S9
  │   ├── checkpoint-latest.json
  │   └── checkpoint-{id}.json      # Audit trail
  └── exploration-{date}/           # Ephemeral, may be GC'd
      └── checkpoint-latest.json
```

**Recovery protocol change**:
When an agent starts:

1. Check if a `target_session_id` was provided (explicit resume)
2. If not: default to the **assistant session** for orientation
3. Assistant session presents "today view" (PK-03) which includes:
    - Open intakes with next actions
    - Exploration sessions that became something
    - Cross-project orientation

**Add this to ADR-0007's "What's Missing" section**:
> - **No multi-session model** — assumes one active session, but real usage requires concurrent assistant, intake, and exploration sessions with different lifecycle properties

**Action**: Add a note in ADR-0007 that this is a **v1-core simplification** and will be extended in v1 with multi-session support. The two-layer checkpoint design (machine + human) remains correct — just the storage hierarchy and session type taxonomy need to be added.

***

## Q2: Will Architecture Docs Be Atoms Eventually?

**Short answer: SOME will, SOME won't — it's a type distinction.**

### The Knowledge Atom Boundary

**What SHOULD become atoms** (durable, queryable, cross-project knowledge):

- **Decision atoms** (D-021, ADR-0008 decisions): "We chose option B because X" — this is durable memory
- **Constraint atoms** (from S2): "We can't use Postgres because Y" — persistent constraint
- **Lesson atoms** (from S9 capture): "VBR caught 3 type errors in module X" — generalizable learning
- **Architectural principles** (from Architecture Vision): "Principle P2: artifacts are the interface" — persistent governance

**What should NOT become atoms** (operational, transient, or too large):

- **Full ADR documents**: Too large, too structured — they're **artifacts** (files), not atoms
- **SYNTHESIS-001**: A synthesis report is a **derived artifact**, not an atomic piece of knowledge
- **Architecture Vision**: This is a **narrative document**, not a queryable fact

**BUT**: Each ADR should produce **derived atoms** when it's accepted:

- ADR-0008 → atom: `"knowledge atom schema has 7 required fields"` (type: `constraint`)
- ADR-0007 → atom: `"session checkpoints are two-layer: machine JSON + human markdown"` (type: `principle`)
- ADR-0010 → atom: `"agents can assign grades up to INFORMED_ESTIMATE only"` (type: `rule`)


### The Pattern: Artifacts → Atoms

The nowu model is:

```
Large artifacts (ADRs, SYNTHESIS, Architecture Vision)
    ↓ (extraction at S9 or acceptance)
Atomic knowledge (decisions, constraints, principles, lessons)
    ↓ (stored in `know`)
Queryable, cross-project, decay-managed knowledge graph
```


### Where This Happens

**S9 (nowu-curator)** is the extraction point:

- At the end of an intake, S9 reads the full session artifacts
- Extracts key decisions, constraints, and learnings
- Creates knowledge atoms in `know` via the `MemoryService`
- Archives the full artifacts (they remain as files, but the **essence** is now queryable)

**ADR-0008 already anticipates this**:
> "At S9 Capture, the session's key decisions and learnings are promoted to knowledge atoms in `know` (per ADR-0008). The session checkpoint itself is NOT an atom — it is transient operational state."

### Action for ADR-0008

Add a new section: **"Artifact-to-Atom Extraction"**

```markdown
## Artifact-to-Atom Extraction

Large structured artifacts (ADRs, SYNTHESIS, Architecture Vision) are NOT stored as atoms directly.
Instead, at acceptance or S9 capture, key facts are extracted as individual atoms:

| Artifact Type | Extracts To | KnowledgeType | Example |
|---|---|---|---|
| ADR (accepted) | 2-5 atoms | `constraint`, `principle`, `rule` | "session continuity requires two-layer checkpoints" |
| SYNTHESIS | 5-10 atoms | `theme`, `architectural_question` | "T2: knowledge lifecycle spans 17+ UCs" |
| Architecture Vision | 3-5 atoms | `principle`, `quality_attribute` | "Principle P2: artifacts are the interface" |
| S4 Decision | 1 atom | `decision` | "Chose Typer for CLI (rejected Click)" |

The full artifact remains as a file. The atoms make its essence queryable.
```

**Answer to your question**: Docs don't *become* atoms — they **produce** atoms. The document is the source of truth; the atoms are the queryable index.

***

## Q3: Should We Add SYNTHESIS/OPTIONS/DECISION Steps to Agent Creation?

**Short answer: YES — and you're already doing it implicitly. Making it explicit would improve quality.**

### What You're Doing Now (Implicit SYNTHESIS → DECISION)

When you asked Omo to create the `synthesis-agent` and `architecture-vision-agent`:

1. You **framed the problem** (handoff-synthesis-session.md) — this is **ANALYSIS phase**
2. Omo **analyzed the need** (what should this agent do?) — **ANALYSIS phase**
3. Omo **wrote the agent** (the artifact) — **IMPLEMENTATION phase**

But you **skipped**:

- **OPTIONS phase**: "What are 2-3 different agent design patterns for SYNTHESIS?"
- **DECISION phase**: "Which pattern should we adopt and why?"


### Why This Matters

The quality risk is that agents are written **reactively** (one approach, justified after the fact) rather than **deliberately** (multiple options considered, tradeoffs explicit).

This is exactly what NF-13 (Multiple Options at Decisions) is designed to prevent: "The system must generate and present at least 2 viable approaches before committing to implementation."

### What It Would Look Like

#### For Agent Creation (DELIVERY altitude)

```
Phase                   Output
INTAKE                  "We need a synthesis-agent to extract themes from UCs"
ANALYSIS                "Synthesis requires: full UC read, theme clustering, ADR recommendations"
OPTIONS                 OPTIONS-synthesis-agent-design.md — 3 approaches:
                          1. Single-pass agent (reads all, outputs themes)
                          2. Two-pass agent (extract → cluster → synthesize)
                          3. Interactive agent (presents themes, human refines)
DECISION                DECISION-synthesis-agent.md — "Chose Option 1 because..."
IMPLEMENTATION          synthesis-agent.md (the agent definition file)
VERIFICATION            Test: run on 10 UCs, validate theme extraction
```


#### For Architecture (ARCHITECTURE altitude)

You already did this correctly for W1-W2:

```
Phase                   Output
SYNTHESIS               SYNTHESIS-001.md — themes across all UCs
ANALYSIS                ARCHITECTURE-VISION.md — principles, quality attributes
DECISION                (implicit) — "These are the hypothesis ADRs to write"
IMPLEMENTATION          ADR-0007, 0008, 0009, 0010 (W3)
VERIFICATION            Fitness functions (W3.5)
```


### Should You Formalize This?

**For high-impact artifacts (agents, ADRs, core workflows): YES.**

**Add to WORKFLOW.md** (or create AGENT-CREATION-WORKFLOW.md):

```markdown
## Agent Creation Workflow (Altitude: DELIVERY, Phases: INTAKE → VERIFICATION)

1. INTAKE: Agent need identified (which altitude? which phase?)
2. ANALYSIS: Agent responsibilities, inputs, outputs, constraints
3. OPTIONS: 2-3 agent design patterns (prompt structure, tool access, scoping)
4. DECISION: Select pattern with rationale
5. IMPLEMENTATION: Write agent definition file
6. VERIFICATION: Test agent on sample input
```

**For routine artifacts (bug fixes, small refactors): NO.**
You don't need OPTIONS/DECISION for "fix typo in S3 prompt" — that's over-engineering.

### The Altitude Rule

Use the full OPTIONS → DECISION → IMPLEMENTATION cycle when:

- **ARCHITECTURE altitude**: Always (ADRs, SYNTHESIS, Architecture Vision)
- **DELIVERY altitude**: For agents, workflow changes, core design decisions
- **EXECUTION altitude**: Only for non-trivial implementation choices (algorithm selection, data structure choice)

**SYNTHESIS → DECISION is expensive** — it takes 2-3x longer than direct implementation. Use it where the cost of a wrong decision is high (hard to reverse, affects many downstream artifacts).

### Action for Your Current State

**Immediate (W3)**: Run hypothesis-adr-agent as-is — Omo already validated the ADR approach through the W1-W2 cycle.

**v1 improvement**: When you create the **orchestrator agent** (the `flow` module router), use the full cycle:

1. INTAKE: "We need an orchestrator that routes S1-S9 agents per ADR-0009"
2. ANALYSIS: "Orchestrator must validate handoffs, enforce gates, handle failures"
3. OPTIONS: "Option A: State machine class. Option B: Event-driven bus. Option C: Declarative config."
4. DECISION: "Chose Option A because..."
5. IMPLEMENTATION: Write the orchestrator agent
6. VERIFICATION: Run first intake with orchestrator active

The orchestrator is **high-impact** (it's the router from D-019) — it deserves the full cycle.

***

## Summary Recommendations

| Question | Answer | Action |
| :-- | :-- | :-- |
| **Q1: Multi-session support** | ADR-0007 needs extension | Add `session_type` + storage hierarchy in v1; note the gap in ADR-0007 as "v1-core simplification" |
| **Q2: Docs as atoms** | Docs → extract atoms, don't store as atoms | Add "Artifact-to-Atom Extraction" section to ADR-0008 |
| **Q3: Add OPTIONS/DECISION to agent creation** | Yes, for high-impact artifacts | Formalize in AGENT-CREATION-WORKFLOW.md; apply to orchestrator agent in v1 |

All three observations are architecturally sound. Q1 and Q2 are **refinements** to existing ADRs (flag them, defer to v1). Q3 is a **process improvement** you can adopt immediately for high-impact work.
<span style="display:none">[^1]</span>

<div align="center">⁂</div>

[^1]: e9f6c64a-7d94-44d3-8f77-fc9e58bc9ad6.md

