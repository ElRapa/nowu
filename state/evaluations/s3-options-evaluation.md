# Workflow Evaluation — S3 Options

**Date**: 2026-03-22
**Artifact ID**: 2026-03-22-memory-integration-options
**Executed by**: GitHub Copilot (Claude Sonnet 4.6) acting as `nowu-options`
**Recommended model**: Claude Sonnet 4.5 — structured creativity, QA scoring, C4 L2 diagrams

---

## ✅ What's Good

1. **S3 resolved the S2 open questions it could** — Before designing options, the agent
   verified `know.today()` return shape, confirmed the `DecisionRecord` → `KnowledgeAtom`
   mapping, and identified the adapter gap. This front-loaded verification prevented
   options from being built on false assumptions. The workflow's context scoping *allows*
   reading `know` public APIs in S3, which was correctly used here.

2. **Three options are genuinely distinct** — Option A (direct), B (adapter injection),
   C (extend adapter) span the design space meaningfully. They differ in testability,
   scope, and architectural purity — not just surface-level variations of the same idea.
   The recommendation isn't arbitrary: Option B wins on scoring AND on risk/appetite fit.

3. **C4 L2 Mermaid diagrams clarify the interaction pattern** — Each option's diagram
   immediately shows "who calls what". The visual distinction between Option B (mixed
   adapter + direct calls) and Option C (pure adapter) is clearer in the diagram than
   in prose alone.

4. **Quality Attribute scoring is honest** — Option C scores higher on type safety and
   modifiability but loses on simplicity and migration cost. The scoring matrix didn't
   manufacture a result — it exposed a real tradeoff. The recommendation overrides the
   raw score difference (51 vs 47) with a qualitative argument about appetite and
   cross-project risk. This is correct usage of ATAM-style evaluation.

5. **Version discrepancy caught** — The `know/__init__.py.__version__ = "0.1.0"` vs.
   `pyproject.toml version = "0.3.0"` mismatch was surfaced here. If this had been
   missed, integration tests checking `know.__version__` would have given misleading
   results.

## ❌ What's Bad / Gaps

1. **Option B's "mixed access pattern" is undersold as a risk** — The sheet says it's a
   "code smell" but "bounded". In practice, mixing direct `know.*` calls alongside adapter
   calls in the same class is a maintenance hazard: if `KnowAdapter` gains the missing
   methods in v0.4.0, the MemoryService won't automatically migrate — someone must
   remember to remove the direct calls. This should have been tracked as a follow-up
   task, not just noted as acceptable.

2. **No evaluation of error propagation** — S2 flagged error handling as a flexible
   constraint. None of the three options explicitly address "what happens when
   `know.create_atom()` raises `ValueError`?". The options sheet should have included
   a brief note on error handling strategy per option, even if one line.

3. **`TodayView` type question deferred silently** — S2 raised it as OQ-1. S3 answered
   the shape but then said "no `TodayView` dataclass needed for v1". This is a valid
   call, but the reasoning (Protocol still returns `dict[str, Any]` because the shape
   is in the docstring) is implicit. Should have been explicit in the options sheet so
   S4 can validate the tradeoff was deliberate.

4. **The recommendation echoes V1_PLAN too closely** — Option B was pre-decided in
   V1_PLAN. The scoring matrix confirms it, but didn't challenge it. A stronger S3
   would have asked: "Given the `KnowAdapter` gap we discovered, should V1_PLAN's Option
   B be reconsidered?" The answer is still "no" — but the question was never asked. A
   workflow that always confirms pre-existing decisions isn't adding much.

5. **Cross-project change in Option C framed as purely negative** — Option C's "Tier 3
   gate" framing is correct, but it implies the adapter extension in `know` is risky.
   In reality, `know` is a sibling project owned by the same developer. Adding 2 methods
   to `KnowAdapter` is low-risk. The workflow's Tier 3 escalation was designed for
   production merges to main, not for adding helper methods to a sibling dev project.
   The risk classification may be over-conservative here.

## 📝 Learnings

- **S3 is the most valuable architecture step** — It's the first place where concrete
  design decisions are made that will affect implementation. S1 and S2 are mostly
  discovery and constraint mapping. S3 produces actionable choices that survive to S6.

- **The QA scoring matrix works best when options are genuinely competing** — When one
  option wins on every dimension (it didn't here), the matrix is useless. The tradeoff
  between Options B and C (testability parity, but C needs cross-project work) is
  exactly what the matrix is designed to surface.

- **"Recommended option" should be locked to context** — The recommendation correctly
  accounts for appetite (8h), not just architectural purity. An S3 that recommends the
  theoretically perfect option regardless of deadline/scope is a liability, not an asset.

- **S3 is where the Protocol gets challenged** — The `list[Any]` return types in the
  Protocol were too vague. S3 correctly identified the concrete types (`list[SearchResult]`)
  and recommended updating the Protocol. This is the right step to make that call —
  early enough to change the interface before any consumers exist.

## Suggested Workflow Improvements

- Add a `follow_up_tasks` section to the options sheet for known future debt
  (e.g., "Option B: if KnowAdapter gains create_decision() in v0.4.0, remove
  direct know.create_atom() call from MemoryService").

- Add a brief `error_strategy` field per option (1-2 sentences): "propagate",
  "wrap and rethrow", "return None on not-found, raise on validation error".

- The options template should ask: "Does this option challenge any upstream
  assumption from S1/S2?" to force the agent to actively question pre-decisions.

- Revisit the Tier 3 escalation definition: distinguish between
  "breaking changes to production systems" and "extending sibling dev projects".
  Currently both trigger Tier 3, which is over-conservative for a solo developer.
