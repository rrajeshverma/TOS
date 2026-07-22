import time

from execution.timeout_handler import TimeoutHandler


def test_not_timed_out():
    handler = TimeoutHandler(timeout_seconds=5)

    start = time.time()

    assert handler.is_timed_out(start) is False


def test_timed_out():
    handler = TimeoutHandler(timeout_seconds=1)

    start = time.time() - 2

    assert handler.is_timed_out(start) is True


def test_remaining_time():
    handler = TimeoutHandler(timeout_seconds=10)

    start = time.time()

    remaining = handler.remaining_time(start)

    assert remaining <= 10
    assert remaining > 0
