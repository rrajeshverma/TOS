"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Plan
Version     : 1.0.0
Author      : Rajesh Varma
Description : Immutable execution-ready trade plan.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from domain.decision import Decision
from domain.position_size import PositionSize


@dataclass(frozen=True, slots=True)
class TradePlan:
    """
    Immutable execution-ready trade plan.

    The original underlying trade information is preserved.
    Option contract details are optional so existing callers
    remain backward compatible while NIFTY option execution
    is introduced.
    """

    decision: Decision
    position_size: PositionSize

    entry_price: Decimal
    stop_loss: Decimal
    target_price: Decimal

    # Selected derivative contract, when applicable.
    symbol: str | None = None
    security_id: str | None = None
    exchange_segment: str | None = None
    lot_size: int | None = None
    expiry: object | None = None
    strike: Decimal | None = None
    option_type: str | None = None
