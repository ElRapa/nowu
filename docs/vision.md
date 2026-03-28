---
last_updated: 2026-03-26
last_approved: 2026-03-26
status: APPROVED
version: 1.0
stage: 1
product: nowu
workflow_level: Above C4
---

# Product Vision: nowu

> **Lifecycle:** Created/updated by `vision-bootstrap` agent (P0.V) via structured interview.
> Human must set `status: APPROVED` and `last_approved` before any new epic is started.
> To refresh: run `/health-check vision`. If YELLOW or RED, re-run `/pre-workflow P0.V`.
> This file is read at: P0.2 (alignment check), P0.UC (use-case-agent), P1.1 (discovery-agent),
> S1 (nowu-intake), health-vision, health-goals, health-use-cases.

---

## The Problem

Solo developers and small teams building with AI agents lose continuity between sessions,
accumulate architectural drift, and have no reliable way to trace why decisions were made
— causing repeated mistakes, scope creep, and frameworks that become too fragile to evolve.
The problem is not the absence of tools, but the absence of **durable, structured memory**
that persists across sessions, projects, and team members and that actively shapes agent
behavior.

## For Whom

### Primary Persona

**Raphael — the solo AI-first developer.** Works across multiple projects simultaneously
(developer tooling, SaaS, business automation, personal knowledge). Uses Claude and other AI
agents heavily. Needs to resume work after interruptions without re-explaining context,
enforce architectural decisions without a team to police them, and trust that AI-generated
output traces back to real intent. Wants fast, but easy-going progress in all his projects, with heavy AI-support starting from a vague idea. Looses context and project track from time to time.

### Secondary Personas

**The small-team technical lead.** 2-4 people, heavy AI usage, no dedicated QA or architect.
Needs the same durability and traceability guarantees as the solo developer, but with
multi-project and multi-person isolation.

## Our Solution

nowu is an AI-first development framework that provides durable memory, structured
decision-making, and reliable execution loops for solo developers and small teams. It runs
as a multi-agent workflow (P0-P4 pre-workflow + S1-S9 implementation) on top of any
codebase, using version-controlled Markdown artifacts as the only persistent state — no
external services, no databases, nothing that can drift out of sync with the code.

## Core Value Proposition

For solo developers building with AI agents, nowu is the operational layer that makes AI
assistance reliable and traceable — unlike general-purpose AI tools that provide a great
session but no continuity — because every decision, every piece of work, and every lesson
learned is recorded, structured, and actively fed back into the next session.

## Success Horizons

### 6 Months — v1 core operational

nowu manages its own development using itself. A developer can resume work within minutes
after any interruption. All architectural decisions are recorded and enforced. Every
delivered feature traces back to a use case. At least one non-framework project (Aperitif
or RE digitalization) is bootstrapped and active.

### 12 Months — framework shipped and dogfooded across 3+ projects

nowu is usable as a framework by anyone who clones the repo. The pre-workflow (P0-P4)
handles ideation-to-intake for any size idea. The `know` module provides persistent
semantic memory across sessions. Health checks run automatically. The framework has been
used for at least 3 distinct project domains.

### 24 Months — platform and potential SaaS

nowu evolves into an installable tool or managed service. Projects can be shared with
collaborators. The knowledge graph (`know`) becomes queryable across projects. The
framework is stable enough to ship as a product to other AI-first developers and small teams.

## What We Are NOT

1. nowu is not a general-purpose project management tool (no Gantt charts, no ticket boards).
2. nowu is not a code generation assistant — it orchestrates agents, it does not write code directly.
3. nowu does not replace version control — Git is the source of truth for code; nowu manages the decision layer above it.
4. nowu does not serve large teams, enterprise workflows, or multi-tenant SaaS in v1.
5. nowu does not provide a web UI in v1 — all interaction is via CLI and Markdown files.

## Guiding Principles

1. **Artifacts are the API.** Agents communicate through structured files, not conversations.
   A broken artifact breaks the pipeline visibly; a broken conversation fails silently.
2. **Problem space before solution space.** Discovery and problem definition always precede
   architecture and implementation. Agents in discovery mode are constitutionally prohibited
   from touching architecture.
3. **Continuity over completeness.** A smaller, reliably resumable system is worth more than
   a feature-complete one that loses context. Every step of the workflow must leave state
   that survives a crash.

---

> **Human:** Review the above, update anything that no longer reflects your intent,
> then set `status: APPROVED` and `last_approved: YYYY-MM-DD`.
