"""
=========================================================
Trading Operating System (TOS)
Module      : Position
Version     : 1.0.0
Author      : Rajesh Varma
Description : Open trading position domain object.
=========================================================
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.order import Order
from shared.enums import TradeStatus


@dataclass(frozen=True, slots=True)
class Position:
    """
    Represents an active market position.

    A Position is created only after an Order
    has been executed by the broker.
    """

    # =====================================================
    # Identity
    # =====================================================

    position_id: str

    # =====================================================
    # Reference
    # =====================================================

    order: Order

    # =====================================================
    # Live Position
    # =====================================================

    quantity: int

    average_price: Decimal

    last_traded_price: Decimal

    # =====================================================
    # Status
    # =====================================================

    status: TradeStatus = TradeStatus.OPEN

    opened_at: datetime | None = None

    closed_at: datetime | None = None

    @property
    def is_open(self) -> bool:
        """
        Returns True if position is open.
        """
        return self.status == TradeStatus.OPEN

    @property
    def is_closed(self) -> bool:
        """
        Returns True if position is closed.
        """
        return self.status == TradeStatus.CLOSED

    @property
    def unrealized_points(self) -> Decimal:
        """
        Current unrealized gain/loss in points.
        """
        return self.last_traded_price - self.average_price
