# Step 01 Architecture Analysis

Date: 2026-03-04
Use-case focus: `NF-01`, `NF-02`, `NF-03`
Affected modules: `core`, `flow`, `bridge`, `soul`
Non-negotiable constraint: `know` remains external system-of-record.

## Problem Statement

Step 01 needs a repository and contract baseline that lets agents implement later slices without boundary drift.
The baseline must be minimal, testable, and enforce module ownership from day one.

## Options

| Option | Summary | Delivery Speed (25) | Reliability (20) | Modularity (20) | Operational Simplicity (15) | Governance (20) | Weighted Total |
|---|---|---:|---:|---:|---:|---:|---:|
| A | Flat package layout with implicit boundaries | 5 | 2 | 2 | 5 | 2 | 3.15 |
| B | Per-module package layout with explicit contracts and boundary tests | 4 | 5 | 5 | 4 | 5 | 4.60 |
| C | Plugin registry and dynamic module loading now | 2 | 3 | 4 | 2 | 4 | 3.00 |

## Selected Option

Selected: **Option B**.

Rationale:
- Keeps the baseline small while giving hard boundaries.
- Produces machine-checkable guardrails for future AI-generated code.
- Avoids premature complexity from plugin systems.

## Risks and Mitigations

1. Risk: boundary tests may become stale as modules evolve.
- Mitigation: keep policy centralized in `nowu.core.boundaries` and test against AST imports.

2. Risk: no runtime logic yet may feel slow.
- Mitigation: Step 01 intentionally focuses on architectural safety; Step 02 immediately adds memory integration behavior.

## Required File/Contract Updates

- Add project packaging (`pyproject.toml`, `src/nowu/...`).
- Add explicit contracts under `src/nowu/core/contracts/`.
- Add boundary policy in `src/nowu/core/boundaries.py`.
- Add architecture tests under `tests/architecture/` and contract import smoke tests under `tests/core/`.

