from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory


def create_trade():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24990,
        high=25010,
        low=24980,
        close=25000,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )

    trade = TradeFactory().create(
        risk=risk,
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24950"),
    )

    return trade


def test_trade_factory():

    trade = create_trade()

    assert trade.quantity == 65

    assert trade.entry_price == Decimal("25000")

    assert trade.stop_loss == Decimal("24950")

    assert trade.target == Decimal("25100")

    assert trade.risk.is_approved


import pytest

from shared.enums import DecisionStatus, Signal, TradeStatus


def create_rejected_risk():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24990,
        high=25010,
        low=24980,
        close=25000,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=4,
        daily_loss=0,
    )

    return risk


def test_trade_status_created():
    trade = create_trade()

    assert trade.status == TradeStatus.CREATED


def test_trade_has_generated_id():
    trade = create_trade()

    assert trade.trade_id
    assert isinstance(trade.trade_id, str)


def test_trade_has_entry_time():
    trade = create_trade()

    assert isinstance(trade.entry_time, datetime)


def test_rejected_risk_raises_value_error():
    risk = create_rejected_risk()

    with pytest.raises(
        ValueError,
        match="Cannot create Trade from rejected Risk.",
    ):
        TradeFactory().create(
            risk=risk,
            entry_price=Decimal("25000"),
            stop_loss=Decimal("24950"),
        )
