"""
=========================================================
Trading Operating System (TOS)

Module      : Position Sizing Service
Version     : 1.0.0
Author      : Rajesh Varma
Description : Calculates risk-based position size.
=========================================================
"""

from decimal import ROUND_DOWN, Decimal

from domain.position_size import PositionSize


class PositionSizingService:
    """
    Calculates the maximum position size based on
    the configured risk per trade.
    """

    def calculate(
        self,
        risk_per_trade: Decimal,
        stop_distance: Decimal,
        lot_size: int,
    ) -> PositionSize:
        """
        Calculate lots and quantity.

        Formula

        Risk Per Lot = Stop Distance x Lot Size

        Lots = Risk Per Trade // Risk Per Lot
        """

        if risk_per_trade <= 0:
            raise ValueError("Risk per trade must be greater than zero.")

        if stop_distance <= 0:
            raise ValueError("Stop distance must be greater than zero.")

        if lot_size <= 0:
            raise ValueError("Lot size must be greater than zero.")

        risk_per_lot = stop_distance * Decimal(lot_size)

        lots = int(
            (risk_per_trade / risk_per_lot).to_integral_value(
                rounding=ROUND_DOWN,
            )
        )

        quantity = lots * lot_size

        risk_amount = Decimal(quantity) * stop_distance

        return PositionSize(
            lots=lots,
            quantity=quantity,
            risk_amount=risk_amount,
        )
