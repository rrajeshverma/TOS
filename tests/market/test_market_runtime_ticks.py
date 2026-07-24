"""
Tests for MarketRuntime tick processing.
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from market.market_runtime import MarketRuntime


def create_tick(
    symbol="NIFTY",
    ltp=22500.0,
    volume=100000,
):
    return BrokerTick(
        symbol=symbol,
        ltp=ltp,
        volume=volume,
        timestamp=datetime.now(),
    )


def test_runtime_start_stop_lifecycle():

    runtime = MarketRuntime()

    assert runtime.is_running() is False

    runtime.start()

    assert runtime.is_running() is True

    runtime.stop()

    assert runtime.is_running() is False


def test_runtime_receives_tick():

    runtime = MarketRuntime()

    runtime.start()

    runtime.on_tick(
        create_tick()
    )

    market = runtime.get_market()

    assert market is not None
    assert market.symbol == "NIFTY"
    assert market.close == 22500.0


def test_runtime_ignores_tick_when_stopped():

    runtime = MarketRuntime()

    runtime.on_tick(
        create_tick()
    )

    assert runtime.get_market() is None


def test_runtime_returns_latest_market():

    runtime = MarketRuntime()

    runtime.start()

    runtime.on_tick(
        create_tick(
            ltp=22500.0,
        )
    )

    runtime.on_tick(
        create_tick(
            ltp=22550.0,
        )
    )

    market = runtime.get_market()

    assert market.close == 22550.0
