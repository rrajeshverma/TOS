"""
=========================================================
Trading Operating System (TOS)
Module      : Market
Version     : 1.0.0
Author      : Rajesh Varma
Description : Represents one completed market candle.
=========================================================
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Market:
    """
    Represents one completed market candle.

    This object contains only raw market data received
    from the broker or data provider.
    """

    symbol: str
    exchange: str
    timeframe: str

    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: int

    @property
    def is_bullish(self) -> bool:
        """
        Returns True if candle closed above open.
        """
        return self.close > self.open

    @property
    def is_bearish(self) -> bool:
        """
        Returns True if candle closed below open.
        """
        return self.close < self.open

    @property
    def body_size(self) -> float:
        """
        Returns candle body size.
        """
        return abs(self.close - self.open)

    @property
    def candle_range(self) -> float:
        """
        Returns complete candle range.
        """
        return self.high - self.low