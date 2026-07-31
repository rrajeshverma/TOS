from events.event import Event
from events.subscriber import Subscriber


class DummySubscriber(Subscriber):
    def handle(self, event: Event):
        self.last_event = event


def test_subscriber_handles_event():
    subscriber = DummySubscriber()

    event = Event(
        name="PRICE_UPDATED",
        payload={"price": 65000},
    )

    subscriber.handle(event)

    assert subscriber.last_event == event


def test_base_subscriber_handle():
    class BaseSubscriber(Subscriber):
        def handle(self, event: Event) -> None:
            super().handle(event)

    subscriber = BaseSubscriber()

    subscriber.handle(Event(name="TEST", payload={}))
