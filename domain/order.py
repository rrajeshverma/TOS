"""
=========================================================
Trading Operating System (TOS)
Module      : Order
Version     : 1.0.0
Author      : Rajesh Varma
Description : Broker order domain object.
=========================================================
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.trade import Trade
from shared.enums import (
    Broker,
    OrderSide,
    OrderStatus,
)


@dataclass(frozen=True, slots=True)
class Order:
    """
    Represents an order sent to the broker.

    An Order is created from a Trade and tracks
    broker-specific execution details.
    """

    # =====================================================
    # Identity
    # =====================================================

    order_id: str

    broker_order_id: str | None

    # =====================================================
    # Reference
    # =====================================================

    trade: Trade

    # =====================================================
    # Broker Details
    # =====================================================

    broker: Broker

    side: OrderSide

    # =====================================================
    # Execution
    # =====================================================

    quantity: int

    requested_price: Decimal

    average_price: Decimal | None = None

    # =====================================================
    # Lifecycle
    # =====================================================

    status: OrderStatus = OrderStatus.CREATED

    created_at: datetime | None = None

    executed_at: datetime | None = None

    @property
    def is_executed(self) -> bool:
        """
        Returns True if the broker executed the order.
        """
        return self.status == OrderStatus.EXECUTED

    @property
    def is_pending(self) -> bool:
        """
        Returns True if the order is waiting for execution.
        """
        return self.status == OrderStatus.PENDING
