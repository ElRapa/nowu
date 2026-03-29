---
id: arch-2026-03-28
check_type: architecture
status: YELLOW
generated_at: 2026-03-28T00:00:00Z
agent_version: health-architecture@2.2
---

# Architecture Health Check: 2026-03-28

## Overall Status
status: YELLOW

## Note on Agent File Path Configuration

The `health-architecture` agent definition (`.claude/agents/health-architecture.md`) specifies:
- Required input: `docs/architecture/containers.md`
- Optional inputs: `docs/architecture/context.md`, `docs/architecture/adr/`

These paths do not exist. The project uses `docs/ARCHITECTURE.md` as a combined C4 L1+L2
document (a deliberate decision: the GAP chain creates `docs/architecture/` subdirectory only
when a Global Architecture Pass has been applied — see `FILE-STRUCTURE.md` notation "(post-GAP optional)").

This check was run against `docs/ARCHITECTURE.md` as the combined architecture document.
**The health-architecture agent definition needs to be updated to recognise `docs/ARCHITECTURE.md`
as the primary input when `docs/architecture/containers.md` is absent.**

## Findings

| Check | Status | Finding |
|---|---|---|
| C4 Accuracy | GREEN | `find src/ -maxdepth 2 -type d` returns: `src/nowu`, `src/nowu/core`, `src/nowu/bridge`, `src/nowu/soul`, `src/nowu/flow`. All 5 modules are documented in `docs/ARCHITECTURE.md` §4.1 module map. No undocumented src/ directory. `know` is correctly documented as an external package (no src/nowu/know/ dir exists, by design). Stage 1 — YELLOW threshold not triggered. |
| ADR Coverage | YELLOW | `docs/DECISIONS.md` contains 10 ACCEPTED decisions (D-001 through D-010). The project uses `DECISIONS.md` as its combined decision + ADR register — there is no separate `docs/architecture/adr/` directory. This is a valid design choice but the health agent was written for a project with separate ADR files. No ADR entries reference separate ADR file paths, which means the ADR Coverage check cannot be run as specified. Flagging YELLOW as informational: if a separate `docs/architecture/adr/` directory is ever created (post-GAP), the agent will need updating. |
| Superseded ADR References | GREEN | No ADR file references in `DECISIONS.md` frontmatter. Check not applicable in current structure. |
| Orphaned ADRs | GREEN | No `docs/architecture/adr/` directory. Check not applicable. |
| Container Interaction Gaps | GREEN | `docs/ARCHITECTURE.md` §4.2 documents data ownership and boundaries. §4.3 and §4.4 describe runtime interactions between containers. All 5 modules have at least one documented dependency/interaction. |
| Pending Arch Passes | YELLOW | Two arch-pass files exist in `state/arch/`, both dating from 2026-03-22 (6 days ago): `2026-03-22-memory-integration-constraints.md` (status: READY\_FOR\_OPTIONS) and `2026-03-22-memory-integration-options.md` (status: READY\_FOR\_DECISION). Both are self-marked STALE due to `know` v0.3→v0.4.0 breaking API changes. They belong to the old intake ID (`intake-2026-03-22-memory-integration`), not the current `intake-001.md`. The STALE flag + mismatched intake ID means these artifacts are in a limbo state — advanced states (READY\_FOR\_DECISION) but referencing a superseded intake and an obsolete API. |

## Key Issue: Agent Definition Path Mismatch

`health-architecture.md` requires `docs/architecture/containers.md` as a mandatory input.
If this agent is invoked by a future automated run, it will fail immediately with "required file missing"
and return a false RED status. The agent definition must be updated.

**Fix required in:** `.claude/agents/health-architecture.md`
- Primary input path: `docs/ARCHITECTURE.md` (when `docs/architecture/containers.md` absent)
- Note: check for `docs/architecture/containers.md` first; fall back to `docs/ARCHITECTURE.md`

## Recommended Actions

1. **Update health-architecture agent** — Fix input file reference. File: `.claude/agents/health-architecture.md`, section: `## Inputs`, action: add fallback logic for `docs/ARCHITECTURE.md` when `docs/architecture/` directory is absent.
2. **Resolve stale arch passes** — Either update `state/arch/2026-03-22-memory-integration-constraints.md` and `...-options.md` to reference `intake-001` and refresh API references for `know` v0.4.0; or archive them and re-run S2+S3 fresh against `intake-001.md`. File: `state/arch/`, both files. Recommend archiving and re-running.
3. **No C4 documentation update needed** — `docs/ARCHITECTURE.md` accurately reflects `src/` structure as of 2026-03-28.
