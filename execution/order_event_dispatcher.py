from __future__ import annotations

from collections.abc import Callable

from execution.order_events import OrderEvent


class OrderEventDispatcher:
    """
    Dispatches order events to registered subscribers.

    Provides:
    - duplicate subscriber protection
    - subscriber failure isolation
    - publish status reporting
    """

    def __init__(self) -> None:
        self._subscribers: list[Callable[[OrderEvent], None]] = []

    def subscribe(
        self,
        callback: Callable[[OrderEvent], None],
    ) -> None:
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def publish(
        self,
        event: OrderEvent,
    ) -> dict:
        failed = 0

        for callback in self._subscribers:
            try:
                callback(event)

            except Exception:
                failed += 1

        return {
            "published": True,
            "failed": failed,
        }

    def clear(self) -> None:
        self._subscribers.clear()
