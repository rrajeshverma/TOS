from events.publisher import Publisher
from events.event import Event


class DummyPublisher(Publisher):
    def publish(self, event: Event) -> None:
        self.last_event = event


def test_publisher_publishes_event():
    publisher = DummyPublisher()

    event = Event(
        name="ORDER_FILLED",
        payload={"order_id": 1001},
    )

    publisher.publish(event)

    assert publisher.last_event == event
