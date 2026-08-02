"""
=========================================================
Trading Operating System (TOS)

Trade Planning Engine Tests
=========================================================
"""

import pytest

from decimal import Decimal

from engines.trade_planning_engine import TradePlanningEngine
from tests.helpers.domain_factory import make_decision


def test_create_trade_plan():
    """
    Trade plan is successfully created.
    """

    decision = make_decision()

    plan = TradePlanningEngine().create_plan(
        decision=decision,
        entry_price=Decimal("250"),
        stop_loss=Decimal("240"),
        target_price=Decimal("270"),
        lots=2,
        quantity=130,
    )

    assert plan.decision == decision
    assert plan.entry_price == Decimal("250")
    assert plan.stop_loss == Decimal("240")
    assert plan.target_price == Decimal("270")
    assert plan.lots == 2
    assert plan.quantity == 130


def test_risk_amount_is_calculated():
    """
    Risk amount should equal
    (entry - stop) × quantity.
    """

    decision = make_decision()

    plan = TradePlanningEngine().create_plan(
        decision=decision,
        entry_price=Decimal("250"),
        stop_loss=Decimal("240"),
        target_price=Decimal("270"),
        lots=2,
        quantity=130,
    )

    assert plan.risk_amount == Decimal("1300")


def test_reward_amount_is_calculated():
    """
    Reward amount should equal
    (target - entry) × quantity.
    """

    decision = make_decision()

    plan = TradePlanningEngine().create_plan(
        decision=decision,
        entry_price=Decimal("250"),
        stop_loss=Decimal("240"),
        target_price=Decimal("270"),
        lots=2,
        quantity=130,
    )

    assert plan.reward_amount == Decimal("2600")


def test_zero_quantity_raises_error():
    decision = make_decision()

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            entry_price=Decimal("250"),
            stop_loss=Decimal("240"),
            target_price=Decimal("270"),
            lots=1,
            quantity=0,
        )


def test_stop_loss_above_entry_raises_error():
    decision = make_decision()

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            entry_price=Decimal("250"),
            stop_loss=Decimal("255"),
            target_price=Decimal("270"),
            lots=1,
            quantity=65,
        )


def test_target_below_entry_raises_error():
    decision = make_decision()

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            entry_price=Decimal("250"),
            stop_loss=Decimal("240"),
            target_price=Decimal("245"),
            lots=1,
            quantity=65,
        )
