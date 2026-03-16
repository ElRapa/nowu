## Why This Matters

Your nowu workflow (Intake → Architecture → Design → Evaluation → Shaping → Implementation → VBR → Review → Capture) needs to load different context at each phase.
Loading architecture docs during code writing wastes attention budget. Loading code files during architecture analysis creates noise.
## Why Context Scoping Matters for AI
Anthropic's own research on context engineering confirms your instinct. Three key findings: [anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

1. **Context rot is real**: As tokens increase, the model's ability to recall information degrades. It's not a hard cliff but a performance gradient — more tokens means less precision. [anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
2. **Minimal relevant context wins**: Chkk's research shows "less but sharper beats more but messy every single time" — dumping your entire codebase into a prompt is like forwarding your intern every email since 2018. [chkk](https://www.chkk.io/blog/your-ai-agent-needs-minimal-relevant-context-at-the-right-time)
3. **Progressive disclosure**: Rather than pre-loading everything, let agents discover context through exploration — each interaction yields context that informs the next decision. [anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)


## How Your Subagents Enforce This
Your Claude Code subagents (from our previous setup) naturally enforce context scoping because each runs in its own context window: [anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

- **`nowu-architect`** (Read-only tools): Can't accidentally load or edit code during architecture analysis. Operates at C4 Level 1-2. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/4d9cb7d0-fc8f-4bd6-938a-a8d20d2bb82f/ARCHITECTURE.md)
- **`nowu-shaper`** (Read + Bash): Explores file structure but doesn't see implementation internals. Operates at C4 Level 3. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/2b69e660-c251-4975-8a51-ad1b684eab2c/WORKFLOW.md)
- **`nowu-reviewer`** (Read + Bash): Gets fresh eyes on code without accumulated context pollution from earlier phases. [chkk](https://www.chkk.io/blog/your-ai-agent-needs-minimal-relevant-context-at-the-right-time)
- **`nowu-curator`** (Read + Write docs only): Can update DECISIONS.md and PROGRESS.md but cannot touch source code — ensuring capture stays at the system level. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/cc179415-fd38-4770-b162-cb21ffa3680a/DECISIONS.md)


The full context scoping guide with implementation details and anti-patterns is in the downloadable artifact:
## Future: `know` as the Context Engine
When your MemoryService is built (Step 02), `know` becomes the ultimate context scoping tool. Instead of loading raw files, the `flow` orchestrator can request context at the right abstraction level: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/64120149/4d9cb7d0-fc8f-4bd6-938a-a8d20d2bb82f/ARCHITECTURE.md)

```python
# Architect phase: system-level context only
context = know.subgraph(project="nowu", types=["DECISION", "TASK"], max_depth=2)

# Implementer phase: component-level context only  
context = know.subgraph(project="nowu", related_to="session-recovery", types=["ACTION"])
```

This is where your framework becomes genuinely self-developing: `know` serves the right atoms, `flow` orchestrates which abstraction level to request, and each agent role receives only what it needs — no more, no less. [anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)


# nowu Workflow vs SDLC & Architecture Levels — Context Scoping Guide

### Where SDLC Concepts Still Apply

SDLC's strength is its explicit design phases. Your workflow should adopt two SDLC concepts:

1. **HLD before LLD before Code**: The SDLC Design phase explicitly separates high-level design (system architecture) from low-level design (component logic). Your workflow does this implicitly — this guide makes it explicit.
2. **Requirements traceability**: SDLC traces every feature to a requirement. Your use-case IDs (NF-01, PK-03) already do this. Keep it.

---

## 2. Abstraction Levels (C4 Model + HLD/LLD)

### The Four Levels

| Level | C4 Equivalent | HLD/LLD | What It Shows | Who Needs It |
|-------|--------------|---------|---------------|-------------|
| **System Context** | Level 1 | HLD | nowu + `know` + external actors | Architect, stakeholders |
| **Module/Container** | Level 2 | HLD | `core`, `flow`, `bridge`, `soul`, `know` | Architect, Shaper |
| **Component** | Level 3 | LLD | `MemoryService`, `SessionManager`, contracts | Shaper, Implementer |
| **Code** | Level 4 | LLD→Code | Classes, functions, tests | Implementer, Reviewer |

### Key Insight: HLD ↔ LLD is Bidirectional

The testRigor analysis makes a critical point: discoveries during LLD can modify HLD. In your workflow, this means:
- If the Implementer discovers that a shaped task violates a module boundary, it should escalate back to the Shaper (or Architect).
- This is already captured in your Tier system — implementation discoveries that require architecture changes are Tier 3 escalations.

---