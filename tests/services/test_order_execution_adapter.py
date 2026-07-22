"""
=========================================================
Trading Operating System (TOS)
Module      : Order Execution Adapter
Version     : 1.1.0
Description : Converts and executes orders through broker.
=========================================================
"""

from __future__ import annotations

from domain.order import Order


class OrderExecutionAdapter:
    """
    Converts domain orders and routes execution to broker.
    """

    def __init__(
        self,
        broker=None,
    ):
        self.broker = broker

    def to_execution_order(
        self,
        order: Order,
    ) -> dict:

        if order is None:
            raise ValueError(
                "Order cannot be None."
            )

        symbol = order.trade.risk.decision.market.symbol

        return {
            "symbol": symbol,
            "side": order.side.value,
            "quantity": order.quantity,
            "price": float(order.requested_price),
        }

    def execute(
        self,
        order: dict,
    ) -> dict:

        if self.broker is None:
            raise RuntimeError(
                "Broker is not configured."
            )

        return self.broker.place_order(order)