# AGENTS.md — nowu

## Overview

AI-first framework runtime scaffold. Python 3.11+, src-layout, setuptools.
Five modules: `core` · `flow` · `bridge` · `soul` · `know` (external sibling at `../know`).
Contract-first design using `typing.Protocol` and frozen dataclasses in `core/contracts/`.
Currently v0.1.0 — mostly contracts and architecture scaffolding; no CLI entrypoint yet.

## Commands

```bash
# Install (uses uv — uv.lock is present)
uv sync                           # preferred: installs from lockfile
# OR: pip install -e ".[dev]"     # fallback without uv

# Tests
uv run pytest                     # runs tests/ (quiet mode via pyproject addopts)

# Quality suite (all three must pass before S8 review)
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .

# Format
uv run ruff format .

# Single test file
uv run pytest tests/architecture/test_import_boundaries.py -v
```

No Makefile, no CI workflows, no pre-commit hooks. Quality checks are enforced
by a `.claude/settings.json` pre-commit hook (runs pytest + mypy + ruff on `git commit`).

## Structure

```
src/nowu/
├── core/                # Shared contracts + boundary policy. Imports NOTHING else.
│   ├── boundaries.py    # ALLOWED_INTERNAL_IMPORTS dict — canonical import rules
│   └── contracts/       # Protocol interfaces + frozen dataclasses
│       ├── types.py     # TaskSpec, DecisionRecord, SessionSnapshot, RoleName, ApprovalTier
│       ├── memory.py    # MemoryService Protocol (know integration)
│       ├── session.py   # SessionStore, RoleOrchestrator Protocols
│       └── approval.py  # ApprovalRouter Protocol, ApprovalItem
├── flow/                # Pipeline orchestrator (P0–P4, S1–S9, GAP, health)
├── bridge/              # User-facing surface (Typer CLI, adapters)
└── soul/                # AI analytical reasoning (pattern detection, health, drift)
tests/
├── architecture/        # AST-based import boundary enforcement test
└── core/                # Contract importability smoke tests
docs/                    # Architecture docs, ADRs, vision, decisions
state/                   # Workflow artifacts (intake, tasks, arch, health, sessions)
templates/               # Markdown templates for every workflow artifact
.claude/                 # Agent definitions (35 agents: 32 execution + 3 orchestrator) + rules + skills
```

## Agent Grid — 5×10 Model Mapping

Canonical mapping of all 35 agents to 5×10 altitude/phase positions. This table is the single source of truth for agent-to-grid assignments. Agent frontmatter `altitude:` and `phase:` fields mirror this table.

| Agent | File | Step | Altitude | Phase | Notes |
|-------|------|------|----------|-------|-------|
| **S1–S9 Pipeline** | | | | | |
| nowu-intake | `.claude/agents/nowu-intake.md` | S1 | DELIVERY | IDEA | Intake brief at DELIVERY/IDEA per MODEL §7. |
| nowu-constraints | `.claude/agents/nowu-constraints.md` | S2 | ARCHITECTURE | ANALYSIS | Constraints analyst; no design proposals. |
| nowu-options | `.claude/agents/nowu-options.md` | S3 | ARCHITECTURE | OPTIONS | Options generation per MODEL §7. |
| nowu-decider | `.claude/agents/nowu-decider.md` | S4 | ARCHITECTURE | DECISION | Records D-NNN decision; MODEL §7 decision step. |
| nowu-shaper | `.claude/agents/nowu-shaper.md` | S5 | DELIVERY | EVALUATION | Scope/AC fit evaluation before implementation. |
| nowu-implementer | `.claude/agents/nowu-implementer.md` | S6+S7 | EXECUTION | IMPLEMENTATION | Primary IMPLEMENTATION; secondary VERIFICATION via built-in VBR gate. |
| nowu-reviewer | `.claude/agents/nowu-reviewer.md` | S8 | EXECUTION | EVALUATION | S8 review/evaluation pass; not VBR. |
| nowu-curator | `.claude/agents/nowu-curator.md` | S9 | EXECUTION | LEARN | Capture + `next_cycle_trigger` promotion. |
| **Pre-Workflow** | | | | | |
| vision-bootstrap | `.claude/agents/vision-bootstrap.md` | P0.V (+P0.G) | STRATEGIC | DECISION | Vision + goal brief creation; MODEL §9 P0.V. |
| signal-capture | `.claude/agents/signal-capture.md` | P0.1 | STRATEGIC | IDEA | Signal intake at idea stage; STRATEGIC primary. |
| idea-decomposition | `.claude/agents/idea-decomposition.md` | P0.D | PRODUCT | ANALYSIS | Classifies/routes ideas by size and stage fit. |
| use-case-agent | `.claude/agents/use-case-agent.md` | P0.UC | PRODUCT | PROBLEM | UC catalog maintenance at PRODUCT problem-space. |
| discovery-agent | `.claude/agents/discovery-agent.md` | P1.1 | PRODUCT | ANALYSIS | Discovery research; no-solution constraint. |
| perspective-interview | `.claude/agents/perspective-interview.md` | P1.2 | PRODUCT | PROBLEM | Produces `problem-NNN.md`; PROBLEM per MODEL §11. |
| story-mapper | `.claude/agents/story-mapper.md` | P2.1 | DELIVERY | OPTIONS | Decomposes into epic/stories and candidate slices. |
| constraint-check | `.claude/agents/constraint-check.md` | P3.1 | ARCHITECTURE | ANALYSIS | Constraint compatibility analysis; no design proposals. |
| architecture-bootstrap | `.claude/agents/architecture-bootstrap.md` | P3.2 | ARCHITECTURE | OPTIONS | L1/L2 architecture shaping; decision deferred to ADR gate. |
| readiness-checker | `.claude/agents/readiness-checker.md` | P4.1–P4.2 | DELIVERY | EVALUATION | Readiness gate before human P4.3 → READY_FOR_S1. |
| qa-elicitation | `.claude/agents/qa-elicitation.md` | P3.2 (parallel) | ARCHITECTURE | ANALYSIS | Elicits/prioritizes QA scenarios; architecture inputs only. |
| **SYNTHESIS + Architecture** | | | | | |
| synthesis-agent | `.claude/agents/synthesis-agent.md` | W1 | ARCHITECTURE | SYNTHESIS | Frontmatter pre-set; values confirmed correct. |
| architecture-vision-agent | `.claude/agents/architecture-vision-agent.md` | W2 | ARCHITECTURE | ANALYSIS | Frontmatter pre-set; W2 derivation pass. |
| architecture-design | `.claude/agents/architecture-design.md` | P3.3 | ARCHITECTURE | OPTIONS | ADD-based structural optioning at C4 L1/L2. |
| atam-lite | `.claude/agents/atam-lite.md` | P3.4 | ARCHITECTURE | EVALUATION | ATAM-style risk/sensitivity/tradeoff evaluation. |
| hypothesis-adr-writer | `.claude/agents/hypothesis-adr-writer.md` | W3 | ARCHITECTURE | DECISION | Formalizes chosen decisions into hypothesis ADRs. |
| fitness-function-writer | `.claude/agents/fitness-function-writer.md` | W3.5 | ARCHITECTURE | VERIFICATION | Structural fitness checks that verify ADR constraints. |
| **Health / GAP** | | | | | |
| health-vision | `.claude/agents/health-vision.md` | `/health-check vision` | STRATEGIC | VERIFICATION | Validates vision freshness/completeness/alignment. |
| health-goals | `.claude/agents/health-goals.md` | `/health-check goals` | STRATEGIC | VERIFICATION | Goal/traceability integrity vs active work. |
| health-architecture | `.claude/agents/health-architecture.md` | `/health-check architecture` | ARCHITECTURE | VERIFICATION | Architecture drift/coverage verification. |
| health-use-cases | `.claude/agents/health-use-cases.md` | `health.UC` | PRODUCT | VERIFICATION | UC catalog validity against vision/plan/activity. |
| gap-detector | `.claude/agents/gap-detector.md` | G0 | ARCHITECTURE | IDEA | GAP loop trigger/sentinel detection; MODEL §10. |
| gap-analyst | `.claude/agents/gap-analyst.md` | G1 | ARCHITECTURE | ANALYSIS | GAP analysis step; MODEL §10. |
| gap-writer | `.claude/agents/gap-writer.md` | G2 | ARCHITECTURE | IMPLEMENTATION | Applies approved global-pass deltas to canonical artifacts. |
| **Orchestrator + Meta** | | | | | |
| roadmap-creator | `.claude/agents/roadmap-creator.md` | Orchestrator milestone | STRATEGIC | IMPLEMENTATION | Frontmatter pre-set; MODEL §8 confirmed. |
| roadmap-updater | `.claude/agents/roadmap-updater.md` | Orchestrator milestone | STRATEGIC | LEARN | Frontmatter pre-set; MODEL §8 confirmed. |
| work-scheduler | `.claude/agents/work-scheduler.md` | Orchestrator query | N/A (meta) | N/A (query) | Read-only meta-layer query agent; outside 5×10 grid per MODEL §8. |

## Import Boundary Rules (Enforced by Test)

Defined in `src/nowu/core/boundaries.py`, enforced by `tests/architecture/test_import_boundaries.py`:

```
core   → (nothing)
flow   → core
bridge → core, flow
soul   → (nothing)
```

All cross-module calls go through `core/contracts/` Protocols. Direct imports between
`flow`, `soul`, `know`, and `bridge` are forbidden (ADR-0001). `soul` ↔ `flow` communicate
only via filesystem artifacts in `state/` (ADR-0006).

## Dependency: `know`

External sibling package at `../know`. Mapped via `[tool.uv.sources]` in pyproject.toml
as an editable local dependency. The workspace file `nowu_framework.code-workspace` links
both repos. `know` provides the knowledge store (SQLite per-project); nowu accesses it
only through the `MemoryService` Protocol.

## Workflow System

This repo uses the **5×10 altitude-phase model** (D-013) with a 9-step implementation
workflow (S1–S9) and a pre-workflow (P0–P4). **Each step has a dedicated agent**
(`.claude/agents/nowu-*.md`), strict context scoping rules, and artifact-based handoffs.

| What | Where |
|------|-------|
| **5×10 model spec** | `docs/model/MODEL-REFERENCE.md` |
| **Workflow standards** | `docs/model/WORKFLOW-STANDARDS.md` |
| **Verification guide** | `docs/model/VERIFICATION-GUIDE.md` |
| Workflow reference (S1-S9) | `docs/WORKFLOW.md` |
| Pre-workflow spec (P0-P4) | `docs/PRE-WORKFLOW.md` |
| Binding decisions | `docs/DECISIONS.md` (D-001 through D-020) |
| ADRs (binding) | `docs/architecture/adr/ADR-0001..0010` |
| Implementation roadmap | `docs/ROADMAP.md` |
| Context scoping table | `CLAUDE.md` (Context Scoping section) |
| Agent definitions | `.claude/agents/` (32 agents) |
| Skills (modes) | `.claude/skills/` (full-cycle, implement-loop, single-step, etc.) |
| Architecture rules | `.claude/rules/architecture.md` |
| Code style rules | `.claude/rules/code-style.md` |
| Testing rules | `.claude/rules/testing.md` |
| Workflow rules | `.claude/rules/workflow.md` |
| Research & insights | `docs/research/` |
| Worked examples | `docs/model/examples/` |

## Context Scoping (Critical)

Each workflow step loads ONLY its C4-level context. Violating this causes anchoring
bias (code during architecture) or re-litigation (architecture during coding).

- **S6–S7 (implementation)**: Load ONLY `task-NNN.md` + `in_scope_files`. Nothing else.
- **P0–P4 (pre-workflow)**: Never touch `src/` or `tests/`.
- **S8 (review)**: No full architecture docs; only VBR report + changeset + task spec + diff.

Full scoping matrix in `CLAUDE.md` and `docs/WORKFLOW.md`.

## Constraints an Agent Must Know

- **ADRs are binding.** Do not contradict without a superseding ADR (Tier 3 — requires human).
- **TDD is mandatory.** Write failing test first, then implement (D-004).
- **mypy --strict, ruff check, pytest** must all pass before review (S8).
- **Domain must not import infrastructure** (D-002). Use Protocols.
- **Scope enforcement**: `.claude/settings.json` has a Write hook that checks `state/tasks/.active-scope`.
- **Approval tiers**: Tier 1 (auto), Tier 2 (batch for human), Tier 3 (STOP and ask: merges to main, breaking changes, new ADRs, deletes, architecture boundary violations).
- **Secrets**: Never commit tokens/credentials. Environment variables only (ADR-0005).
- **`state/SESSION_STATE.md`** is a bookmark, NOT source of truth. Canonical state lives in S1–S9 artifacts.

## Code Style

- Type annotations on all public functions. Google-style docstrings.
- Functions < 20 lines, pure in domain layer.
- One class per file for domain objects.
- Test naming: `test_[unit]_[scenario]_[expected_outcome]`.
- Import order: stdlib → third party → local (ruff-enforced).
- Contracts use frozen dataclasses. Treat as immutable transfer objects.
- `contracts/__init__.py` is empty — import submodules directly (e.g., `from nowu.core.contracts.types import TaskSpec`).

## How We Work (Session-Independent Core)

These conventions apply to ALL sessions regardless of altitude, phase, or task type.

### Artifacts & Metadata

- Every artifact has **YAML frontmatter**: `artifact_type`, `status`, `created_at` at minimum.
- **Naming**: `{type}-NNN.md` (e.g., `intake-001.md`, `task-023.md`, `SYNTHESIS-001.md`).
- **Templates**: Always use the template from `templates/` when creating a new artifact.
- **Status lifecycle**: DRAFT → APPROVED/ACCEPTED → consumed by next step. See CLAUDE.md for full lifecycle table.

### Approval Tiers

- **Tier 1 (auto):** Tests, docs, refactors within existing ADRs, work within shaped scope.
- **Tier 2 (batch):** Feature implementation, design changes, new dependencies.
- **Tier 3 (STOP):** Merges to main, breaking changes, new ADRs, deletes, architecture boundary violations.
- When unsure → Tier 2.

### Quality Gates (Before Any Review)

```bash
uv run pytest --tb=short -q
uv run mypy src/ --strict
uv run ruff check .
```

All three must pass before S8 review or any merge.

### Decisions & ADRs Are Binding

- `docs/DECISIONS.md` (D-001 through D-020) — never contradict.
- `docs/architecture/adr/ADR-0001..0006` — never contradict without a superseding ADR (Tier 3).
- New decisions get the next D-NNN number. New ADRs start at HYPOTHESIS grade.

### Session Entry (Do NOT Load Everything)

Start sessions with a **skill invocation** that matches your work type, or read the
altitude-specific bootstrap (see `BOOTSTRAP.md` routing index):

#### Pre-Workflow (P0-P4)

Use when you are **not yet at an intake brief**.

| Situation | Skill | Mode | Outcome |
|---|---|---|---|
| New product / big idea (from zero) | `pre-workflow-runner` | Bootstrap | `docs/vision.md` + `docs/ROADMAP.md` + first `intake-NNN` READY_FOR_S1 |
| New epic on existing product | `pre-workflow-runner` | Full | `problem-NNN`, `epic-NNN`, `story-NNN-*`, `arch-pass-NNN`, `intake-NNN` READY_FOR_S1 |
| New story on existing epic | `pre-workflow-runner` | Standard | new `story-NNN-*` + `intake-NNN` READY_FOR_S1, no arch pass |
| Small feature / tweak | `pre-workflow-runner` | Lite | 1-few approved stories + `intake-NNN` READY_FOR_S1 |

#### SYNTHESIS + Architecture Vision + ADRs (W1-W3.5)

Run ONCE before the first S1-S9 intake. Re-run W1-W2 when significant new UCs are added.

| Situation | Step | Skill / Agent | Outcome |
|---|---|---|---|
| UCs approved, no SYNTHESIS yet | W1+W2 | `synthesis-vision` | `state/arch/SYNTHESIS-NNN.md` + `docs/architecture/ARCHITECTURE-VISION.md` |
| ≥10 new UCs added | W1+W2 | `synthesis-vision` | Updated SYNTHESIS + Architecture Vision |
| Arch Vision approved, write ADRs | W3 | `hypothesis-adr-writer` | `docs/architecture/adr/ADR-NNNN-*.md` (HYPOTHESIS grade) |
| ADRs written, validate contracts | W3.5 | `fitness-function-writer` | `tests/architecture/test_adr_fitness.py` |

#### Implementation (S1-S9)

Use when you **already have `state/intake/intake-NNN.md [READY_FOR_S1]`**.

| Situation | Skill | Mode | Entry |
|---|---|---|---|
| Full feature from intake | `full-cycle` | A | `intake-NNN.md [READY_FOR_S1]` |
| Already-shaped tasks | `implement-loop` | B | `task-NNN [READY_FOR_IMPL]` |
| Quick bugfix / refactor / docs | `single-step` | C | thin `task-NNN` or direct |
| Architecture / design spike, no code | `architecture-only` | D | `intake-NNN.md [READY_FOR_S1]` |

#### Health, GAP & Learnings

| Situation | Skill | What It Loads |
|---|---|---|
| Health check | `health-sweep` | Health targets + vision |
| GAP analysis | `gap-chain` | Architecture docs, health reports |
| Capture learnings | `session-learning` | Session artifacts, git diff |
| Full orientation | Read `BOOTSTRAP.md` | Altitude routing index → choose bootstrap |

**Altitude-specific bootstraps** (use when no skill matches your work type):

| Altitude | Bootstrap File | Use When |
|---|---|---|
| STRATEGIC / PRODUCT | `BOOTSTRAP-STRATEGIC.md` | Vision, goals, roadmap, SYNTHESIS, P0-P4 |
| ARCHITECTURE | `BOOTSTRAP-ARCHITECTURE.md` | ADRs, module design, contracts, orchestrator |
| DELIVERY / EXECUTION | `BOOTSTRAP-DELIVERY.md` | S1-S9 workflow, task shaping, implementation |
| RETROSPECTIVE | `BOOTSTRAP-RETROSPECTIVE.md` | GAP analysis, health checks, learnings |

For lean follow-up sessions: `BOOTSTRAP_lean.md`.

Each skill defines exactly what context to load. This prevents context bloat and
enforces the context scoping rules from CLAUDE.md.

### Learnings & Optimization

Session learnings are captured in `state/learnings/` via the `session-learning` skill.
Running index at `state/learnings/INDEX.md`. Run at end of significant sessions.

## Gotchas

- **No CLI entrypoint** — the package is a library scaffold, not runnable.
- **`uv` is the package manager** — `uv.lock` at root. Use `uv run` prefix for all commands.
- **Dev tools not in pyproject extras** — ruff and mypy are in uv.lock metadata but not declared in `[project.optional-dependencies]`. `uv sync` installs them; bare `pip install -e ".[dev]"` only gets pytest.
- **Tests are unittest-style** — `unittest.TestCase` classes discovered by pytest. No conftest.py or fixtures.
- **No CI pipelines** — no `.github/workflows/`. Quality is enforced by local hooks only.
- **Heavy documentation repo** — ~250 markdown files vs ~10 Python files. The docs/state/templates directories are the primary working surface.
