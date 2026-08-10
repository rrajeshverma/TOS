"""
=========================================================
Trading Operating System (TOS)

Module      : ATR Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Calculates Average True Range (ATR).
=========================================================
"""

from __future__ import annotations

from decimal import Decimal

from domain.atr import ATR


class ATREngine:
    """
    Calculates Average True Range (ATR).
    """

    def calculate(
        self,
        true_ranges: list[Decimal],
        period: int = 14,
    ) -> ATR:
        """
        Calculate ATR from a list of True Range values.
        """

        if period <= 0:
            raise ValueError("Period must be greater than zero.")

        if len(true_ranges) < period:
            raise ValueError("Not enough True Range values.")

        atr = sum(
            true_ranges[-period:],
            Decimal(0),
        ) / Decimal(period)

        return ATR(
            period=period,
            value=atr,
        )
