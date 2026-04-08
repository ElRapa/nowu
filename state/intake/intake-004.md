---
id: intake-004
created: 2026-04-06
status: READY_FOR_ARCH
appetite: spike
affected_modules:
  - soul
  - flow
  - core
use_case_ids:
  - NF-13
  - NF-06
  - NF-08
workflow_mode: D
source_global_pass: global-pass-2026-04-06
s1_validated_at: 2026-04-06T10:00:00Z
s1_validation: >
  Well-formed. UC anchors NF-13 (v1-core, ACTIVE), NF-06 (v1-core, ACTIVE),
  and NF-08 (v1.1, ACTIVE) verified in USE_CASES.md. Affected modules
  soul+flow+core correct (ADR-F coupling pattern + Q4 LLM ownership). Global-pass
  Q3/Q4 mapping confirmed. P3 constraint 8 reference verified. No corrections needed.
s1_note: >
  Mode D (Architecture Only) spike. No implementation expected. Resolves two
  coupled open questions from global-pass-2026-04-06 that block v1-core: Q3
  (ADR-F, soul/flow integration pattern) and Q4 (LLM call ownership). Q4 is
  structurally dependent on Q3: if artifact-based coupling is chosen (no runtime
  soul→flow dependency), then flow cannot route LLM calls through soul at
  runtime and must call the LLM API directly. Both questions should be decided
  together in a single spike.
---

# Intake Brief: Agent-Workflow Integration Pattern and LLM Call Ownership

## Problem Statement

`soul` produces analytical outputs that `flow` depends on — options sheets (NF-13),
health metrics (NF-08), pattern insights (NF-06). It is currently undefined how
this dependency is expressed at runtime. Two incompatible patterns are possible:
artifact-based coupling (soul writes files that flow reads on the next cycle;
no function calls between modules) or direct function call (`flow` calls
`soul.generate_options()` at the S3 step; simpler code path but tight coupling
with import discipline risk). Additionally, if `flow` calls `soul` at runtime for
LLM-backed operations, the question of which module owns the LLM API client
becomes structurally significant: a single-client model (all calls through soul)
conflicts with artifact-based coupling; direct LLM calls from `flow` preserves
the no-runtime-dependency constraint. NF-13 (options sheet generation) is v1-core
and cannot be shaped without this decision.

## Context

This spike is triggered by global-pass-2026-04-06 open questions Q3 and Q4.
NF-13 is v1-core — the S3 implementer step for options generation cannot be
scoped without knowing whether `flow` triggers `soul` directly or reads an
artifact. P3 constraint 8 from the global-pass states: "ADR-F resolved before
NF-13 is shaped." The global-pass recommends artifact-based coupling (Option A)
and notes this is consistent with the existing "artifacts are the API" principle
in the codebase. The spike should evaluate this recommendation rigorously, not
assume it is settled.

## Appetite

Spike — time-boxed to the decision. The artifact-based option is directionally
preferred; if S3 confirms this with no significant disqualifying tradeoffs, the
decision should be recorded immediately. Do not over-engineer the options sheet
with edge cases unless S3 finds a genuine gap in the recommended option.

## Open Questions

1. **ADR-F — Integration pattern:** Artifact-based (Option A, no runtime coupling —
   soul reads state/ and writes insight files; flow reads them on the next cycle)
   vs. direct function call (Option B — flow imports soul and calls it synchronously)?
   Option C (event bus) is available but likely over-engineered for a single-user
   local CLI — S3 should confirm this or disqualify it.

2. **Q4 — LLM call ownership:** Should `flow` call the LLM API directly (each
   module that needs LLM reasoning calls independently), or should all LLM calls
   be routed through `soul` (making soul the single LLM client)? The single-client
   model is architecturally cleaner but conflicts with artifact-based coupling —
   it creates a runtime dependency of flow on soul. If artifact-based coupling is
   confirmed, Q4 resolves as: flow calls LLM directly; soul calls LLM directly;
   no shared client.

3. **Triggering model:** If artifact-based, what triggers soul to run? Options
   include: the curator step (S9) always runs soul; a cron-like scheduled trigger;
   or soul is manually invoked by the human as needed. S2 should surface this as
   a constraint — the triggering model affects whether soul needs its own entry
   point in `bridge`.
