from datetime import datetime

import pytest

from market.tick import Tick


def test_tick_can_be_created():

    tick = Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )

    assert tick.symbol == "NIFTY"
    assert tick.price == 24500.50
    assert tick.volume == 100
    assert tick.exchange == "NSE"


def test_tick_requires_symbol():

    with pytest.raises(ValueError):

        Tick(
            symbol="",
            price=24500.50,
            volume=100,
            timestamp=datetime.now(),
            exchange="NSE",
        )


def test_tick_requires_positive_price():

    with pytest.raises(ValueError):

        Tick(
            symbol="NIFTY",
            price=0,
            volume=100,
            timestamp=datetime.now(),
            exchange="NSE",
        )


def test_tick_requires_positive_volume():

    with pytest.raises(ValueError):

        Tick(
            symbol="NIFTY",
            price=24500.50,
            volume=0,
            timestamp=datetime.now(),
            exchange="NSE",
        )


def test_tick_is_immutable():

    tick = Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )

    with pytest.raises(
        Exception
    ):
        tick.price = 25000


def test_tick_representation():

    tick = Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )

    assert "NIFTY" in repr(tick)
