from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.portfolio import Portfolio
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory


def make_trade():
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

    return TradeFactory().create(
        risk=risk,
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24950"),
    )


def make_portfolio():
    return Portfolio(
        account_id="ACC001",
        cash=100000.0,
        available_margin=90000.0,
        used_margin=10000.0,
        equity=100000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0,
        positions=0,
        holdings=0,
    )
