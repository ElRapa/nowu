# Workflow Evaluation — S1 Intake

**Date**: 2026-03-22
**Intake ID**: intake-2026-03-22-memory-integration
**Executed by**: GitHub Copilot (Claude Opus 4.6) acting as `nowu-intake`
**Recommended model**: Haiku (Claude 3.5 Haiku) — lightweight translation task

---

## ✅ What's Good

1. **Forces problem articulation** — Even though Step 02 was already described in
   V1_PLAN, writing the intake brief forced surfacing 4 concrete open questions
   that V1_PLAN glossed over (API compatibility, project scoping model, error
   strategy, statefulness).

2. **Use-case anchoring** — Mapping to NF-01, NF-02, PK-03, XP-01 creates a
   traceable chain from the start. If implementation drifts, S8 (reviewer) can
   catch it.

3. **Appetite as a scope knife** — The "if it takes longer, cut to two methods"
   clause is a real Shape Up principle. It prevents the "8h task becomes 20h" trap.

4. **Template is lightweight** — Takes ~5 minutes. The cost/value ratio is good.

## ❌ What's Bad / Gaps

1. **Redundancy with V1_PLAN** — About 60% of this brief restates what V1_PLAN
   already says. For a self-developing framework where planning preceded the
   workflow, S1 feels like ceremony. The workflow assumes ideas arrive
   *unstructured*, but Step 02 arrived *pre-analyzed*.

2. **No "who benefits" field** — The template says "user-centric" but the
   framework's user is itself. The problem statement naturally drifts to
   technical ("no integration layer") rather than user-pain ("agent can't resume
   work"). Consider adding an explicit `user_impact` field.

3. **`affected_modules` is a guess** — The template says "first guess" but with
   existing architecture docs, it's not really a guess. The step doesn't
   distinguish between "I looked it up" and "I'm guessing".

4. **Open questions could be answered by S2 or by reading `know`** — Question 1
   ("has the API changed?") could be answered right now by reading code. The
   strict context scoping (S1 never loads src/) prevents the intake agent from
   answering it, which is correct for bias prevention but adds a round-trip.

## 📝 Learnings

- **For pre-planned work, S1 still adds value** — but mainly through the *open
  questions* section, not the problem statement. Consider a "thin S1" variant
  that focuses on questions + use-case mapping only.

- **The appetite + cut-scope pattern is the most valuable part** of the brief.
  Without it, every step risks becoming unbounded.

- **The context scoping rule works** — by not loading ARCHITECTURE.md or src/,
  the agent was forced to write from the user's perspective rather than jumping
  to solution details.

## Suggested Workflow Improvements

- Add a `depth: thin | medium | thick` field to the intake template so
  pre-planned work can skip the verbose problem statement.
- Add a `user_impact` field to keep the brief user-centric even for meta/
  framework work.
- Allow S1 to mark open questions as "answerable in S2" vs "needs human input"
  to reduce unnecessary blocking.

---

## Iteration 2 — 2026-03-22 (after reiteration)

**Trigger**: V1_PLAN updated to add NF-09 (traceability use case). Previous intake-001 had
three quality issues: premature Acceptance Signal, an L4 latency question (Q3), and a
D-006 re-litigation risk (Q4). User requested reiteration to apply learnings.

### Changes made to intake-001

| Change | Reasoning |
|--------|-----------|
| Added `NF-09` to `use_case_ids` | MemoryService is the *foundation* of the `validation_trace` chain — `create_task`/`record_decision` store the atoms that S5/S8 reference. Without NF-09 here, it has no implementation home. |
| Removed `Acceptance Signal` section | This is a done-criteria — it belongs in S5 (Shaping), not S1. Having it at intake anchors the shaper prematurely and blurs the S1↔S5 boundary. |
| Removed Q3 (latency / caching) | Latency bounds and caching strategy are C4 L4 concerns. Raising them at S1 (L1) violates the C4 scoping rule. They belong in S3 Options at the earliest. |
| Removed Q4 (conflict/staleness) | The question implicitly asks whether MemoryService should own conflict detection — but D-006 already settled that `know` owns memory semantics. Re-raising it at S1 risks re-litigating a closed decision. |
| Narrowed `affected_modules` to `[core]` | `flow` and `bridge` are consumers, not owners. They should appear in S2 constraints as *dependent* modules, not as modules to be changed by this task. |
| Replaced Q2 + Q5 with sharper NF-09 question | The new Q3 asks precisely where `use_case_ids` attach — at the storage layer (MemoryService signature) or by caller convention. This is the key design ambiguity introduced by NF-09. |

### Updated learnings

- **C4 level discipline is the hardest thing to enforce in S1** — the intake agent
  naturally wants to drift into solution space. Every open question should be
  challenged: "is this L1/L2, or am I sneaking L4 in?"
- **Use-case list must be kept current** — when V1_PLAN changes, existing intake
  briefs may be stale. Consider a check: does any use case ID in the brief appear
  in V1_PLAN Step description?
- **`affected_modules` overreach is common** — agents list every module that
  *touches* the work rather than every module that *owns* a change. The field
  should reflect ownership, not dependency.
