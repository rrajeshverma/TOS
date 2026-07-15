"""
=========================================================
Trading Operating System (TOS)
Module      : Indicator Engine
Version     : 1.0.0
Author       : Rajesh Varma
Description : Calculates technical indicators from
              completed market candles.
=========================================================
"""

from __future__ import annotations

from typing import List

import pandas as pd

from domain.market import Market
from domain.indicator_set import IndicatorSet
from shared.logger import get_logger

from config.indicators import (
    EMA_PERIOD,
    RSI_PERIOD,
    VOLUME_AVG_PERIOD,
)


class IndicatorEngine:
    """
    Calculates all technical indicators required
    by the trading strategy.

    Input:
        List[Market]

    Output:
        IndicatorSet
    """

    MIN_CANDLES = max(
        EMA_PERIOD,
        RSI_PERIOD,
        VOLUME_AVG_PERIOD,
    )

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def calculate(
        self,
        candles: List[Market],
    ) -> IndicatorSet:
        """
        Calculate all indicators from market history.
        """

        self._validate_history(candles)

        df = self._to_dataframe(candles)

        ema_high = self._ema(df["high"])
        ema_low = self._ema(df["low"])
        rsi = self._rsi(df["close"])
        vwap = self._vwap(df)
        volume_avg = self._volume_average(df)

        indicator = IndicatorSet(
            ema_high=ema_high,
            ema_low=ema_low,
            vwap=vwap,
            rsi=rsi,
            volume_average=volume_avg,
        )

        self._logger.info(
            "IndicatorSet calculated successfully."
        )

        return indicator

    def _validate_history(
        self,
        candles: List[Market],
    ) -> None:

        if candles is None:
            raise ValueError("Market history is None.")

        if len(candles) < self.MIN_CANDLES:
            raise ValueError(
                f"Minimum {self.MIN_CANDLES} candles required."
            )

    @staticmethod
    def _to_dataframe(
        candles: List[Market],
    ) -> pd.DataFrame:

        return pd.DataFrame(
            {
                "high": [c.high for c in candles],
                "low": [c.low for c in candles],
                "close": [c.close for c in candles],
                "volume": [c.volume for c in candles],
            }
        )