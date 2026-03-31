# Org Chart Pattern for nowu Multi-Agent Orchestration

**Inspired by**: Paperclip's hierarchical org chart model with CEO/CTO/Engineer/QA roles

---

## The Insight

Paperclip structures agents as a company org chart: CEO sets strategy and delegates, CTO manages technical direction, Engineers implement, QA verifies. This produces:
- Clear decision authority (who approves what)
- Clear context scope (CEO doesn't read source code; engineer doesn't read vision docs)
- Natural escalation paths (engineer → CTO → CEO)

nowu already has this encoded in the S1–S9 step structure, but without explicit role names or a "reporting" mental model.

---

## nowu Role Map (Org Chart Style)

```
Human (Board of Directors)
  └─ nowu-intake (S1)         ← Context analyst, above C4
       └─ nowu-constraints (S2)  ← Architect, L1–L2
            └─ nowu-options (S3)    ← Solution designer, L2
                 └─ nowu-decider (S4)  ← Decision authority, L2 [HUMAN GATE]
                      └─ nowu-shaper (S5)   ← Product manager, L3 [HUMAN GATE]
                           └─ nowu-implementer (S6–S7)  ← Engineer, L4
                                └─ nowu-reviewer (S8)   ← QA, L3–L4
                                     └─ nowu-curator (S9)  ← Scrum master, L1–L2
```

---

## Key Insight: Context Isolation = Quality

Each agent's **quality** depends on it NOT loading context from the wrong level.

| Agent | Loads | Forbidden |
|---|---|---|
| nowu-intake | vision, USECASES, PROGRESS | src, architecture docs |
| nowu-constraints | intake, ARCHITECTURE, DECISIONS, arch-pass | src internals, tests |
| nowu-options | constraints-sheet, contracts, module surfaces | Full ARCHITECTURE.md, src internals |
| nowu-decider | options-sheet, DECISIONS | src, tests, contracts |
| nowu-shaper | decision handoff, file tree, contracts, test structure | ARCHITECTURE.md, DECISIONS.md, vision |
| nowu-implementer | task spec + in_scope_files ONLY | Everything else |
| nowu-reviewer | VBR, changeset, task spec, git diff, .clauderules | Full arch docs, upstream artifacts |
| nowu-curator | review report, DECISIONS, PROGRESS, intake, git log | src, tests |

This is Paperclip's key insight applied to nowu: **context boundaries = architectural integrity**.

---

## Applying the Pattern

When adding a new agent or step:
1. Assign it a C4 level (Above C4 / L1-L2 / L3 / L4)
2. Define exactly what it loads and what it never loads
3. Define its output artifact and gate type (auto / human)
4. Give it a role title (makes it easier to reason about authority)

---

## Multi-Company → Multi-Project

Paperclip runs multiple "companies" in one deployment with data isolation. nowu's equivalent is `project_scope` in `know` — every atom, task, and artifact is scoped to a project. This enables cross-project knowledge discovery without cross-project contamination.
