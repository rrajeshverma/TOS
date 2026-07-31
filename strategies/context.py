"""
TOS Strategy Context

Provides controlled trading information access
to strategy plugins.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyContext:
    """
    Immutable context passed to strategies.
    """

    market: object
    indicators: object
    positions: object
    risk_state: object
    account: object

    def __post_init__(self) -> None:
        if self.market is None:
            raise ValueError("Market context is required")

        if self.indicators is None:
            raise ValueError("Indicators context is required")

        if self.positions is None:
            raise ValueError("Positions context is required")

        if self.risk_state is None:
            raise ValueError("Risk state is required")

        if self.account is None:
            raise ValueError("Account context is required")
