from datetime import datetime
from decimal import Decimal

from domain.market import Market
from domain.indicator_set import IndicatorSet
from domain.decision import Decision
from domain.risk import Risk
from domain.trade import Trade

from shared.enums import (
    Signal,
    DecisionStatus,
)

market = Market(
    symbol="NIFTY",
    exchange="NSE",
    timeframe="5m",
    timestamp=datetime.now(),
    open=24100,
    high=24125,
    low=24095,
    close=24120,
    volume=152340.0,
)

indicator = IndicatorSet(
    ema_high=24152.3,
    ema_low=24134.7,
    vwap=24120.1,
    rsi=58.75,
    volume_average=125000.0,
)

decision = Decision(
    decision_id="D202607140001",
    timestamp=datetime.now(),
    market=market,
    indicator_set=indicator,
    signal=Signal.BUY_CE,
    status=DecisionStatus.VALID,
    reasons=("All strategy rules passed",),
)

risk = Risk(
    decision=decision,
    approved=True,
    reasons=("Risk checks passed",),
)

trade = Trade(
    trade_id="T202607140001",
    risk=risk,
    entry_price=Decimal("248.35"),
    stop_loss=Decimal("242.10"),
    target=Decimal("260.85"),
    quantity=400,
    entry_time=datetime.now(),
)

print(trade)
print(trade.is_open)
print(trade.is_closed)
print(trade.pnl)
