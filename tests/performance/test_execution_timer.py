import time

from performance.execution_timer import ExecutionTimer


def test_initial_state():
    timer = ExecutionTimer()

    assert timer.is_running is False
    assert timer.start_time is None
    assert timer.end_time is None
    assert timer.elapsed == 0.0


def test_start():
    timer = ExecutionTimer()

    timer.start()

    assert timer.is_running is True
    assert timer.start_time is not None
    assert timer.end_time is None


def test_stop():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.001)
    timer.stop()

    assert timer.is_running is False
    assert timer.end_time is not None
    assert timer.elapsed >= 0.0


def test_stop_without_start():
    timer = ExecutionTimer()

    timer.stop()

    assert timer.is_running is False
    assert timer.start_time is None
    assert timer.end_time is None


def test_elapsed_while_running():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.001)

    assert timer.elapsed > 0.0


def test_str_contains_execution_timer():
    timer = ExecutionTimer()

    text = str(timer)

    assert "ExecutionTimer" in text


def test_repr_matches_str():
    timer = ExecutionTimer()

    assert repr(timer) == str(timer)


def test_context_manager():
    with ExecutionTimer() as timer:
        time.sleep(0.001)

    assert timer.is_running is False
    assert timer.elapsed > 0.0


def test_start_again_resets_end_time():
    timer = ExecutionTimer()

    timer.start()
    timer.stop()

    first_end_time = timer.end_time

    timer.start()

    assert timer.is_running is True
    assert timer.end_time is None
    assert timer.start_time > first_end_time


def test_stop_called_multiple_times_does_not_change_end_time():
    timer = ExecutionTimer()

    timer.start()
    timer.stop()

    first_end_time = timer.end_time

    timer.stop()

    assert timer.end_time == first_end_time
    assert timer.is_running is False


def test_elapsed_before_start_returns_zero():
    timer = ExecutionTimer()

    assert timer.elapsed == 0.0


def test_elapsed_returns_execution_time():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.01)
    timer.stop()

    assert timer.elapsed > 0
    assert isinstance(timer.elapsed, float)
