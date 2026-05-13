"""Shared contract types for nowu modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

RoleName = Literal["architect", "shaper", "implementer", "reviewer", "curator"]
ApprovalTier = Literal["tier1", "tier2", "tier3"]


@dataclass(frozen=True)
class TaskSpec:
    """A bounded work item emitted by the shaper role."""

    id: str
    title: str
    use_case_ids: list[str]
    in_scope: list[str]
    out_of_scope: list[str]
    acceptance_criteria: list[str]
    verification_commands: list[str]
    dependencies: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionRecord:
    """Architecture or workflow decision with explicit rationale."""

    title: str
    rationale: str
    risks: list[str] = field(default_factory=list)
    mitigations: list[str] = field(default_factory=list)
    use_case_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SessionSnapshot:
    """Deprecated — use SessionCheckpoint. Retained for compatibility; will be removed in v1."""

    session_id: str
    active_project: str
    active_role: RoleName
    next_action: str
    blockers: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SessionCheckpoint:
    """Durable session checkpoint with epistemic grade and workflow context."""

    session_id: str
    active_project: str
    active_role: RoleName
    next_action: str
    active_step: str
    last_artifact_path: str
    checkpoint_grade: str
    active_ids: dict[str, str] = field(default_factory=dict)
    completed_steps: list[str] = field(default_factory=list)
    schema_version: str = "v1"
