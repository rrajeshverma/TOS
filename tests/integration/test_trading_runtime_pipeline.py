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


def test_pipeline_forwards_market_to_runtime():
    candle_builder = Mock()
    candle_builder.update.return_value = FakeCandle()

    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="1m",
        timestamp=datetime.now(),
        open=Decimal(100),
        high=Decimal(101),
        low=Decimal(99),
        close=Decimal(100),
        volume=100,
    )

    market_engine = Mock()
    market_engine.build_market.return_value = market

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

    tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal(100),
    )

    result = pipeline.on_tick(tick)

    candle_builder.update.assert_called_once_with(tick)
    market_engine.build_market.assert_called_once()
    runtime.on_market_tick.assert_called_once()

    runtime_market, runtime_history = runtime.on_market_tick.call_args.args

    assert runtime_market == market
    assert runtime_history == [market]
    assert result == "processed"
