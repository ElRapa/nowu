---
version: 1.0
generated_from: global-pass-2026-04-06
status: DRAFT
last_gap_check: 2026-04-06
---

# nowu — C4 L1 System Context

## Narrative

nowu is a **local Python CLI tool** running on a single machine, for a single human user.
It is not cloud-hosted, not SaaS, and not multi-tenant through v1.2. The system boundary is
clear: all project data is stored locally; the only external compute dependency is an LLM API
called over the network (outbound only). At v1 — after the v1-core CLI is stable — a messaging
platform adapter is added to `bridge` to support remote access (PK-08).

### Primary Actor

**Raphael — the Multi-Project Human.**
Initiates captures, reads daily orientation, approves decisions, resumes any of several
concurrent projects (software, food business, real estate). Not always at a desk — needs
the system to meet him via mobile, voice, or remote interface. Does not want to manage the
system; wants it to surface what matters and hold the thread between sessions.

### System Boundary Statement

nowu runs locally as a Python process. There is no server, no authentication service,
no JWT, no Kubernetes, and no cloud storage through v1.2. The three external systems it
interacts with are:

1. **LLM API** — outbound reasoning calls; the only non-local compute.
2. **External Documents** — PDFs, Markdown files, URLs ingested by the PK-07 pipeline.
3. **Remote Interface** — a messaging platform (Telegram) enabling PK-08's capture,
   review, and light-action modes from any device. Added at v1, after v1-core CLI is stable.

---

## System Context Diagram (C4 L1)

```
%%{init: {'theme': 'default'}}%%
C4Context
    title nowu — System Context

    Person(raphael, "Raphael", "Multi-project human. Captures ideas, reads today view, approves decisions, resumes projects across domains.")

    System(nowu, "nowu", "Local Python CLI. Continuity layer between having a goal and making it real. Holds project intent, decisions, and knowledge across sessions.")

    System_Ext(llm, "LLM API", "Claude / GPT. Provides reasoning and completion for all agent steps. Called by flow (workflow agents) and soul (analytical tasks).")
    System_Ext(ext_docs, "External Documents", "PDFs, Markdown, URLs. Regulatory documents, market reports, specs. Ingested by PK-07.")
    System_Ext(remote_iface, "Remote Interface", "Messaging platform (e.g. Telegram). Capture/review/light-action from mobile. v1 stage, after v1-core CLI is stable.")

    Rel(raphael, nowu, "Captures ideas, reads orientation, approves decisions, reviews state")
    Rel(nowu, llm, "Sends agent prompts, receives reasoning and completions")
    Rel(nowu, ext_docs, "Ingests knowledge atoms from external sources (PK-07)")
    Rel(nowu, remote_iface, "Sends digest + action prompts; receives captures and approvals (PK-08)")
    Rel(remote_iface, raphael, "Delivers digest, receives input from any device")
```

---

## External Systems

| External System | Why it exists | UC anchor |
|---|---|---|
| **LLM API** (Claude / GPT) | Provides reasoning, completion, and synthesis for all agent steps in `flow` and analytical tasks in `soul`. The only non-local compute dependency. | NF-01 through NF-14 (all agent-driven workflow UCs); soul UCs |
| **External Documents** | PDFs, Markdown files, URLs — regulatory documents, market reports, product specs — ingested by PK-07 and processed into knowledge atoms. | PK-07 |
| **Remote Interface** (messaging platform, v1) | Enables PK-08's three interaction modes (capture, review, light action) from mobile/remote without a CLI session. Adapter in `bridge`. | PK-08 |

---

## Stage Boundary Note

| Stage | Interface Model |
|---|---|
| **v1-core** (now — ~3 months) | Local single-user CLI only. `bridge` is a Typer CLI. No remote interface. No messaging platform dependency. |
| **v1** (~6 months, after v1-core stable) | Messaging platform adapter added to `bridge` (PK-08). Telegram selected as the first non-CLI adapter. The adapter implements `AdapterProtocol` in `bridge` — no new top-level module. |
| **v1.1 – v1.2** | Additional know capabilities, domain projects (AP, RE). Single-user local model unchanged. |
| **v2** | Multi-user access control (XP-10) — beyond scope of this context document. Architecture remains local-first at v1.2. |

---

## Key Decisions

The following binding decisions directly shape this L1 context:

| Decision | What it means for L1 |
|---|---|
| **D-011** — Per-project SQLite isolation | `know` maintains one SQLite file per project locally. No cloud database. `core` is I/O-free; only `know` holds DB connections. Cross-project queries are federated inside `know`, not via a shared external store. |
| **D-012** — Artifact-based soul↔flow coupling | `soul` and `flow` do not call each other at runtime. They communicate exclusively via `state/` artifacts on the local filesystem. This means all data held by nowu is local and inspectable; there is no hidden inter-process channel. |
| **PK-08 / Q2 Resolution** — Telegram selected | The Remote Interface (v1) is Telegram via python-telegram-bot. This is the only external platform runtime dependency through v1.2. The adapter lives in `bridge`; `flow`, `soul`, and `know` are unaware of it. |
