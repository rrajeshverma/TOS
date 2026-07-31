import pytest

from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest
from execution.execution_result import ExecutionResult
from execution.order_service import (
    OrderService,
    OrderStatus,
)


def test_engine_rejects_none_request():
    engine = ExecutionEngine(None)

    with pytest.raises(ValueError):
        engine.execute(None)


def test_engine_returns_execution_result():
    class Service:
        def submit(self, request):
            return "ORD001"

    result = ExecutionEngine(Service()).execute(
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=65,
        )
    )

    assert isinstance(result, ExecutionResult)
    assert result.success is True


def test_engine_returns_order_id():
    class Service:
        def submit(self, request):
            return "ORD001"

    result = ExecutionEngine(Service()).execute(
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=65,
        )
    )

    assert result.order_id == "ORD001"


def test_engine_handles_service_exception():
    class Service:
        def submit(self, request):
            raise Exception("Broker Down")

    result = ExecutionEngine(Service()).execute(
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=65,
        )
    )

    assert result.success is False
    assert "Broker Down" in result.error


def test_execution_request_validation():
    with pytest.raises(ValueError):
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=0,
        )


def create_service():
    return OrderService()


def test_submit_creates_first_order_id():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert order_id == 1


def test_submit_creates_incremental_order_ids():
    service = create_service()

    first = service.submit({"symbol": "NIFTY"})
    second = service.submit({"symbol": "BANKNIFTY"})

    assert first == 1
    assert second == 2


def test_get_existing_order():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    order = service.get(order_id)

    assert order["symbol"] == "NIFTY"


def test_get_unknown_order():
    service = create_service()

    assert service.get(999) is None


def test_initial_order_status_is_new():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert service.status(order_id) == OrderStatus.NEW


def test_initial_filled_quantity_zero():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert service.filled_quantity(order_id) == 0


def test_remaining_quantity():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert service.remaining_quantity(order_id) == 65


def test_average_fill_price_before_fill():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    assert service.average_fill_price(order_id) == 0.0


def test_partial_fill_updates_status():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    service.record_fill(
        order_id,
        quantity=20,
        price=100,
    )

    assert service.status(order_id) == OrderStatus.PARTIALLY_FILLED


def test_full_fill_updates_status():
    service = create_service()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    service.record_fill(
        order_id,
        quantity=65,
        price=100,
    )

    assert service.status(order_id) == OrderStatus.FILLED


def test_cannot_modify_unknown_order():
    service = OrderService()

    with pytest.raises(KeyError):
        service.modify_order(
            999,
            quantity=10,
        )


def test_cannot_modify_filled_order():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 10,
        }
    )

    service.record_fill(
        order_id,
        quantity=10,
        price=100,
    )

    with pytest.raises(ValueError):
        service.modify_order(
            order_id,
            quantity=20,
        )


def test_cannot_overfill_order():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 10,
        }
    )

    with pytest.raises(ValueError):
        service.record_fill(
            order_id,
            quantity=11,
            price=100,
        )


def test_duplicate_broker_registration_rejected():
    service = OrderService()

    order_id = service.submit(
        {
            "symbol": "NIFTY",
        }
    )

    service.register_broker_order(
        order_id,
        "BROKER123",
    )

    with pytest.raises(ValueError):
        service.register_broker_order(
            order_id,
            "BROKER456",
        )


def test_unknown_broker_callback_rejected():
    service = OrderService()

    with pytest.raises(KeyError):
        service.process_broker_callback(
            "UNKNOWN",
            OrderStatus.SUBMITTED,
        )
