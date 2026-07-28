from datetime import datetime

import pytest

from market.event import MarketEvent
from market.paper_adapter import PaperMarketAdapter
from market.tick import Tick


def create_tick():

    return Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )


def test_adapter_can_publish_tick():

    adapter = PaperMarketAdapter()

    tick = create_tick()

    event = adapter.publish_tick(tick)

    assert isinstance(
        event,
        MarketEvent,
    )



def test_adapter_creates_price_update_event():

    adapter = PaperMarketAdapter()

    event = adapter.publish_tick(
        create_tick()
    )

    assert (
        event.event_type
        == "PRICE_UPDATE"
    )



def test_adapter_source_is_paper():

    adapter = PaperMarketAdapter()

    event = adapter.publish_tick(
        create_tick()
    )

    assert (
        event.source
        == "PAPER"
    )



def test_adapter_rejects_empty_tick():

    adapter = PaperMarketAdapter()

    with pytest.raises(ValueError):

        adapter.publish_tick(
            None
        )



def test_adapter_tracks_last_tick():

    adapter = PaperMarketAdapter()

    tick = create_tick()

    adapter.publish_tick(tick)

    assert (
        adapter.last_tick()
        == tick
    )



def test_adapter_returns_none_without_tick():

    adapter = PaperMarketAdapter()

    assert (
        adapter.last_tick()
        is None
    )
