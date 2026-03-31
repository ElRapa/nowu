# Agent Circuit Breaker — nowu Governance Rule

**Inspired by**: Paperclip's circuit breaker system and 80/100 budget model

## Purpose

Prevent runaway or stuck agents from burning tokens, creating infinite loops, or silently diverging. These rules are enforced by the reviewer (S8) and the curator (S9).

---

## Breaker Conditions

| Condition | Threshold | Action |
|---|---|---|
| **No progress** | 3 heartbeat cycles on same task with no status change | Flag task as `BLOCKED`, require human review |
| **Consecutive failure** | 3 failed VBR runs (`S7 FAIL`) in a row | Pause implementation, escalate to S4 re-shaping |
| **Scope drift** | `git diff --name-only` includes files outside `in_scope_files` | Auto-fail S7 VBR gate, require task re-shaping |
| **Context overload** | Agent loads more than its C4 level context | STOP, reload with correct context, restart step |
| **Stale health** | `lastHealthCheck` > 7 days | Warn before next step; RED status blocks all gates |
| **Vision drift** | `health-check vision` returns RED | Block all new intakes until vision re-approved |

---

## Budget Model (Soft / Hard Stop)

Inspired by Paperclip's 80% soft / 100% hard budget:

- **80% token estimate reached**: Warn. Post progress summary to `state/SESSION-STATE.md`. Consider splitting task.
- **100% / context window limit**: Hard stop. Write partial changeset. Resume next session using `state/SESSION-STATE.md` bookmark.

---

## No-Progress Detection

The S9 capture agent MUST check before closing a cycle:

```
if task.heartbeats_without_progress >= 3:
    set task.status = BLOCKED
    write "No-progress circuit breaker triggered" to capture-record
    set next_cycle_trigger = ARCHPIVOT
```

---

## How to Integrate

1. Add this file to `.claude/agents/` or reference from `CLAUDE.md`
2. S8 reviewer reads this before any `APPROVE` decision
3. S9 curator reads this before setting `next_cycle_trigger`

---

## Why This Matters

Without circuit breakers, a stuck agent silently re-attempts the same failing pattern. With them, failures surface as explicit BLOCKED states with a clear re-entry path (ARCHPIVOT or PRODUCTPIVOT). The human is notified; no tokens wasted on repeated failures.
