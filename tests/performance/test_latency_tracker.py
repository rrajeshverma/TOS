from performance.latency_tracker import LatencyTracker


def test_tracker_initializes_empty():
    tracker = LatencyTracker()
    assert tracker.count == 0


def test_add_single_latency():
    tracker = LatencyTracker()
    tracker.add(10)
    assert tracker.count == 1


def test_average_latency():
    tracker = LatencyTracker()

    tracker.add(10)
    tracker.add(20)
    tracker.add(30)

    assert tracker.average == 20


def test_minimum_latency():
    tracker = LatencyTracker()

    tracker.add(8)
    tracker.add(3)
    tracker.add(15)

    assert tracker.minimum == 3


def test_maximum_latency():
    tracker = LatencyTracker()

    tracker.add(8)
    tracker.add(3)
    tracker.add(15)

    assert tracker.maximum == 15


def test_latest_latency():
    tracker = LatencyTracker()

    tracker.add(5)
    tracker.add(9)

    assert tracker.latest() == 9


def test_clear_tracker():
    tracker = LatencyTracker()

    tracker.add(10)
    tracker.clear()

    assert tracker.count == 0


def test_values_returns_all_samples():
    tracker = LatencyTracker()

    tracker.add(1)
    tracker.add(2)
    tracker.add(3)

    assert tracker.values() == [1.0, 2.0, 3.0]


def test_empty_average():
    tracker = LatencyTracker()

    assert tracker.average == 0.0


def test_empty_minimum():
    tracker = LatencyTracker()

    assert tracker.minimum == 0.0


def test_empty_maximum():
    tracker = LatencyTracker()

    assert tracker.maximum == 0.0


def test_empty_latest():
    tracker = LatencyTracker()

    assert tracker.latest() == 0.0


def test_len_matches_count():
    tracker = LatencyTracker()

    tracker.add(1)
    tracker.add(2)

    assert len(tracker) == 2


def test_max_samples_limit():
    tracker = LatencyTracker(max_samples=2)

    tracker.add(1)
    tracker.add(2)
    tracker.add(3)

    assert tracker.values() == [2.0, 3.0]


def test_repr_contains_tracker_information():
    tracker = LatencyTracker()

    tracker.add(10)

    result = repr(tracker)

    assert "LatencyTracker" in result
    assert "count=1" in result