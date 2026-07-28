"""
Tests:
Live Trade -> Order Execution Flow

Flow:

Trade
 |
 ▼
ExecutionRequest
 |
 ▼
ExecutionEngine
 |
 ▼
OrderService
 |
 ▼
ExecutionResult
"""

from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest


class DummyOrderService:
    def __init__(self):
        self.orders = []

    def submit(
        self,
        request,
    ):
        self.orders.append(request)

        return "ORDER001"


def create_request():

    return ExecutionRequest(
        symbol="NIFTY",
        quantity=65,
        side="BUY",
    )


def test_execution_engine_submits_live_order():

    service = DummyOrderService()

    engine = ExecutionEngine(
        service
    )

    request = create_request()

    result = engine.execute(
        request
    )

    assert result.success is True
    assert result.order_id == "ORDER001"


def test_execution_engine_sends_correct_request():

    service = DummyOrderService()

    engine = ExecutionEngine(
        service
    )

    request = create_request()

    engine.execute(
        request
    )

    submitted = service.orders[0]

    assert submitted.symbol == "NIFTY"
    assert submitted.quantity == 65


def test_execution_engine_handles_order_failure():

    class FailedOrderService:

        def submit(
            self,
            request,
        ):
            raise RuntimeError(
                "Order rejected"
            )

    engine = ExecutionEngine(
        FailedOrderService()
    )

    result = engine.execute(
        create_request()
    )

    assert result.success is False
    assert result.error == "Order rejected"


def test_execution_engine_rejects_empty_request():

    service = DummyOrderService()

    engine = ExecutionEngine(
        service
    )

    try:
        engine.execute(None)

    except ValueError:
        assert True

    else:
        assert False