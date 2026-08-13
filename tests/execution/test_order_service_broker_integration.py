from execution.execution_request import ExecutionRequest
from execution.order_event_dispatcher import OrderEventDispatcher
from execution.order_events import OrderEventType
from execution.order_service import OrderService, OrderStatus


class DummyBroker:
    def __init__(self):
        self.placed = []
        self.cancelled = []

    def place_order(self, order):
        self.placed.append(order)
        return {
            "broker_order_id": "BRK123",
            "status": "SUCCESS",
        }

    def cancel_order(self, order_id):
        self.cancelled.append(order_id)


class DummyRepository:
    def __init__(self):
        self.saved = []

    def add(self, order):
        self.saved.append(order)


def make_order():
    return {
        "symbol": "NIFTY",
        "quantity": 65,
    }


def test_place_order_without_broker():
    service = OrderService()

    try:
        service.place_order(make_order())
        assert False
    except RuntimeError:
        pass


def test_place_order_calls_broker():
    broker = DummyBroker()

    service = OrderService(broker=broker)

    result = service.place_order(make_order())

    assert broker.placed
    assert result["broker_order_id"] == "BRK123"


def test_place_order_persists_repository():
    broker = DummyBroker()
    repository = DummyRepository()

    service = OrderService(
        broker=broker,
        repository=repository,
    )

    result = service.place_order(make_order())

    assert repository.saved == [result]


def test_broker_order_id_none_before_registration():
    service = OrderService()

    order_id = service.submit(make_order())

    assert service.broker_order_id(order_id) is None


def test_register_broker_order_success():
    service = OrderService()

    order_id = service.submit(make_order())

    service.register_broker_order(
        order_id,
        "BRK-1",
    )

    assert service.broker_order_id(order_id) == "BRK-1"


def test_process_broker_callback_updates_status():
    service = OrderService()

    order_id = service.submit(make_order())

    service.register_broker_order(
        order_id,
        "BRK-1",
    )

    service.process_broker_callback(
        "BRK-1",
        OrderStatus.SUBMITTED,
    )

    assert service.status(order_id) is OrderStatus.SUBMITTED


def test_process_broker_callback_publishes_event():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(received.append)

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit(make_order())

    service.register_broker_order(
        order_id,
        "BRK-1",
    )

    received.clear()

    service.process_broker_callback(
        "BRK-1",
        OrderStatus.SUBMITTED,
    )

    assert len(received) == 1
    assert received[0].event_type is OrderEventType.SUBMITTED
    assert received[0].broker_order_id == "BRK-1"


def test_cancel_order_calls_broker():
    broker = DummyBroker()

    service = OrderService(broker=broker)

    order_id = service.submit(make_order())

    service.cancel_order(order_id)

    assert broker.cancelled == [order_id]


def test_cancel_order_without_broker():
    service = OrderService()

    order_id = service.submit(make_order())

    assert service.cancel_order(order_id) is True


def test_cancel_order_publishes_event():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(received.append)

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit(make_order())

    received.clear()

    service.cancel_order(order_id)

    assert len(received) == 1
    assert received[0].event_type is OrderEventType.CANCELLED


def test_cancel_order_event_contains_registered_broker_id():
    dispatcher = OrderEventDispatcher()

    received = []

    dispatcher.subscribe(received.append)

    service = OrderService(dispatcher=dispatcher)

    order_id = service.submit(make_order())

    service.register_broker_order(
        order_id,
        "BRK-XYZ",
    )

    received.clear()

    service.cancel_order(order_id)

    assert received[0].broker_order_id == "BRK-XYZ"


def test_submit_accepts_execution_request():
    service = OrderService()

    request = ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )

    order_id = service.submit(request)

    assert order_id == 1
    assert service.get(order_id) == {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
    }
