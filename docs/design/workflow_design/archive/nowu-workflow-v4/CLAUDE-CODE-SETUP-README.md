# Claude Code Setup for nowu

This directory contains the complete Claude Code configuration for developing the nowu framework.

## File Structure

```
CLAUDE.md                              ← Root config (auto-loaded every session)
.claude/
├── settings.json                      ← Hooks (VBR enforcement before commits)
├── rules/                             ← Modular rules (auto-loaded)
│   ├── architecture.md                ← Module boundaries, data ownership
│   ├── testing.md                     ← TDD, test organization, quality gates
│   ├── code-style.md                  ← Python standards, naming, docstrings
│   └── workflow.md                    ← Delivery loop, approval tiers, task sizing
├── agents/                            ← Subagents (separate context windows)
│   ├── nowu-architect.md              ← Architecture analysis and decisions
│   ├── nowu-shaper.md                 ← Task breakdown and scoping
│   ├── nowu-reviewer.md               ← VBR enforcement and quality review
│   └── nowu-curator.md                ← Decision/lesson/progress capture
└── skills/                            ← Reusable workflows (main context)
    ├── full-cycle/SKILL.md            ← Complete delivery cycle
    └── implement-step/SKILL.md        ← Execute a V1 plan step
```

## How to Use

### First Session
```bash
claude                                 # Start Claude Code in the nowu repo
# Claude auto-loads CLAUDE.md + all rules
```

### Implement the Next Step
```
Use the implement-step skill to execute Step 02 from V1_PLAN.md
```

### Full Feature Cycle
```
Use the full-cycle skill for: [describe the feature or goal]
```

### Run Individual Agents
```
Use the nowu-architect agent to evaluate: [architecture question]
Use the nowu-shaper agent to break down: [goal or framed problem]
Use the nowu-reviewer agent to review recent changes
Use the nowu-curator agent to capture what we just decided
```

### Quick Implementation (no agent delegation)
```
Implement [specific task] using TDD. Follow the workflow rules.
```

## Agent Memory
All agents use `memory: project` (stored in `.claude/agent-memory/`).
Over time, agents accumulate knowledge about the codebase:
- Architect remembers architectural patterns and tradeoffs
- Shaper learns effective task sizes and boundary patterns
- Reviewer tracks recurring issues
- Curator knows what gets forgotten between sessions

## Future: Replacing with Framework Agents
These Claude Code agents mirror the roles defined in WORKFLOW.md:
- `nowu-architect` → `flow` Architect role
- `nowu-shaper` → `flow` Shaper role
- Implementer → main Claude Code session (later: `flow` Implementer)
- `nowu-reviewer` → `flow` Reviewer role + VBR loop
- `nowu-curator` → `flow` Curator role → `know` persistence

When `flow` module is implemented (Steps 03-04), these agents can be gradually
replaced by the framework's own role pipeline. The subagent definitions serve
as executable specifications for what the framework roles should do.
