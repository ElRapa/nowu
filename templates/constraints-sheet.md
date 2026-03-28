***
id: intake-id-constraints
intake_id: intake-YYYY-MM-DD-slug
created: YYYY-MM-DD
status: DRAFT | READY_FOR_OPTIONS
arch_pass_ref: arch-pass-NNN | ~
***

# Constraints Sheet: [intake-id]

> If `arch-pass-NNN` exists from pre-workflow, this sheet extends it — do not replace it.
> Document divergences from arch-pass in the section below.

## Affected Modules

| Module | Container (C4 L2) | Impact | Confidence |
|---|---|---|---|
| [name] | [container] | add / modify / query | HIGH / MED / LOW |

## Binding Decisions

| D-ID | Title | How it constrains this work |
|---|---|---|
| D-NNN | [title] | [constraint description] |

## Binding Contracts

| Contract | Interface | Constraint |
|---|---|---|
| [name] | [method/protocol] | [what is and is not allowed] |

## Architectural Risks

| Risk | Severity | Mitigation |
|---|---|---|
| [risk description] | HIGH / MED / LOW | [mitigation or "flag for S3"] |

## Divergences from arch-pass (if applicable)

| arch-pass says | This analysis says | Rationale |
|---|---|---|
| [quoted arch-pass text] | [revised assessment] | [why different] |

## Open Questions for S3

1. [question]

***
```yaml
from_step: S2
to_step: S3
agent: nowu-options
status: READY_FOR_OPTIONS