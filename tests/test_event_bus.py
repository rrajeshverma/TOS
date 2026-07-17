from events.event import Event
from events.event_bus import EventBus
from events.subscriber import Subscriber


class DummySubscriber(Subscriber):
    def __init__(self):
        self.events = []

    def handle(self, event: Event) -> None:
        self.events.append(event)


def test_event_bus_subscribes_and_publishes():
    bus = EventBus()
    subscriber = DummySubscriber()

    bus.subscribe("PRICE_UPDATED", subscriber)

    event = Event(
        name="PRICE_UPDATED",
        payload={"price": 65000},
    )

    bus.publish(event)

    assert len(subscriber.events) == 1
    assert subscriber.events[0] == event

def test_multiple_subscribers_receive_same_event():
    bus = EventBus()

    s1 = DummySubscriber()
    s2 = DummySubscriber()

    bus.subscribe("PRICE_UPDATED", s1)
    bus.subscribe("PRICE_UPDATED", s2)

    event = Event(
        name="PRICE_UPDATED",
        payload={"price": 65000},
    )

    bus.publish(event)

    assert len(s1.events) == 1
    assert len(s2.events) == 1
    assert s1.events[0] == event
    assert s2.events[0] == event

def test_unsubscribe_removes_subscriber():
    bus = EventBus()

    subscriber = DummySubscriber()

    bus.subscribe("PRICE_UPDATED", subscriber)
    bus.unsubscribe("PRICE_UPDATED", subscriber)

    event = Event(
        name="PRICE_UPDATED",
        payload={"price": 65000},
    )

    bus.publish(event)

    assert subscriber.events == []

def test_publish_with_no_subscribers_does_not_raise():
    bus = EventBus()

    event = Event(
        name="UNKNOWN_EVENT",
        payload={},
    )

    # Should not raise any exception
    bus.publish(event)

def test_duplicate_subscriber_is_registered_only_once():
    bus = EventBus()

    subscriber = DummySubscriber()

    bus.subscribe("PRICE_UPDATED", subscriber)
    bus.subscribe("PRICE_UPDATED", subscriber)

    event = Event(
        name="PRICE_UPDATED",
        payload={"price": 65000},
    )

    bus.publish(event)

    assert len(subscriber.events) == 1