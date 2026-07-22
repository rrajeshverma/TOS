"""
=========================================================
Trading Operating System (TOS)
Module      : Order Factory
Version     : 1.0.0
Author      : Rajesh Varma
Description : Creates Order domain objects from Trades.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal

from domain.order import Order
from domain.trade import Trade
from shared.enums import (
    Broker,
    OrderSide,
    OrderStatus,
)
from shared.logger import get_logger
from utils.id_generator import generate_order_id


class OrderFactory:
    """
    Creates immutable Order objects.
    """

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def create(
        self,
        trade: Trade,
        broker: Broker,
        side: OrderSide,
        price: Decimal,
    ) -> Order:
        """
        Create an Order from an approved Trade.
        """

        if trade is None:
            raise ValueError(
                "Cannot create Order without Trade."
            )

        if not trade.risk.is_approved:
            raise ValueError(
                "Cannot create Order from rejected Trade."
            )

        order = Order(
            order_id=generate_order_id(),
            broker_order_id=None,
            trade=trade,
            broker=broker,
            side=side,
            quantity=trade.quantity,
            requested_price=price,
            status=OrderStatus.CREATED,
        )

        self._logger.info(
            "Order created: %s",
            order.order_id,
        )

        return order