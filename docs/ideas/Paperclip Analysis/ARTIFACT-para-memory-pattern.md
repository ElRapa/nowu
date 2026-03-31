# PARA Memory Pattern for nowu Agents

**Inspired by**: Paperclip's file-based PARA memory system (Projects, Areas, Resources, Archives)
**Applies to**: Agents that need persistent memory beyond a single session

---

## When to Use This Pattern

Use PARA memory when an agent needs to remember things across heartbeat cycles that:
- Are not structural enough to be a `know` atom (too informal / too transient)
- Are not captured in artifacts (no explicit file home)
- Would lose context if the agent restarts (Memento Man problem)

---

## PARA Structure for nowu

```
soul/memory/
├── PARA-projects.md      # Active focus: current epics, in-progress tasks
├── PARA-areas.md         # Ongoing responsibilities: architecture principles, standing decisions
├── PARA-resources.md     # Reference material: links, patterns, prior research
└── PARA-archive.md       # Completed cycles, closed epics, resolved decisions
```

---

## PARA-projects.md Template

```markdown
# Projects (Active Focus)
Last updated: YYYY-MM-DD

## Current Epic: epic-NNN — <title>
- Active intake: intake-NNN (status: READY_FOR_S1)
- Active task: task-NNN (status: IN_PROGRESS)
- Story: story-NNN
- Estimated remaining: <Small / Medium / Large>
- Blocking issues: <none | describe>
- Last heartbeat progress: <one sentence>
```

---

## PARA-areas.md Template

```markdown
# Areas (Standing Responsibilities)
Last updated: YYYY-MM-DD

## Architecture Principles
- <ADR-NNN: key constraint>
- <ADR-NNN: key constraint>

## Known Agent Behavioral Patterns
- <agent-name>: tends to over-scope at S5, apply scope hammer
- <pattern>: <mitigation>

## Human Preferences (Tacit Knowledge)
- Prefers short AC lists per task (max 4)
- Approves decisions in batches, not one-by-one
```

---

## PARA-resources.md Template

```markdown
# Resources (Reference Material)
Last updated: YYYY-MM-DD

## Patterns
- [Heartbeat pattern](ARTIFACT-heartbeat-skill.md)
- [Goal ancestry](ARTIFACT-goal-ancestry.md)

## Prior Research
- <topic>: <one-line summary> (see disc-NNN-research.md)

## External References
- <URL or file>: <reason it matters>
```

---

## Compounding Rule

At the end of each S9 capture cycle, the curator agent SHOULD:
1. Move completed tasks from `PARA-projects.md` → `PARA-archive.md`
2. Extract any durable behavioral patterns into `PARA-areas.md`
3. Create `know` atoms for any facts that are important enough to be cross-project knowledge

This prevents `PARA-projects.md` from becoming a graveyard. Only active items live in Projects.

---

## Relationship to `know`

PARA memory is **informal, session-scoped working memory**.
`know` atoms are **formal, structured, searchable knowledge**.

Write to PARA first. Graduate to `know` when a fact is:
- Referenced across more than one project
- Epistemically graded at INFORMED_ESTIMATE or above
- Worth tracking with version history

---

## Why Not Just Use `know` for Everything?

`know` requires a `KnowledgeType`, `epistemic_grade`, and justification. For transient working notes (what happened in the last session, what the human prefers today), that overhead is wrong. PARA is the "scratch pad"; `know` is the "library".
