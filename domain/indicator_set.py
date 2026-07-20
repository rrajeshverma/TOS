"""
=========================================================
Trading Operating System (TOS)
Module      : Indicator Set
Version     : 1.0.0
Author      : Rajesh Varma
Description : Represents calculated technical indicators
              for one completed market candle.
=========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IndicatorSet:
    """
    Represents all technical indicators
    calculated for a single completed candle.
    """

    ema_high: float
    ema_low: float

    vwap: float

    rsi: float

    volume_average: float

    @property
    def is_bullish(self) -> bool:
        """
        Bullish indicator confirmation.
        """
        return self.rsi > 55

    @property
    def is_bearish(self) -> bool:
        """
        Bearish indicator confirmation.
        """
        return self.rsi < 45
