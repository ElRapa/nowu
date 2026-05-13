---
name: intake-001-options-decision
description: S3 options for intake-001 session checkpoint; Option C (versioned schema) recommended; Tier 3 Protocol change required at S4
metadata:
  type: project
---

Option C (SessionCheckpoint as single type, Protocol updated, schema translation in FileSessionStore) was recommended for intake-001.

**Why:** Options B and C tied on QA score (49). Option B's Optional fields create permanent type ambiguity. Option C tests ADR-0007 hypothesis most directly (D-017 requirement). Option A creates dual-path Protocol divergence with deferred migration cost.

**How to apply:** S4 must approve two Tier 3 actions before S5 begins: updating both `SessionStore.load()` and `SessionStore.save()` signatures from `SessionSnapshot` to `SessionCheckpoint`. S5 shaper must audit all `SessionStore` call sites before implementation. `SessionSnapshot` is deprecated-in-place (not deleted) as a stub in `core/contracts/types.py`.

Key resolved questions:
- Bookmark writer: `FileSessionStore.save()` writes JSON checkpoint first, then `state/SESSION_STATE.md` YAML projection — atomic by ordering
- AC-3 hallucination guard: flow-orchestration concern only; `flow` session-start logic loads checkpoint and passes it verbatim into agent prompt before any reasoning
- Step-boundary hook: `checkpoint_at_step_boundary()` in flow's pipeline dispatcher, no new infrastructure needed
- `state/sessions/` directory created on first write by `FileSessionStore`
