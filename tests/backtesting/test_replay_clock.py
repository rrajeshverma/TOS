from datetime import datetime

from backtesting.replay_clock import ReplayClock


def test_replay_clock_initially_none():
    clock = ReplayClock()

    assert clock.now is None


def test_replay_clock_advance():
    clock = ReplayClock()

    timestamp = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    clock.advance(timestamp)

    assert clock.now == timestamp


def test_replay_clock_reset():
    clock = ReplayClock()

    clock.advance(
        datetime(
            2026,
            1,
            1,
            9,
            15,
        )
    )

    clock.reset()

    assert clock.now is None
