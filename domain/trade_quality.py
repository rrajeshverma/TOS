"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Quality
Version     : 1.0.0
Author      : Rajesh Varma
Description : Represents the outcome of trade quality
              evaluation before risk assessment.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TradeQuality:
    """
    Represents whether a strategy signal is
    considered good enough to continue to
    risk evaluation.
    """

    approved: bool

    reasons: tuple[str, ...]

    @property
    def is_approved(self) -> bool:
        """
        Returns True if the trade passed all
        quality filters.
        """
        return self.approved

    @property
    def reason_count(self) -> int:
        """
        Number of rejection reasons.
        """
        return len(self.reasons)
