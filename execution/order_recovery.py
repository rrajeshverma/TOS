"""
=========================================================
Trading Operating System (TOS)

Module      : Order Recovery
Description : Recovers broker orders after restart/failure.
=========================================================
"""

from dataclasses import dataclass, field


@dataclass
class OrderRecovery:
    """
    Handles pending order recovery.

    Supports:
    - Local pending order tracking
    - Broker order recovery
    """

    broker: object | None = None
    pending_orders: dict = field(
        default_factory=dict
    )


    def add_order(
        self,
        order_id,
        symbol,
    ):
        self.pending_orders[order_id] = symbol


    def remove_order(
        self,
        order_id,
    ):
        self.pending_orders.pop(
            order_id,
            None,
        )


    def has_pending_orders(self):

        return len(
            self.pending_orders
        ) > 0


    def pending_count(self):

        return len(
            self.pending_orders
        )


    def clear(self):

        self.pending_orders.clear()


    def get_order(
        self,
        order_id,
    ):

        return self.pending_orders.get(
            order_id
        )


    def recover(self):
        """
        Recover orders from broker.
        """

        if self.broker is None:
            raise RuntimeError(
                "Broker is not configured."
            )

        return self.broker.get_orders()


    def sync(self):
        """
        Recover and update local pending orders.
        """

        orders = self.recover()

        self.pending_orders.clear()

        for order in orders:

            if order.get("status") in (
                "PENDING",
                "OPEN",
            ):

                self.pending_orders[
                    order["order_id"]
                ] = order.get(
                    "symbol"
                )

        return orders


    def summary(self):

        return {
            "pending_orders": self.pending_orders.copy(),
            "pending_count": self.pending_count(),
            "has_pending": self.has_pending_orders(),
        }