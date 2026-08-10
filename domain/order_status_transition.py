"""
=========================================================
Trading Operating System (TOS)
Module      : Order Status Transition
Version     : 1.0.0
Description : Defines valid order lifecycle transitions.
=========================================================
"""

from typing import ClassVar

from shared.enums import OrderStatus


class OrderStatusTransition:
    """
    Controls valid transitions between order statuses.
    """

    _TRANSITIONS: ClassVar[dict] = {
        OrderStatus.CREATED: {
            OrderStatus.PENDING,
        },
        OrderStatus.PENDING: {
            OrderStatus.EXECUTED,
            OrderStatus.REJECTED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.EXECUTED: set(),
        OrderStatus.REJECTED: set(),
        OrderStatus.CANCELLED: set(),
    }

    @classmethod
    def can_transition(
        cls,
        current: OrderStatus,
        target: OrderStatus,
    ) -> bool:
        """
        Check whether an order status change is allowed.
        """

        return target in cls._TRANSITIONS.get(
            current,
            set(),
        )
