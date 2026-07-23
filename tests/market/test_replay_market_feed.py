from market.replay_market_feed import ReplayMarketFeed


def test_empty_feed():
    feed = ReplayMarketFeed([])
    assert feed.has_next() is False


def test_single_tick():
    ticks = [{"symbol": "NIFTY"}]

    feed = ReplayMarketFeed(ticks)

    assert feed.has_next() is True
    assert feed.next_tick() == {"symbol": "NIFTY"}
    assert feed.has_next() is False


def test_multiple_ticks():
    ticks = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]

    feed = ReplayMarketFeed(ticks)

    assert feed.next_tick()["id"] == 1
    assert feed.next_tick()["id"] == 2
    assert feed.next_tick()["id"] == 3
    assert feed.has_next() is False


def test_reset():
    ticks = [{"id": 1}]

    feed = ReplayMarketFeed(ticks)

    feed.next_tick()
    feed.reset()

    assert feed.has_next() is True
    assert feed.next_tick()["id"] == 1