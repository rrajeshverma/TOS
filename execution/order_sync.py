"""
Order synchronization coordinator.

Coordinates synchronization of broker orders and positions with
the local execution state.
"""

from __future__ import annotations


class OrderSync:
    """Coordinates broker order and position synchronization."""

    def __init__(
        self,
        broker,
        execution_sync,
        position_synchronizer,
    ) -> None:
        self._broker = broker
        self._execution_sync = execution_sync
        self._position_synchronizer = position_synchronizer

    def synchronize_orders(self) -> None:
        """
        Synchronize broker orders.

        The broker should return broker order objects or dictionaries
        containing at least:

            order_id
            status
            broker_order_id
        """

        for order in self._broker.get_orders():
            self._execution_sync.process(
                order_id=order.order_id,
                status=order.status,
                broker_order_id=order.broker_order_id,
            )

    def synchronize_positions(self) -> None:
        """Synchronize broker positions."""

        self._position_synchronizer.synchronize()

    def synchronize(self) -> None:
        """Synchronize both orders and positions."""

        self.synchronize_orders()
        self.synchronize_positions()
