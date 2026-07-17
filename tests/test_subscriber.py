from events.subscriber import Subscriber
from events.event import Event


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