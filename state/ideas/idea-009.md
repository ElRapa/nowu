---
id: idea-009
created: 2026-05-14
status: DRAFT
tl_dr: "Use claude-code and OhMyOpenCode source as reference implementations for A3 orchestrator design"
linked_work_items: [A3]
human_action_required: "When A3 work begins, ask the human to provide claude-code source and OhMyOpenCode (OmO) source as reference material for orchestrator pattern analysis."
---

# Idea Note: idea-009

## Raw Signal

The A3 work item (orchestrator with altitude routing logic) could benefit from studying
real-world orchestrator implementations in claude-code (Claude's own coding agent) and
OhMyOpenCode (OmO — the tool powering our current workflow). Both implement agent routing,
context scoping, and tool orchestration patterns that are directly relevant to nowu's
orchestrator design.

## Type

- [x] Idea / feature request
- [ ] Bug or broken behaviour
- [ ] Problem observation
- [ ] Architectural concern
- [ ] Other: ___

## Source

- [ ] Personal frustration
- [x] Dogfooding
- [x] Technical opportunity
- [ ] User feedback
- [ ] Market or external observation
- [ ] Other: ___

## Initial Appetite Guess

- [ ] Tiny (< 2 h)
- [ ] Small (< 1 day)
- [ ] Medium (2–3 days)
- [ ] Large (1 week +)
- [x] Unknown — needs decomposition

## Why Now?

Not now — A3 depends on W5 (complete). When A3 enters S2 (constraints), the agent
should load this idea and request the source materials from the human.

## What to Study

- **claude-code**: Agent routing logic, tool permissions, context window management,
  multi-agent coordination patterns
- **OhMyOpenCode (OmO)**: Category-based model routing, skill loading system, background
  agent orchestration, explore/librarian/oracle delegation patterns, session continuity

## How to Surface This

The `human_action_required` frontmatter field is the mechanism. When an agent picks up
A3 and enters S2 (constraints analysis), it should:
1. Check `state/ideas/` for ideas with `linked_work_items` containing A3
2. Read `human_action_required` field
3. Ask the human to provide the referenced source code

## Related Context

- Related ideas: idea-008 (multi-altitude session coordination)
- Related use cases: NF-05 (approval routing), NF-04 (self-assessment)
- Related decisions: D-019 (router-based agents), D-022 (orchestrator layer)
- Related work items: A3 (orchestrator with altitude routing), W-orch (orchestrator layer — done)
