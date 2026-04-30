# Evaluation on two new ideas 
that are not yet in the vision or use cases but are important enough to be added.

## My prompt:
I like your changes. I have some more ideas which might be useful for vision or use-cases.md. Tell me what you think of them and add them if useful:
1. I am thinking that I would like to use nowu from everywhere. It is like a daily helper. And I do have ideas whereever i am. Not only when I am at home at my computer. And because the main lift is happening by AI. I should not be restricted to use only the computer. 
2. The knowledge-layer has different views. For example it is atomar. So that we can build proper knowledge-graphs with each atom with it's own epidemistic-grade or source or connection. And a view which allows humans to let atoms or subgraphs comprehend quickly (for example by reading, visual or whatever is the best method for humans). And a view for AI-agents.


***
# The Evalutation:

## Idea 1: nowu as a daily helper from everywhere

**This belongs in the vision, not just the use cases.**[1]

It reframes the *access model* of nowu entirely. Right now the vision implies a computer-first, session-first workflow — you sit down, open a terminal or file, run an agent. But if "the AI carries 90–99% of the work" and "the human just shows up and moves forward," then logically the human should be able to show up from a phone, a voice note, a quick message — anywhere an idea or a decision happens.[2][1]

This also closes a real gap against the primary persona: Raphael "loses context easily, picks things back up after gaps, carrying the guilt of half-finished ideas." That guilt often comes from ideas that appear on a commute or at dinner and vanish because the capture point is too far away.[1]

**Where it fits:**
- A short addition to **Our Solution** in vision.md: nowu is not just a desktop workflow — it is a daily presence accessible wherever the human is.
- A new **use case PK-08: Capture and Act from Any Device or Context** in USE_CASES.md.
- It also directly strengthens the "minimum viable human attention" supporting guideline — the system must work at the level of attention the human actually has in that moment, not the level they have when sitting at a desk.

**One thing to be careful about:** "from everywhere" should not imply a full web app or mobile product in v1. The vision already says "no web UI in v1." But capturing a thought via a minimal interface (a message, a voice note, a quick API call) and having AI process it asynchronously is very different from a full UI — and consistent with the "AI carries the work" model.[1]

***

## Idea 2: Atomic knowledge layer with multiple views

**This is one of the most architecturally significant ideas you've had and it is currently missing from both documents.**[2][1]

It has three distinct components that deserve to be named separately:

**A. Atomicity** — knowledge is stored as discrete, self-contained atoms, each with its own epistemic grade, source, and relationships. This is what makes the knowledge graph queryable, trustable, and non-monolithic. A "fact" and a "working hypothesis" are different atoms with different weights.[3][1]

**B. The knowledge graph** — atoms are connected by typed relationships (supports, contradicts, depends on, refines, etc.). This is what enables cross-project discovery, conflict detection, and the "system learns by running" principle to actually work mechanically.[2][1]

**C. Multiple views of the same graph** — this is the smartest part of the idea:
- **Human-readable view:** atoms and subgraphs condensed into summaries, visual maps, or narrative — whatever helps a human understand quickly without reading raw data.
- **AI-agent view:** structured, machine-readable, filterable — the exact context an agent needs for a specific task, scoped ruthlessly per the second guiding principle.[1]
- **The same underlying data powers both.** No separate documentation for humans, no separate prompt construction for agents — one knowledge layer, multiple lenses.

**Where it fits:**
- This is important enough to warrant a sentence in the **Our Solution** chapter of vision.md — it is part of what nowu *is*, not just how it works.
- It should inform a new **use case XP-11: Query the Knowledge Graph in Role-Appropriate Format** in USE_CASES.md.
- It also strengthens and concretizes the guiding principle "Know how much to trust each piece of knowledge" — epistemic grading is not abstract anymore, it is a property of every atom.[1]

***

## Proposed additions

### Vision.md — Our Solution (small addition)

Add one sentence to the "under the hood" paragraph:

> The knowledge layer is atomic — every fact, decision, lesson, and idea is stored as a discrete unit with its own source, confidence grade, and relationships to other atoms. This same knowledge graph is rendered differently depending on who is reading it: condensed and visual for the human, structured and scoped for the AI agent — same data, different lenses.[1]

***

### PK-08: Capture and Act from Any Context

| Field | Detail |
|---|---|
| **Actor** | Human (mobile, voice, remote); Ingestion Agent |
| **Situation** | The human is not at a computer. They are on a commute, at a supplier meeting, walking between tasks. An idea, a decision trigger, or a relevant observation appears. The capture moment is brief and the interface is limited — a phone, a voice message, a quick text. |
| **Need** | Capture the input with minimal friction regardless of device or context. The AI handles all classification, linking, and enrichment asynchronously. The human is not required to structure anything at capture time — that overhead happens later, invisibly. |
| **Success looks like** | The human sends a 15-second voice note: "The pili nut supplier said they can only guarantee supply until November." By the time the human is back at a computer, the note has been transcribed, linked to AP supply chain knowledge, flagged as a risk in the AP-03 use case context, and queued for human confirmation. |
| **Failure looks like** | Capturing a thought away from the computer requires opening a CLI, running a command, or navigating to a specific file. The friction is high enough that the human uses a paper napkin instead. The idea is lost. The system that was meant to reduce guilt about half-finished ideas adds to it. |
| **Open questions** | What is the minimum viable capture interface for v1 — a messaging bot, a web form, a voice API? How should low-context captures (a two-word note) be handled vs. rich captures (a voice memo with detail)? Should the human confirm AI enrichment before it's committed, or can enrichment be provisional and self-correcting? |

***

### XP-11: Query the Knowledge Graph in Role-Appropriate Format

| Field | Detail |
|---|---|
| **Actor** | Human (reader); AI Agent (consumer); System (renderer) |
| **Situation** | The knowledge base contains hundreds of atoms across multiple projects. A human wants to understand "what do we know about our pili nut supply risk?" An AI agent needs the same underlying data to make a scoping decision. The raw graph is too dense for the human and potentially mis-structured for the agent. |
| **Need** | Render the same knowledge subgraph in a format matched to the consumer: a human-readable summary or visual map for the human, a structured, scoped, and confidence-graded context block for the AI agent — without duplicating or maintaining separate versions of the knowledge. |
| **Success looks like** | The human asks "what do we know about pili nut supply?" and receives a 3-paragraph narrative with a risk summary and confidence indicators. The AP-Options Agent reads the same subgraph as a structured JSON context with atoms ranked by confidence and freshness — and can trace each claim back to its source. Neither consumer had to request a different format; the system inferred what was needed. |
| **Failure looks like** | The human has to read raw Markdown knowledge files to understand what the system knows. AI agents are fed full narrative documents and have to re-parse them for relevant facts. Low-confidence atoms are not distinguished from high-confidence ones in either view. The knowledge base grows but becomes harder, not easier, to use. |
| **Open questions** | Should view format be determined by the actor type (human vs. agent) automatically, or should both be explicitly requestable? How do we handle knowledge atoms that belong to multiple subgraphs — do they appear in all relevant views, or only the most closely related? At what scale does the knowledge graph need an indexing or search layer rather than traversal? |

***

Should I now produce a **complete updated USE_CASES.md** with all 11 new use cases (NF-10 through NF-13, XP-08 through XP-11, PK-07, PK-08, AP-08) added in the right sections, and a small addition to vision.md for the atomic knowledge layer and everywhere-access ideas?

Sources
[1] vision.md 
[2] USE_CASES.md 
[3] GRADE: an emerging consensus on rating quality of evidence and ... https://pmc.ncbi.nlm.nih.gov/articles/PMC2335261/
