from execution.order_events import OrderEventType

from execution.order_service import (
    OrderService,
    OrderStatus,
)

def create_order(service):

    return service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )


def test_register_broker_order():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    assert service.broker_order_id(
        order_id
    ) == "BROKER001"


def test_process_submitted_callback():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.SUBMITTED,
    )

    assert service.status(
        order_id
    ) == OrderStatus.SUBMITTED


def test_process_filled_callback():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.FILLED,
    )

    assert service.status(
        order_id
    ) == OrderStatus.FILLED


def test_process_cancelled_callback():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.CANCELLED,
    )

    assert service.status(
        order_id
    ) == OrderStatus.CANCELLED


def test_unknown_broker_callback_rejected():

    import pytest

    service = OrderService()

    with pytest.raises(KeyError):

        service.process_broker_callback(
            "UNKNOWN",
            OrderStatus.FILLED,
        )


def test_multiple_broker_orders():

    service = OrderService()

    first = create_order(service)
    second = create_order(service)

    service.register_broker_order(
        first,
        "BROKER001",
    )

    service.register_broker_order(
        second,
        "BROKER002",
    )

    service.process_broker_callback(
        "BROKER002",
        OrderStatus.FILLED,
    )

    assert service.status(
        second
    ) == OrderStatus.FILLED

    assert service.status(
        first
    ) == OrderStatus.NEW


def test_duplicate_registration_rejected():

    import pytest

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    with pytest.raises(ValueError):

        service.register_broker_order(
            order_id,
            "BROKER002",
        )

def test_callback_publishes_event():

    events = []

    class Dispatcher:

        def publish(self, event):
            events.append(event)

    service = OrderService(
        dispatcher=Dispatcher()
    )

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.SUBMITTED,
    )

    assert events[-1].event_type == OrderEventType.SUBMITTED


def test_callback_updates_only_matching_order():

    service = OrderService()

    first = create_order(service)
    second = create_order(service)

    service.register_broker_order(
        first,
        "BROKER001",
    )

    service.register_broker_order(
        second,
        "BROKER002",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.FILLED,
    )

    assert service.status(first) == OrderStatus.FILLED
    assert service.status(second) == OrderStatus.NEW


def test_partial_fill_callback():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.PARTIALLY_FILLED,
    )

    assert service.status(order_id) == OrderStatus.PARTIALLY_FILLED


def test_duplicate_callback_is_safe():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.SUBMITTED,
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.SUBMITTED,
    )

    assert service.status(order_id) == OrderStatus.SUBMITTED


def test_stale_callback_ignored():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.FILLED,
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.NEW,
    )

    assert service.status(order_id) == OrderStatus.FILLED


def test_broker_order_lookup():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER100",
    )

    assert service.broker_order_id(order_id) == "BROKER100"


def test_callback_after_cancel():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.CANCELLED,
    )

    assert service.status(order_id) == OrderStatus.CANCELLED


def test_callback_status_persistence():

    service = OrderService()

    order_id = create_order(service)

    service.register_broker_order(
        order_id,
        "BROKER001",
    )

    service.process_broker_callback(
        "BROKER001",
        OrderStatus.FILLED,
    )

    assert service.status(order_id).value == "FILLED"