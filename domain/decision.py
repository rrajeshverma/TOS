"""
=========================================================
Trading Operating System (TOS)
Module      : Decision
Version     : 1.0.0
Author      : Rajesh Varma
Description : Strategy decision domain object.
=========================================================
"""

from dataclasses import dataclass
from datetime import datetime

from domain.market import Market
from domain.indicator_set import IndicatorSet

from shared.enums import Signal
from shared.enums import DecisionStatus


@dataclass(frozen=True, slots=True)
class Decision:
    """
    Represents the final output of the Strategy Engine.

    A Decision is NOT a trade.

    It simply records what the strategy concluded after
    evaluating a completed market candle.
    """

    # =====================================================
    # Identity
    # =====================================================

    decision_id: str

    timestamp: datetime

    # =====================================================
    # References
    # =====================================================

    market: Market

    indicator_set: IndicatorSet

    # =====================================================
    # Strategy Result
    # =====================================================

    signal: Signal

    status: DecisionStatus

    # =====================================================
    # Explanation
    # =====================================================

    reasons: tuple[str, ...]

    @property
    def is_tradeable(self) -> bool:
        """
        Returns True if strategy produced
        a valid trade opportunity.
        """
        return self.status == DecisionStatus.VALID

    @property
    def has_signal(self) -> bool:
        """
        Returns True if strategy generated
        a BUY signal.
        """
        return self.signal != Signal.NONE

    @property
    def reason_count(self) -> int:
        """
        Number of decision reasons.
        """
        return len(self.reasons)