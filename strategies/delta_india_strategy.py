"""
=========================================================
Trading Operating System (TOS)

Module      : Delta India Strategy
Version     : 1.0.0
Author      : Rajesh Varma
Description : Production strategy for
              Delta Exchange India BTC Futures.
=========================================================
"""

from __future__ import annotations

from datetime import time
from decimal import Decimal

from domain.strategy_result import StrategyResult
from shared.enums import Signal
from strategies.base_strategy import BaseStrategy
from strategies.filters.big_candle_filter import (
    BigCandleFilter,
)
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


class DeltaIndiaStrategy(BaseStrategy):
    """
    Production strategy for BTC Futures.
    """

    def __init__(self) -> None:
        self._time_filter = TimeFilter(
            time(0, 0),
            time(23, 59),
        )

        self._ema_filter = EMAFilter()

        self._rsi_filter = RSIFilter()

        self._vwap_filter = VWAPFilter()

        self._trade_limit_filter = TradeLimitFilter()

        self._confirmation_filter = ConfirmationFilter()

        self._big_candle_filter = BigCandleFilter()

    def name(self) -> str:
        return "DELTA_INDIA"

    def analyze(
        self,
        market,
        indicators,
    ) -> StrategyResult:
        """
        Analyze market conditions and return a trading decision.
        """

        close = market.close

        open_price = Decimal(str(market.open))
        close_price = Decimal(str(market.close))

        candle_body = abs(close_price - open_price)

        # Temporary fixed threshold.
        # Will be replaced with ATR / average candle size.
        average_body = Decimal(100)

        if not self._big_candle_filter.allowed(
            candle_body,
            average_body,
        ):
            return StrategyResult(
                signal=Signal.NONE,
                reasons=("Big candle rejected",),
            )

        buy_ema = self._ema_filter.buy_allowed(
            close,
            indicators.ema_high,
        )

        sell_ema = self._ema_filter.sell_allowed(
            close,
            indicators.ema_low,
        )

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
                    "Close above EMA High",
                    "Price above VWAP",
                    "RSI above 55",
                ),
            )

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
                    "Close below EMA Low",
                    "Price below VWAP",
                    "RSI below 45",
                ),
            )

        return StrategyResult(
            signal=Signal.NONE,
            reasons=("No trading opportunity",),
        )

    def generate_signal(
        self,
        market,
        indicators,
    ) -> Signal:
        """
        Return only the trading signal.
        """

        return self.analyze(
            market,
            indicators,
        ).signal
