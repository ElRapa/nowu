# Update for MODEL-REFERENCE.md: Add Orchestrator Layer Section

**Location:** Insert after the "Phase Types" section and before "Altitude × Phase Examples"

---

## Orchestrator Layer (External to 5×10)

The orchestrator is a **meta-layer** that sits **outside** the 5×10 execution grid. It decides what work enters the field, when, and in what sequence. The orchestrator is not a phase type — it is a separate system that operates on the field from the outside.

### Why the Orchestrator is External

Every mature workflow system separates:
- **Execution**: The actual work (SENSE, PROBLEM, ANALYSIS, etc. inside the 5×10 field)
- **Orchestration**: Deciding what work happens next (external to the field)

Examples from industry:
- **Shape Up**: The betting table (cooldown) decides what work enters the 6-week cycle
- **SAFe**: PI Planning decides what work enters the next 8-12 week Program Increment
- **Temporal**: Workflow tasks (orchestration) coordinate Activity tasks (execution)
- **AFLOW**: The optimizer generates and refines workflows but is not a node inside the workflow

The nowu orchestrator follows this pattern: it is a **planning agent that feeds work into the 5×10 execution agents**.

### Orchestrator Agents (Meta-Level)

These agents live in `.claude/agents/orchestrator/` and are **not part of the 19 execution agents** in the standard roster.

| Agent | Trigger | Altitude | Phase | Input | Output |
|---|---|---|---|---|---|
| `roadmap-creator` | P0.V+P0.G complete, 10+ UCs exist | STRATEGIC | IMPLEMENTATION | vision, goals, partial UCs | ROADMAP-001.md |
| `roadmap-updater` | SYNTHESIS complete, Arch Vision complete, stage gates | STRATEGIC | LEARN | current ROADMAP-NNN.md + milestone artifact | ROADMAP-NNN+1.md |
| `work-scheduler` | User asks "what's next?" or agent completes task | N/A (meta) | N/A (query) | current ROADMAP-NNN.md + system state | Next work item decision (console output) |

**Key distinction:**
- Execution agents (19 agents in roster) operate **inside** the 5×10 field and have altitude + phase assignments
- Orchestrator agents (3 meta-agents) operate **outside** the field and decide what work enters the field next

### Orchestrator Artifacts

| Artifact | Location | Versioned? | Grade Progression | Purpose |
|---|---|---|---|---|
| `ROADMAP-NNN.md` | `docs/` | Yes (version number in filename and frontmatter) | HYPOTHESIS → INFORMED_ESTIMATE → EVIDENCE_BASED | System of record for "what's next" and stage sequencing |

**Why `docs/` not `state/`:**
- `state/` contains session-specific work artifacts (transient)
- `docs/` contains canonical project-level documentation (durable)
- ROADMAP is project-level, not session-specific — it lives alongside vision, goals, and decisions

**Grade progression:**
- HYPOTHESIS: Initial roadmap based on vision + goals + early UCs
- INFORMED_ESTIMATE: Updated after SYNTHESIS or Architecture Vision (architectural evidence added)
- EVIDENCE_BASED: Updated after stage gates (actual execution data validates or refines estimates)

### Orchestrator vs. Execution Layer

| Property | 5×10 Execution Layer | Orchestrator Layer |
|---|---|---|
| **What it does** | Executes work (SENSE, PROBLEM, ANALYSIS, etc.) | Decides what work to execute next |
| **Where it lives** | Inside the 5×10 grid (altitude × phase) | Outside the grid (meta-level) |
| **Agents** | 19 execution agents (nowu-intake, nowu-shaper, etc.) | 3 meta-agents (roadmap-creator, roadmap-updater, work-scheduler) |
| **State location** | `state/` (session artifacts) | `docs/` (versioned roadmap) |
| **Epistemic grade** | Starts at SPECULATION, improves to EVIDENCE_BASED | Starts at HYPOTHESIS, improves with milestone feedback |
| **Triggered by** | Orchestrator or user | Milestones (SYNTHESIS, Arch Vision, stage gates) or user query |
| **Output** | Artifacts in `state/` or `docs/` | ROADMAP-NNN.md (versioned) or console decision (query) |

### Invocation Flow

```
User: "What should I work on next?"
  ↓
work-scheduler reads ROADMAP-003.md + state/
  ↓
work-scheduler: "Next is W4 (First S1-S9 intake), status: READY"
  ↓
User invokes nowu-intake (execution agent, DELIVERY/SENSE)
  ↓
nowu-intake executes S1 inside the 5×10 field
  ↓
nowu-intake completes, writes INTAKE-001.md to state/
  ↓
User: "What's next?"
  ↓
work-scheduler: "Next is S2 (constraints)"
```

**Key insight:** The orchestrator never executes work itself — it only decides what work the execution agents should do next.

### Orchestrator Invocation Points

The orchestrator is invoked at **milestone boundaries**, not during execution:

```
P0.V  Vision Bootstrap         [execution: STRATEGIC/DECISION]
P0.G  Goal Brief Creation      [execution: STRATEGIC/DECISION]
      ↓
      [10-20 UCs captured]
      ↓
🔵    roadmap-creator          [orchestrator: creates ROADMAP-001.md]
      ↓
P0.UC Continue UC capture      [execution: PRODUCT/PROBLEM]
      ↓
P1-P4 (as needed per epic)     [execution: various altitudes]
      ↓
W1    SYNTHESIS                [execution: ARCHITECTURE/SYNTHESIS]
W2    Architecture Vision      [execution: ARCHITECTURE/ANALYSIS]
      ↓
🔵    roadmap-updater          [orchestrator: ROADMAP-001 → ROADMAP-002]
      ↓
W3    Write hypothesis ADRs    [execution: ARCHITECTURE/IMPLEMENTATION]
      ↓
🔵    roadmap-updater          [orchestrator: validate readiness → ROADMAP-003]
      ↓
W4    First S1-S9 intake       [execution: DELIVERY/full cycle S1-S9]
      ↓
      [v1-core stage gate]
      ↓
🔵    roadmap-updater          [orchestrator: record actuals → ROADMAP-004]
```

**Note:** Blue circles (🔵) are orchestrator invocations; all other steps are execution inside the 5×10 field.

### When to Use Which Agent

| Scenario | Agent | Why |
|---|---|---|
| Just finished P0.V + P0.G, have 10+ UCs, no roadmap exists | `roadmap-creator` | Bootstrap the initial plan |
| SYNTHESIS-001 just completed | `roadmap-updater` | Integrate ADR roadmap and architectural themes |
| Architecture Vision just completed | `roadmap-updater` | Integrate risks and quality attribute priorities |
| Just passed a stage gate (v1-core → v1) | `roadmap-updater` | Record actuals, adjust future estimates |
| User asks "what should I work on next?" | `work-scheduler` | Query current roadmap + system state to decide next work item |
| Agent completes a task and signals "ready for next work" | `work-scheduler` | Automatic progression to next work item |

### Hard Constraints

1. **Orchestrator agents MUST NOT execute work inside the 5×10 field** — they only decide what work happens next
2. **ROADMAP-NNN.md is the single source of truth for sequencing** — execution agents MUST consult the roadmap (via work-scheduler) before starting work
3. **Orchestrator artifacts MUST be versioned** — every roadmap update creates a new version with `supersedes` field
4. **Epistemic grade MUST NOT decrease** — roadmaps can only improve in confidence or stay the same
5. **work-scheduler is read-only** — it never modifies the roadmap, only queries it

### Integration with Existing Model

The orchestrator layer **does not replace** any part of the 5×10 model — it **complements** it:

- **5×10 field**: Execution agents do the work (SENSE, PROBLEM, ANALYSIS, etc.)
- **Orchestrator**: Meta-agents decide what work enters the field next

**Analogy:**
- 5×10 field = the players on the field executing plays
- Orchestrator = the coach on the sideline deciding which play to run next

The coach is not on the field, but the players cannot function without the coach deciding the next play.
