"""
=========================================================
Trading Operating System (TOS)
Module      : Position Sizing Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Calculates position size based on
              account risk and stop-loss distance.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN

from domain.position_size import PositionSize


class PositionSizingEngine:
    """
    Calculates position size using fixed percentage risk.
    """

    def calculate(
        self,
        capital: Decimal,
        risk_percent: Decimal,
        stop_loss_distance: Decimal,
        lot_size: int = 1,
    ) -> PositionSize:
        """
        Calculate position size.
        """

        if capital <= 0:
            raise ValueError("Capital must be greater than zero.")

        if risk_percent <= 0:
            raise ValueError("Risk percent must be greater than zero.")

        if stop_loss_distance <= 0:
            raise ValueError("Stop loss distance must be greater than zero.")

        if lot_size <= 0:
            raise ValueError("Lot size must be greater than zero.")

        risk_amount = capital * risk_percent / Decimal("100")

        quantity = (risk_amount / stop_loss_distance).to_integral_value(
            rounding=ROUND_DOWN
        )

        lots = int(quantity) // lot_size

        quantity = lots * lot_size

        return PositionSize(
            lots=lots,
            quantity=quantity,
            risk_amount=risk_amount,
        )
