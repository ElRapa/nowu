---
name: nowu-heartbeat
description: Re-establishes agent context at the start of any nowu session or step. Use when resuming work, starting a new session, or beginning a new heartbeat cycle.
metadata:
  version: "1.0"
  source: inspired-by-paperclip-heartbeat
  author: nowu-framework
---

# nowu Heartbeat — Session Context Boot

Run this at the start of every session (replaces blank-page paralysis).

## Steps

1. **Identity** — Confirm current agent role (S1–S9 or P0–P4 pre-workflow stage).
2. **Vision** — Read `docs/vision.md`. Check `status: APPROVED` and `lastapproved` within 90 days.
3. **State** — Read `state/SESSION-STATE.md`. Identify current step, active intake-NNN, active task-NNN.
4. **Health** — If `lastHealthCheck` > 7 days ago, run `health-check all` and inspect RED/YELLOW items.
5. **Assignments** — List open tasks: query `state/tasks/` for files with status `READY_FOR_IMPL` or `IN_PROGRESS`.
6. **Budget** — If AI cost tracking is in scope, confirm no runaway loops (no single task > 5 heartbeats without status change).
7. **Execute** — Work on the highest-priority assignment. Follow the step's agent rules.
8. **Report** — At natural stopping point, update `state/SESSION-STATE.md` with current step, last action, next checkpoint.

## Rules

- Never start implementation without a `READY_FOR_S1` intake.
- Never skip health checks when `lastHealthCheck` is stale.
- If `state/SESSION-STATE.md` is missing or empty, treat as a fresh Bootstrap session and run P0.V first.
- One task per heartbeat cycle. Do not context-switch mid-task.

## Output Format

On session start, print a brief summary:
```
HEARTBEAT BOOT
Agent: <role>
Step: <S0–S9 or P0–P4>
Active intake: <intake-NNN or NONE>
Active task: <task-NNN or NONE>
Health: <GREEN / YELLOW / RED / UNCHECKED>
Next action: <one sentence>
```
