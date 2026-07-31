from unittest.mock import Mock

from execution.execution_engine import ExecutionEngine
from execution.live_execution_engine import LiveExecutionEngine


def test_live_execution_engine_is_execution_engine():
    engine = LiveExecutionEngine(Mock())

    assert isinstance(engine, ExecutionEngine)


def test_live_execution_engine_executes_order():
    order_service = Mock()

    order_service.submit.return_value = "ORDER-1"
    order_service.place_order.return_value = {
        "orderId": "LIVE-ORDER",
    }
    order_service.register_broker_order = Mock()
    order_service.update_status = Mock()

    engine = LiveExecutionEngine(order_service)

    result = engine.execute(Mock())

    assert result.success is True
    assert result.order_id == "ORDER-1"

    order_service.submit.assert_called_once()
    order_service.place_order.assert_called_once()
    order_service.register_broker_order.assert_called_once_with(
        "ORDER-1",
        "LIVE-ORDER",
    )
