---
last_updated: 2026-03-31
last_approved: 2026-03-31
status: APPROVED
version: 2.0
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

The gap between having an idea and making it real has always been a problem of sustained
attention, direction, and memory. Now that AI can carry enormous amounts of the work, the
bottleneck has shifted — it's no longer *can I build this?* but *can I keep everything
moving toward what I actually want, across many sessions, many projects, many
interruptions?* Individual sessions feel productive but rarely add up to a coherent,
evolving body of work. The problem is not capability. It is continuity: the absence of
something that remembers what matters, holds the thread when you drop it, pulls back when
things drift — one that grows more useful the longer it runs, so that six months in, you
still trust your own past reasoning.

## For Whom

### Primary Persona

**Raphael — the multi‑project human.** Runs several things at once across different domains — software, a business venture, a creative project — and uses AI heavily for all of them. Loses context easily and feels the low‑grade guilt of stalled projects and half‑finished ideas, which he has to keep picking back up again. Wants steady, meaningful progress without having to keep everything in his head, and does not want to manage a system; wants a system that manages itself well enough that he can just show up and move forward.

### Secondary Personas

Other people who use AI to get things done — developers, founders, makers — who want their projects to have direction and memory, not just great individual sessions.

Anyone with a goal longer than a todo list — building a business, learning a skill, running a project — who needs more structure than a notes app but less overhead than a team.

## Our Solution

nowu is a product‑centric AI workflow — the layer between having a goal and making it real. Where vibe‑coding gives you momentum inside a session, nowu makes the project progressively more defined across sessions: it holds the project's intent, decisions, and the reasoning behind them — so nothing disappears between sessions and the AI always knows what it's building toward. The more you use it, the more it knows — the vision sharpens, the decisions compound, and the knowledge becomes part of the product itself.

## Core Value Proposition

nowu is the difference between a project that compounds and one that resets.

For anyone turning a real idea into a real outcome, nowu is the continuity layer that keeps AI working toward what actually matters — unlike general AI tools that feel productive in a session but accumulate nothing between them.

nowu holds the full thread: goals, decisions, reasoning, and lessons — structured, actively fed back into every new session, across every project. Direction is enforced. Progress compounds. And six months in, you still trust why you're building what you're building.

## Success Horizons

### 6 Months — The workflow is yours

nowu runs its own development using itself. The AI carries the full cycle — discovery, architecture, implementation, and capture — with 90–99% of the work handled by AI, and a human can start from a vague idea and get meaningful output without the process feeling like overhead. The experience is genuinely enjoyable — low friction, clear feedback, visible progress. At least two real projects outside software are active and growing, and you trust what nowu knows about each project because you've seen it hold the thread through real interruptions.

### 12 Months — Knowledge compounds across projects

At least six projects are active across different domains, including both software and non-software work. They do not interfere with each other; knowledge accumulates within each project and starts to connect usefully across them through a shared, queryable knowledge base. Someone else could pick up any project from the artifacts alone, because the workflow, decisions, and reasoning are durable enough to survive the original builder stepping away. The workflow itself improves with each cycle — the path from vision to shipped becomes faster, more direct, and clearer.

### 24 Months — It runs the operation

nowu is infrastructure, not just a tool. Every project, decision, and capture flows through it — a company operating system by practice, not just by claim. It is stable enough to ship as a framework, installable product, or service that other people adopt, with collaboration and data governance built in as natural parts of how the system works. nowu is a full collaboration layer for humans and AI, and a knowledge-layer which is accessible in the best ways for both.

## What We Are NOT

1. **We are not a human replacer.** Full automation from a single prompt to a finished product is not the goal. nowu relies on minimal, meaningful human interaction to set direction and verify intent; AI handles the execution.

2. **We are not a task manager for humans.** We keep state so the AI stays oriented and the human stays informed — but no Gantt charts, no manual sprint boards, no overhead for its own sake. If it feels like bureaucracy, we built it wrong.

3. **We are not a walled garden.** Where possible we build on open formats. Where we need something new — a knowledge graph, a structured memory layer — it stays inspectable, portable, and yours.

4. **We are not an LLM provider or code-generation assistant.** We orchestrate agents to solve problems systematically, not write code directly.

5. **We are not built for enterprise (yet).** nowu is optimized for solo builders and small, fast-moving teams. We are deliberately trading enterprise scale and compliance for speed and personal alignment.

## Guiding Principles

### Foundation

**0. Artifacts are the API.** Agents do not communicate through conversations — they communicate through structured, version-controlled files. A broken artifact breaks the pipeline visibly; a broken conversation fails silently and leaves nothing behind. Every principle in this framework works because artifacts are the persistent interface between agents, between sessions, and between the human and the system.

### Core Principles

**1. Memory is the infrastructure.** Both humans and AI forget. Every session must leave behind structured, durable state that the next session can reliably pick up — not a transcript, not a summary, but a living artifact that actively shapes what happens next. Without persistent memory, continuity is a promise the system cannot keep.

**2. Scope ruthlessly.** Only what is relevant to the current step belongs in the current session — for the human and for the AI. Context is curated, not dumped. An agent that sees everything sees nothing well; a human that is asked for everything gives nothing useful.

**3. Clarity is earned, not imposed.** A vague start is expected and fine. The workflow protects the early fuzzy phase and resolves ambiguity progressively through structured doing, not by forcing decisions before they are ready. Premature structure is as dangerous as no structure at all.

**4. Different work lives at different altitudes.** Vision, goals, decisions, architecture, and implementation each live at the right level of abstraction. Agents operating at one altitude do not bleed into another. Discovery does not touch architecture; architecture does not prescribe implementation details. Altitude discipline is what keeps the system coherent over time.

**5. Decisions are provisional and traceable.** Every significant decision is recorded, marked with its confidence level, and linked to what depends on it — so it can be found and changed when new information arrives. A decision made today may be correct today and wrong in three months; the system makes that easy to find and easy to update, not buried and fragile.

**6. The system learns by running.** Every cycle is an opportunity to absorb what worked, what drifted, and what the world has learned — from past decisions and from new external sources. Using nowu improves nowu. The longer it runs, the more aligned, efficient, and trustworthy it becomes.

### Supporting Guidelines

- **Right role, right task.** Specialized agents outperform generalists. Each agent has one job at one altitude — focused, bounded, and replaceable without affecting the rest of the system.
- **Small steps, not big leaps.** Incremental changes that can be validated beat large changes that cannot. If a step is too big to verify, it is too big to take.
- **Multiple options before a decision.** At key decision points — especially high-altitude ones — generate at least two paths before committing. The best option is rarely the first one.
- **Know how much to trust each piece of knowledge.** Not all decisions and facts are created equal. The system distinguishes confident, validated knowledge from working hypotheses and early-stage ideas — so future sessions know how much weight to give each piece.
- **If it feels like bureaucracy, we built it wrong.** Every interaction the human has with nowu should feel necessary and worthwhile. Overhead that does not serve the work is a design failure, not a feature.

---

> **Human:** Review the above, update anything that no longer reflects your intent,
> then set `status: APPROVED` and `last_approved: YYYY-MM-DD`.
