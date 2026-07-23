"""
=========================================================
Trading Operating System (TOS)
Module      : Order Execution Adapter
Version     : 1.1.0
Description : Converts and executes orders through broker.
=========================================================
"""

from __future__ import annotations

from execution.order_idempotency import OrderIdempotency

from domain.order import Order


class OrderExecutionAdapter:
    """
    Converts domain orders and routes execution to broker.
    """

    def __init__(
        self,
        broker=None,
        order_service=None,
        idempotency=None,
    ):
        self.broker = broker
        self.order_service = order_service
        self.idempotency = idempotency or OrderIdempotency()

    def to_execution_order(
        self,
        order: Order,
    ) -> dict:
        """
        Convert domain Order into execution order payload.
        """

        if order is None:
            raise ValueError("Order cannot be None.")

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
        """
        Execute order with duplicate protection.
        """

        order_key = str(sorted(order.items()))

        if self.idempotency.is_duplicate(order_key):
            return self.idempotency.get(order_key)

        if self.order_service is not None:
            result = self.order_service.place_order(order)

            self.idempotency.record(
                order_key,
                result,
            )

            return result

        if self.broker is not None:
            if hasattr(
                self.broker,
                "is_connected",
            ):
                if not self.broker.is_connected():
                    raise RuntimeError("Broker is not connected.")

            result = self.broker.place_order(order)

            self.idempotency.record(
                order_key,
                result,
            )

            return result

        raise RuntimeError("Execution service is not configured.")
