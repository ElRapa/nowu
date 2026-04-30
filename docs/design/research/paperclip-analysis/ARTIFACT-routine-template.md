# nowu Routine — Scheduled Health & Capture Task Template

**Inspired by**: Paperclip's "Routines" — cron-scheduled task templates that create recurring work

---

## What is a Routine?

A routine is a standing task that recurs on a schedule. Unlike a one-off intake, it doesn't go through the full P0–P4 pre-workflow. It has a fixed template, a fixed agent, and a fixed output.

---

## Built-in nowu Routines

### Routine 1: Weekly Health Sweep
```yaml
routine: health-sweep-weekly
trigger: every Monday at session start
agent: health-sweep
inputs:
  - docs/vision.md
  - docs/architecture/containers.md
  - state/stories/ (all APPROVED)
output: state/health/health-sweep-YYYY-MM-DD.md
action: Run all four health checks (vision, architecture, goals, use-cases). Set status GREEN/YELLOW/RED.
on_red: BLOCK next cycle until resolved
```

### Routine 2: Session Start Heartbeat
```yaml
routine: session-start-heartbeat
trigger: every new Claude Code session
agent: nowu-heartbeat (see ARTIFACT-heartbeat-skill.md)
inputs:
  - state/SESSION-STATE.md
  - docs/vision.md
output: printed boot summary (not saved to file)
action: Re-establish context. Identify current step, active tasks, health status.
```

### Routine 3: Weekly Knowledge Curation
```yaml
routine: know-curation-weekly
trigger: every Friday after last session
agent: know curator (kb.curator_run())
inputs:
  - ~/.know/ (all active atoms)
output: ~/.know/views/weekly_review.md
action: Recalculate importance scores. Flag stale/risky atoms. Write review summary.
on_flag: Human reviews weekly_review.md and promotes or archives flagged atoms
```

### Routine 4: Capture Audit
```yaml
routine: capture-audit-monthly
trigger: first session of each month
agent: nowu-curator
inputs:
  - state/captures/ (all capture-records from past 30 days)
  - docs/PROGRESS.md
output: state/health/capture-audit-YYYY-MM.md
action: Review all lessons learned. Check if any lesson should become a know atom or architecture ADR.
```

---

## Creating a Custom Routine

```yaml
routine: <routine-name>
trigger: <cron | on-session-start | on-epic-close | manual>
agent: <agent-name>
inputs:
  - <file or path>
output: <file path>
action: <one paragraph description>
on_completion: <CONTINUE | NOTIFY | BLOCK>
```

---

## Why Routines Matter

Without routines, health checks and knowledge curation only happen when you remember to do them. Paperclip's insight: **routines transform reactive maintenance into proactive hygiene**. The system stays healthy by default, not by effort.
