from datetime import datetime

from brokers.dhan.models import BrokerTick
from market.candle_builder import CandleBuilder


def test_create_first_candle():

    builder = CandleBuilder(
        timeframe="5m"
    )

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000,
        volume=100,
        timestamp=datetime.now(),
    )

    candle = builder.update(tick)

    assert candle.open == 25000
    assert candle.high == 25000
    assert candle.low == 25000
    assert candle.close == 25000



def test_update_high_low_close():

    builder = CandleBuilder(
        timeframe="5m"
    )

    t1 = BrokerTick(
        "NIFTY",
        25000,
        100,
        datetime.now(),
    )

    t2 = BrokerTick(
        "NIFTY",
        25050,
        200,
        datetime.now(),
    )

    builder.update(t1)

    candle = builder.update(t2)

    assert candle.high == 25050
    assert candle.close == 25050
