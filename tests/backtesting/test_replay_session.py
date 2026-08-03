from backtesting.replay_clock import ReplayClock
from backtesting.replay_session import ReplaySession


def test_replay_session_initial_state():
    session = ReplaySession(ReplayClock())

    assert session.processed_candles == 0


def test_process_next():
    session = ReplaySession(ReplayClock())

    session.process_next()
    session.process_next()

    assert session.processed_candles == 2


def test_reset():
    session = ReplaySession(ReplayClock())

    session.process_next()
    session.reset()

    assert session.processed_candles == 0
    assert session.clock.now is None
