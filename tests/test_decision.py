from datetime import datetime

from domain.market import Market
from domain.indicator_set import IndicatorSet
from domain.decision import Decision

from shared.enums import Signal
from shared.enums import DecisionStatus

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
    ema_high=24152.30,
    ema_low=24134.70,
    vwap=24120.10,
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
    reasons=(
        "Previous Close crossed EMA High",
        "Close above VWAP",
        "RSI above 55",
        "Volume above average",
    ),
)

print(decision)

print(decision.has_signal)

print(decision.is_tradeable)

print(decision.reason_count)
