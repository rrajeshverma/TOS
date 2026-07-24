"""
Tests for WebSocketFeed + TickDispatcher + MarketRuntime integration.
"""

from datetime import datetime

from brokers.dhan.models import BrokerTick
from market.market_runtime import MarketRuntime
from market.tick_dispatcher import TickDispatcher
from market.websocket_feed import WebSocketFeed


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


def test_market_feed_dispatches_tick_to_runtime():

    dispatcher = TickDispatcher()

    runtime = MarketRuntime()

    runtime.start()

    dispatcher.register(
        runtime.on_tick
    )

    feed = WebSocketFeed(
        dispatcher=dispatcher.dispatch,
    )

    feed.connect()

    feed.receive_tick(
        create_tick()
    )

    market = runtime.get_market()

    assert market is not None
    assert market.symbol == "NIFTY"
    assert market.close == 22500.0


def test_runtime_does_not_process_tick_when_stopped():

    dispatcher = TickDispatcher()

    runtime = MarketRuntime()

    dispatcher.register(
        runtime.on_tick
    )

    feed = WebSocketFeed(
        dispatcher=dispatcher.dispatch,
    )

    feed.receive_tick(
        create_tick()
    )

    assert runtime.get_market() is None


def test_multiple_ticks_update_market_state():

    dispatcher = TickDispatcher()

    runtime = MarketRuntime()

    runtime.start()

    dispatcher.register(
        runtime.on_tick
    )

    feed = WebSocketFeed(
        dispatcher=dispatcher.dispatch,
    )

    feed.receive_tick(
        create_tick(
            ltp=22500.0,
        )
    )

    feed.receive_tick(
        create_tick(
            ltp=22550.0,
        )
    )

    market = runtime.get_market()

    assert market.close == 22550.0


def test_feed_rejects_empty_tick():

    feed = WebSocketFeed()

    try:
        feed.receive_tick(None)
    except ValueError as exc:
        assert str(exc) == "Tick cannot be None."
