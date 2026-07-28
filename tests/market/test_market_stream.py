from datetime import datetime

import pytest

from market.event import MarketEvent
from market.stream import MarketStream
from market.tick import Tick


def create_event():

    tick = Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )

    return MarketEvent(
        event_type="PRICE_UPDATE",
        tick=tick,
        source="DHAN",
    )


def test_stream_can_subscribe_symbol():

    stream = MarketStream()

    stream.subscribe("NIFTY")

    assert (
        "NIFTY"
        in stream.subscriptions()
    )



def test_stream_can_unsubscribe_symbol():

    stream = MarketStream()

    stream.subscribe("NIFTY")
    stream.unsubscribe("NIFTY")

    assert (
        "NIFTY"
        not in stream.subscriptions()
    )



def test_stream_publishes_event():

    stream = MarketStream()

    event = create_event()

    stream.publish(event)

    assert (
        stream.latest_tick("NIFTY")
        == event.tick
    )



def test_stream_rejects_invalid_event():

    stream = MarketStream()

    with pytest.raises(ValueError):

        stream.publish(None)



def test_stream_returns_none_for_unknown_symbol():

    stream = MarketStream()

    assert (
        stream.latest_tick("BANKNIFTY")
        is None
    )



def test_stream_keeps_latest_tick():

    stream = MarketStream()

    first = create_event()

    stream.publish(first)

    assert (
        stream.latest_tick("NIFTY").price
        == 24500.50
    )
