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

        self._logger.info("IndicatorSet calculated successfully.")

        return indicator

    def _validate_history(
        self,
        candles: List[Market],
    ) -> None:

        if candles is None:
            raise ValueError("Market history is None.")

        if len(candles) < self.MIN_CANDLES:
            raise ValueError(f"Minimum {self.MIN_CANDLES} candles required.")

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

    @staticmethod
    def _ema(series: pd.Series) -> float:
        """
        Calculate the latest EMA value.
        """
        return float(
            series.ewm(
                span=EMA_PERIOD,
                adjust=False,
            )
            .mean()
            .iloc[-1]
        )

    @staticmethod
    def _rsi(series: pd.Series) -> float:
        """
        Calculate RSI using Wilder's method.
        """

        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / RSI_PERIOD,
            adjust=False,
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / RSI_PERIOD,
            adjust=False,
        ).mean()

        rs = avg_gain / avg_loss.replace(0, float("nan"))

        rsi = 100 - (100 / (1 + rs))

        return float(rsi.fillna(50).iloc[-1])

    @staticmethod
    def _vwap(df: pd.DataFrame) -> float:
        """
        Calculate VWAP.
        """

        typical_price = (df["high"] + df["low"] + df["close"]) / 3

        cumulative_tp_volume = (typical_price * df["volume"]).cumsum()

        cumulative_volume = (df["volume"]).cumsum()

        vwap = cumulative_tp_volume / cumulative_volume

        return float(vwap.iloc[-1])

    @staticmethod
    def _volume_average(
        df: pd.DataFrame,
    ) -> float:
        """
        Calculate rolling volume average.
        """

        return float(df["volume"].rolling(window=VOLUME_AVG_PERIOD).mean().iloc[-1])
