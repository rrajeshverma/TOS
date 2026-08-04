"""
=========================================================
Trading Operating System (TOS)

Module      : Market Statistics
Version     : 1.0.0
Author      : Rajesh Varma
Description : Derived statistics from recent candles.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarketStatistics:
    """
    Derived statistics from recent market history.
    """

    average_body_size: float

    average_range: float

    highest_high: float

    lowest_low: float
