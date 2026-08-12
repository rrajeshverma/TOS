from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from brokers.dhan.models import BrokerTick
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
            "trading_pipeline": trading_pipeline,
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
            "trading_pipeline": trading_pipeline,
        },
        mode=RuntimeMode.PAPER,
    )

    market_data.emit_market_tick(create_broker_tick())

    trading_pipeline.on_tick.assert_not_called()
