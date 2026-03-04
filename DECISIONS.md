# Decision Log (ADR-style)

Update this file when a non-trivial architecture, workflow, or scope decision is made.
Format: `## D-NNN Title` then Context / Decision / Consequences.

---

## D-001 Treat `know` as the external memory system of record
**Date:** 2026-03-04
**Context:** The original nowu draft planned to implement a local `know` module from scratch.
**Decision:** Reuse the existing sibling project `know` (v0.2.0) through public API and `KnowAdapter`. No internal reimplementation in nowu.
**Consequences:** Faster delivery, lower risk, and tighter contract boundaries. nowu modules must not bypass `know`.

## D-002 Choose integration-first modular monolith for nowu v1
**Date:** 2026-03-04
**Context:** Evaluated three options: modular monolith, event-driven internal bus, and early microservices.
**Decision:** Use an integration-first modular monolith for v1, with explicit interfaces to allow future event-driven evolution.
**Consequences:** Best speed/reliability tradeoff for solo + AI development. Scale/distribution concerns deferred beyond v1.

## D-003 Rebase v1 planning around integration slices, not component reinvention
**Date:** 2026-03-04
**Context:** Prior `V1_PLAN.md` did not reflect current repository reality and lacked architecture decision gates per step.
**Decision:** Replace with seven incremental steps: contracts, memory integration, session/WAL, role pipeline, bridge/approvals, learning/curation, bootstrap/cross-project context.
**Consequences:** Each step now includes architecture analysis, design options, evaluation, detailed plan, and implementation verification.

## D-004 Standardize role-driven workflow with VBR and approval tiers
**Date:** 2026-03-04
**Context:** Existing workflow text was tied to a tool-specific issue pattern and did not define strict AI handoffs.
**Decision:** Adopt a role loop (Architect, Shaper, Implementer, Reviewer, Curator) with Verify Before Reporting, Tier 1/2/3 approvals, and WAL discipline.
**Consequences:** Reduced scope drift, higher review quality, and clearer escalation behavior.

## D-005 Prioritize NF core use cases for v1 and treat full use-case set as direction
**Date:** 2026-03-04
**Context:** `USE_CASES.md` contains 35 use cases across NF/AP/RE/PK/XP and is intentionally broad.
**Decision:** Focus v1 on NF-01..NF-07 plus PK-01/PK-03 and XP-01 as enabling coverage.
**Consequences:** Keeps v1 achievable while preserving expansion path for domain-specific capabilities.

## D-006 Create dedicated architecture and shaping skills for AI consistency
**Date:** 2026-03-04
**Context:** Repeated architecture/tradeoff and task-shaping work benefits from reusable process constraints.
**Decision:** Create `skills/nowu-architect` and `skills/nowu-shaper`, validate them, and install copies to `~/.codex/skills`.
**Consequences:** Stronger consistency across sessions and reduced prompt drift for planning tasks.

## D-007 Establish Step 01 baseline with explicit contracts and AST boundary tests
**Date:** 2026-03-04
**Context:** Step 01 required a safe implementation base before runtime features.
**Decision:** Implement package scaffold under `src/nowu`, define contract protocols in `core/contracts`, and enforce module import policy via AST-based architecture tests.
**Consequences:** Future steps can add behavior without uncontrolled cross-module coupling; violations are caught early in tests.

---

*Add new decisions above this line. Use the next available D-NNN number.*

