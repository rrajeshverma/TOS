"""
TOS Portfolio Context

Provides portfolio state information
to risk and strategy components.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioContext:
    """
    Immutable portfolio snapshot.
    """

    cash: float
    positions: list
    exposure: float
    available_margin: float
    pnl: float


    def __post_init__(self) -> None:

        if self.cash is None:
            raise ValueError(
                "Cash is required"
            )

        if self.positions is None:
            raise ValueError(
                "Positions are required"
            )

        if self.available_margin < 0:
            raise ValueError(
                "Available margin cannot be negative"
            )
