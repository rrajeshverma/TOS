from datetime import datetime
from decimal import Decimal

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.order import Order
from domain.risk import Risk
from domain.trade import Trade
from shared.enums import (
    Broker,
    DecisionStatus,
    OrderSide,
    Signal,
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

order = Order(
    order_id="O202607140001",
    broker_order_id=None,
    trade=trade,
    broker=Broker.DHAN,
    side=OrderSide.BUY,
    quantity=400,
    requested_price=Decimal("248.35"),
)

print(order)
print(order.is_pending)
print(order.is_executed)
