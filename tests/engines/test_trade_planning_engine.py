"""
=========================================================
Trading Operating System (TOS)

Trade Planning Engine Tests
=========================================================
"""

from dataclasses import replace
from decimal import Decimal

import pytest

from engines.trade_planning_engine import TradePlanningEngine
from domain.instrument import Instrument
from shared.enums import Signal
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


def test_create_buy_pe_trade_plan():
    decision = replace(
        make_decision(),
        signal=Signal.BUY_PE,
    )
    position_size = make_position_size()

    plan = TradePlanningEngine().create_plan(
        decision=decision,
        position_size=position_size,
        entry_price=Decimal(250),
        stop_loss=Decimal(260),
        target_price=Decimal(230),
    )

    assert plan.decision == decision
    assert plan.entry_price == Decimal(250)
    assert plan.stop_loss == Decimal(260)
    assert plan.target_price == Decimal(230)


def test_buy_pe_invalid_stop_loss_raises_error():
    decision = replace(
        make_decision(),
        signal=Signal.BUY_PE,
    )

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            position_size=make_position_size(),
            entry_price=Decimal(250),
            stop_loss=Decimal(240),
            target_price=Decimal(230),
        )


def test_buy_pe_invalid_target_raises_error():
    decision = replace(
        make_decision(),
        signal=Signal.BUY_PE,
    )

    with pytest.raises(ValueError):
        TradePlanningEngine().create_plan(
            decision=decision,
            position_size=make_position_size(),
            entry_price=Decimal(250),
            stop_loss=Decimal(260),
            target_price=Decimal(270),
        )


def test_create_trade_plan_preserves_instrument():
    decision = make_decision()
    position_size = make_position_size()

    instrument = Instrument(
        symbol="NIFTY-Sep2026-23900-CE",
        security_id="42635",
        exchange_segment="NSE_FNO",
        lot_size=65,
        tick_size=Decimal("0.05"),
        instrument_type="OPTIDX",
        option_type="CE",
        strike=Decimal("23900"),
    )

    plan = TradePlanningEngine().create_plan(
        decision=decision,
        position_size=position_size,
        entry_price=Decimal(24000),
        stop_loss=Decimal(23950),
        target_price=Decimal(24100),
        instrument=instrument,
    )

    assert plan.instrument is instrument
    assert plan.symbol == instrument.symbol
    assert plan.security_id == instrument.security_id
    assert plan.exchange_segment == instrument.exchange_segment
    assert plan.lot_size == instrument.lot_size
    assert plan.strike == instrument.strike
    assert plan.option_type == instrument.option_type
