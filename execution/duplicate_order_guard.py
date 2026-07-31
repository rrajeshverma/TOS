"""
Duplicate order protection.
"""

from execution.order_registry import OrderRegistry


class DuplicateOrderGuard:
    """Prevents duplicate order submissions."""

    def __init__(self, registry: OrderRegistry) -> None:
        self._registry = registry

    def should_submit(self, request_id: str) -> bool:
        return not self._registry.exists(request_id)

    def register(self, request_id: str, order: object) -> None:
        self._registry.register(request_id, order)
