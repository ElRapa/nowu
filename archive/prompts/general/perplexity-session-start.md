# Perplexity Session Start Prompt

Use this at the start of any Perplexity conversation about nowu.

---

I am working on the **nowu framework** — a modular monolith for personal and project knowledge management, task tracking, and AI-agent orchestration. Here is the architecture context:

**Five modules:**
- `know`: knowledge atoms (types: fact, concept, task, decision, lesson, reference, preference, ephemeral), SQLite storage, FTS5 search, workflow lifecycle, today-view
- `soul`: VISION.md, AGENTS.md, ADR decisions (files only, no code)
- `flow`: agent orchestration, session state (WAL), conversation capture → know atoms
- `bridge`: MCP server, CLI proxy (nowu continue / today / status / approve)
- `dash`: web UI (v2 only, not yet implemented)

**Key decisions already made:**
- Task = KnowledgeAtom with type="task"
- SQLite + FTS5, no ORM
- workflow_state is computed (not stored)
- Conversation capture: auto at session end + manual `know capture`
- PARA maps to: project_scope field + status=archived

**Current v1 status:** [FILL IN WHICH STEPS ARE DONE]

**My question today:** [FILL IN YOUR QUESTION]

Please respond with this context in mind. If I ask you to help design or analyze something, reference the architecture. If I need to update a decision, remind me to add it to DECISIONS.md.
