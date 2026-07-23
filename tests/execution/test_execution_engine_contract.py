from unittest.mock import Mock

from execution.execution_engine import ExecutionEngine
from execution.execution_result import ExecutionResult


def test_execution_engine_requires_order_service():
    service = Mock()

    engine = ExecutionEngine(service)

    assert engine.order_service is service


def test_execution_engine_returns_execution_result():
    service = Mock()
    service.submit.return_value = "ORD-001"

    engine = ExecutionEngine(service)

    result = engine.execute(Mock())

    assert isinstance(result, ExecutionResult)
