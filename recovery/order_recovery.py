"""
TOS Order Recovery Service

Recovers order state after runtime restart.
"""

from __future__ import annotations


class OrderRecoveryService:
    """
    Handles recovery of submitted orders.
    """

    def __init__(self) -> None:
        self._recovered_orders: dict[str, dict] = {}

    def recover(
        self,
        order_id: str,
        broker_status: dict,
    ) -> dict:
        """
        Store recovered broker order state.
        """

        state = {
            "order_id": order_id,
            "status": broker_status.get("status"),
            "broker_order_id": broker_status.get("orderId"),
        }

        self._recovered_orders[order_id] = state

        return state

    def get(
        self,
        order_id: str,
    ) -> dict | None:
        """
        Return recovered order.
        """

        return self._recovered_orders.get(order_id)

    def count(self) -> int:
        """
        Number of recovered orders.
        """

        return len(self._recovered_orders)

    def clear(self) -> None:
        """
        Clear recovery state.
        """

        self._recovered_orders.clear()
