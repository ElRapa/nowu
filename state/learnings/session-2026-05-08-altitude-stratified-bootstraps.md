---
artifact_type: SESSION_LEARNINGS
session: "Altitude-Stratified Bootstrap Architecture"
created_at: 2026-05-08
session_type: "workflow-optimization"
source_artifacts:
  - BOOTSTRAP.md (replaced with routing index)
  - BOOTSTRAP-ARCHITECTURE.md (new)
  - BOOTSTRAP-STRATEGIC.md (new)
  - BOOTSTRAP-DELIVERY.md (new)
  - BOOTSTRAP-RETROSPECTIVE.md (new)
  - BOOTSTRAP_lean.md (updated)
  - AGENTS.md (updated session entry table)
  - CLAUDE.md (updated quick start reference)
purpose: "Implement altitude-stratified bootstrap files from Perplexity research (Option B: Hybrid Approach)"
---

# Session Learnings: Altitude-Stratified Bootstrap Architecture

## What Was Done

- Evaluated 3 context-loading architecture options from Perplexity research (Skill-Only, Altitude-Stratified, Modular Dynamic)
- Validated all file references in the proposed templates against the actual repo state — found 6 ambivalences
- Created 4 altitude-specific bootstrap files (STRATEGIC, ARCHITECTURE, DELIVERY, RETROSPECTIVE)
- Replaced monolithic BOOTSTRAP.md with a routing index that preserves the document map and approval tiers
- Updated BOOTSTRAP_lean.md, AGENTS.md session entry table, and CLAUDE.md quick start to reference the new system

## Decisions Made

### D-SESS-01: Chose Option B (Altitude-Stratified) over Options A (Skill-Only) and C (Modular Dynamic)

**Decision:** Bootstrap files load altitude-common context; skills load only step-specific context on top.
**Context:** OmO suggested pushing all context into skills (Option A), but this creates a chicken-and-egg problem for novel work types. Option C (modular includes) is over-engineered for current scale.
**Why it matters:** Bootstrap files remain meaningful orientation documents while skills stay lean. AI agents can self-route: "I'm doing ARCHITECTURE work → read BOOTSTRAP-ARCHITECTURE.md first."

### D-SESS-02: Archive CLAUDE-SETUP.md (omit from new bootstraps)

**Decision:** Do not include docs/CLAUDE-SETUP.md in any altitude-stratified bootstrap.
**Context:** Current BOOTSTRAP.md loaded it, but skills and AGENTS.md already cover the same information.
**Why it matters:** Reduces context duplication. CLAUDE-SETUP.md remains available for reference but is not part of the default loading sequence.

### D-SESS-03: Use future-proof decision references ("all D-NNN" instead of "D-001 through D-022")

**Decision:** Bootstrap templates reference decisions generically rather than hardcoding the current count.
**Context:** The research doc said "D-001 through D-022" but actual repo had D-001 through D-021. Hardcoded ranges go stale.
**Why it matters:** Prevents bootstraps from becoming incorrect as new decisions are added.

---

## Process Insights

### Insight 1: Research docs accumulate stale file references

**Observation:** The Perplexity research doc referenced `state/arch/ARCHITECTURE-VISION.md` (wrong — it's at `docs/architecture/ARCHITECTURE-VISION.md`), `state/sessions/` (doesn't exist), `state/SESSION-STATE.md` (uses hyphen, actual file uses underscore), and "D-001 through D-022" (actual last is D-021).
**Type:** workflow-process
**Implication:** Always validate file references from research docs against the actual repo before implementing. Research docs capture intent at a point in time but the repo evolves independently.

### Insight 2: Monolithic bootstrap files resist altitude-aware context scoping

**Observation:** The original BOOTSTRAP.md loaded 20 items covering all altitudes. An agent doing S6-S7 implementation would read vision docs, architecture docs, AND execution docs — violating the context scoping rules that CLAUDE.md itself defines.
**Type:** domain-insight
**Implication:** Context loading should mirror the altitude model. If we have 5 altitudes, we should have altitude-specific bootstraps, not a single "load everything" bootstrap.

### Insight 3: Routing indexes preserve the value of monolithic docs while splitting their content

**Observation:** Simply deleting BOOTSTRAP.md and replacing it with 4 files would lose the Document Map and Approval Tiers — valuable orientation content that doesn't belong to any single altitude. Keeping BOOTSTRAP.md as a routing index preserves this while directing to altitude-specific content.
**Type:** workflow-process
**Implication:** When splitting a monolithic doc, keep the original as a routing/index document for cross-cutting concerns rather than picking one altitude to host them.

---

## Anti-Patterns Observed

### Anti-Pattern 1: Trusting research doc file paths without validation

**Temptation:** The Perplexity research doc has carefully structured templates with file paths — just copy-paste them into the new bootstrap files.
**Reality:** 6 out of ~25 file references were wrong or stale. Copy-pasting without validation would create bootstraps that point to non-existent files, causing agent confusion and wasted context window on error recovery.

---

## What This Session Produced

| Artifact | Location | Status | Purpose |
|----------|----------|--------|---------|
| Bootstrap routing index | `BOOTSTRAP.md` | APPROVED | Routes to altitude-specific bootstraps |
| Strategic bootstrap | `BOOTSTRAP-STRATEGIC.md` | APPROVED | Context loading for STRATEGIC/PRODUCT altitude |
| Architecture bootstrap | `BOOTSTRAP-ARCHITECTURE.md` | APPROVED | Context loading for ARCHITECTURE altitude |
| Delivery bootstrap | `BOOTSTRAP-DELIVERY.md` | APPROVED | Context loading for DELIVERY/EXECUTION altitude |
| Retrospective bootstrap | `BOOTSTRAP-RETROSPECTIVE.md` | APPROVED | Context loading for RETROSPECTIVE altitude |
| Lean bootstrap (updated) | `BOOTSTRAP_lean.md` | APPROVED | Updated to reference altitude bootstraps |
| AGENTS.md (updated) | `AGENTS.md` | APPROVED | Session entry table now includes altitude routing |
| CLAUDE.md (updated) | `CLAUDE.md` | APPROVED | Quick start references altitude routing |

## What Should Happen Next

1. Update `.claude/skills/` files to reference altitude-specific bootstraps instead of the monolithic BOOTSTRAP.md (e.g., `full-cycle.md` should reference `BOOTSTRAP-DELIVERY.md`)
2. Create `orchestrator-implement` skill that references `BOOTSTRAP-ARCHITECTURE.md` for orchestrator implementation work
3. Consider archiving or deprecating `docs/CLAUDE-SETUP.md` since it's no longer in any bootstrap loading sequence
4. Validate that existing skills still work correctly with the new bootstrap structure
