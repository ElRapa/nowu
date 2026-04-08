---
id: ADR-0003
title: LLM Client Architecture
date: 2026-04-06
status: ACCEPTED
superseded_by: ~
source_arch_pass: global-pass-2026-04-06
---

# ADR-0003: LLM Client Architecture

## Status

ACCEPTED — ratified on 2026-04-07. This ADR formalises the already-constrained outcome
of ADR-0006 and is binding for all LLM-calling code in `flow` and `soul`.

## Context

`flow` and `soul` both require LLM API access: `flow` for all workflow pipeline agent
steps (S1–S9, P0–P4, G0–G2); `soul` for analytical reasoning (options generation, pattern
detection, drift analysis). The question is whether LLM calls should be centralised in one
module or distributed independently.

Two patterns were considered:
- **Single-client model**: all LLM calls route through `soul`, making `soul` the system's
  LLM gateway. `flow` calls `soul` at runtime to obtain completions.
- **Dual-client model**: `flow` and `soul` each maintain an independent LLM client,
  instantiated from a shared configuration type in `core`.

This question (Q4 in the global-pass) was resolved automatically as a corollary of D-012
(artifact-based soul↔flow coupling). If artifact-based coupling is enforced, `flow` cannot
call `soul` at runtime — including for LLM access. Therefore dual independent clients are
the only viable pattern.

This ADR formalises that corollary as a numbered architectural decision, so implementers
have a clear binding rule when writing LLM client code in either module.

## Decision

**Dual independent LLM clients with shared `LLMClientConfig` in `core/contracts.py`.**

- `flow` instantiates and owns its own LLM client for workflow pipeline agent steps.
- `soul` instantiates and owns its own LLM client for analytical reasoning calls.
- `LLMClientConfig` in `core/contracts.py` is the single source of truth for provider,
  credentials, model selection, and shared tuning parameters.
- Changing provider or model configuration must be done through `LLMClientConfig`, not
  by introducing module-specific hidden config.
- No runtime call from `flow` to `soul` is permitted for LLM access.
- `know` and `bridge` do not call the LLM API directly in v1.

## Rationale

The single-client model would require `flow` to depend on `soul` at runtime, violating
D-002 (DDD layer constraint) and the artifact-based coupling decision (D-012). The
dual-client model is the only pattern compatible with the existing constraint set.
`LLMClientConfig` in `core` ensures credentials are managed in one place and injected
into both clients — no duplication, no hidden dependency.

## Consequences

**Positive:**
- `flow` and `soul` remain independently testable without instantiating the other module.
- Both modules can be upgraded to different LLM models independently.
- No hidden runtime dependency between `flow` and `soul`.
- AI agents changing model/provider settings have one explicit configuration contract to edit instead of searching across modules.

**Negative:**
- Two LLM clients means two sets of retry/rate-limit logic to maintain (unless abstracted
  into a shared utility in `core`).
- If LLM provider credentials change, both clients must be reconfigured (mitigated by
  `LLMClientConfig` being the single source of truth).

**Neutral:**
- `know` and `bridge` are unaffected — they hold no LLM-requiring UCs in v1.

## Alternatives Considered

| Option | Pros | Cons | Rejected because |
|---|---|---|---|
| Single client in `soul`; `flow` calls `soul` for LLM | One credential source; one retry policy | Requires runtime `flow`→`soul` call; violates D-012 and D-002 | Incompatible with artifact-based coupling |
| Single client in `core`; both modules use a shared instance | One retry policy; one credential source | `core` becomes stateful (holds an LLM connection) — violates core's I/O-free constraint | `core` must remain I/O-free (D-011 corollary, contracts-only) |
| Dual independent clients + shared `LLMClientConfig` in `core` | Compatible with all constraints; independently testable | Retry/rate-limit logic potentially duplicated | Selected as the constrained-optimal option |

## Related

- arch_pass: global-pass-2026-04-06
- decisions: D-002, D-012
- containers: `flow`, `soul`, `core`
- use_cases: NF-01 through NF-14 (all LLM-calling workflow and soul UCs)
- adr: ADR-0006 (soul↔flow integration pattern — parent decision)
