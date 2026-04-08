---
id: intake-004-decision
intake: intake-004
status: ACCEPTED
created: 2026-04-06
agent: nowu-decider@S4
decision_id: D-012
---

# Decision Record — intake-004: Agent-Workflow Integration Pattern and LLM Call Ownership

## Chosen Option

**Option A (Artifact-Based Coupling) + Trigger A1 (S9 Curator Invokes Soul as Subprocess)**

This is the binding decision for ADR-F (soul/flow integration pattern) and Q4 (LLM call
ownership). Option B (direct function call) and Option C (in-process event bus) are
rejected — both are structurally blocked by accepted constraints before scoring. The
operative decision is the triggering model. Trigger A1 wins decisively.

---

## Coupling Pattern — Why Option A Is the Only Viable Choice

Option B is blocked by P3 constraint 4 (global-pass-2026-04-06): "Direct imports between
`flow`, `soul`, `know`, and `bridge` are forbidden." and by D-002 (DDD layer architecture),
which requires any cross-module interaction to be mediated by a Protocol in `core/contracts.py`.
A runtime function call from `flow` to `soul` satisfies neither constraint without Tier 3 override.

Option C is blocked by D-003 (five-module ceiling) and D-007 (integration-first monolith).
An in-process event bus requires either a sixth module or a capability injection into `core`
that violates `core`'s definition as a no-I/O contract surface.

**Option A is confirmed as the sole binding choice by existing constraints. No score comparison
is necessary for the coupling pattern — the comparison is among trigger sub-options only.**

Q4 resolves automatically: if `flow` and `soul` are artifact-coupled with no runtime dependency,
`flow` cannot route LLM calls through `soul`. Both modules call the LLM API directly with
independent clients instantiated from a shared `LLMClientConfig` type in `core/contracts.py`.

---

## Weighted Scoring Matrix — Trigger Sub-Options

| Criterion                                  | Weight | A1 Score | A1 Weighted | A2 Score | A2 Weighted | A3 Score | A3 Weighted |
|--------------------------------------------|--------|----------|-------------|----------|-------------|----------|-------------|
| NF-13 synchrony guarantee                  | 40%    | H = 3    | 120         | L = 1    | 40          | M = 2    | 80          |
| Operational simplicity                     | 30%    | H = 3    | 90          | L = 1    | 30          | M = 2    | 60          |
| NF-08 independence (on-demand invocation)  | 20%    | H = 3    | 60          | H = 3    | 60          | H = 3    | 60          |
| Implementation complexity (inverted: H=low)| 10%    | H = 3    | 30          | H = 3    | 30          | M = 2    | 20          |
| **Total**                                  | 100%   |          | **300**     |          | **160**     |          | **220**     |

**A1 wins with 300/300.** A3 is runner-up at 220. A2 is eliminated at 160.

A2's L(1) on NF-13 synchrony and operational simplicity creates a 140-point deficit against A1
that no other criterion can recover. A1's perfect score is structurally justified: it was
designed to close NF-13's synchrony gap and to serve NF-08 through the same CLI entry point.

---

## ATAM Analysis

### Sensitivity Point 1 — NF-13 Synchrony (40% weight, cycle-blocking)

NF-13 synchrony is the singular sensitivity point. A1 and A2 diverge by H vs L on the
highest-weighted criterion. The intake explicitly states NF-13 is "v1-core and cannot be
shaped without this decision." A2's L score here is not a marginal disadvantage — it is a
structural failure to address the intake's stated problem. A2 is not a viable option within
v1-core constraints. A3 provides partial mitigation but does not close the gap.

### Sensitivity Point 2 — Non-Fatal Soul Failure Policy at S9

A1 introduces soul's LLM call into S9's execution path. This is the highest-severity
implementation risk in the decision — **fully resolved** by the non-fatal failure policy
(see Companion Decisions), which changes soul's S9 invocation from a "must-succeed"
precondition to a "best-effort enhancement." S9 always completes; soul failure produces a
sentinel, not a crash.

This policy is a **binding corollary of choosing A1** — not optional and not a shaper decision.

### Tradeoff Point 1 — S9 Critical-Path Exposure vs. Structural Synchrony

A1 places soul's subprocess call in S9's critical path. This is a deliberate exchange: S9
accepts the responsibility of triggering soul so that S3 on the next cycle can read a
guaranteed artifact. Bounded risk: soul's subprocess call is time-bounded by the LLM API
timeout. Soul failure never propagates to S9's completion state. The tradeoff is accepted.

### Tradeoff Point 2 — One-Cycle Artifact Staleness vs. Zero Runtime Dependency

Under A1, the options artifact at S3 is exactly one cycle old. The staleness is:
- **Bounded:** exactly one cycle (never more without a soul failure)
- **Detectable:** S3 checks the artifact's `generated_at` timestamp and logs a staleness
  warning if more than one cycle gap is detected
- **Acceptable for v1-core:** single-cycle staleness is not a correctness defect

The alternative — zero staleness — requires a runtime soul call during S3, which is blocked.
The tradeoff is accepted.

---

## Use Case Coverage

| UC-ID | Stage   | Covered? | How |
|-------|---------|----------|-----|
| NF-13 | v1-core | YES | Soul runs at S9 and writes options artifact; guaranteed present at S3 on next cycle. |
| NF-06 | v1-core | YES | Soul's S9 subprocess includes pattern detection over session/capture artifacts. |
| NF-08 | v1.1    | YES | Same `nowu soul run` CLI entry point serves both S9 subprocess and on-demand use. |

---

## Contradictions Check — D-001 through D-011

| Decision | Compatible? | Note |
|---|---|---|
| D-001 File-Based Memory | YES | Soul artifacts are Markdown/YAML files in `state/`. Subprocess call is OS-level; no in-memory coupling between `flow` and `soul`. |
| D-002 DDD Layer Architecture | YES | S9→soul subprocess is an OS-level invocation through `bridge`'s CLI — not a Python import. `core` holds `LLMClientConfig` and artifact schema protocols. No layer boundary crossed. |
| D-003 5-Module Structure | YES | `nowu soul run` is a CLI command within `bridge`. No sixth module created. |
| D-004 TDD | YES | Architecture spike only. TDD applies to subsequent implementation intakes. |
| D-005 Dedicated Agent Per Step | YES | S9's curator agent invokes soul as a subprocess; soul is its own module, not a new step agent. |
| D-006 know as External Memory | YES | D-012 operates at soul/flow coupling layer; no interaction with know's storage model. |
| D-007 Integration-First Monolith | YES — reinforced | A1's subprocess invocation retains the monolith structure. D-007's rationale ("avoid event bus complexity") is directly upheld by Option C's disqualification. |
| D-008 Integration Slices | YES | Not affected. |
| D-009 VBR and Approval Tiers | YES | Not affected. |
| D-010 Prioritize NF Core UCs | YES — advances | A1 enables NF-13 (v1-core) to be subsequently shaped. |
| D-011 (DRAFT) | YES | D-011 governs `know`'s cross-project isolation model. D-012 governs `soul`/`flow` coupling. Distinct module boundaries; no overlap. |

**No blocking contradiction found.**

---

## Companion Decisions (Binding Corollaries)

1. **`LLMClientConfig` in `core/contracts.py`.** Both `flow` and `soul` call the LLM API
   independently. LLM client configuration (API key, model, timeout, retry policy) must be
   defined as a typed config type in `core/contracts.py`. Each module instantiates its own
   client from this shared config type. No shared singleton LLM client exists.

2. **Soul artifact schema in `core/contracts.py`.** Soul's output artifact schema — at
   minimum the options sheet for NF-13 — must be defined as a dataclass or TypedDict in
   `core/contracts.py` so that `soul` (writer) and `flow` (reader) validate against the
   same contract without importing each other. Schema definition precedes implementation of
   either the soul writer or the flow reader.

3. **Non-fatal soul failure policy at S9.** Soul failure during the S9 subprocess invocation
   is non-fatal. S9 logs the error and writes `state/soul-error.yaml` as a sentinel. S9
   completes with a success exit code regardless of soul's outcome. S3 on the next cycle
   checks for soul artifact presence at startup; if the expected artifact is absent or
   `state/soul-error.yaml` is present, S3 raises an explicit error before proceeding.
   This policy is binding on all S9 implementers and all S3 implementers.

4. **`nowu soul run` CLI entry point in `bridge`.** Soul must expose a `nowu soul run`
   command through `bridge`'s CLI. The same entry point serves S9's subprocess call and
   on-demand human invocation (NF-08).

---

## What S4 Is NOT Deciding

- The system call used by S9 to invoke soul (subprocess.run, asyncio subprocess etc.) — unconstrained.
- `soul-error.yaml` sentinel schema field names — unconstrained.
- Soul artifact YAML field names — constrained to `core/contracts.py` type; field design by shaper.
- `LLMClientConfig` field names and defaults — type in `core`; field design by shaper.
- Soul's LLM retry policy — internal to soul.
- Whether S9 awaits soul synchronously or asynchronously — unconstrained.
- Staleness threshold for S3's timestamp check — unconstrained; documented in task spec.
- Whether `nowu soul run` accepts additional CLI flags — unconstrained.

---

## Mode Note

Mode D (Architecture Only) spike. No S5 shaping or S6 implementation follows from intake-004
directly. D-012 and this decision file are the sole deliverables. Subsequent implementation of
the S9 subprocess call (in `flow` and `bridge`) and soul's options generation capability
(NF-13 in `soul`) each require their own intakes. Both intakes are unblocked by this decision.
P3 constraint 8 from global-pass-2026-04-06 ("ADR-F resolved before NF-13 is shaped") is
satisfied by D-012.
