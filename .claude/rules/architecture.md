# Architecture Rules v2.1

## Layer Boundaries

Agents and Claude sessions must respect C4 level boundaries at all times.

| Level | What you may access | What you must never access |
|---|---|---|
| Above L1 (P0-P2) | vision.md, ideas, discovery, problems, stories | src/, tests/, ARCHITECTURE.md |
| L1 (S1, S2) | ARCHITECTURE.md system section, DECISIONS.md, intake | src/ bodies, tests/ |
| L2 (S3, S4) | containers, module __init__.py surfaces, contracts | src/ bodies, test bodies |
| L3 (S5, S8) | file tree, contracts, task specs | ARCHITECTURE.md, vision |
| L4 (S6, S7) | in_scope_files ONLY, task spec, pyproject.toml | everything else |

## Module Boundaries

- Modules communicate only through contracts defined in `core/contracts.py`.
- Direct imports between non-adjacent modules are forbidden.
- No module may write to another module's private state.

## ADR Rules

- All ADRs in `docs/architecture/adr/` are binding.
- A decision may not be contradicted without a superseding ADR.
- Superseding ADRs must be created and marked ACCEPTED before the decision changes.
- ADR status flow: PROPOSED -> ACCEPTED -> SUPERSEDED.

## Pre-Workflow Boundary

Pre-workflow agents (P0-P4) must never:
- Read or write files in `src/` or `tests/`
- Make implementation decisions
- Specify function signatures, class names, or database schemas

S1-S9 agents must never:
- Read `docs/vision.md` during implementation steps (S5-S7)
- Read full `docs/ARCHITECTURE.md` during implementation (S5-S7)
- Modify `state/arch/arch-pass-NNN.md` -- it is a read-only input from pre-workflow
