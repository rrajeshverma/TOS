"""
TOS Duplicate Order Guard

Prevents duplicate order submissions.
"""

from __future__ import annotations


class OrderDuplicateGuard:
    """
    Tracks submitted orders and blocks duplicates.
    """

    def __init__(self) -> None:

        self._orders: set[str] = set()


    def is_duplicate(
        self,
        order_key: str,
    ) -> bool:
        """
        Check whether order already exists.
        """

        return (
            order_key
            in self._orders
        )


    def register(
        self,
        order_key: str,
    ) -> None:
        """
        Register submitted order.
        """

        self._orders.add(
            order_key
        )


    def can_submit(
        self,
        order_key: str,
    ) -> bool:
        """
        Return True when order is new.
        """

        return not self.is_duplicate(
            order_key
        )


    def clear(self) -> None:
        """
        Reset tracked orders.
        """

        self._orders.clear()
