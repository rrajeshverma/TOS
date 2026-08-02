"""
=========================================================
Trading Operating System (TOS)

Module      : Stop Loss
Version     : 1.0.0
Author      : Rajesh Varma
Description : Immutable stop-loss domain object.
=========================================================
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class StopLoss:
    """
    Represents the calculated stop-loss.
    """

    price: Decimal
    reason: str
