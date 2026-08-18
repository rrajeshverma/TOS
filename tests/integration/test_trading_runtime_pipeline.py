from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from domain.market import Market
from domain.market_tick import MarketTick
from integration.pipeline import TradingPipeline


class FakeCandle:
    def __init__(self):
        self.symbol = "NIFTY"
        self.timeframe = "1m"
        self.timestamp = datetime.now()
        self.open = Decimal(100)
        self.high = Decimal(101)
        self.low = Decimal(99)
        self.close = Decimal(100)
        self.volume = 100


def test_pipeline_forwards_completed_market_to_runtime():
    candle_builder = Mock()

    first_candle = FakeCandle()
    first_candle.timeframe = "5m"
    first_candle.timestamp = datetime(2026, 8, 18, 10, 40)

    second_candle = FakeCandle()
    second_candle.timeframe = "5m"
    second_candle.timestamp = datetime(2026, 8, 18, 10, 45)

    candle_builder.update.side_effect = [
        first_candle,
        second_candle,
    ]

    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=first_candle.timestamp,
        open=Decimal(100),
        high=Decimal(101),
        low=Decimal(99),
        close=Decimal(100),
        volume=100,
    )

    next_market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=second_candle.timestamp,
        open=Decimal(101),
        high=Decimal(102),
        low=Decimal(100),
        close=Decimal(101),
        volume=100,
    )

    market_engine = Mock()
    market_engine.build_market.side_effect = [
        market,
        next_market,
    ]

    indicator_engine = Mock()
    indicator_engine.MIN_CANDLES = 1

    runtime = Mock()
    runtime.on_market_tick.return_value = "processed"

    pipeline = TradingPipeline(
        candle_builder=candle_builder,
        market_engine=market_engine,
        indicator_engine=indicator_engine,
        runtime=runtime,
    )

    first_tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(100),
        timestamp=datetime(2026, 8, 18, 10, 40, 1),
    )

    second_tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(101),
        timestamp=datetime(2026, 8, 18, 10, 45, 1),
    )

    assert pipeline.on_tick(first_tick) is None

    result = pipeline.on_tick(second_tick)

    candle_builder.update.assert_any_call(first_tick)
    candle_builder.update.assert_any_call(second_tick)

    assert market_engine.build_market.call_count == 1
    runtime.on_market_tick.assert_called_once()

    runtime_market, runtime_history = runtime.on_market_tick.call_args.args

    assert runtime_market == market
    assert runtime_history == [market]
    assert result == "processed"


def test_pipeline_processes_same_5m_candle_only_once():
    candle_builder = Mock()
    market_engine = Mock()
    indicator_engine = Mock()
    indicator_engine.MIN_CANDLES = 1

    runtime = Mock()
    runtime.on_market_tick.return_value = "processed"

    candle_1040 = FakeCandle()
    candle_1040.timeframe = "5m"
    candle_1040.timestamp = datetime(2026, 8, 18, 10, 40)

    candle_1045 = FakeCandle()
    candle_1045.timeframe = "5m"
    candle_1045.timestamp = datetime(2026, 8, 18, 10, 45)

    candle_builder.update.side_effect = [
        candle_1040,
        candle_1040,
        candle_1040,
        candle_1045,
    ]

    market_1040 = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=candle_1040.timestamp,
        open=Decimal(100),
        high=Decimal(101),
        low=Decimal(99),
        close=Decimal(100),
        volume=100,
    )

    market_1045 = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=candle_1045.timestamp,
        open=Decimal(101),
        high=Decimal(102),
        low=Decimal(100),
        close=Decimal(101),
        volume=100,
    )

    market_engine.build_market.side_effect = [
        market_1040,
        market_1040,
        market_1040,
        market_1045,
    ]

    pipeline = TradingPipeline(
        candle_builder=candle_builder,
        market_engine=market_engine,
        indicator_engine=indicator_engine,
        runtime=runtime,
    )

    ticks = [
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal("100"),
            timestamp=datetime(2026, 8, 18, 10, 40, 1),
        ),
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal("100"),
            timestamp=datetime(2026, 8, 18, 10, 41, 0),
        ),
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal("100"),
            timestamp=datetime(2026, 8, 18, 10, 44, 59),
        ),
        MarketTick(
            symbol="NIFTY",
            ltp=Decimal("101"),
            timestamp=datetime(2026, 8, 18, 10, 45, 1),
        ),
    ]

    for tick in ticks:
        pipeline.on_tick(tick)

    assert runtime.on_market_tick.call_count == 1

    runtime_market, runtime_history = runtime.on_market_tick.call_args_list[0].args

    assert runtime_market == market_1040
    assert runtime_history == [market_1040]
