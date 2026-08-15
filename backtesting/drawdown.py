"""
=========================================================
Trading Operating System (TOS)
Module      : Drawdown
Description : Calculates drawdown from an equity curve.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal


class Drawdown:
    """
    Calculates maximum drawdown from equity values.
    """

    def __init__(self, equity: list[Decimal]) -> None:
        self._equity = equity

    @property
    def maximum(self) -> Decimal:
        """
        Return the maximum peak-to-trough drawdown.
        """

        peak = Decimal("0")
        maximum_drawdown = Decimal("0")

        for value in self._equity:
            if value > peak:
                peak = value

            drawdown = peak - value

            if drawdown > maximum_drawdown:
                maximum_drawdown = drawdown

        return maximum_drawdown
