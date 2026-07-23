from events.event import Event
from events.event_bus import EventBus
from events.subscriber import Subscriber


class GoodSubscriber(Subscriber):
    def __init__(self):
        self.received = []

    def handle(self, event):
        self.received.append(event)


class BadSubscriber(Subscriber):
    def handle(self, event):
        raise Exception("subscriber failed")


def test_failed_subscriber_does_not_stop_others():
    bus = EventBus()

    bad = BadSubscriber()
    good = GoodSubscriber()

    bus.subscribe(
        "PRICE_UPDATED",
        bad,
    )

    bus.subscribe(
        "PRICE_UPDATED",
        good,
    )

    event = Event(
        name="PRICE_UPDATED",
        payload={"price": 25000},
    )

    bus.publish(event)

    assert good.received == [event]


def test_event_bus_reports_failures():
    bus = EventBus()

    bus.subscribe(
        "PRICE_UPDATED",
        BadSubscriber(),
    )

    result = bus.publish(
        Event(
            name="PRICE_UPDATED",
            payload={},
        )
    )

    assert result["failed"] == 1
