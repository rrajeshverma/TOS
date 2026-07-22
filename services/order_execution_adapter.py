"""
=========================================================
Trading Operating System (TOS)
Module      : Order Execution Adapter
Version     : 1.0.0
Description : Converts domain orders into execution orders.
=========================================================
"""

from __future__ import annotations

from domain.order import Order


class OrderExecutionAdapter:
    """
    Converts domain Order objects into execution layer format.
    """

    def to_execution_order(
        self,
        order: Order,
    ) -> dict:
        """
        Convert domain Order into execution order payload.
        """

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