"""
TOS Risk Decision Object
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskDecision:
    """
    Immutable risk evaluation result.
    """

    approved: bool
    reason: str
    risk_score: int
    metadata: dict
