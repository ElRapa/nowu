# Package 2: Phase-Operator Agent Definitions

**Purpose:** Create 10 phase-operator agents — one per phase — that enforce the 5×10 model rules within their cognitive domain.

**Prerequisite:** Package 1 (metadata foundation) must be complete and verified.

---

## What to Build

Create one agent definition per phase. Each agent:
- Operates at its phase across ALL permitted altitudes (phases are cognitive modes, not altitude-locked)
- Enforces epistemic grade thresholds appropriate to its altitude context
- Produces artifacts with correct frontmatter (per ARTIFACT-TEMPLATE.md)
- Respects human gates at DECISION phases

### Agent List

| Agent | Phase | Permitted Altitudes | Key Responsibility |
|---|---|---|---|
| idea-agent | IDEA | ALL | Capture raw ideas, tag with origin altitude, assign SPECULATION grade |
| problem-agent | PROBLEM | ALL | Structure problems from ideas, identify constraints, map stakeholders |
| analysis-agent | ANALYSIS | ALL | Research and evidence gathering, upgrade epistemic grades with justification |
| synthesis-agent | SYNTHESIS | ARCHITECTURE only | Cross-cutting UC analysis, theme grouping, ADR recommendations |
| options-agent | OPTIONS | ARCHITECTURE, DELIVERY | Generate 2-4 evaluated alternatives with tradeoff matrices |
| decision-agent | DECISION | ALL | Facilitate human gates, record rationale, create ADR/approval artifacts |
| evaluation-agent | EVALUATION | ARCHITECTURE, DELIVERY | Post-decision fitness checks, security review triggers |
| implementation-agent | IMPLEMENTATION | ARCHITECTURE, DELIVERY, EXECUTION | Write artifacts (ADRs, shapes, code) matching altitude context |
| verification-agent | VERIFICATION | STRATEGIC, ARCH, DELIVERY, EXEC | Validate against acceptance criteria, run automated checks |
| learn-agent | LEARN | ALL | Extract lessons, promote insights upward after abstraction |

### Per-Agent Definition Must Include

1. **Identity block**: Name, phase, permitted altitudes
2. **Input contract**: What artifacts/context this agent receives
3. **Output contract**: What artifacts this agent produces (with frontmatter schema)
4. **Epistemic rules**: Minimum grade at creation, advisory threshold, gate threshold (per altitude from WORKFLOW-STANDARDS-v1.1.md §3)
5. **Altitude behavior**: How the agent's work differs at each permitted altitude
6. **Transition rules**: When to hand off to next phase, what triggers completion
7. **Human gate**: Whether this phase requires human approval (DECISION phases always do)
8. **Anti-patterns**: Common mistakes to avoid (e.g., implementation-agent writing code at ARCHITECTURE altitude)

---

## Implementation Approach

### Step 1: Create Agent Template
Use `templates/agent-definition-template.md` as the base. Each agent definition follows the same structure.

### Step 2: Define Each Agent
For each of the 10 agents, fill in the template with phase-specific rules from:
- `docs/MODEL-REFERENCE.md` — phase definitions, altitude mappings
- `standards/WORKFLOW-STANDARDS-v1.1.md` — binding rules
- `docs/IMPLEMENTATION-GUIDE.md` — artifact schemas

### Step 3: Verify Agent Consistency
Cross-check all 10 agents against:
- [ ] Every phase has exactly one agent
- [ ] Permitted altitudes match MODEL-REFERENCE.md phase-altitude matrix
- [ ] Epistemic thresholds match WORKFLOW-STANDARDS §3 tiered table
- [ ] Input/output contracts form a complete chain (agent N's output = agent N+1's input)
- [ ] Human gates are present at all 5 DECISION points (WORKFLOW-STANDARDS §2.3)
- [ ] SYNTHESIS agent is altitude-locked to ARCHITECTURE

---

## Critical Rules (from v1.1 corrections)

1. **Phases are cognitive modes** — Do NOT restrict agents to single altitudes (except SYNTHESIS)
2. **S1–S9 zigzag** — Agents must support the altitude descent pattern, not flat EXECUTION
3. **Epistemic grades are tiered** — Use the 3-column threshold table, not a single bar
4. **LEARN promotes upward** — learn-agent is the only agent that pushes information up the altitude stack

---

## Success Criteria

- [ ] 10 agent definitions created, one per phase
- [ ] All agents reference correct altitude permissions
- [ ] Agent chain is complete: IDEA → PROBLEM → ANALYSIS → SYNTHESIS → OPTIONS → DECISION → EVALUATION → IMPLEMENTATION → VERIFICATION → LEARN
- [ ] No agent contradicts WORKFLOW-STANDARDS-v1.1.md rules
- [ ] Human gates documented at all DECISION points
