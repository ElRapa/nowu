# Workflow Rules v2.1

## Status Values

Valid status values and their meanings:

```
DRAFT              -- agent output, not yet reviewed
APPROVED           -- human has reviewed and approved
READY_FOR_S1       -- intake brief cleared for S1 (human-set only)
READY_FOR_ARCH     -- S1 confirmed, ready for S2
READY_FOR_OPTIONS  -- S2 done, ready for S3
READY_FOR_DECISION -- S3 done, ready for S4
READY_FOR_SHAPING  -- S4 decision recorded, ready for S5
READY_FOR_IMPL     -- S5 task spec approved, ready for S6
READY_FOR_VBR      -- S6 implementation done, running VBR
READY_FOR_REVIEW   -- S7 VBR passed, ready for S8
DONE               -- S9 complete
CHANGES_REQUESTED  -- review failed, loops back to originating step
BLOCKED            -- human decision required before proceeding
```

## Approval Tiers

**Tier 1 -- auto-proceed:**
- Tests, documentation, refactors following existing ADRs
- Implementation within shaped task spec and in_scope_files
- VBR gate passage (automated via hooks)

**Tier 2 -- batch for human review:**
- Feature implementation with design changes
- New dependencies
- New story creation

**Tier 3 -- STOP and ask immediately:**
- Merges to main branch
- Breaking changes to contracts
- New ADR creation
- File deletion
- Architecture boundary violations
- Vision changes

When unsure, treat as Tier 2.

## Modes

- A (Full Cycle): S1-S9 -- use for new features from intake
- B (Implement Loop): S5-S6/S7(n)-S8-S9 -- use when tasks already shaped
- C (Single Step): S6-S9 -- use for bug fixes and small changes
- D (Architecture Only): S1-S4-S9 -- use for design spikes

## Pre-Workflow Modes

- BOOTSTRAP: P0.V + P0 + P1 + P2 + P3 + P4 (new product/project)
- FULL: P0 + P1 + P2 + P3 + P4 (new epic on existing product)
- STANDARD: P0 + P1 + P2 + P4 (new story, architecture current)
- LITE: P0 + P2 + P4 (feature on known project)

Entry: /pre-workflow run NNN --mode [BOOTSTRAP|FULL|STANDARD|LITE]
Exit: state/intake/intake-NNN.md with status READY_FOR_S1