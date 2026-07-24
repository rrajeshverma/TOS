"""
Order registry for duplicate order protection.
"""

from collections.abc import Hashable


class OrderRegistry:
    """Tracks submitted orders by request ID."""

    def __init__(self) -> None:
        self._orders: dict[Hashable, object] = {}

    def register(self, request_id: Hashable, order: object) -> None:
        """Register a new order."""
        if request_id in self._orders:
            raise ValueError(f"Duplicate request: {request_id}")

        self._orders[request_id] = order

    def exists(self, request_id: Hashable) -> bool:
        """Return True if request exists."""
        return request_id in self._orders

    def get(self, request_id: Hashable) -> object | None:
        """Return stored order."""
        return self._orders.get(request_id)

    def remove(self, request_id: Hashable) -> None:
        """Remove order if present."""
        self._orders.pop(request_id, None)

    def clear(self) -> None:
        """Clear registry."""
        self._orders.clear()

    def size(self) -> int:
        """Return registry size."""
        return len(self._orders)
