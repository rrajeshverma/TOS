"""
=========================================================
Trading Operating System (TOS)

Module      : Position Aggregator
Description : Converts positions into portfolio metrics.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal

from portfolio.portfolio_snapshot import PortfolioSnapshot


class PositionAggregator:
    """
    Aggregates active positions for portfolio calculations.
    """

    def position_count(
        self,
        positions,
    ):
        """
        Return number of open positions.
        """
        if not positions:
            return 0

        return len(positions)

    def exposure(
        self,
        positions,
    ):
        """
        Calculate total position exposure.

        Exposure =
        Quantity × Average Entry Price
        """

        total = Decimal("0")

        for position in positions:
            total += Decimal(str(position.quantity)) * Decimal(
                str(position.average_price)
            )

        return total

    def unrealized_pnl(
        self,
        positions,
    ):
        """
        Calculate unrealized profit/loss.

        P&L =
        (Last Price - Entry Price) × Quantity
        """

        total = Decimal("0")

        for position in positions:
            total += (
                Decimal(str(position.last_traded_price))
                - Decimal(str(position.average_price))
            ) * Decimal(str(position.quantity))

        return total

    def build_snapshot(
        self,
        positions,
        cash,
        realized_pnl=Decimal("0"),
    ):
        """
        Build portfolio snapshot from active positions.
        """

        unrealized = self.unrealized_pnl(positions)

        total_pnl = Decimal(str(realized_pnl)) + unrealized

        equity = Decimal(str(cash)) + total_pnl

        return PortfolioSnapshot(
            cash=cash,
            equity=equity,
            realized_pnl=realized_pnl,
            unrealized_pnl=unrealized,
            open_positions=self.position_count(positions),
        )
