from datetime import datetime

from domain.market import Market
from domain.indicator_set import IndicatorSet
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine


def create_decision():
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

    return DecisionEngine().evaluate(
        market,
        indicators,
    )


def test_risk_approved():

    risk = RiskEngine().evaluate(
        decision=create_decision(),
        trades_today=0,
        daily_loss=0,
    )

    assert risk.is_approved


def test_max_trades_reached():

    risk = RiskEngine().evaluate(
        decision=create_decision(),
        trades_today=4,
        daily_loss=0,
    )

    assert not risk.is_approved


def test_daily_loss_reached():

    risk = RiskEngine().evaluate(
        decision=create_decision(),
        trades_today=0,
        daily_loss=5000,
    )

    assert not risk.is_approved
