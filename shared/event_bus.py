"""
Simple synchronous event bus.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    """Simple publish/subscribe event bus."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(
        self,
        event: str,
        callback: Callable[[Any], None],
    ) -> None:
        """Register a callback for an event."""

        self._subscribers[event].append(callback)

    def unsubscribe(
        self,
        event: str,
        callback: Callable[[Any], None],
    ) -> None:
        """Remove a callback."""

        if event not in self._subscribers:
            return

        if callback in self._subscribers[event]:
            self._subscribers[event].remove(callback)

    def publish(
        self,
        event: str,
        payload: Any,
    ) -> None:
        """Publish an event."""

        for callback in self._subscribers.get(event, []):
            callback(payload)

    def clear(self) -> None:
        """Remove all subscribers."""

        self._subscribers.clear()
