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
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
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
        self._filled_quantities: dict[int, int] = {}
        self._filled_values: dict[int, float] = {}

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
        self._filled_quantities[order_id] = 0
        self._filled_values[order_id] = 0.0

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

    def filled_quantity(self, order_id: int) -> int:
        """Return filled quantity."""
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        return self._filled_quantities[order_id]

    def remaining_quantity(self, order_id: int) -> int:
        """Return remaining quantity."""
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        total = self._orders[order_id]["quantity"]
        return total - self._filled_quantities[order_id]
    
    def average_fill_price(self, order_id: int) -> float:
        """
        Return the average execution price for an order.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        filled = self._filled_quantities[order_id]

        if filled == 0:
            return 0.0

        return self._filled_values[order_id] / filled
    
    def modify_order(
        self,
        order_id: int,
        quantity: int | None = None,
    ) -> None:
        """
        Modify an existing order.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        current = self.status(order_id)

        if current in (
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
        ):
            raise ValueError(
                f"Cannot modify order in {current.value} state."
            )

        if quantity is not None:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            if quantity < self._filled_quantities[order_id]:
                raise ValueError(
                    "Modified quantity cannot be less than filled quantity."
                )

            self._orders[order_id]["quantity"] = quantity

    def order(self, order_id: int) -> dict[str, Any]:
        """
        Return a copy of the order details.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        return dict(self._orders[order_id])


    def record_fill(
        self,
        order_id: int,
        quantity: int,
        price: float = 0.0,
    ) -> None:
        """
        Record an execution fill.
        """
        if order_id not in self._orders:
            raise KeyError(f"Unknown order id: {order_id}")

        total = self._orders[order_id]["quantity"]
        filled = self._filled_quantities[order_id]

        new_total = filled + quantity

        if new_total > total:
            raise ValueError("Order overfilled.")

        self._filled_quantities[order_id] = new_total
        self._filled_values[order_id] += quantity * price

        if new_total == total:
            self.update_status(order_id, OrderStatus.FILLED)
        else:
            self.update_status(order_id, OrderStatus.PARTIALLY_FILLED)

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

        # Ignore stale / out-of-order status updates
        if self._STATUS_ORDER[status] < self._STATUS_ORDER[current]:
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
        
        current_status = self.status(order_id)

        if current_status in (
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
        ):
            raise ValueError(
                f"Cannot cancel order in {current_status.value} state."
            )

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
    
    def process_broker_callback(
        self,
        broker_order_id: str,
        status: OrderStatus,
    ) -> None:
        """
        Process a broker callback using the broker order ID.
        """
        for order_id, registered_broker_id in self._broker_order_ids.items():
            if registered_broker_id == broker_order_id:
                self.update_status(order_id, status)
                return

        raise KeyError(f"Unknown broker order id: {broker_order_id}")

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

    _STATUS_ORDER = {
        OrderStatus.NEW: 0,
        OrderStatus.PENDING: 1,
        OrderStatus.SUBMITTED: 2,
        OrderStatus.PARTIALLY_FILLED: 3,
        OrderStatus.FILLED: 4,
        OrderStatus.CANCELLED: 4,
    }

    _ALLOWED_TRANSITIONS = {
        OrderStatus.NEW: {
            OrderStatus.PENDING,
            OrderStatus.SUBMITTED,
            OrderStatus.PARTIALLY_FILLED,
            OrderStatus.CANCELLED,
            OrderStatus.FILLED,
        },
        OrderStatus.PENDING: {
            OrderStatus.SUBMITTED,
            OrderStatus.PARTIALLY_FILLED,
            OrderStatus.CANCELLED,
            OrderStatus.FILLED,
        },
        OrderStatus.SUBMITTED: {
            OrderStatus.PARTIALLY_FILLED,
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.PARTIALLY_FILLED: {
            OrderStatus.PARTIALLY_FILLED,
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.FILLED: set(),
        OrderStatus.CANCELLED: set(),
    }