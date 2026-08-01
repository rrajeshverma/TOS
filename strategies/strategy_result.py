"""
Strategy evaluation result.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StrategyResult:
    """
    Result returned by every strategy.
    """

    signal: str
    reason: str = ""

    @property
    def is_buy(self) -> bool:
        return self.signal == "BUY"

    @property
    def is_sell(self) -> bool:
        return self.signal == "SELL"

    @property
    def is_hold(self) -> bool:
        return self.signal == "HOLD"
