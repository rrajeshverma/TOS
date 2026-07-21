from __future__ import annotations

from collections.abc import Callable

from execution.order_events import OrderEvent


class OrderEventDispatcher:
    """Dispatches order events to registered subscribers."""

    def __init__(self) -> None:
        self._subscribers: list[Callable[[OrderEvent], None]] = []

    def subscribe(
        self,
        callback: Callable[[OrderEvent], None],
    ) -> None:
        self._subscribers.append(callback)

    def publish(
        self,
        event: OrderEvent,
    ) -> None:
        for callback in self._subscribers:
            callback(event)

    def clear(self) -> None:
        self._subscribers.clear()