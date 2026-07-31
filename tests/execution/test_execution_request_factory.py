from datetime import datetime

import pytest

from domain.decision import Decision
from domain.market import Market
from domain.risk import Risk
from execution.execution_context import ExecutionContext
from execution.execution_request_factory import (
    ExecutionRequestFactory,
)
from shared.enums import (
    DecisionStatus,
    Signal,
)


def create_context(
    signal: Signal = Signal.BUY_CE,
):
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

    risk = Risk(
        decision=decision,
        approved=True,
        reasons=(),
    )

    return ExecutionContext(
        risk=risk,
        quantity=25,
    )


def test_create_execution_request():
    context = create_context()

    request = ExecutionRequestFactory.create(context)

    assert request.symbol == "NIFTY"
    assert request.side == "BUY"
    assert request.quantity == 25


def test_symbol_is_copied():
    context = create_context()

    request = ExecutionRequestFactory.create(context)

    assert request.symbol == context.risk.decision.market.symbol


def test_quantity_is_copied():
    context = create_context()

    request = ExecutionRequestFactory.create(context)

    assert request.quantity == context.quantity


def test_none_context_raises_value_error():
    with pytest.raises(ValueError):
        ExecutionRequestFactory.create(None)


def test_buy_signal_maps_to_buy():
    context = create_context()

    request = ExecutionRequestFactory.create(context)

    assert request.side == "BUY"


def test_buy_pe_maps_to_buy():
    request = ExecutionRequestFactory.create(create_context(Signal.BUY_PE))

    assert request.side == "BUY"
