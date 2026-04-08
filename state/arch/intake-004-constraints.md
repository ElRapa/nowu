---
id: intake-004-constraints
intake: intake-004
status: READY_FOR_OPTIONS
created: 2026-04-06
agent: nowu-constraints@S2
arch_pass_ref: global-pass-2026-04-06
---

# Constraints Sheet — intake-004: Agent-Workflow Integration Pattern and LLM Call Ownership

## Fixed Constraints (Non-Negotiable)

1. **P3 constraint 4 (global-pass-2026-04-06) — no runtime function call between `flow` and `soul`.** The global-pass explicitly states: "direct imports between `flow`, `soul`, `know`, and `bridge` are forbidden. The only legal import graph is: all modules → `core`; `soul` reads/writes file artifacts owned by `flow` (no function call)." This pre-commits the design to artifact-based coupling (Option A). Option B (direct function call) directly contradicts this constraint and cannot be pursued without a Tier 3 constraint override and a superseding P3-level decision. This is not a recommendation — it is a stated boundary condition.

2. **D-002 — DDD layer architecture.** All cross-module dependencies must go through `core/contracts/*.py`. Even if Option B were unblocked by an override, `flow` importing `soul` directly would still be forbidden — any call must be mediated by a Protocol in `core/contracts.py`. Source: D-002.

3. **D-003 — Five-module ceiling.** No new top-level Python module may be created without a superseding ADR and Tier 3 approval. Option C (event bus) cannot create a new `eventbus` module. If Option C is pursued, the event bus infrastructure must live in `core` — which the global-pass defines as "a Python module — no I/O," with zero UC ownership. An in-process event bus in `core` violates both the container definition and the layer model of D-002. Source: D-003, P3 constraint 1, global-pass `core` container definition.

4. **D-007 — Integration-first modular monolith for v1.** An in-process event bus is the architecture that D-007 explicitly chose not to adopt. "Scale and distribution concerns deferred beyond v1." Option C is the over-engineered solution the decision was taken specifically to avoid. This compounds the D-003 and container-definition disqualifications. Source: D-007.

5. **"Artifacts are the API" principle — confirmed unchanged.** The global-pass "What Stays the Same" section explicitly confirms this principle as unaltered and identifies it as the driver for ADR-F's Option A recommendation. It is not a new proposal — it is a pre-existing codebase principle. Source: global-pass, "What Stays the Same," point 4.

6. **D-001 — File-based memory architecture.** Active working state is persisted as Markdown/YAML files in `state/`. Soul's insight outputs (options sheets, health metrics, pattern lessons) must conform to this model. The global-pass assigns soul's write targets as `state/health/` and `state/arch/`; flow reads from those paths. Source: D-001, global-pass `soul` container definition.

7. **P3 constraint 8 (global-pass-2026-04-06) — ADR-F must be resolved before NF-13 is shaped.** NF-13 (options sheet generation) is v1-core and cannot proceed past S4 without this architecture decision accepted in DECISIONS.md. This intake is the gate. Source: P3 constraint 8, global-pass.

8. **NF-13 (v1-core, ACTIVE) assigned to `soul`.** The global-pass UC matrix assigns NF-13 to `soul`. Flow orchestrates the S3 step, but the analytical reasoning that produces the options artifact is soul's responsibility. Flow must read soul's output, not generate it. Source: global-pass UC matrix.

9. **NF-06 (v1-core, ACTIVE) pattern model confirms artifact coupling.** NF-06 (pattern detection) is already described as: "reads flow's session/capture artifacts; writes lessons back to `state/`." This UC is artifact-coupled by description — soul reads flow's files, writes its own. NF-06 provides a running confirmation of the artifact-based model across two of the three affected UCs. Source: global-pass UC matrix, NF-06 description.

10. **NF-08 (v1.1, ACTIVE) requires `soul` to be independently triggerable.** Health metrics computation "reads both `flow` and `know` state; writes to `state/health/`." Health checks are run outside pipeline steps (they are invoked as `health-check` commands). Soul must have a trigger mechanism that does not require a synchronous call from `flow`. A design where soul can only run when `flow` calls it conflicts with NF-08's independent invocation model. Source: global-pass UC matrix, NF-08 description, health-check command definitions.

---

## Flexible Parameters (S3 May Choose)

1. **Soul trigger mechanism.** How soul knows when to run is not fixed by any current decision. Three implementations are in scope — S3 must select one and include it in the ADR-F record:
   - **(a) S9 curator step invokes soul as a pipeline action.** The curator step (S9) always executes `nowu soul run` as its final action, via a bridge CLI entry point. Soul runs at end-of-cycle, producing options and health artifacts ready for the next S3 and S8. Lowest coordination complexity; options artifact is always one cycle old.
   - **(b) Explicit bridge CLI entry point only.** Soul has its own `nowu soul run` command that the human or a scheduled job triggers independently. Flow makes no call and has no trigger knowledge. Matches NF-08's independent invocation model exactly; requires human or scheduler discipline for NF-13's synchrony requirement.
   - **(c) Trigger-file pattern.** Flow writes a `state/soul-trigger.yaml` at defined points (end of S9, or pre-S3 check); soul's startup reads this file and processes pending work before producing artifacts. Still fully artifact-based and no function call. Adds a lightweight coordination primitive without coupling the two modules at the function level.

2. **NF-13 synchronization strategy.** The options artifact must exist when flow reaches S3. With Option A (artifact-based), S3 must define when soul runs relative to S3:
   - Pre-computation at S9 (artifact ready before next S3 — low-risk, one cycle lag).
   - On-demand via bridge entry point as a documented pre-step to S3 (human triggers `nowu soul generate-options` before starting S3).
   - Trigger-file checked at S3 start, with `flow` waiting for soul's artifact (adds wait logic in `flow`, but the call is still file-level, not a function call).

3. **LLM client library and instantiation model.** Specific SDK choice (Anthropic client, OpenAI package, or other) and how credentials are supplied is unconstrained. `core` may expose a shared `LLMConfig` dataclass (API key, model name, timeout — sourced from environment) without providing a shared client instance. Each module (flow, soul) instantiates its own client from this configuration.

4. **Soul artifact schema.** Format, directory location, and naming convention for soul's outputs (options sheets, pattern records, health metrics files) are not fixed by any existing decision. S3 should define a schema as part of the ADR-F record; formal typing as a dataclass in `core/contracts.py` is recommended (see risk 5 below) but not required.

5. **Whether `core` holds shared LLM configuration.** A `core/llm_config.py` providing environment variable management and model defaults (not a shared client object) is a compliant design pattern under D-002. Not required, but reduces duplication between `flow` and `soul` when both call LLM independently. S3 may recommend this as a corollary of the ADR-F artifact option.

---

## Key Risks for S3 to Address

1. **[HIGH] Option A — NF-13 synchrony gap.** If soul's options artifact is not present when `flow` reaches S3, the step fails or blocks. This is the sharpest operational risk of the artifact-based model. Mitigation direction: S3 must select a trigger model (flexible parameter 1) and synchronization strategy (flexible parameter 2) that guarantee the artifact is present — pre-computation at S9 is the lowest-risk path. The ADR-F record must specify which strategy is chosen and what happens when the artifact is absent (explicit error vs. fallback to empty options).

2. **[HIGH] Option B — P3 constraint 4 is a hard block, not a tradeoff.** If S3 evaluates Option B at all, the options sheet must flag that it requires Tier 3 approval to override P3 constraint 4, which itself is derived from the still-PROPOSED global-pass. S3 should not present Option B as a symmetric design choice — it is blocked by a binding constraint from a higher-level architectural decision. If Option B is included in the options sheet for completeness, it must be labelled BLOCKED.

3. **[HIGH] Option C — Disqualified by two independent decisions.** Option C requires either a new module (violates D-003, P3 constraint 1) or an event bus inside `core` (violates D-002/D-007 and the `core` container definition). S3 should confirm this disqualification explicitly rather than leaving it as an implied "not recommended." Confirming disqualification in writing prevents the option from re-emerging at S4.

4. **[MEDIUM] Soul trigger model gap: no trigger = no output.** All three affected UCs (NF-13, NF-06, NF-08) require soul to run at defined points. If ADR-F is accepted without specifying the trigger model, the three UCs cannot be shaped — there is no trigger to implement. The trigger model is part of ADR-F's scope, not a detail to be deferred to S5.

5. **[MEDIUM] Artifact schema drift.** If `flow` and `soul` independently evolve the artifact format — flow writes `state/arch/` files assuming one layout; soul reads them in a different format — the contract breaks without a test catching it at the boundary. Mitigation direction: define soul's output artifact schema as a typed dataclass in `core/contracts.py` and validate at both the write (soul) and read (flow) sides using that type.

6. **[MEDIUM] Dual LLM credential management.** With Option A, both `flow` and `soul` maintain independent LLM clients — two code paths for API key sourcing, retry logic, and error handling. Mitigation direction: `core` provides a shared `LLMConfig` dataclass (credentials from environment, model names, timeouts) so neither module embeds its own credential lookup. Client instantiation stays per-module; configuration is shared. This does not create a runtime dependency between modules.

7. **[LOW] `core/LLMConfig` scope creep.** If a shared LLM configuration type is added to `core/contracts.py`, future implementers may assume `bridge` or `know` can also acquire an LLM client through it, implicitly expanding `core`'s scope. Mitigation: scope the type name and docstring to the modules that currently call LLM (`flow`, `soul`) and add a governance note specifying that expanding LLM call ownership to additional modules requires an explicit S2 analysis.

---

## Q3↔Q4 Structural Link

The resolution of Q4 (LLM call ownership) is entirely determined by Q3 (coupling mechanism). They are not independent decisions.

- **Option A (artifact-based, recommended) → Q4 = dual independent LLM clients.** `flow` and `soul` have no runtime communication channel. Each module must instantiate its own LLM client. A single-client model is structurally impossible under artifact-based coupling — `flow` cannot route LLM calls through `soul` without a runtime function call, which Option A forbids. The global-pass C4 L2 diagram already encodes this: it shows two arrows from `flow` and `soul` to LLM API separately. **Q4 resolves automatically when Option A is confirmed. No separate Q4 decision is needed.**

- **Option B (direct function call, BLOCKED) → Q4 = soul as single LLM client becomes feasible.** If `flow` calls `soul` at runtime (via a `core`-contracted protocol), `soul` can hold the LLM client and serve `flow`'s reasoning requests. This creates a single-client model where `flow` has no direct LLM dependency. However, Option B is blocked by P3 constraint 4. Q4 single-client is only available if Option B is unblocked through Tier 3 approval.

- **Option C (event bus, DISQUALIFIED) → Q4 = dual independent clients.** The event bus changes the trigger mechanism, not the call path to LLM. Soul still calls LLM from its own handler; flow still calls LLM for workflow agent steps. Same as Option A for Q4.

**Consequence for S3:** Q4 is not a decision S3 needs to resolve independently. S3's task is to confirm Option A (which resolves Q4 automatically as dual clients), and to select the trigger model and NF-13 synchronization strategy that close the operational gap artifact-based coupling creates.

---

## Constraint Summary for Options Agent

ADR-F candidate is substantially pre-constrained: P3 constraint 4 of global-pass-2026-04-06 already names artifact-based coupling as the only legal import graph for `soul`↔`flow`, and the "artifacts are the API" principle is confirmed unchanged. Option B (direct call) is blocked without a Tier 3 override; Option C (event bus) is disqualified by D-003, D-007, and the `core` container definition. S3's primary work is (a) confirming no disqualifying tradeoff exists for Option A, particularly for the NF-13 synchrony requirement at S3, and (b) selecting the soul trigger mechanism from the three sub-options above — this choice is the operational core of ADR-F and must be included in the decision record. Q4 resolves as a corollary of Q3 and does not require independent evaluation.

---

## Assumptions

- **global-pass-2026-04-06 P3 constraints are directionally binding** — UNVALIDATED. The global-pass status is PROPOSED. If the human declines to accept it, P3 constraint 4's explicit "no function call" language becomes advisory rather than binding, and the constraint landscape changes materially. This sheet treats P3 constraint 4 as binding consistent with the same architectural logic underlying the accepted decisions (D-002, D-003, D-007) it extends.
- **NF-13 requires soul to produce an artifact consumed by flow's S3 step** — VALIDATED by UC matrix assignment (global-pass: NF-13 → soul) and intake description.
- **No existing `bridge` soul entry point exists** — UNVALIDATED. If a `nowu soul run` CLI command already exists, the trigger mechanism question is partially answered. S3 should confirm before specifying a new entry point.
- **LLM API credentials are single-environment (one key, one model configuration)** — UNVALIDATED. If flow and soul use different API keys or model configurations, the `core/LLMConfig` pattern becomes more important for avoiding credential duplication. S3 should confirm.

## Open Questions Passed to S3

1. **Which soul trigger model is selected?** S3 must choose among (a) S9 curator invokes soul, (b) explicit bridge CLI entry point only, or (c) trigger-file pattern — and include the selection in the ADR-F record. This is not optional: without a trigger model, NF-13, NF-06, and NF-08 cannot be shaped.
2. **Is Option B presented for evaluation or immediately flagged as blocked?** S3 should clarify whether the global-pass PROPOSED status means Option B is a live option requiring Tier 3 approval, or whether its disqualification is pre-settled. The answer should come from the human, not be an S3 judgment call.
3. **Does `flow` need to know when soul's artifact is stale?** If soul runs at S9 and then the human delays starting S3 for several cycles, the options artifact ages. S3 should determine whether staleness matters for NF-13 and whether a timestamp check is needed before flow reads the artifact.

## arch_pass_divergences

No pre-workflow arch-pass exists for intake-004. Constraints derived from global-pass-2026-04-06 (used as the equivalent — it is the source document for P3 constraint 8, ADR-F, and Q4, and was the trigger for this intake via S1 validation).

Note: the global-pass does not use "arch-pass" language but functions as the architectural input for this spike. Its P3 constraint 4 is stronger than a directional recommendation — it explicitly names no function call as the binding rule for the `soul`↔`flow` import graph. S3's evaluation of Option B must treat this as a constraint override requiring Tier 3 approval, not a fresh design comparison.

## c4_l1_update_needed

false. This spike does not introduce a new external actor or system boundary. The C4 L1 diagram in the global-pass is unaffected. The C4 L2 container descriptions for `flow` and `soul` (which describe artifact-based coupling directionally) will require confirmation or a one-line update once ADR-F is accepted in DECISIONS.md.
