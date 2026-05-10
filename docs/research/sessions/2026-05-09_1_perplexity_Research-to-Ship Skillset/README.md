# Research-to-Ship Skillset

**Package for OmO to implement the Perplexity → OmO research handoff workflow.**

---

## What's in This Package

| File | Purpose |
|------|---------|
| `research-artifact-schema.yaml` | Formal schema for structured research artifacts |
| `research-artifact-example.md` | Complete filled example of a structured artifact |
| `evaluate-research-skill.md` | Skill definition for `/evaluate-research` |
| `implementation-guide.md` | Step-by-step guide for OmO to implement the skill |
| `README.md` | This file |

---

## Quick Start

1. **Read `implementation-guide.md`** — follow step-by-step instructions
2. **Create `.claude/skills/evaluate-research.md`** — copy from `evaluate-research-skill.md`
3. **Test with example** — use `research-artifact-example.md` as test input
4. **Integrate with Perplexity** — Perplexity adds structured YAML to reports, you consume it

---

## Workflow Overview

```
┌─────────────┐
│ Perplexity  │ Research + generate structured artifact (YAML)
└──────┬──────┘
       │
       │ Manual handoff (copy YAML)
       ▼
┌─────────────┐
│    OmO      │ /evaluate-research [artifact]
│             │ → Generate alternatives
│             │ → Score each alternative  
│             │ → Recommend best option
│             │ → Create implementation plan
└──────┬──────┘
       │
       │ Present to user
       ▼
┌─────────────┐
│    User     │ Review alternatives, approve chosen option
└──────┬──────┘
       │
       │ Approval
       ▼
┌─────────────┐
│    OmO      │ /implement-choice [decision_doc] [A|B|C]
│             │ → Execute changes
│             │ → Verify changes
│             │ → /session-learning (save insights)
│             │ → /ship (commit changes)
└─────────────┘
```

---

## Implementation Phases

### Phase 1: Structured Artifacts (Immediate)
- **Perplexity:** Add structured YAML section to all future research reports
- **OmO:** Consume YAML manually (no skill yet)
- **Goal:** Validate format works for 2-3 sessions

### Phase 2: /evaluate-research Skill (Next Week)
- **OmO:** Implement `/evaluate-research` skill
- **Perplexity:** Continue providing YAML artifacts
- **Goal:** OmO can now auto-generate alternatives + recommendation from artifacts

### Phase 3: /implement-choice Skill (After 2-3 Uses)
- **OmO:** Implement `/implement-choice` skill
- **Goal:** Full evaluate → approve → implement flow is automated

### Phase 4: /research-to-ship Pipeline (After 5+ Uses)
- **OmO:** Chain the 4 skills (evaluate → implement → learn → ship)
- **Goal:** One-command flow from research artifact to shipped changes

---

## Design Principles

1. **Modular:** Each skill works standalone. Pipeline is optional.
2. **Human-in-the-loop:** Approval gate is load-bearing. Never skip it.
3. **Structured > Prose:** YAML artifacts are easier to parse than prose.
4. **Fallback gracefully:** If input is prose, extract structure and validate with user.
5. **Immutable decisions:** Decision docs don't change after creation. New info → new doc.

---

## Schema Version History

- **v1.0 (2026-05-09):** Initial schema with alternatives, evaluation, implementation plan

---

## Questions?

- Schema unclear? See `research-artifact-example.md` for a complete filled example.
- Implementation stuck? See `implementation-guide.md` for step-by-step instructions.
- Need clarification? Ask Perplexity to refine the skill definition.

---

**Status:** Ready for Phase 1 implementation (structured artifacts).
