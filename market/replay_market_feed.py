class ReplayMarketFeed:
    def __init__(self, ticks):
        self._ticks = ticks
        self._index = 0

    def has_next(self):
        return self._index < len(self._ticks)

    def next_tick(self):
        tick = self._ticks[self._index]
        self._index += 1
        return tick

    def reset(self):
        self._index = 0

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
