import time

from performance.execution_timer import ExecutionTimer


def test_execution_timer_initializes_with_default_state():
    timer = ExecutionTimer()

    assert timer.is_running is False
    assert timer.start_time is None
    assert timer.end_time is None

def test_start_sets_running_state():
    timer = ExecutionTimer()

    timer.start()

    assert timer.is_running is True
    assert timer.start_time is not None
    assert timer.end_time is None

def test_stop_sets_end_time_and_stops_timer():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.001)
    timer.stop()

    assert timer.is_running is False
    assert timer.end_time is not None
    assert timer.end_time >= timer.start_time

def test_elapsed_returns_execution_time():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.01)
    timer.stop()

    assert timer.elapsed > 0
    assert isinstance(timer.elapsed, float)

def test_elapsed_before_start_returns_zero():
    timer = ExecutionTimer()

    assert timer.elapsed == 0.0

def test_elapsed_while_running_returns_positive_time():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.01)

    assert timer.elapsed > 0
    assert timer.is_running is True

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

def test_stop_before_start_does_not_raise_error():
    timer = ExecutionTimer()

    timer.stop()

    assert timer.is_running is False
    assert timer.start_time is None
    assert timer.end_time is None
    assert timer.elapsed == 0.0

def test_string_representation_contains_elapsed_time():
    timer = ExecutionTimer()

    timer.start()
    time.sleep(0.001)
    timer.stop()

    result = str(timer)

    assert "ExecutionTimer" in result
    assert "elapsed=" in result

def test_repr_matches_string_representation():
    timer = ExecutionTimer()

    timer.start()
    timer.stop()

    assert repr(timer) == str(timer)

def test_context_manager_times_execution():
    with ExecutionTimer() as timer:
        time.sleep(0.01)

    assert timer.is_running is False
    assert timer.elapsed > 0