from unittest.mock import Mock

from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest


def test_execute_calls_order_service():
    order_service = Mock()

    order_service.submit.return_value = "ORD123"

    engine = ExecutionEngine(order_service)

    request = ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )

    engine.execute(request)

    order_service.submit.assert_called_once()


def test_execute_returns_result():
    order_service = Mock()

    order_service.submit.return_value = "ORD123"

    engine = ExecutionEngine(order_service)

    request = ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )

    result = engine.execute(request)

    assert result.success
    assert result.order_id == "ORD123"
