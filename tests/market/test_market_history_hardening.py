import pytest

from datetime import datetime

from domain.market import Market
from market.market_history import MarketHistory


def make_market(price: float) -> Market:
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="1m",
        timestamp=datetime(2026, 1, 1, 9, 15),
        open=price,
        high=price + 1,
        low=price - 1,
        close=price,
        volume=100,
    )


def test_history_is_empty_on_creation():
    history = MarketHistory()

    assert history.count() == 0
    assert history.get() == []
    assert history.latest() is None


def test_add_single_market():
    history = MarketHistory()

    market = make_market(100)

    history.add(market)

    assert history.count() == 1
    assert history.latest() is market


def test_add_multiple_markets():
    history = MarketHistory()

    m1 = make_market(100)
    m2 = make_market(101)
    m3 = make_market(102)

    history.add(m1)
    history.add(m2)
    history.add(m3)

    assert history.count() == 3
    assert history.latest() is m3


def test_get_returns_copy():
    history = MarketHistory()

    m1 = make_market(100)

    history.add(m1)

    markets = history.get()

    markets.clear()

    assert history.count() == 1
    assert history.latest() is m1


def test_clear_history():
    history = MarketHistory()

    history.add(make_market(100))
    history.add(make_market(101))

    history.clear()

    assert history.count() == 0
    assert history.latest() is None


def test_latest_empty_returns_none():
    history = MarketHistory()

    assert history.latest() is None


def test_latest_returns_last_market():
    history = MarketHistory()

    m1 = make_market(100)
    m2 = make_market(101)

    history.add(m1)
    history.add(m2)

    assert history.latest() is m2


def test_add_none_raises_value_error():
    history = MarketHistory()

    with pytest.raises(ValueError):
        history.add(None)


def test_max_size_keeps_latest_entries():
    history = MarketHistory(max_size=3)

    history.add(make_market(100))
    history.add(make_market(101))
    history.add(make_market(102))
    history.add(make_market(103))

    markets = history.get()

    assert len(markets) == 3
    assert markets[0].close == 101
    assert markets[1].close == 102
    assert markets[2].close == 103


def test_max_size_one():
    history = MarketHistory(max_size=1)

    history.add(make_market(100))
    history.add(make_market(200))

    assert history.count() == 1
    assert history.latest().close == 200


def test_max_size_none_grows_without_limit():
    history = MarketHistory()

    for i in range(20):
        history.add(make_market(i))

    assert history.count() == 20


def test_get_returns_new_list_each_time():
    history = MarketHistory()

    history.add(make_market(100))

    first = history.get()
    second = history.get()

    assert first is not second


def test_clear_empty_history_safe():
    history = MarketHistory()

    history.clear()

    assert history.count() == 0


def test_count_after_clear_and_readd():
    history = MarketHistory()

    history.add(make_market(100))
    history.clear()
    history.add(make_market(200))

    assert history.count() == 1
    assert history.latest().close == 200


def test_add_same_market_instance_twice():
    history = MarketHistory()

    market = make_market(100)

    history.add(market)
    history.add(market)

    assert history.count() == 2
    assert history.get()[0] is market
    assert history.get()[1] is market


def test_latest_after_max_size_trim():
    history = MarketHistory(max_size=2)

    history.add(make_market(100))
    history.add(make_market(101))
    history.add(make_market(102))

    assert history.latest().close == 102


def test_history_order_preserved():
    history = MarketHistory()

    history.add(make_market(100))
    history.add(make_market(101))
    history.add(make_market(102))

    closes = [m.close for m in history.get()]

    assert closes == [100, 101, 102]


def test_get_does_not_modify_internal_storage():
    history = MarketHistory()

    history.add(make_market(100))

    external = history.get()
    external.append(make_market(200))

    assert history.count() == 1
