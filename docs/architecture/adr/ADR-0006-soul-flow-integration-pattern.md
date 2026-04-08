---
id: ADR-0006
title: Soul–Flow Integration Pattern — Artifact-Based Coupling with S9 Subprocess
date: 2026-04-06
status: ACCEPTED
superseded_by: ~
source_arch_pass: global-pass-2026-04-06
---

# ADR-0006: Soul–Flow Integration Pattern — Artifact-Based Coupling with S9 Subprocess

## Status

ACCEPTED — ratified via D-012 (intake-004, 2026-04-06). This ADR records the full
decision; D-012 in DECISIONS.md is the canonical reference for status and review trigger.

## Context

`soul` produces analytical outputs that `flow` depends on at defined pipeline steps:

- **S3** (options generation, NF-13) depends on soul's options-sheet artifact being present.
- **S8** (pre-review health check) depends on soul's health-metrics artifact.
- **S9** (curator step, NF-06, NF-08) triggers soul analysis of the completed session.

The coupling mechanism between `soul` and `flow` was undefined, blocking NF-13 (v1-core).
P3 constraint 8 in global-pass-2026-04-06 required ADR-F (now ADR-0006) to be resolved
before NF-13 could be shaped.

Two coupling patterns were evaluated: artifact-based (no runtime call) and direct function
call (`flow` calls `soul.generate_options()` at S3). A third option — an in-process event
bus — was considered but rejected as over-engineered.

The primary sensitivity for this decision was **NF-13 synchrony**: options coherence at S3
must be guaranteed without requiring human discipline to manually run `soul` before each
S3 step. Any chosen mechanism must guarantee artifact presence.

## Decision

**Artifact-based coupling (Option A) + S9 subprocess invocation (Trigger A1).**

`soul` and `flow` are coupled exclusively at the file-system level:

- `soul` reads `state/` artifacts produced by `flow` (session logs, capture records,
  decision files) and writes insight artifacts to `state/health/` and `state/arch/`.
- `flow` reads soul's insight artifacts on the next cycle.
- **No Python import crosses the `soul`↔`flow` boundary at runtime.**

At the close of every S9 (curator) step, `flow`'s S9 orchestration invokes
`nowu soul run` as an OS-level subprocess via `bridge`'s CLI entry point. Soul runs to
completion, writes its artifacts, and exits.

**Soul failure handling:** S9 treats soul's subprocess failure as non-fatal. On failure,
S9 logs the error and writes `state/soul-error.yaml` (staleness sentinel file), then
completes normally. On the next cycle, S3 checks for soul artifact presence and checks
for the sentinel file. If the artifact is absent or the sentinel is present, S3 raises
an explicit error (halts the current step and surfaces the issue for human intervention).

**Q4 resolution (corollary):** Because `flow` cannot call `soul` at runtime, `flow` must
call the LLM API directly for its own workflow steps. Both `flow` and `soul` use
independent LLM client instances instantiated from `LLMClientConfig` in `core/contracts.py`.
See ADR-0003.

## Rationale

**S9 critical-path exposure vs. structural synchrony guarantee.**  
The S9 subprocess approach accepts that soul runs in S9's temporal scope — adding latency
to the curator step. But it guarantees NF-13 synchrony without human discipline: S3 on
the next cycle always has a fresh options artifact (or an explicit error if soul failed).
The alternative (human manually triggers soul) was judged unacceptable for a system whose
value proposition is continuity without manual management.

**One-cycle artifact staleness vs. zero runtime dependency.**  
The soul artifact at S3 is always one cycle old (from the previous S9). This staleness is
bounded and detectable (S3 checks artifact timestamp and the sentinel). Zero-staleness is
not achievable without a runtime call from `flow` to `soul` — which is blocked by D-002
(DDD layer constraint) and D-003 (module structure constraint).

**Why not direct function call (Option B)?**  
Direct function call would make `flow` depend on `soul` as a runtime import, violating
D-002 and the "artifacts are the API" principle. It would also prevent soul from being
triggered independently (e.g., as a CLI command or scheduled job).

## Consequences

**Positive:**
- NF-13 is unblocked for shaping — soul artifact guaranteed present at S3 on next cycle.
- `flow` and `soul` can be tested in isolation without instantiating each other.
- Soul is independently triggerable as a CLI command (`nowu soul run`) outside S9.
- All inter-module data is inspectable on the filesystem at any time.
- S9 failure policy is explicit: soul failure is non-fatal, error is surfaced at next S3.

**Negative:**
- Options artifact at S3 is always one cycle old (inherent staleness of artifact model).
- Soul's LLM call is in S9's temporal critical path (bounded; non-fatal by policy).
- If soul fails, the user sees the error at the next S3, not immediately at S9.

**Neutral:**
- S9's non-fatal failure policy must be consistently implemented; deviation requires
  a superseding ADR.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Artifact-based coupling + S9 subprocess (Option A / Trigger A1) | Independently testable; NF-13 synchrony guaranteed; soul independently triggerable | One-cycle staleness; S9 latency from subprocess | **Selected** |
| Direct function call at S3/S8 (Option B) | Simpler code path; zero staleness | Violates D-002 and D-003; soul cannot be triggered independently | Incompatible with DDD layer constraint and module boundary rule |
| In-process event bus (Option C) | Fully decoupled; asyncable | Adds event bus dependency; over-engineered for single-user CLI; race conditions to manage | Over-engineered; no clear benefit over artifacts for this scale |

## Review Trigger

If soul's LLM failure rate at S9 causes S3 to block more than once per project per week,
reconsider the non-fatal policy or surface a retry option. Also review if soul's subprocess
wall-clock time regularly exceeds the S9 budget (not currently defined; define at NF-08 shaping).

## Related

- arch_pass: global-pass-2026-04-06
- decisions: D-012 (canonical status record)
- containers: `flow`, `soul`, `core`
- use_cases: NF-13, NF-06, NF-08
- adr: ADR-0003 (LLM client architecture — Q4 corollary of this decision)
