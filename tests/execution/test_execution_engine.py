from unittest.mock import Mock

from execution.execution_engine import ExecutionEngine


def test_execute_returns_failure_when_guard_blocks():
    order_service = Mock()

    guard = Mock()
    guard.can_execute.return_value = False

    engine = ExecutionEngine(
        order_service,
        execution_guard=guard,
    )

    request = Mock()

    result = engine.execute(
        request,
    )

    assert result.success is False
    assert result.error == "Execution blocked by safety guard"

    order_service.submit.assert_not_called()


def test_execute_calls_guard_once():
    order_service = Mock()
    order_service.submit.return_value = "ORDER-1"

    guard = Mock()
    guard.can_execute.return_value = True

    engine = ExecutionEngine(
        order_service,
        execution_guard=guard,
    )

    request = Mock()

    result = engine.execute(
        request,
    )

    assert result.success is True

    guard.can_execute.assert_called_once()
    order_service.submit.assert_called_once_with(request)


def test_execute_returns_failure_for_invalid_guard():
    order_service = Mock()

    class InvalidGuard:
        pass

    engine = ExecutionEngine(
        order_service,
        execution_guard=InvalidGuard(),
    )

    request = Mock()

    result = engine.execute(
        request,
    )

    assert result.success is False
    assert "can_execute" in result.error


class StubExecutionEngine(ExecutionEngine):
    def __init__(self):
        super().__init__(order_service=Mock())
        self.called = False

    def _place_order(self, request):
        self.called = True
        return {"orderId": "TEST-ORDER"}


def test_execute_uses_place_order_hook():
    order_service = Mock()
    order_service.submit.return_value = "ORDER-1"
    order_service.register_broker_order = Mock()
    order_service.update_status = Mock()

    engine = StubExecutionEngine()
    engine.order_service = order_service

    request = Mock()

    result = engine.execute(request)

    assert engine.called is True
    assert result.success is True
