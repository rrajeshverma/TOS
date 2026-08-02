"""
=========================================================
Trading Operating System (TOS)

Module      : Stop Loss Engine
Description : Calculates logical stop-loss.
=========================================================
"""

from decimal import Decimal

from domain.stop_loss import StopLoss
from shared.enums import Signal


class StopLossEngine:
    """
    Calculates logical stop-loss.
    """

    def calculate(
        self,
        signal: Signal,
        previous_high: Decimal,
        previous_low: Decimal,
        ema_high: Decimal,
        ema_low: Decimal,
    ) -> StopLoss:
        if signal == Signal.BUY_CE:
            return StopLoss(
                price=previous_low,
                reason="Previous Candle Low",
            )

        if signal == Signal.BUY_PE:
            return StopLoss(
                price=previous_high,
                reason="Previous Candle High",
            )

        raise ValueError("Cannot calculate stop-loss.")
