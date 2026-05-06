---
artifact_type: HANDOFF
created_at: 2026-05-06
target_session: "SYNTHESIS + Architecture Vision"
source_session: "5×10 Workflow Model Design"
prerequisite_reading:
  - state/arch/5x10-session-synthesis-2026-05-06.md
  - docs/STAGED-PLAN.md
  - docs/model/MODEL-REFERENCE.md
  - docs/research/5x10-session-insights-2026-05-06.md
status: ACTIVE
---

# Handoff Brief: SYNTHESIS + Architecture Vision Session

## What This Session Must Produce

Two artifacts (plan tasks W1 and W2 from `docs/STAGED-PLAN.md`):

1. **SYNTHESIS-001** → `state/arch/SYNTHESIS-001.md`
   - Cross-cutting themes extracted from all 50 approved UCs
   - ADR recommendations: which architectural questions the themes raise
   - Theme-to-UC mapping (which UCs contribute to each theme)

2. **Architecture Vision** → `docs/architecture/ARCHITECTURE-VISION.md`
   - System identity: what KIND of system nowu is (not what it does — vision.md covers that)
   - Architectural principles derived from SYNTHESIS themes
   - Quality attribute priorities (ranked, with tradeoffs)
   - Key risks and constraints
   - Recommended hypothesis ADRs to write next

## Why This Matters

The project is blocked here:

```
Goals (4)          ✅ exist
UCs (50)           ✅ approved
                   ↓
         ┌── BLOCKED ──┐
         │ No global   │
         │ synthesis   │
         │ across UCs  │
         └─────────────┘
                   ↓
ADRs (6)           ⚠️ exist but not connected to UC themes
S1-S9              ❌ never run end-to-end
```

Without SYNTHESIS, every intake (S1) starts from scratch — no shared architectural understanding, no cross-cutting themes to guide options (S3) or decisions (S4). The result is patchwork architecture.

## Input Files (Read These)

### Primary Inputs (MUST read)

| File | What It Contains | How to Use It |
|---|---|---|
| `docs/USE_CASES.md` | All 50 approved UCs with stage targets | **THE** input to SYNTHESIS — read every UC |
| `docs/vision.md` | Product vision v2.0 (approved) | System identity framing |
| `docs/goals/goal-001.md` | Momentum survives interruptions (6mo) | Goal-to-theme alignment |
| `docs/goals/goal-002.md` | AI-led, low-friction workflow (6mo) | Goal-to-theme alignment |
| `docs/goals/goal-003.md` | Knowledge compounds across projects (12mo) | Goal-to-theme alignment |
| `docs/goals/goal-004.md` | Trusted infrastructure / shippable (24mo) | Goal-to-theme alignment |

### Context Inputs (Read for constraint awareness)

| File | What It Contains | How to Use It |
|---|---|---|
| `state/arch/5x10-session-synthesis-2026-05-06.md` | All decisions from the model design session | Constraints on the 5×10 model |
| `docs/STAGED-PLAN.md` | Areas × stages implementation plan | Where SYNTHESIS outputs feed |
| `docs/DECISIONS.md` | Existing D-001 through D-012 | Don't contradict these |
| `docs/architecture/adr/ADR-0001..0006` | Existing ADRs | Don't contradict; note gaps |

### UC Categories (50 total)

| Prefix | Domain | Count | Relevance to SYNTHESIS |
|---|---|---|---|
| NF | Framework capabilities | 16 | HIGH — these define core architecture |
| PK | Personal knowledge | 9 | HIGH — knowledge layer architecture |
| XP | Cross-project / extensibility | 11 | MEDIUM — scaling/platform concerns |
| AP | Artisan Pantry (food domain) | 7 | LOW — domain-specific, but validate domain-agnostic architecture |
| RE | Real estate domain | 7 | LOW — same as AP |

## How to Do SYNTHESIS

### Step 1: Read All 50 UCs

For each UC, extract:
- Core capability required
- Implicit architectural requirement (what kind of system must exist for this UC to work?)
- Cross-UC connections (which other UCs share infrastructure needs?)

### Step 2: Find Cross-Cutting Themes

A theme = an architectural concern that appears across 3+ UCs and cannot be solved by addressing any single UC alone.

Expected theme candidates (from prior analysis — validate, don't assume):
- **Continuity**: session survival, context carryover, thread maintenance (NF-01, NF-10, goal-001)
- **Knowledge persistence**: atomic capture, decay, cross-project recall (PK-01..PK-09, goal-003)
- **Workflow orchestration**: role sequencing, approval routing, quality gates (NF-02..NF-05, goal-002)
- **Epistemic awareness**: confidence grades, drift detection, trust calibration (NF-15, NF-16, NF-11)
- **Domain agnosticism**: same framework for software, food, real estate (NF-07, AP-*, RE-*, XP-07)
- **Observability**: health metrics, traceability, human visibility (NF-08, NF-09, NF-14)

Discover additional themes. Challenge the expected ones if evidence doesn't support them.

### Step 3: Write ADR Recommendations

For each theme:
- What architectural question does it raise?
- What's the design space? (2-3 possible approaches)
- Which existing ADRs partially address it?
- What's MISSING?

### Step 4: Architecture Vision

After SYNTHESIS, write the Architecture Vision as a 1-page narrative:
- **System Classification**: what kind of system is nowu? (framework? platform? runtime? operating environment?)
- **Architectural Principles**: 3-5 principles derived from themes (not aspirational — derived from evidence)
- **Quality Attribute Priorities**: ranked list with explicit tradeoffs (e.g., "continuity > performance")
- **Key Risks**: what could go wrong architecturally
- **ADR Roadmap**: ordered list of hypothesis ADRs to write, with priorities

## Constraints

- DO NOT write code or modify `src/` or `tests/`
- DO NOT modify existing ADRs (ADR-0001 through ADR-0006)
- DO NOT modify existing decisions (D-001 through D-012)
- Artifacts produced at HYPOTHESIS grade — they WILL be refined through S1-S9 feedback
- Use the 5×10 model coordinates in frontmatter (altitude: ARCHITECTURE, phase: SYNTHESIS)
- Include traceability metadata: `source_goal`, `source_uc`, `source_themes`

## What Comes AFTER This Session

With SYNTHESIS-001 and Architecture Vision done, the next step is W3 from STAGED-PLAN:
- Write hypothesis ADRs (ADR-0007+) based on SYNTHESIS themes
- Each ADR at HYPOTHESIS grade with validation criteria
- Then W4: first S1-S9 intake end-to-end against the hypothesis architecture

## Session Approach Recommendation

This is ARCHITECTURE-altitude, SYNTHESIS+ANALYSIS phase work. It requires:
- Reading breadth (all 50 UCs) — not depth in any single UC
- Pattern recognition across UCs — finding themes, not designing solutions
- Judgment about what's architecturally significant vs. implementation detail

Recommended: use Oracle consultation for theme validation and Architecture Vision quality check.
