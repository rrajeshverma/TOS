import pytest

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

def test_next_tick_on_empty_feed_raises_stop_iteration():
    feed = ReplayMarketFeed([])

    with pytest.raises(StopIteration):
        feed.next_tick()


def test_next_tick_after_end_raises_stop_iteration():
    feed = ReplayMarketFeed([1])

    assert feed.next_tick() == 1

    with pytest.raises(StopIteration):
        feed.next_tick()


def test_reset_empty_feed():
    feed = ReplayMarketFeed([])

    feed.reset()

    assert feed.has_next() is False


def test_multiple_resets():
    feed = ReplayMarketFeed([1, 2])

    feed.reset()
    feed.reset()

    assert feed.next_tick() == 1


def test_tick_order_preserved():
    ticks = [1, 2, 3, 4, 5]

    feed = ReplayMarketFeed(ticks)

    assert [feed.next_tick() for _ in range(5)] == ticks


def test_duplicate_ticks():
    ticks = [1, 1, 2, 2]

    feed = ReplayMarketFeed(ticks)

    assert [feed.next_tick() for _ in range(4)] == ticks


def test_none_tick():
    feed = ReplayMarketFeed([None])

    assert feed.next_tick() is None


def test_has_next_idempotent():
    feed = ReplayMarketFeed([1])

    assert feed.has_next()
    assert feed.has_next()
    assert feed.has_next()


def test_reset_after_complete_replay():
    feed = ReplayMarketFeed([1, 2])

    feed.next_tick()
    feed.next_tick()

    feed.reset()

    assert feed.next_tick() == 1


def test_replay_twice_same_sequence():
    ticks = [10, 20, 30]

    feed = ReplayMarketFeed(ticks)

    first = []

    while feed.has_next():
        first.append(feed.next_tick())

    feed.reset()

    second = []

    while feed.has_next():
        second.append(feed.next_tick())

    assert first == second


def test_large_feed():
    ticks = list(range(1000))

    feed = ReplayMarketFeed(ticks)

    count = 0

    while feed.has_next():
        feed.next_tick()
        count += 1

    assert count == 1000


def test_dictionary_identity_preserved():
    tick = {"symbol": "NIFTY"}

    feed = ReplayMarketFeed([tick])

    assert feed.next_tick() is tick


def test_dictionary_mutation_visible():
    tick = {"price": 100}

    feed = ReplayMarketFeed([tick])

    returned = feed.next_tick()

    returned["price"] = 200

    assert tick["price"] == 200


def test_end_state_stable():
    feed = ReplayMarketFeed([1])

    feed.next_tick()

    assert feed.has_next() is False
    assert feed.has_next() is False


def test_reset_does_not_modify_ticks():
    ticks = [1, 2]

    feed = ReplayMarketFeed(ticks)

    feed.reset()

    assert ticks == [1, 2]


def test_mixed_payloads():
    ticks = [
        1,
        {"id": 2},
        None,
        "ABC",
    ]

    feed = ReplayMarketFeed(ticks)

    assert feed.next_tick() == 1
    assert feed.next_tick() == {"id": 2}
    assert feed.next_tick() is None
    assert feed.next_tick() == "ABC"


def test_has_next_false_after_complete_iteration():
    feed = ReplayMarketFeed([1, 2])

    feed.next_tick()
    feed.next_tick()

    assert not feed.has_next()


def test_has_next_true_after_reset():
    feed = ReplayMarketFeed([1])

    feed.next_tick()
    feed.reset()

    assert feed.has_next()


def test_multiple_complete_replays():
    ticks = [1, 2, 3]
    feed = ReplayMarketFeed(ticks)

    for _ in range(3):
        assert [feed.next_tick() for _ in range(3)] == ticks
        assert not feed.has_next()
        feed.reset()


def test_single_tick_multiple_resets():
    feed = ReplayMarketFeed(["A"])

    for _ in range(5):
        feed.reset()
        assert feed.next_tick() == "A"


def test_empty_feed_multiple_resets():
    feed = ReplayMarketFeed([])

    for _ in range(10):
        feed.reset()
        assert not feed.has_next()


def test_reset_after_partial_iteration():
    feed = ReplayMarketFeed([1, 2, 3])

    assert feed.next_tick() == 1
    feed.reset()

    assert feed.next_tick() == 1


def test_original_tick_list_not_modified():
    ticks = [{"id": 1}, {"id": 2}]
    original = list(ticks)

    feed = ReplayMarketFeed(ticks)

    while feed.has_next():
        feed.next_tick()

    assert ticks == original


def test_next_tick_returns_correct_types():
    ticks = [1, "abc", {"x": 1}, [1, 2], (3, 4)]

    feed = ReplayMarketFeed(ticks)

    for expected in ticks:
        assert feed.next_tick() == expected


def test_reset_after_stop_iteration():
    feed = ReplayMarketFeed([1])

    feed.next_tick()

    with pytest.raises(StopIteration):
        feed.next_tick()

    feed.reset()

    assert feed.next_tick() == 1


def test_stop_iteration_repeatable():
    feed = ReplayMarketFeed([])

    for _ in range(3):
        with pytest.raises(StopIteration):
            feed.next_tick()


def test_sequential_access_matches_source():
    ticks = list(range(50))

    feed = ReplayMarketFeed(ticks)

    for expected in ticks:
        assert feed.next_tick() == expected


def test_has_next_does_not_advance():
    feed = ReplayMarketFeed([10])

    feed.has_next()
    feed.has_next()

    assert feed.next_tick() == 10


def test_reset_preserves_sequence():
    ticks = [5, 6, 7]

    feed = ReplayMarketFeed(ticks)

    feed.next_tick()
    feed.reset()

    assert [feed.next_tick() for _ in range(3)] == ticks


def test_large_number_of_resets():
    feed = ReplayMarketFeed([1])

    for _ in range(100):
        feed.reset()

    assert feed.next_tick() == 1


def test_multiple_stop_iteration_after_completion():
    feed = ReplayMarketFeed([1])

    feed.next_tick()

    for _ in range(5):
        with pytest.raises(StopIteration):
            feed.next_tick()


def test_empty_feed_remains_empty_after_reset():
    feed = ReplayMarketFeed([])

    feed.reset()
    feed.reset()

    assert not feed.has_next()