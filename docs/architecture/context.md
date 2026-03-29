---
last_gap: 2026-03-29
---

# nowu — System Context (C4 L1)

> Baseline established by Global Architecture Pass 2026-03-29 (FULL_RESET).
> No prior `context.md` existed. This is the first authoritative C4 L1 boundary document.

```mermaid
C4Context
    title System Context — nowu (Stage 1 v1 · baseline 2026-03-29)

    Person(developer, "Developer (Human)", "Primary user. Triggers workflows via CLI + VS Code. Approves Tier 2 and Tier 3 decisions.")
    Person(ai_agent, "AI Agent (Claude / Copilot)", "Co-producer. Operates every S1–S9 workflow step. Reads state, writes artifacts and code. One specialised agent per step (D-005).")

    System_Boundary(nowu_boundary, "nowu System") {
        System(nowu, "nowu", "AI-assisted software development framework. Modules: core · flow · bridge · soul. Artifact layer: state/ · docs/ · .claude/")
    }

    System_Ext(know, "know (v0.4.0)", "External system of record for durable knowledge atoms, connections, tasks, decisions, and lessons. Accessed via KnowledgeBase + KnowAdapter only (D-006).")
    System_Ext(git, "Git / Version Control", "Source of truth for all code artifacts and Markdown workflow state.")
    System_Ext(filesystem, "File System", "Passive state medium. WAL entries, Markdown artifacts, soul/ identity docs, state/ workflow files. No external service dependency (D-001).")
    System_Ext(vscode, "VS Code / IDE", "Agent execution environment. Loads .claude/rules/ and .github/copilot-instructions.md. Invokes S1–S9 steps.")

    %% ── Future actors (greyed) — not connected until the stage noted in description ──
    Person_Ext(collaborators, "Collaborators / External Users [Stage 3]", "Future team members who onboard via NF-07. Required for AP-07 and RE-07 report delivery.")
    System_Ext(domain_sources, "External Domain Data Sources [Stage 2+]", "Philippines FDA, permit APIs, property registries. Required by AP-01, RE-01.")
    System_Ext(ai_provider, "AI Provider API [future standalone]", "Claude API / Copilot API as explicit dependency when nowu ships as a standalone tool.")
    %% ─────────────────────────────────────────────────────────────────────────────────────

    Rel(developer, nowu, "Commands + approvals", "CLI / IDE")
    BiRel(ai_agent, nowu, "Reads state / writes artifacts", "Agent protocol")
    Rel(nowu, know, "API calls", "KnowledgeBase + KnowAdapter")
    Rel(nowu, git, "Commits, history", "git CLI")
    BiRel(nowu, filesystem, "Read / write", "File I/O")
    Rel(vscode, nowu, "Context loading, agent invocation", "VS Code agent API")

    UpdateElementStyle(collaborators, $bgColor="#e8e8e8", $borderColor="#aaaaaa", $fontColor="#888888")
    UpdateElementStyle(domain_sources, $bgColor="#e8e8e8", $borderColor="#aaaaaa", $fontColor="#888888")
    UpdateElementStyle(ai_provider, $bgColor="#e8e8e8", $borderColor="#aaaaaa", $fontColor="#888888")
```

## External Actor Reference

| Actor | Role | Direction | Stage |
|---|---|---|---|
| **Developer (Human)** | Primary user. Triggers workflows via CLI + VS Code; approves Tier 2/3 decisions. Secondary persona: small-team lead. | → nowu System | v1 — active |
| **AI Agent (Claude / Copilot)** | Co-producer. Dedicated specialised agent per workflow step (D-005). Writes code and artifacts. | ↔ nowu System | v1 — active |
| **`know` (v0.4.0)** | External system of record for all durable knowledge. No internal reimplementation permitted (D-006). Access via `KnowledgeBase` + `KnowAdapter` only. | nowu → know | v1 — active |
| **Git / Version Control** | Source of truth for code artifacts and Markdown state. Decision memory belongs to `know`, not Git. | nowu → Git | v1 — active |
| **File System** | Passive medium for WAL entries, Markdown artifacts, `soul/` identity files, and `state/` workflow state. | ↔ nowu | v1 — active |
| **VS Code / IDE** | Loads `.claude/rules/`, `.github/copilot-instructions.md`. Invokes agent steps. Becomes explicit if nowu ships standalone. | → nowu | v1 — active |
| **Collaborators / External Users** | Future: team members onboarding via NF-07; targets for AP-07, RE-07 reports. | → nowu | Stage 3 |
| **External Domain Data Sources** | Future: Philippines FDA, permit APIs, property registries. Required by AP-01, RE-01. | nowu → sources | Stage 2+ |
| **AI Provider API** | Future: explicit Claude API / Copilot API dependency when nowu ships as a standalone tool. | nowu → provider | Standalone product |
