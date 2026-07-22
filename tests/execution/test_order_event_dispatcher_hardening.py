from execution.order_event_dispatcher import OrderEventDispatcher
from execution.order_events import (
    OrderEvent,
    OrderEventType,
)


def test_failed_subscriber_does_not_stop_others():

    dispatcher = OrderEventDispatcher()

    received = []


    def bad(event):
        raise Exception(
            "subscriber failed"
        )


    def good(event):
        received.append(event)


    dispatcher.subscribe(bad)
    dispatcher.subscribe(good)


    event = OrderEvent(
        order_id=1,
        event_type=OrderEventType.FILLED,
    )


    dispatcher.publish(event)


    assert received == [event]



def test_publish_returns_failure_count():

    dispatcher = OrderEventDispatcher()


    def bad(event):
        raise Exception(
            "failed"
        )


    dispatcher.subscribe(bad)


    result = dispatcher.publish(
        OrderEvent(
            order_id=1,
            event_type=OrderEventType.NEW,
        )
    )


    assert result["failed"] == 1



def test_duplicate_subscriber_is_ignored():

    dispatcher = OrderEventDispatcher()


    received = []


    def callback(event):
        received.append(event)


    dispatcher.subscribe(callback)
    dispatcher.subscribe(callback)


    dispatcher.publish(
        OrderEvent(
            order_id=1,
            event_type=OrderEventType.NEW,
        )
    )


    assert len(received) == 1
