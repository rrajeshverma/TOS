from unittest.mock import Mock

import pytest

from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest


def test_broker_exception():
    order_service = Mock()

    order_service.submit.side_effect = RuntimeError("Broker unavailable")

    engine = ExecutionEngine(order_service)

    request = ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )

    result = engine.execute(request)

    assert result.success is False
    assert result.error == "Broker unavailable"


def test_none_request():
    engine = ExecutionEngine(Mock())

    with pytest.raises(ValueError):
        engine.execute(None)
