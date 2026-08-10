from abc import ABC, abstractmethod

from events.event import Event


class Subscriber(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None:
        """Handle an event."""
