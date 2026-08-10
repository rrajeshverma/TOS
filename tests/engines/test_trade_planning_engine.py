"""
=========================================================
Trading Operating System (TOS)

Trade Planning Engine Tests
=========================================================
"""

from decimal import Decimal

import pytest

from engines.trade_planning_engine import TradePlanningEngine
from tests.helpers.domain_factory import (
    make_decision,
    make_position_size,
)


def test_create_trade_plan():
    """
    Trade plan is successfully created.
    """

    decision = make_decision()
    position_size = make_position_size()

    plan = TradePlanningEngine().create_plan(
        decision=decision,
        position_size=position_size,
        entry_price=Decimal(250),
        stop_loss=Decimal(240),
        target_price=Decimal(270),
    )

    assert plan.decision == decision
    assert plan.position_size == position_size
    assert plan.entry_price == Decimal(250)
    assert plan.stop_loss == Decimal(240)
    assert plan.target_price == Decimal(270)


def test_stop_loss_above_entry_raises_error():
    decision = make_decision()

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            position_size=make_position_size(),
            entry_price=Decimal(250),
            stop_loss=Decimal(255),
            target_price=Decimal(270),
        )


def test_target_below_entry_raises_error():
    decision = make_decision()

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            position_size=make_position_size(),
            entry_price=Decimal(250),
            stop_loss=Decimal(240),
            target_price=Decimal(245),
        )
