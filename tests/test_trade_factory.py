from datetime import datetime
from decimal import Decimal

from domain.market import Market
from domain.indicator_set import IndicatorSet
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
