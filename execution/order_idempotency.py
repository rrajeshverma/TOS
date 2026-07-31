"""
=========================================================
Trading Operating System (TOS)

Module      : Order Idempotency
Description : Prevents duplicate order execution.
=========================================================
"""


class OrderIdempotency:
    """
    Tracks submitted orders to prevent duplicates.
    """

    def __init__(self):
        self._orders = {}

    def is_duplicate(
        self,
        order_key,
    ):
        return order_key in self._orders

    def record(
        self,
        order_key,
        result=None,
    ):
        self._orders[order_key] = result

    def get(
        self,
        order_key,
    ):
        return self._orders.get(order_key)

    def clear(
        self,
        order_key,
    ):
        self._orders.pop(
            order_key,
            None,
        )

    def reset(self):
        self._orders.clear()

    def count(self):
        return len(self._orders)
