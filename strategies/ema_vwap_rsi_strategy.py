"""
EMA + VWAP + RSI Trend Strategy.

Strategy Rules

BUY
- Close > EMA High
- RSI > 55
- Price > VWAP

SELL
- Close < EMA Low
- RSI < 45
- Price < VWAP

Otherwise HOLD.
"""

from __future__ import annotations
from datetime import time

from shared.enums import Signal

from strategies.base_strategy import BaseStrategy
from strategies.filters.confirmation_filter import (
    ConfirmationFilter,
)
from strategies.filters.ema_filter import EMAFilter
from strategies.filters.rsi_filter import RSIFilter
from strategies.filters.time_filter import TimeFilter
from strategies.filters.trade_limit_filter import (
    TradeLimitFilter,
)
from strategies.filters.vwap_filter import VWAPFilter


class EMAVWAPRSIStrategy(BaseStrategy):
    """
    EMA + VWAP + RSI Trend Strategy.
    """

    def __init__(self) -> None:
        self._time_filter = TimeFilter(
            time(10, 15),
            time(14, 30),
        )

        self._rsi_filter = RSIFilter()

        self._ema_filter = EMAFilter()

        self._vwap_filter = VWAPFilter()

        self._trade_limit_filter = TradeLimitFilter()

        self._confirmation_filter = ConfirmationFilter()

    def name(self):
        return "EMA_VWAP_RSI"

    def analyze(
        self,
        market,
        indicators,
    ):
        return {
            "market": market,
            "indicators": indicators,
        }

    def generate_signal(
        self,
        market,
        indicators,
    ):
        close = market.close

        if not self._ema_filter.buy_allowed(
            close,
            indicators.ema_high,
        ) and not self._ema_filter.sell_allowed(
            close,
            indicators.ema_low,
        ):
            return Signal.NONE

        if self._rsi_filter.buy_allowed(
            indicators.rsi,
        ):
            if self._vwap_filter.buy_allowed(
                close,
                indicators.vwap,
            ):
                return Signal.BUY_CE

        if self._rsi_filter.sell_allowed(
            indicators.rsi,
        ):
            if self._vwap_filter.sell_allowed(
                close,
                indicators.vwap,
            ):
                return Signal.BUY_PE

        return Signal.NONE
