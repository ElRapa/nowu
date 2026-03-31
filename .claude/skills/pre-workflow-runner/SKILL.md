---
name: pre-workflow-runner
version: 2.2
mode: P0–P4 + S1–S9
---

# Skill: Pre-Workflow Runner + Full Cycle

## Purpose

Orchestrate the pre-workflow (P0–P4) plus the core S1–S9 cycle for a
given initiative `NNN`, keeping:

- Vision, use cases, and plan in sync.
- Slices small (1–3 days end-to-end).
- Feedback from S9 (`next_cycle_trigger`) routed back to the right phase.

---

## Entry conditions

You have one of:

- A raw idea (human says "capture" or describes a signal — run `/capture` first
  to write `state/ideas/idea-NNN.md`, then continue from P0.D).
- An existing `state/ideas/idea-NNN.md` (P0.1 already done).
- A `next_cycle_trigger` from the last capture record that tells you
  where to resume (e.g. `PRODUCT_PIVOT`).

---

## High-level flow

1. **Determine mode** and resume point.
2. Run **P0.1 Signal Capture** if no `state/ideas/idea-NNN.md` exists yet
   (invoke `signal-capture` agent via `/capture`, or human writes it manually).
3. Optionally run **P0.VISION** (vision health + update).
4. Run **P0.UC** (use-case catalog maintenance) when needed.
4. Run **P1** (discovery + perspective interview).
5. Run **P2** (story mapping + human gate).
6. Optionally run **P3** (constraint check + architecture bootstrap).
7. Run **P4** (readiness + assemble `intake-NNN.md`).
8. Run **Full Cycle SKILL** (S1–S9) for that `intake-NNN`.
9. React to `next_cycle_trigger` from S9.

---

## 0. Determine run mode

Write or update:

- `state/pre-workflow/NNN-mode.md`:

```markdown
id: NNN
mode: FULL | STANDARD | LITE | BOOTSTRAP
reason: [one sentence why]
skipped_phases: [list or none]
started_at: [ISO timestamp]
```

Use this checklist:

- **BOOTSTRAP** (new product):
    - No `docs/vision.md` or it is placeholder-only.
    - No `docs/USE_CASES.md`.
    - No `docs/architecture/containers.md`.
- **FULL**:
    - Product exists, but this is a major new capability.
    - Vision and UCs exist, but architecture needs an explicit pass.
- **STANDARD**:
    - Product and architecture are stable.
    - This is a normal feature/epic.
    - P3 can be skipped unless architecture changes.
- **LITE**:
    - Small improvement or bugfix.
    - Use existing discovery/problem/epic/story context.
    - Typically: P2 + P4 + S1–S9 only.

Also check `next_cycle_trigger` from the latest `state/capture/*.md`:

- `PRODUCT_PIVOT` → force P0.VISION + P0.UC + P1.
- `ARCH_PIVOT` → force P3 before next implementation.
- `CONTINUE` → you may re-enter at P2/P4 with remaining stories.
- `COMPLETE` → start fresh from P0 idea.

---

## 1. P0.VISION (optional)

- Run `health-vision` agent.
- If vision health is `YELLOW` or `RED`:
    - Run your vision-bootstrap / update flow (separate skill/agent).
    - Update `docs/vision.md`.
- If `mode = BOOTSTRAP` and `docs/vision.md` missing:
    - Use vision-bootstrap to create an initial `docs/vision.md`.

Proceed when `vision.md` reflects current intent.

---

## 2. P0.UC — Use Case Catalog Maintenance

Run when:

- `mode = BOOTSTRAP`, or
- `health-use-cases` overall_status is `YELLOW` or `RED`, or
- `next_cycle_trigger = PRODUCT_PIVOT`.

Steps:

1. (Optional) Run `health-use-cases` to understand drift.
2. Invoke `use-case-agent`:
    - **BOOTSTRAP**:
        - If no `docs/USE_CASES.md`, agent writes initial catalog there.
    - **UPDATE**:
        - Agent writes `docs/USE_CASES.proposed.md`.
3. Human gate:
    - If `docs/USE_CASES.proposed.md` exists:
        - Review, then overwrite `docs/USE_CASES.md` when satisfied.

After this, `docs/USE_CASES.md` is the canonical UC catalog for P1–P4
and S1–S9.

---

## 3. P1 — Discovery

### P1.1 Discovery Agent

- Invoke `discovery-agent`.
- Inputs:
    - `state/ideas/idea-NNN.md`
    - `docs/vision.md`
- Output:
    - `state/discovery/disc-NNN-research.md` (status: DRAFT)


### P1.2 Perspective Interview (Problem synthesis)

- Invoke `perspective-interview`.
- Input:
    - `state/discovery/disc-NNN-research.md`
- Output:
    - `state/problems/problem-NNN.md` (status: DRAFT)

Human gate:

- Edit `problem-NNN.md` if needed.
- Set `status: APPROVED` when the problem statement is correct,
appetite is set, and out-of-scope is explicit.

Do not proceed to P2 until `problem-NNN.md` is APPROVED.

---

## 4. P2 — Story Mapping

### P2.1 Story Mapper

- Invoke `story-mapper`.
- Inputs:
    - `state/problems/problem-NNN.md`
    - `docs/USE_CASES.md`
    - `state/discovery/disc-NNN-research.md`
- Outputs:
    - `state/epics/epic-NNN.md`
    - `state/stories/story-NNN-*.md` (status: DRAFT)


### P2.2 Human story gate

Human reviews epic and stories:

- Scope hammer (split / merge / cut).
- Validate:
    - Story statements and ACs.
    - Validation trace to UC-IDs and success criteria.
    - Appetite per story.

Set `status: APPROVED` on each story that passes.

Do not proceed to P3/P4 with DRAFT stories.

---

## 5. P3 — Architecture Phase (mode-dependent)

Mode gating:

- **LITE**: Skip P3 entirely if stories clearly fit within existing containers
  and decisions.
- **STANDARD**: Run P3.1 only; skip P3.0 and P3.2–P3.6.
- **FULL / BOOTSTRAP**: Run P3.0–P3.6 in full.

> If `next_cycle_trigger = ARCH_PIVOT`, always run P3.1–P3.4 regardless of mode.

---

### P3.0 Domain Modeling (FULL / BOOTSTRAP only; optional)

Only run if the problem introduces a new bounded context.

If a domain-modeling agent is available in `.claude/agents/`, invoke it.
Otherwise, skip this step and note the absence in the runner state file.

- Output (if run): `state/arch/bounded-context-NNN.md`

---

### P3.1 Constraint Check

- Invoke `constraint-check`.
- Inputs:
    - Approved `state/stories/story-NNN-*.md`
    - `docs/architecture/containers.md` (if exists)
    - `docs/architecture/adr/` (if exists)
- Output:
    - `state/pre-workflow/NNN-constraint-check.md`

Human reviews conflicts (if any) and resolves before P3.2.

---

### P3.2 QA Elicitation (FULL / BOOTSTRAP only)

- Invoke `qa-elicitation`.
- Inputs:
    - `state/problems/problem-NNN.md`
    - `docs/vision.md`
    - `docs/architecture/quality.md` (optional; existing global QA registry)
    - Approved `state/stories/story-NNN-*.md`
- Output:
    - `state/arch/NNN-qa-scenarios.md`

Do not proceed to P3.3 if `NNN-constraint-check.md` has
`status: CONFLICTS_FOUND` with unresolved conflicts.

---

### P3.3 Architecture Design (FULL / BOOTSTRAP only)

- Invoke `architecture-design`.
- Inputs:
    - `state/problems/problem-NNN.md`
    - Approved `state/stories/story-NNN-*.md`
    - `state/arch/NNN-qa-scenarios.md`
    - `state/pre-workflow/NNN-constraint-check.md`
    - `state/arch/bounded-context-NNN.md` (if produced in P3.0)
    - `docs/architecture/context.md` (if exists)
    - `docs/architecture/containers.md` (if exists)
    - `docs/architecture/crosscutting.md` (if exists)
    - `docs/architecture/adr/` (if exists)
- Output:
    - `state/arch/arch-pass-NNN.md`

---

### P3.4 ATAM-Lite Evaluation (FULL / BOOTSTRAP only)

- Invoke `atam-lite`.
- Inputs:
    - `state/arch/arch-pass-NNN.md`
    - `state/arch/NNN-qa-scenarios.md`
    - `docs/architecture/containers.md` (if exists)
    - `docs/architecture/risks.md` (if exists)
- Output:
    - `state/arch/NNN-atam-lite.md`

---

### P3.5 ADR Authoring (human)

- For each ADR candidate in `arch-pass-NNN.md` (section "ADR Candidates"):
    - Human writes `docs/architecture/adr/ADR-NNN-*.md`.
- Review `state/arch/NNN-atam-lite.md`:
    - Accept identified risks (status ACCEPTED with documented mitigation), or
    - Request a design revision by looping back to P3.3 for any HIGH-impact
      risk that remains unmitigated.
- Update `docs/architecture/context.md` and `containers.md` as needed.

Do not proceed to P3.6 while any HIGH-impact risks remain OPEN
without a mitigation decision.

---

### P3.6 Architecture Documentation Update (human)

After ADRs are in place, update `docs/architecture/` to reflect the new design:

- `quality.md` — merge new QA scenarios from `state/arch/NNN-qa-scenarios.md`.
- `crosscutting.md` — add or revise crosscutting decisions from `arch-pass-NNN.md`.
- `runtime.md` — add C4 Dynamic scenarios for any new key flows.
- `deployment.md` — update if a new topology was decided.
- `risks.md` — promote new OPEN risks from `NNN-atam-lite.md` (append only).

This step is human-driven. Agents write only to `state/arch/`;
promotion to `docs/architecture/` is always manual.

---

## 6. P4 — Readiness and Intake Assembly

### P4.1 Readiness Checker

- Invoke `readiness-checker`.
- Inputs:
    - `state/ideas/idea-NNN.md`
    - `state/discovery/disc-NNN-research.md`
    - `state/problems/problem-NNN.md`
    - `state/epics/epic-NNN.md`
    - Approved `state/stories/story-NNN-*.md`
    - `state/arch/arch-pass-NNN.md` (if mode requires)
    - `state/pre-workflow/NNN-constraint-check.md`
- Output:
    - `state/pre-workflow/NNN-readiness.md`
    - If all blocking checks PASS:
        - `state/intake/intake-NNN.md` (status: `DRAFT_FOR_REVIEW`)

If `status: BLOCKED`:

- Fix the listed issues.
- Re-run `readiness-checker`.


### P4.2 Human intake approval

- Review `state/intake/intake-NNN.md`.
- When satisfied, set:
    - `status: READY_FOR_S1`.

This is the **handoff contract** into S1–S9.

---

## 7. Full S1–S9 cycle

- Invoke **Full-cycle SKILL** (S1–S9) with `intake-NNN.md`.
- Run through S1–S9 as defined in that SKILL.
- At S9, `nowu-curator` writes `state/capture/capture-task-NNN.md`
with `next_cycle_trigger`.

---

## 8. React to `next_cycle_trigger`

Read the most recent `state/capture/capture-*.md` for this initiative.

- `CONTINUE`
    - There are more APPROVED stories in `epic-NNN`.
    - Pick next story.
    - Optionally skip P1/P0 if still fresh.
    - Re-enter at P2/P4 → S1–S9.
- `ARCH_PIVOT`
    - Implementation revealed an architecture mismatch.
    - Re-run P3.1–P3.4 (constraint-check → qa-elicitation → architecture-design → atam-lite)
      on the epic/problem before shaping further work.
- `PRODUCT_PIVOT`
    - Discovery from implementation shows product direction should change.
    - Re-run:
        - P0.VISION (vision health \& update),
        - P0.UC (refresh UCs),
        - P1 (discovery) as needed.
- `COMPLETE`
    - All stories in `epic-NNN` DONE.
    - Optionally run health checks (vision/goals/U C/architecture).
    - Start from a new idea (new NNN) if desired.

---

## State tracking

Maintain:

- `state/pre-workflow/NNN-runner-state.md`:

```markdown
current_phase: P2.2
status: IN_PROGRESS | AWAITING_HUMAN | BLOCKED | COMPLETE
last_updated: [ISO timestamp]
next_action: [short description]
```

Update after each automated step and each human gate, to keep sessions
resumable.