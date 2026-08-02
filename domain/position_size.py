"""
=========================================================
Trading Operating System (TOS)

Module      : Position Size
Version     : 1.0.0
Author      : Rajesh Varma
Description : Immutable position sizing result.
=========================================================
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class PositionSize:
    """
    Result of position sizing calculation.
    """

    lots: int

    quantity: int

    risk_amount: Decimal
