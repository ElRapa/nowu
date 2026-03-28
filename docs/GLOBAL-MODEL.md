# GLOBAL-MODEL — C4 Model and Workflow Levels

## 1. Levels Overview

Simon Brown’s C4 model provides four zoom levels for software architecture.
Each level answers a different question and serves a different audience.

| Level | Name | Question | Audience | nowu Artifact |
|-------|------|----------|----------|---------------|
| Above C4 | Problem Space | What problem? For whom? Why now? | Product owner, Stakeholders | `docs/vision.md`, `state/problems/`, `docs/V1_PLAN.md` |
| L1 | System Context | What does the system do? Who uses it? | Stakeholders, Architect | `ARCHITECTURE.md` §1 |
| L2 | Containers / Modules | How do modules interact? | Architect, Shaper | `ARCHITECTURE.md` §4.1 |
| L3 | Components | What files/classes exist? | Shaper, Implementer | `core/contracts/`, file tree |
| L4 | Code | How does it work internally? | Implementer, Reviewer | `src/`, `tests/` |

Above C4 is where **vision, product stages, and problem statements** live.
C4 L1–L4 describe the **software system** that serves that vision.

---

## 2. Workflow × Level Mapping (P0–P4 and S1–S9)

This table answers: *for each phase/step, what “level” should agents and humans think at,
and which artifacts are primary?*

| Phase / Step | Level | Primary Focus | Main Artifacts (read/write) |
|--------------|-------|---------------|------------------------------|
| P0 – Signal Capture (vision bootstrap, idea note, decomposition) | Above C4 | Idea, product vision, stage, appetite | `docs/vision.md`, `docs/V1_PLAN.md`, `state/ideas/idea-NNN.md`, `state/pre-workflow/NNN-decomp.md` |
| P1 – Discovery (research + interview + problem statement) | Above C4 | Problem, personas, outcomes, appetite | `state/discovery/disc-NNN-research.md`, `state/problems/problem-NNN.md` |
| P2 – Story Mapping (epic + stories) | Above C4 → edge of L1 | User behaviour, use cases, acceptance criteria | `docs/USE_CASES.md`, `state/epics/epic-NNN.md`, `state/stories/story-NNN-*.md` |
| P3 – Architecture Bootstrap | L1–L2 | System boundary, module map, invariants | `docs/architecture/context.md`, `docs/architecture/containers.md`, `state/arch/arch-pass-NNN.md`, `docs/architecture/adr/` |
| P4 – Readiness Assembly | Above C4 + pointers into L1–L2 | Handoff contract into S1 | `state/pre-workflow/NNN-readiness.md`, `state/intake/intake-NNN.md` |
| S1 – Intake | Above C4 | Confirm problem, appetite, use cases | `state/intake/intake-NNN.md`, `docs/vision.md`, `docs/V1_PLAN.md`, `docs/PROGRESS.md`, `docs/USE_CASES.md` |
| S2 – Constraints | L1–L2 | System + module constraints, risks | `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `core/contracts/`, `state/arch/arch-pass-NNN.md` (if present) |
| S3 – Options | L2 | Module interaction options | `state/arch/intake-NNN-constraints.md`, `core/contracts/`, module `__init__.py` |
| S4 – Decision | L2 | Choose option, record decision | `state/arch/intake-NNN-options.md`, `docs/DECISIONS.md` |
| S5 – Shaping | L3 | Files/classes, task boundaries | `state/arch/intake-NNN-decision.md`, file tree, `core/contracts/`, `tests/` structure, `state/tasks/task-NNN.md` |
| S6–S7 – Implementation + VBR | L4 | Code and tests | `state/tasks/task-NNN.md`, `src/`, `tests/`, `state/changes/`, `state/vbr/` |
| S8 – Review | L4 → L3 | Code vs component intent, story coverage | `state/vbr/vbr-task-NNN.md`, `state/changes/changes-task-NNN.md`, `state/tasks/task-NNN.md`, `state/stories/story-NNN-*.md`, `git diff` |
| S9 – Capture | L1–Above C4 | System impact, product progress, next cycle | `state/reviews/review-task-NNN.md`, `docs/DECISIONS.md`, `docs/PROGRESS.md`, `state/intake/intake-NNN.md (next_cycle_trigger)`, `state/capture/capture-task-NNN.md` |

**Rule of thumb:**  
- Pre‑workflow lives mostly **Above C4**, with a single dip into L1–L2 at P3.  
- S1–S4 stay at **Above C4 → L2**, S5–S7 at **L3–L4**, S8 bridges **L4→L3**, S9 zooms back to **L1 / Above C4**.

---

## 3. Global Architecture Pass (GAP)

GAP sits **above** any single NNN and covers C4 L1/L2 for the whole product.
It is implemented by the gap-chain skill: gap-detector → gap-analyst → gap-writer, operating on gap-trigger.md and global-pass-YYYY-MM-DD.md.
- Triggered by: product stage change, large UC catalog changes, or repeated RED health-architecture checks.
- Output: updated global ARCHITECTURE.md §1 and §4.1, plus ADRs capturing structural choices.
- Effect: P3 Architecture Bootstrap for individual epics must respect GAP decisions unless explicitly proposing new ADRs.

GAP is the city plan; P3 is local building placement.

---

## 4. Practical C4 for nowu v1

These are the concrete anchors for each level in *this* codebase:

- **Above C4**  
  - Vision and stages: `docs/vision.md`, `docs/V1_PLAN.md`  
  - Problems/stories: `state/problems/`, `state/epics/`, `state/stories/`  

- **L1 – System Context**  
  - `ARCHITECTURE.md` §1 describes the system boundary and actors.  
  - Updated when major external dependencies or user roles change (typically via P3/S2/S9).

- **L2 – Containers / Modules**  
  - `ARCHITECTURE.md` §4.1 defines the 5-module map (`core`, `flow`, `bridge`, `soul`, `know`).  
  - Updated at **P3.2** (arch-pass) and reconciled at **S2/S9** when boundaries change.

- **L3 – Components**  
  - `core/contracts/*.py` protocol files *are* the component graph for agents.  
  - S5 and S8 should treat these contracts + the file tree as the source of truth for L3.

- **L4 – Code**  
  - `src/` and `tests/` contain implementations.  
  - AST-based tests (for example `tests/unit/core/test_architecture.py`) enforce import boundaries
    and guard the L2/L3 rules at code level.

---

## 5. Code Property Graph (future — via `know`)

A Code Property Graph (CPG) merges three representations into one queryable graph:

- **AST** (Abstract Syntax Tree): syntactic structure — what the code *says*.  
- **CFG** (Control Flow Graph): execution order — *when* things run.  
- **PDG** (Program Dependence Graph): data dependencies — *what flows where*.

CPG enables queries like:

- “Show all paths from user input to file write.”  
- “Which functions depend (directly or indirectly) on `MemoryService`?”  

**Today (v1)**  
- Use AST-based tests to enforce import and layering rules.  
- Keep C4 diagrams as the human-facing model.

**Future (v2+)**  
- Store code atoms and edges (`CALLS`, `FLOWS_TO`, `IMPLEMENTS`) in `know`.  
- Allow queries like `kb.subgraph(from="MODULE:flow", depth=3)` to reconstruct C4 views
  without loading raw files.

---

## 6. Why C4 Is the Primary Visual Model

CPG is for machines. It’s excellent for deep analysis but bad for motivation and communication.

C4’s explicit **Above C4 → L1 → L2 → L3 → L4** zoom, plus your pre‑workflow and S1–S9,
gives a clean narrative:

- Start with **why** (vision, problems, outcomes).  
- Decide **what** the system is and how it’s sliced (L1/L2).  
- Shape **how** it’s implemented (L3/L4).  
- Then zoom back out and update the vision/plan if reality changed.

Use:

- **C4 + pre‑workflow levels** for all diagrams, docs, onboarding, and agent scoping.  
- **CPG‑style analysis** only when `know` has enough code atoms to make it worthwhile.
