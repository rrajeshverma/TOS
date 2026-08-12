from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock

from brokers.dhan.models import BrokerTick
from engines.market_engine import MarketEngine
from integration.pipeline import TradingPipeline
from market.candle_builder import CandleBuilder
from runtime.runtime_mode import RuntimeMode
from runtime.trading_runtime import TradingRuntime
from services.market_data_service import MarketDataService


def create_broker_tick():
    return BrokerTick(
        symbol="NIFTY",
        ltp=24367.75,
        volume=0,
        timestamp=datetime.now(),
    )


def test_dhan_broker_tick_reaches_trading_pipeline():
    market_data = MarketDataService(websocket=None)

    trading_pipeline = Mock()

    runtime = TradingRuntime(
        {
            "market_data_service": market_data,
            "market_data_pipeline": trading_pipeline,
        },
        mode=RuntimeMode.PAPER,
    )

    runtime.start()

    tick = create_broker_tick()

    market_data.emit_market_tick(tick)

    trading_pipeline.on_tick.assert_called_once()

    received_tick = trading_pipeline.on_tick.call_args.args[0]

    assert received_tick.symbol == "NIFTY"
    assert received_tick.ltp == Decimal("24367.75")
    assert received_tick.volume == 0
    assert received_tick.timestamp == tick.timestamp


def test_dhan_tick_pipeline_does_not_execute_without_runtime_start():
    market_data = MarketDataService(websocket=None)

    trading_pipeline = Mock()

    TradingRuntime(
        {
            "market_data_service": market_data,
            "market_data_pipeline": trading_pipeline,
        },
        mode=RuntimeMode.PAPER,
    )

    market_data.emit_market_tick(create_broker_tick())

    trading_pipeline.on_tick.assert_not_called()


def test_dhan_tick_reaches_full_trading_pipeline():
    market_data = MarketDataService(websocket=None)

    candle_builder = Mock()
    market_engine = Mock()

    indicator_engine = Mock()
    indicator_engine.MIN_CANDLES = 33

    runtime = TradingRuntime(
        {
            "market_data_service": market_data,
        },
        mode=RuntimeMode.PAPER,
    )

    market_data_pipeline = TradingPipeline(
        candle_builder=candle_builder,
        market_engine=market_engine,
        indicator_engine=indicator_engine,
        runtime=runtime,
    )

    candles = []

    for index in range(33):
        timestamp = datetime(
            2026,
            8,
            12,
            9,
            15,
        ) + timedelta(minutes=index * 5)

        candle = Mock()
        candle.symbol = "NIFTY"
        candle.timeframe = "5m"
        candle.timestamp = timestamp
        candle.open = 24000 + index
        candle.high = 24010 + index
        candle.low = 23990 + index
        candle.close = 24005 + index
        candle.volume = 1000

        candles.append(candle)

    candle_builder.update.side_effect = candles

    markets = []

    for candle in candles:
        market = Mock()
        market.symbol = "NIFTY"
        markets.append(market)

    market_engine.build_market.side_effect = markets

    runtime.on_market_tick = Mock(return_value="PROCESSED")

    market_data.register_tick_callback(
        market_data_pipeline.on_tick,
    )

    for index in range(33):
        tick = BrokerTick(
            symbol="NIFTY",
            ltp=24367.75 + index,
            volume=0,
            timestamp=datetime(
                2026,
                8,
                12,
                9,
                15,
            )
            + timedelta(minutes=index * 5),
        )

        market_data.emit_market_tick(tick)

    runtime.on_market_tick.assert_called_once()

    market, history = runtime.on_market_tick.call_args.args

    assert market.symbol == "NIFTY"
    assert len(history) == 33


def test_dhan_market_data_reaches_runtime_through_real_pipeline():
    market_data = MarketDataService(websocket=None)

    candle_builder = CandleBuilder(timeframe="5m")
    market_engine = MarketEngine()

    indicator_engine = Mock()
    indicator_engine.MIN_CANDLES = 1

    runtime = Mock()

    pipeline = TradingPipeline(
        candle_builder=candle_builder,
        market_engine=market_engine,
        indicator_engine=indicator_engine,
        runtime=runtime,
    )

    market_data.register_tick_callback(pipeline.on_tick)

    tick = create_broker_tick()

    market_data.emit_market_tick(tick)

    runtime.on_market_tick.assert_called_once()

    market, history = runtime.on_market_tick.call_args.args

    assert market.symbol == "NIFTY"
    assert market.exchange == "NSE"
    assert market.timeframe == "5m"
    assert market.close == Decimal("24367.75")
    assert history == [market]
