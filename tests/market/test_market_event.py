from datetime import datetime

import pytest

from market.event import MarketEvent
from market.tick import Tick


def create_tick():

    return Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )


def test_market_event_can_be_created():

    event = MarketEvent(
        event_type="PRICE_UPDATE",
        tick=create_tick(),
        source="DHAN",
    )

    assert event.event_type == "PRICE_UPDATE"
    assert event.source == "DHAN"



def test_market_event_contains_tick():

    tick = create_tick()

    event = MarketEvent(
        event_type="PRICE_UPDATE",
        tick=tick,
        source="DHAN",
    )

    assert event.tick == tick



def test_market_event_requires_event_type():

    with pytest.raises(ValueError):

        MarketEvent(
            event_type="",
            tick=create_tick(),
            source="DHAN",
        )



def test_market_event_requires_source():

    with pytest.raises(ValueError):

        MarketEvent(
            event_type="PRICE_UPDATE",
            tick=create_tick(),
            source="",
        )



def test_market_event_is_immutable():

    event = MarketEvent(
        event_type="PRICE_UPDATE",
        tick=create_tick(),
        source="DHAN",
    )

    with pytest.raises(Exception):
        event.source = "TEST"



def test_market_event_has_timestamp():

    event = MarketEvent(
        event_type="PRICE_UPDATE",
        tick=create_tick(),
        source="DHAN",
    )

    assert event.created_at is not None
