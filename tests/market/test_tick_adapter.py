"""
Tests for TickAdapter.
"""

from datetime import datetime

import pytest

from brokers.dhan.models import BrokerTick
from market.tick_adapter import TickAdapter


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


def test_adapt_tick_to_market():
    adapter = TickAdapter()

    tick = create_tick()

    market = adapter.adapt(tick)

    assert market.symbol == "NIFTY"
    assert market.close == 22500.0
    assert market.volume == 100000
    assert market.timeframe == "TICK"


def test_last_tick_storage():
    adapter = TickAdapter()

    tick = create_tick()

    adapter.adapt(tick)

    stored = adapter.last_tick("NIFTY")

    assert stored == tick


def test_last_tick_unknown_symbol():
    adapter = TickAdapter()

    assert adapter.last_tick("BANKNIFTY") is None


def test_adapt_none_tick():
    adapter = TickAdapter()

    with pytest.raises(ValueError):
        adapter.adapt(None)


def test_clear_ticks():
    adapter = TickAdapter()

    adapter.adapt(create_tick())

    adapter.clear()

    assert adapter.last_tick("NIFTY") is None
