"""
TOS Approval Decision Object
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovalDecision:
    """
    Result of trade approval evaluation.
    """

    approved: bool
    reason: str
    metadata: dict
