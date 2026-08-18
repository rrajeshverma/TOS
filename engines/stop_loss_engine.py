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
            price = min(previous_low, ema_low)
            return StopLoss(
                price=price,
                reason="Minimum of Previous Candle Low and EMA Low",
            )

        if signal == Signal.BUY_PE:
            price = max(previous_high, ema_high)
            return StopLoss(
                price=price,
                reason="Maximum of Previous Candle High and EMA High",
            )

        raise ValueError("Cannot calculate stop-loss.")
