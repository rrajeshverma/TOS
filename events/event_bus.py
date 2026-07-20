from collections import defaultdict

from events.event import Event
from events.subscriber import Subscriber


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)

    def subscribe(self, event_name: str, subscriber: Subscriber) -> None:
        subscribers = self._subscribers[event_name]

        if subscriber not in subscribers:
            subscribers.append(subscriber)

    def unsubscribe(self, event_name: str, subscriber: Subscriber) -> None:
        subscribers = self._subscribers.get(event_name, [])
        if subscriber in subscribers:
            subscribers.remove(subscriber)

    def publish(self, event: Event) -> None:
        for subscriber in self._subscribers.get(event.name, []):
            subscriber.handle(event)
