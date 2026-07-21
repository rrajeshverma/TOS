"""
Order Service.

Manages the lifecycle of orders within the Trading Operating System.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from execution.order_events import OrderEvent, OrderEventType


class OrderStatus(str, Enum):
    """Represents the lifecycle state of an order."""

    NEW = "NEW"
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


class OrderService:
    """Service responsible for managing and placing orders."""

    def __init__(
        self,
        broker=None,
        repository=None,
        dispatcher=None,
    ) -> None:
        self._broker = broker
        self._repository = repository
        self._dispatcher = dispatcher

        self._orders: dict[int, dict[str, Any]] = {}
        self._statuses: dict[int, OrderStatus] = {}
        self._broker_order_ids: dict[int, str] = {}

        self._next_order_id = 1

    @property
    def order_count(self) -> int:
        """Return the number of tracked orders."""
        return len(self._orders)

    def submit(self, order: dict[str, Any]) -> int:
        """
        Register an order locally.

        Returns the generated internal order ID.
        """
        order_id = self._next_order_id

        self._orders[order_id] = dict(order)
        self._statuses[order_id] = OrderStatus.NEW

        self._next_order_id += 1

        self._publish_event(
            order_id=order_id,
            event_type=OrderEventType.NEW,
        )

        return order_id

    def get(self, order_id: int) -> dict[str, Any] | None:
        """Return an order by its internal ID."""
        return self._orders.get(order_id)

    def status(self, order_id: int) -> OrderStatus | None:
        """Return the current status of an order."""
        return self._statuses.get(order_id)

    def update_status(self, order_id: int, status: OrderStatus) -> None:
        """
        Update the status of an existing order.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        current = self._statuses[order_id]

        # Ignore duplicate status updates (idempotent)
        if status == current:
            return

        allowed = self._ALLOWED_TRANSITIONS.get(current, set())

        if status not in allowed:
            raise ValueError(
                f"Invalid status transition: {current.value} -> {status.value}"
            )

        self._statuses[order_id] = status

        self._publish_event(
            order_id=order_id,
            event_type=OrderEventType(status.value),
            broker_order_id=self.broker_order_id(order_id),
        )

    def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        """
        Place an order through the configured broker.

        The broker response is optionally persisted using the configured
        repository and then returned.
        """
        if self._broker is None:
            raise RuntimeError("Broker is not configured.")

        result = self._broker.place_order(order)

        if self._repository is not None:
            self._repository.add(result)

        return result

    def cancel_order(self, order_id: int) -> bool:
        """
        Cancel an existing order.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        self._statuses[order_id] = OrderStatus.CANCELLED

        if self._broker is not None and hasattr(self._broker, "cancel_order"):
            self._broker.cancel_order(order_id)

        self._publish_event(
            order_id=order_id,
            event_type=OrderEventType.CANCELLED,
            broker_order_id=self.broker_order_id(order_id),
        )

        return True

    def register_broker_order(
        self,
        order_id: int,
        broker_order_id: str,
    ) -> None:
        """
        Associate an internal order with a broker order.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        if order_id in self._broker_order_ids:
            raise ValueError(
                f"Broker order already registered for order {order_id}"
            )

        self._broker_order_ids[order_id] = broker_order_id

    def broker_order_id(self, order_id: int) -> str | None:
        """
        Return the broker order ID for an internal order.
        """
        return self._broker_order_ids.get(order_id)

    def _publish_event(
        self,
        *,
        order_id: int,
        event_type: OrderEventType,
        broker_order_id: str | None = None,
    ) -> None:
        """Publish an order event if a dispatcher is configured."""
        if self._dispatcher is None:
            return

        self._dispatcher.publish(
            OrderEvent(
                order_id=order_id,
                event_type=event_type,
                broker_order_id=broker_order_id,
            )
        )

    _ALLOWED_TRANSITIONS = {
        OrderStatus.NEW: {
            OrderStatus.PENDING,
            OrderStatus.SUBMITTED,
            OrderStatus.CANCELLED,
            OrderStatus.FILLED,
        },
        OrderStatus.PENDING: {
            OrderStatus.SUBMITTED,
            OrderStatus.CANCELLED,
            OrderStatus.FILLED,
        },
        OrderStatus.SUBMITTED: {
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.FILLED: set(),
        OrderStatus.CANCELLED: set(),
    }