"""
=========================================================
Trading Operating System (TOS)
Module      : Trade
Version     : 1.0.0
Author      : Rajesh Varma
Description : Trade domain object.
=========================================================
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.risk import Risk
from shared.enums import ExitReason, TradeStatus


@dataclass(frozen=True, slots=True)
class Trade:
    """
    Represents an approved trade.

    A Trade is created only after the Risk evaluation
    has approved the strategy decision.
    """

    # =====================================================
    # Identity
    # =====================================================

    trade_id: str

    # =====================================================
    # Reference
    # =====================================================

    risk: Risk

    # =====================================================
    # Entry
    # =====================================================

    entry_price: Decimal

    stop_loss: Decimal

    target: Decimal

    quantity: int

    entry_time: datetime

    # =====================================================
    # Exit
    # =====================================================

    exit_price: Decimal | None = None

    exit_time: datetime | None = None

    exit_reason: ExitReason = ExitReason.NONE

    # =====================================================
    # Status
    # =====================================================

    status: TradeStatus = TradeStatus.CREATED

    # =====================================================
    # Result
    # =====================================================

    pnl: Decimal = Decimal(0)

    @property
    def is_open(self) -> bool:
        """Returns True if the trade is currently open."""
        return self.status == TradeStatus.OPEN

    @property
    def is_closed(self) -> bool:
        """Returns True if the trade has been closed."""
        return self.status == TradeStatus.CLOSED
