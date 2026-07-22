from datetime import datetime

from domain.market import Market
from market.market_history import MarketHistory


def create_market():

    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
    )


def test_add_market():

    history = MarketHistory()

    history.add(
        create_market()
    )

    assert history.count() == 1



def test_get_history():

    history = MarketHistory()

    history.add(
        create_market()
    )

    candles = history.get()

    assert len(candles) == 1



def test_clear_history():

    history = MarketHistory()

    history.add(
        create_market()
    )

    history.clear()

    assert history.count() == 0
