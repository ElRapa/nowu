---
id: idea-003
created: 2026-04-07
status: DRAFT
size: Story
captured_by: human (Raphael)
session: pre-workflow P1→P4 run
related_ucs: PK-05, PK-09
---

# Idea: Learn on the Way

## Raw Signal

When AI agents research and synthesise domain expertise on my behalf, I want the option
to absorb and retain that knowledge myself — not just receive the answer. The system
should be able to present research outputs in a mode that teaches me, not only informs me.

## Why It Matters

PK-09 (Access Domain Expertise On Demand) delivers answers when I need them. But if I
only ever get the answer and never build my own mental model, I remain permanently
dependent on the system for every related question. In domains where I'm running a
business — food regulation, real estate, supply chain — I want to compound my own
understanding over time, not just the system's knowledge store.

This is different from PK-05 (Build Understanding Incrementally Over a Topic), which is
about patience and accumulation. This idea is about *learning modality*: when AI
researches for me, can it also teach me?

## Concrete Example

I ask nowu to look up the regulatory requirements for importing distilled spirits to the
Philippines. It returns a clear, structured answer. But it could also offer a "learn this"
mode that:
- Explains the principle behind the requirement (not just the rule)
- Surfaces related concepts I should know to navigate this domain
- Tests my recall later ("you learned this 3 weeks ago — still applies?")

## What's Unclear

- Is this a presentation/rendering concern (how knowledge is shown) or a new knowledge
  type (a "teaching atom" vs. a "fact atom")?
- Does this overlap with PK-05 enough to be a story on that UC, or is it genuinely new?
- Is "teach me" something the human opts into per-query, or a project-level setting?
- How does this interact with confidence grading on the knowledge atom — if I've
  "learned" something the system later updates, how does my understanding get refreshed?

## Parking Decision

Captured here for future discovery. Do not force into the current v1-core or v1.1 scope.
Route to P0 idea decomposition when the team has bandwidth to explore it properly.
Likely enters pre-workflow as a Story-size idea at Stage 2 or 3.
