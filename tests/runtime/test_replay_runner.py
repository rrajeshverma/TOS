from unittest.mock import Mock

from runtime.replay_runner import ReplayRunner


def test_replay_runner_initial_state():
    runner = ReplayRunner()

    assert runner.cycles == 0
    assert runner.completed is False


def test_replay_runner_accepts_engine_runner():
    runner = ReplayRunner()
    engine_runner = Mock()

    runner.set_engine_runner(engine_runner)

    assert runner.engine_runner is engine_runner


def test_replay_runner_processes_all_ticks():
    engine_runner = Mock()

    replay_feed = Mock()
    replay_feed.has_next.side_effect = [True, True, True, False]
    replay_feed.next_tick.side_effect = [
        {"symbol": "NIFTY"},
        {"symbol": "NIFTY"},
        {"symbol": "NIFTY"},
    ]

    runner = ReplayRunner()
    runner.set_engine_runner(engine_runner)
    runner.run(replay_feed)

    assert engine_runner.run_cycle.call_count == 3
    assert runner.cycles == 3


def test_replay_runner_marks_completed():
    engine_runner = Mock()

    replay_feed = Mock()
    replay_feed.has_next.return_value = False

    runner = ReplayRunner()
    runner.set_engine_runner(engine_runner)
    runner.run(replay_feed)

    assert runner.completed is True


def test_replay_runner_handles_empty_session():
    engine_runner = Mock()

    replay_feed = Mock()
    replay_feed.has_next.return_value = False

    runner = ReplayRunner()
    runner.set_engine_runner(engine_runner)
    runner.run(replay_feed)

    engine_runner.run_cycle.assert_not_called()
