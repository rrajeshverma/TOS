"""
=========================================================
Trading Operating System (TOS)

Module      : Trade Management
Version     : 1.0.0
Author      : Rajesh Varma
Description : Immutable trade management decision.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class TradeManagement:
    """
    Represents trade management actions.
    """

    move_stop_loss: bool

    new_stop_loss: Decimal | None

    exit_trade: bool
