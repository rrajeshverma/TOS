from __future__ import annotations

from decimal import Decimal

from domain.trade import Trade


class EquityCurve:
    """
    Builds cumulative realized P&L from completed trades.
    """

    def __init__(self, trades: list[Trade]) -> None:
        self.trades = trades

    def values(self) -> list[Decimal]:
        """
        Return cumulative realized P&L after each completed trade.
        """

        equity = Decimal("0")
        curve: list[Decimal] = []

        for trade in self.trades:
            equity += trade.pnl
            curve.append(equity)

        return curve
