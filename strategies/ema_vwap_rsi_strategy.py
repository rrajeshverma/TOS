"""
=========================================================
Trading Operating System (TOS)

Module      : EMA + VWAP + RSI Strategy
Version     : 2.0.0
Author      : Rajesh Varma
Description : Trend-following strategy using
              EMA, VWAP and RSI.
=========================================================
"""

from __future__ import annotations

from datetime import time

from domain.strategy_result import StrategyResult
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

    BUY
        • Close > EMA High
        • RSI > 55
        • Close > VWAP

    SELL
        • Close < EMA Low
        • RSI < 45
        • Close < VWAP
    """

    def __init__(self) -> None:
        self._time_filter = TimeFilter(
            time(10, 15),
            time(14, 30),
        )

        self._ema_filter = EMAFilter()

        self._rsi_filter = RSIFilter()

        self._vwap_filter = VWAPFilter()

        self._trade_limit_filter = TradeLimitFilter()

        self._confirmation_filter = ConfirmationFilter()

    def name(self) -> str:
        return "EMA_VWAP_RSI"

    def analyze(
        self,
        market,
        indicators,
    ) -> StrategyResult:
        """
        Analyze the current market and return a StrategyResult.
        """
        if not self._time_filter.allow(market.timestamp.time()):
            return StrategyResult(
                signal=Signal.NONE,
                reasons=("Outside trading window",),
            )

        close = market.close

        # ------------------------------------------
        # EMA Filter
        # ------------------------------------------

        buy_ema = self._ema_filter.buy_allowed(
            close,
            indicators.ema_high,
        )

        sell_ema = self._ema_filter.sell_allowed(
            close,
            indicators.ema_low,
        )

        if not buy_ema and not sell_ema:
            return StrategyResult(
                signal=Signal.NONE,
                reasons=("EMA conditions not met",),
            )

        # ------------------------------------------
        # BUY
        # ------------------------------------------

        if (
            buy_ema
            and self._rsi_filter.buy_allowed(
                indicators.rsi,
            )
            and self._vwap_filter.buy_allowed(
                close,
                indicators.vwap,
            )
        ):
            return StrategyResult(
                signal=Signal.BUY_CE,
                reasons=(
                    "EMA bullish confirmation",
                    "RSI bullish confirmation",
                    "VWAP bullish confirmation",
                ),
            )

        # ------------------------------------------
        # SELL
        # ------------------------------------------

        if (
            sell_ema
            and self._rsi_filter.sell_allowed(
                indicators.rsi,
            )
            and self._vwap_filter.sell_allowed(
                close,
                indicators.vwap,
            )
        ):
            return StrategyResult(
                signal=Signal.BUY_PE,
                reasons=(
                    "EMA bearish confirmation",
                    "RSI bearish confirmation",
                    "VWAP bearish confirmation",
                ),
            )

        # ------------------------------------------
        # NO SIGNAL
        # ------------------------------------------

        return StrategyResult(
            signal=Signal.NONE,
            reasons=("Strategy conditions not met",),
        )
