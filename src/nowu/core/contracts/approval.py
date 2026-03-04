"""Approval routing contract used by bridge and flow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .types import ApprovalTier


@dataclass(frozen=True)
class ApprovalItem:
    """Single unit of work pending approval."""

    id: str
    title: str
    tier: ApprovalTier
    reason: str


class ApprovalRouter(Protocol):
    """Route work items to tiered approval queues."""

    def classify(self, title: str, risk_markers: list[str]) -> ApprovalTier:
        """Classify work item into an approval tier."""

    def enqueue(self, item: ApprovalItem) -> None:
        """Queue an item for review/approval."""
