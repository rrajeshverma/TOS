"""
Tests for TradeQualityEngine.
"""

from datetime import datetime

from config.risk import MAX_TRADES_PER_DAY
from domain.decision import Decision
from engines.trade_quality_engine import TradeQualityEngine
from shared.enums import (
    DecisionStatus,
    Signal,
)


class DummyMarket:
    pass


class DummyIndicators:
    pass


def create_decision(
    signal: Signal = Signal.BUY_CE,
    status: DecisionStatus = DecisionStatus.VALID,
):
    return Decision(
        decision_id="D1",
        timestamp=datetime.now(),
        market=DummyMarket(),
        indicator_set=DummyIndicators(),
        signal=signal,
        status=status,
        reasons=(),
    )


def test_quality_approved():
    engine = TradeQualityEngine()

    quality = engine.evaluate(
        decision=create_decision(),
        trades_today=0,
    )

    assert quality.is_approved


def test_reject_no_signal():
    engine = TradeQualityEngine()

    quality = engine.evaluate(
        decision=create_decision(
            signal=Signal.NONE,
        ),
        trades_today=0,
    )

    assert not quality.is_approved


def test_reject_invalid_decision():
    engine = TradeQualityEngine()

    quality = engine.evaluate(
        decision=create_decision(
            status=DecisionStatus.BLOCKED,
        ),
        trades_today=0,
    )

    assert not quality.is_approved


def test_reject_max_daily_trades():
    engine = TradeQualityEngine()

    quality = engine.evaluate(
        decision=create_decision(),
        trades_today=MAX_TRADES_PER_DAY,
    )

    assert not quality.is_approved
