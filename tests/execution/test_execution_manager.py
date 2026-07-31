from datetime import datetime
from unittest.mock import Mock

import pytest


from domain.decision import Decision
from domain.market import Market
from domain.risk import Risk
from execution.execution_manager import ExecutionManager
from execution.execution_result import ExecutionResult
from shared.enums import (
    DecisionStatus,
    Signal,
)

from execution.execution_request import ExecutionRequest


def create_risk(
    approved: bool = True,
) -> Risk:
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
    )

    decision = Decision(
        decision_id="DEC-1",
        timestamp=datetime.now(),
        market=market,
        indicator_set=None,
        signal=Signal.BUY_CE,
        status=DecisionStatus.VALID,
        reasons=(),
    )

    return Risk(
        decision=decision,
        approved=approved,
        reasons=(),
    )


def test_execute_raises_for_none_risk():
    engine = Mock()

    manager = ExecutionManager(engine)

    with pytest.raises(ValueError):
        manager.execute(None)


def test_execute_returns_unapproved_risk():
    engine = Mock()

    manager = ExecutionManager(engine)

    risk = create_risk(False)

    result = manager.execute(risk)

    assert result is risk
    engine.execute.assert_not_called()


def test_execute_calls_execution_engine():
    engine = Mock()

    engine.execute.return_value = ExecutionResult(
        success=True,
        order_id="ORD-1",
    )

    manager = ExecutionManager(engine)

    result = manager.execute(create_risk())

    engine.execute.assert_called_once()

    assert result.success is True
    assert result.order_id == "ORD-1"


def test_execute_returns_execution_result():
    engine = Mock()

    expected = ExecutionResult(
        success=True,
        order_id="ORDER-123",
    )

    engine.execute.return_value = expected

    manager = ExecutionManager(engine)

    result = manager.execute(create_risk())

    assert result is expected


def test_constructor_raises_for_none_execution_engine():
    with pytest.raises(
        ValueError,
        match="Execution engine cannot be None",
    ):
        ExecutionManager(None)


def test_execute_passes_execution_request_to_engine():
    engine = Mock()

    engine.execute.return_value = ExecutionResult(
        success=True,
        order_id="ORD-1",
    )

    manager = ExecutionManager(engine)

    manager.execute(create_risk())

    request = engine.execute.call_args.args[0]

    assert isinstance(request, ExecutionRequest)
    assert request.symbol == "NIFTY"
    assert request.side == "BUY"
    assert request.quantity == 1
