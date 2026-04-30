# Workflow Evaluation — S2 Constraints

**Date**: 2026-03-22
**Artifact ID**: 2026-03-22-memory-integration-constraints
**Executed by**: GitHub Copilot (Claude Sonnet 4.5) acting as `nowu-constraints`
**Recommended model**: Claude 3.5 Sonnet — analytical synthesis of architecture + decisions

---

## ✅ What's Good

1. **Synthesis adds value beyond source docs** — Even though DECISIONS.md and ARCHITECTURE.md exist, the constraints sheet surfaces *implications* that weren't explicit. Example: "MemoryService must live in `core/` (Application layer)" follows from D-002 but wasn't stated anywhere. The synthesis work is real, not just copy-paste.

2. **Risks section is concrete and actionable** — Each risk has a specific mitigation task for S3. "Verify current API surface against Protocol requirements" is a real action item, not handwaving. The "Medium" severity ratings are justified.

3. **Flexible vs. Fixed split works well** — The distinction between "must follow" (D-NNN decisions) and "can choose" (project scoping model) is clear. S3 now knows exactly what's negotiable.

4. **Open questions guide S3 effectively** — All 5 questions have clear owners (S3 must answer) and are truly unresolved. They don't ask "should we?" — they ask "which option?" or "what shape?", which is the right level of specificity.

5. **Assumptions table catches verification gaps** — Two assumptions are marked "Unknown" — this prevents S3 from building on false premises. The agent correctly identified what it doesn't know from reading docs alone.

## ❌ What's Bad / Gaps

1. **Redundancy with V1_PLAN Option B** — V1_PLAN.md already stated "Option B: `core/memory_service.py` wrapper around `KnowAdapter`". The constraints sheet rediscovers this but adds no new constraint that would invalidate it. For pre-analyzed work, S2 feels like re-validation rather than discovery.

2. **"Flexible Constraints" recommendations pre-empt S3** — The sheet says "Recommendation for S3: Explore Option A..." — but that's S3's job. S2 should present constraints, not options. The line between S2 (constraints) and S3 (options) blurs here. Consider removing recommendations from the S2 template.

3. **Missing: dependency on Step 01 artifacts** — The constraints sheet assumes `core/contracts/memory.py` exists but doesn't reference *which file* it read or what commit/version. If Step 01 is incomplete or the Protocol changes, S3 won't know. Consider adding a `verified_artifacts` section with file paths + checksums or commit hashes.

4. **`know` API verification is deferred to S3** — S2 says "S3 must verify current API surface" — but S2 *already loaded* `know.__init__.py` and `know/docs/API.md`. Why not do the verification now? The context scoping rule (S2 can read contracts/interfaces) allows it. This creates unnecessary round-trip.

5. **No explicit module boundary diagram** — The sheet says `core` → `know` but doesn't show it visually. A simple Mermaid box-and-arrow (C4 L2) would clarify the interaction. The template has a C4 L1 section but no L2 equivalent.

## 📝 Learnings

- **S2 adds most value when it *challenges* upstream assumptions** — The best parts of this sheet are where it says "V1_PLAN assumed X, but D-002 means Y, so we need to verify Z." When constraints just confirm what's already decided, the step feels ceremonial.

- **The Risks table is the highest-signal section** — It's the only place where S2 adds uncertainty quantification and mitigation tasks. If S2 were compressed to a single section, keep Risks.

- **Recommendations in S2 blur roles** — S2 should constrain; S3 should propose. Mixing them weakens both. If S2 already knows Option A is best, it should escalate to S3 with "only Option A is viable" rather than "recommend exploring Option A."

- **Verification can happen earlier than the workflow prescribes** — The rule "S2 doesn't load source internals" is correct, but "S2 doesn't verify public API compatibility" is overly strict. If S2 already loaded `know.__init__.py`, it has the data to answer "does the Protocol match the API?" Deferring this to S3 adds latency for no benefit.

## Suggested Workflow Improvements

- Remove "Recommendation for S3" bullets from the Flexible Constraints section. Replace with "Options to evaluate in S3: A, B, C."
- Add a `verified_artifacts` section to S2 template: "Constraints based on: [file path @ commit/version]."
- Add a C4 L2 diagram slot to the S2 template (not just L1). Most constraints live at the module-interaction level.
- Clarify in the S2 agent definition: "If you can definitively rule out an option based on constraints, say so. Don't defer viable/non-viable judgment to S3."
