---
name: session-learning
version: 1.0
mode: any
---

# Skill: Session Learning Capture

## Purpose

Capture decisions, insights, anti-patterns, and process learnings at the end of a
work session. Produces a structured learnings file and updates a running index.
Over time, the index becomes a calibration dataset for workflow optimization.

## When to use

Run at the end of any significant work session:

- After completing one or more S1-S9 steps
- After SYNTHESIS, Architecture Vision, or ADR work
- After multi-hour sessions with design decisions
- After debugging sessions that revealed process issues
- After workflow optimization sessions (like this one)
- When explicitly requested by human

**Do NOT use for:**

- Trivial single-file edits
- Sessions that only read/explored without producing artifacts
- Sessions shorter than 30 minutes with no decisions made

## Outputs

- `state/learnings/session-YYYY-MM-DD-{slug}.md` - Structured learnings file
- `state/learnings/INDEX.md` - Updated running index (append, newest first)

## Orchestration Steps

### L1 - Gather Session Evidence

Review what happened this session. Collect:

1. **Artifacts produced or modified** - list with file paths
2. **Decisions made** - both formal (D-NNN) and informal session decisions
3. **Tools/approaches tried** - what was attempted, including failed attempts
4. **Friction points** - where the process was slow, confusing, or error-prone
5. **What worked well** - approaches, prompts, or patterns worth repeating

Sources to check:
- Files modified this session (git diff or recent changes)
- Todo list (if maintained during session)
- Conversation history (decisions discussed)
- Agent delegations (what was delegated, what came back)

### L2 - Classify Learnings

For each learning, assign exactly one type:

| Type | Definition | Example |
|------|-----------|---------|
| `agent-behavior` | How agents performed; prompt patterns that worked or failed | "Synthesis agent needs ALL UCs, not a sample" |
| `workflow-process` | S1-S9 or P0-P4 process insights; step ordering, handoffs | "S5 shaping catches scope creep that S2 missed" |
| `tooling` | Tool configuration, environment, infrastructure | "uv sync must run before mypy" |
| `domain-insight` | About the problem space, not the process | "Knowledge atom model is foundational for 5/9 themes" |
| `anti-pattern` | Something to actively avoid in future sessions | "Don't synthesize from UC samples - read all" |

### L3 - Write Learnings File

Write to `state/learnings/session-YYYY-MM-DD-{slug}.md` using the template below.

Rules:
- `{slug}` is a 2-4 word kebab-case description (e.g., `synthesis-evaluation`, `workflow-wiring`, `adr-writing`)
- Every insight must have an `Implication` field stating what to do differently
- Every anti-pattern must have both `Temptation` (why it seems reasonable) and `Reality` (why it's wrong)
- Decisions must have `Why it matters` explaining downstream impact
- Keep insights actionable, not philosophical

### L4 - Update Index

Append key items to `state/learnings/INDEX.md`:
- Add a row to the entries table (newest first)
- Summarize the 2-3 most important learnings in the `Key Learnings` column
- If a pattern appears in 3+ sessions, add it to the `Recurring Patterns` section

### L5 - Cross-reference (optional)

If learnings have implications for specific skills or agents:
- Note which skill/agent is affected in the learnings file
- Do NOT modify the skill/agent files directly - that's a separate task
- Add a recommendation to "What Should Happen Next"

## Constraints

- DO NOT modify `src/` or `tests/`
- DO NOT modify existing decisions or ADRs
- DO NOT modify skill or agent definitions (only recommend changes)
- Learnings are descriptive (what happened), not prescriptive (what to change)
- Prescriptive changes go into "What Should Happen Next" as recommendations

## Template

```markdown
---
artifact_type: SESSION_LEARNINGS
session: "{session_description}"
created_at: YYYY-MM-DD
session_type: "{S1-S9 | SYNTHESIS | architecture | debugging | workflow-optimization}"
source_artifacts:
  - {list of artifacts produced or modified this session}
purpose: "{one-line: what was this session about}"
---

# Session Learnings: {session_description}

## What Was Done

{3-5 bullet points summarizing the session's work}

## Decisions Made

### D-SESS-NN: {title}

**Decision:** {what was decided}
**Context:** {why this came up}
**Why it matters:** {downstream impact on workflow, architecture, or future sessions}

---

## Process Insights

### Insight N: {title}

**Observation:** {what happened}
**Type:** {agent-behavior | workflow-process | tooling | domain-insight}
**Implication:** {what to do differently next time}

---

## Anti-Patterns Observed

### Anti-Pattern N: {title}

**Temptation:** {what seems reasonable to do}
**Reality:** {why it's wrong and what happens if you do it}

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| {name} | `{path}` | {status} | {purpose} |

## What Should Happen Next

1. {actionable next step}
2. {actionable next step}
3. {actionable next step}
```

## Relationship to Other Skills

- **synthesis-vision**: Already captures learnings in SV5 (optional). This skill
  formalizes and standardizes that capture. Use this skill instead of ad-hoc SV5.
- **full-cycle / implement-loop**: Run session-learning after completing S9 capture
  to record process insights that capture-record doesn't cover.
- **gap-chain**: Run session-learning after GAP to record what the gap analysis revealed
  about the architecture's health.
