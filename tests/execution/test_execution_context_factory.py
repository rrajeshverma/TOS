from datetime import datetime

import pytest

from domain.decision import Decision
from domain.market import Market
from domain.risk import Risk
from execution.execution_context_factory import ExecutionContextFactory
from shared.enums import DecisionStatus, Signal


def create_risk() -> Risk:
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
        approved=True,
        reasons=(),
    )


def test_create_raises_for_none_risk():
    with pytest.raises(
        ValueError,
        match="Risk cannot be None",
    ):
        ExecutionContextFactory.create(None)


def test_create_returns_execution_context():
    context = ExecutionContextFactory.create(create_risk())

    assert context is not None


def test_create_sets_risk():
    risk = create_risk()

    context = ExecutionContextFactory.create(risk)

    assert context.risk is risk


def test_create_sets_default_quantity():
    context = ExecutionContextFactory.create(create_risk())

    assert context.quantity == ExecutionContextFactory.DEFAULT_QUANTITY
