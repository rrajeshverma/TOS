from abc import ABC, abstractmethod

from events.event import Event


class Publisher(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        """Publish an event."""
