from datetime import datetime
from decimal import Decimal

from domain.market_tick import MarketTick
from market.candle_builder import CandleBuilder


def test_create_first_candle():
    builder = CandleBuilder(timeframe="5m")

    tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25000),
        volume=100,
        timestamp=datetime.now(),
    )

    candle = builder.update(tick)

    assert candle.open == Decimal(25000)
    assert candle.high == Decimal(25000)
    assert candle.low == Decimal(25000)
    assert candle.close == Decimal(25000)


def test_update_high_low_close():
    builder = CandleBuilder(timeframe="5m")

    t1 = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25000),
        volume=100,
        timestamp=datetime.now(),
    )

    t2 = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25050),
        volume=200,
        timestamp=datetime.now(),
    )

    builder.update(t1)

    candle = builder.update(t2)

    assert candle.high == Decimal(25050)
    assert candle.close == Decimal(25050)


def test_candle_timestamp_is_aligned_to_timeframe():
    builder = CandleBuilder(timeframe="5m")

    tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(25000),
        volume=100,
        timestamp=datetime(
            2026,
            8,
            11,
            9,
            17,
            30,
        ),
    )

    candle = builder.update(tick)

    assert candle.timestamp == datetime(
        2026,
        8,
        11,
        9,
        15,
    )


def test_new_candle_starts_at_five_minute_boundary():
    builder = CandleBuilder(timeframe="5m")

    first = builder.update(
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal(25000),
            volume=100,
            timestamp=datetime(
                2026,
                8,
                11,
                9,
                19,
                59,
            ),
        )
    )

    second = builder.update(
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal(25050),
            volume=200,
            timestamp=datetime(
                2026,
                8,
                11,
                9,
                20,
            ),
        )
    )

    assert first.timestamp == datetime(
        2026,
        8,
        11,
        9,
        15,
    )

    assert second.timestamp == datetime(
        2026,
        8,
        11,
        9,
        20,
    )

    assert second.open == Decimal(25050)
    assert second.high == Decimal(25050)
    assert second.low == Decimal(25050)
    assert second.close == Decimal(25050)


def test_symbols_have_independent_candles():
    builder = CandleBuilder(timeframe="5m")

    nifty = builder.update(
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal(25000),
            volume=100,
            timestamp=datetime(
                2026,
                8,
                11,
                9,
                15,
            ),
        )
    )

    banknifty = builder.update(
        MarketTick(
            symbol="BANKNIFTY",
            ltp=Decimal(55000),
            volume=200,
            timestamp=datetime(
                2026,
                8,
                11,
                9,
                16,
            ),
        )
    )

    assert nifty.symbol == "NIFTY"
    assert nifty.close == Decimal(25000)

    assert banknifty.symbol == "BANKNIFTY"
    assert banknifty.close == Decimal(55000)
