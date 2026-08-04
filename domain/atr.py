"""
=========================================================
Trading Operating System (TOS)

Module      : ATR
Version     : 1.0.0
Author      : Rajesh Varma
Description : Immutable Average True Range.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ATR:
    """
    Average True Range.
    """

    period: int

    value: Decimal
