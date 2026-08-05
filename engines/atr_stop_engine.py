"""
=========================================================
Trading Operating System (TOS)

Module      : ATR Stop Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Calculates ATR-based stop loss.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal


class ATRStopEngine:
    """
    Calculates ATR-based stop loss.
    """

    def calculate(
        self,
        entry_price: Decimal,
        atr: Decimal,
        multiplier: Decimal = Decimal("1.5"),
    ) -> Decimal:
        """
        Calculate stop loss using ATR.
        """

        if atr <= 0:
            raise ValueError("ATR must be greater than zero.")

        if multiplier <= 0:
            raise ValueError("Multiplier must be greater than zero.")

        return entry_price - (atr * multiplier)
