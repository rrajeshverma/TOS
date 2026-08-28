from datetime import datetime

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.risk import Risk
from shared.enums import DecisionStatus, Signal

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
)

decision = Decision(
    decision_id="D202607140001",
    timestamp=datetime.now(),
    market=market,
    indicator_set=indicator,
    signal=Signal.BUY_CE,
    status=DecisionStatus.VALID,
    reasons=(
        "EMA Cross",
        "VWAP Passed",
        "RSI Passed",
        "Volume Passed",
    ),
)

risk = Risk(
    decision=decision,
    approved=True,
    reasons=(
        "Daily loss within limit",
        "Trade count available",
        "Market timing valid",
    ),
)

print(risk)

print(risk.is_approved)

print(risk.reason_count)
