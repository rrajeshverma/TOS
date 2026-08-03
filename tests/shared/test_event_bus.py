"""
Tests for EventBus.
"""

from shared.event_bus import EventBus


def test_subscribe_and_publish() -> None:
    """Subscriber receives published payload."""

    bus = EventBus()
    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("TEST_EVENT", handler)

    bus.publish("TEST_EVENT", {"price": 100})

    assert received == [{"price": 100}]


def test_multiple_subscribers_receive_event() -> None:
    """All subscribers receive the event."""

    bus = EventBus()

    first = []
    second = []

    def handler_one(payload):
        first.append(payload)

    def handler_two(payload):
        second.append(payload)

    bus.subscribe("TEST_EVENT", handler_one)
    bus.subscribe("TEST_EVENT", handler_two)

    bus.publish("TEST_EVENT", 123)

    assert first == [123]
    assert second == [123]


def test_unsubscribe_removes_handler() -> None:
    """Unsubscribed handler should not receive events."""

    bus = EventBus()

    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("TEST_EVENT", handler)
    bus.unsubscribe("TEST_EVENT", handler)

    bus.publish("TEST_EVENT", "hello")

    assert received == []


def test_clear_removes_all_subscribers() -> None:
    """Clear removes every subscriber."""

    bus = EventBus()

    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("TEST_EVENT", handler)

    bus.clear()

    bus.publish("TEST_EVENT", 1)

    assert received == []


def test_publish_without_subscribers() -> None:
    """Publishing without subscribers should not fail."""

    bus = EventBus()

    bus.publish("UNKNOWN_EVENT", {"value": 10})


def test_unsubscribe_unknown_event() -> None:
    """Unsubscribing unknown event should not fail."""

    bus = EventBus()

    def handler(payload):
        pass

    bus.unsubscribe("UNKNOWN_EVENT", handler)


def test_same_handler_can_subscribe_multiple_times() -> None:
    """Same handler is invoked for each subscription."""

    bus = EventBus()

    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("TEST_EVENT", handler)
    bus.subscribe("TEST_EVENT", handler)

    bus.publish("TEST_EVENT", "A")

    assert received == ["A", "A"]


def test_multiple_events_are_independent() -> None:
    """Subscribers receive only their own events."""

    bus = EventBus()

    first = []
    second = []

    def first_handler(payload):
        first.append(payload)

    def second_handler(payload):
        second.append(payload)

    bus.subscribe("EVENT_ONE", first_handler)
    bus.subscribe("EVENT_TWO", second_handler)

    bus.publish("EVENT_ONE", 1)
    bus.publish("EVENT_TWO", 2)

    assert first == [1]
    assert second == [2]


def test_clear_keeps_bus_reusable() -> None:
    """Subscribers can be registered again after clear."""

    bus = EventBus()

    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("TEST_EVENT", handler)

    bus.clear()

    bus.subscribe("TEST_EVENT", handler)

    bus.publish("TEST_EVENT", "OK")

    assert received == ["OK"]


def test_publish_none_payload() -> None:
    """None payload is supported."""

    bus = EventBus()

    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("TEST_EVENT", handler)

    bus.publish("TEST_EVENT", None)

    assert received == [None]
