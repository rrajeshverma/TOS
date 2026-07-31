from brokers.dhan.models import BrokerTick
from market.websocket_feed import WebSocketFeed

from datetime import datetime


def test_receive_tick_dispatches():
    received = []

    feed = WebSocketFeed(dispatcher=received.append)

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000,
        volume=100,
        timestamp=datetime.now(),
    )

    feed.receive_tick(tick)

    assert received == [tick]


def test_invalid_tick_rejected():
    feed = WebSocketFeed()

    try:
        feed.receive_tick(None)
        assert False

    except ValueError:
        assert True


def test_receive_tick_without_dispatcher_safe():
    feed = WebSocketFeed()

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000,
        volume=100,
        timestamp=datetime.now(),
    )

    feed.receive_tick(tick)
