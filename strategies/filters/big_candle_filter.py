"""
=========================================================
Trading Operating System (TOS)

Module      : Big Candle Filter
Version     : 1.0.0
Author      : Rajesh Varma
Description : Rejects trades after abnormally large candles.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal


class BigCandleFilter:
    """
    Reject entries after oversized candles.
    """

    def __init__(
        self,
        multiplier: Decimal = Decimal("2.0"),
    ) -> None:
        self._multiplier = multiplier

    def allowed(
        self,
        candle_body: Decimal,
        average_body: Decimal,
    ) -> bool:
        """
        Returns True if candle size is acceptable.
        """

        if average_body <= 0:
            return True

        return candle_body <= average_body * self._multiplier
