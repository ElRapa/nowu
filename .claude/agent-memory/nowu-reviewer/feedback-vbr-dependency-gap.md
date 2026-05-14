---
name: vbr-dependency-gap
description: VBR does not catch undeclared runtime dependencies; transitive deps mask the gap
metadata:
  type: feedback
---

In intake-001, `session_store.py` imports `yaml` at runtime but `pyyaml` is only added
as a dev type-stub (`types-pyyaml`) in `[dependency-groups].dev`, not in
`[project.dependencies]`. All 5 VBR reports passed without catching this. `pyyaml` was
available transitively via `know` → `sentence-transformers` → `huggingface_hub`.

**Why:** VBR runs tests (which pass) and mypy/ruff (which pass because types-pyyaml
provides the stubs). Neither tool checks that production imports have declared runtime
dependencies.

**How to apply:** When reviewing S8, check every `import X` in `src/` that is not stdlib.
Confirm `X` appears in `pyproject.toml[project.dependencies]` (not just dev deps or
dependency-groups). If a package is only available transitively (not declared directly),
flag as W-1 warning.

Related: [[tdd-commit-order]], [[out-of-scope-decisions-md]]
