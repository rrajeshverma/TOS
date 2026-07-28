from datetime import datetime, timedelta

import pytest

from market.health import MarketDataHealth
from market.tick import Tick


def create_tick():

    return Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )


def test_health_initial_state():

    health = MarketDataHealth()

    assert (
        health.is_healthy()
        is False
    )


def test_health_becomes_healthy_after_tick():

    health = MarketDataHealth()

    health.record_tick(
        create_tick()
    )

    assert (
        health.is_healthy()
        is True
    )


def test_health_tracks_last_tick_time():

    health = MarketDataHealth()

    tick = create_tick()

    health.record_tick(tick)

    assert (
        health.last_tick_time()
        == tick.timestamp
    )


def test_health_detects_stale_feed():

    health = MarketDataHealth()

    old_tick = Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now()
        - timedelta(minutes=10),
        exchange="NSE",
    )

    health.record_tick(old_tick)

    assert (
        health.is_feed_stale()
        is True
    )


def test_health_requires_tick():

    health = MarketDataHealth()

    with pytest.raises(ValueError):

        health.record_tick(None)


def test_recovery_required_when_stale():

    health = MarketDataHealth()

    assert (
        health.recovery_required()
        is True
    )
