import time

from performance.performance_monitor import PerformanceMonitor


def test_monitor_initializes_empty():
    monitor = PerformanceMonitor()

    assert monitor.count == 0


def test_start_creates_timer():
    monitor = PerformanceMonitor()

    monitor.start("engine")

    assert monitor.exists("engine")


def test_stop_returns_elapsed_time():
    monitor = PerformanceMonitor()

    monitor.start("engine")
    time.sleep(0.01)

    elapsed = monitor.stop("engine")

    assert elapsed > 0


def test_elapsed_returns_same_value():
    monitor = PerformanceMonitor()

    monitor.start("engine")
    time.sleep(0.01)
    monitor.stop("engine")

    assert monitor.elapsed("engine") > 0


def test_exists_returns_true():
    monitor = PerformanceMonitor()

    monitor.start("engine")

    assert monitor.exists("engine")


def test_exists_returns_false():
    monitor = PerformanceMonitor()

    assert monitor.exists("engine") is False


def test_remove_timer():
    monitor = PerformanceMonitor()

    monitor.start("engine")
    monitor.remove("engine")

    assert monitor.count == 0


def test_clear_removes_all_timers():
    monitor = PerformanceMonitor()

    monitor.start("one")
    monitor.start("two")

    monitor.clear()

    assert monitor.count == 0


def test_names_returns_registered_names():
    monitor = PerformanceMonitor()

    monitor.start("one")
    monitor.start("two")

    names = monitor.names()

    assert "one" in names
    assert "two" in names


def test_multiple_timers():
    monitor = PerformanceMonitor()

    monitor.start("one")
    monitor.start("two")

    time.sleep(0.01)

    first = monitor.stop("one")
    second = monitor.stop("two")

    assert first > 0
    assert second > 0


def test_count_tracks_registered_timers():
    monitor = PerformanceMonitor()

    monitor.start("one")
    monitor.start("two")

    assert monitor.count == 2


def test_restart_existing_timer():
    monitor = PerformanceMonitor()

    monitor.start("engine")
    monitor.stop("engine")

    monitor.start("engine")

    assert monitor.exists("engine")


def test_remove_missing_timer_is_safe():
    monitor = PerformanceMonitor()

    monitor.remove("missing")

    assert monitor.count == 0


def test_clear_empty_monitor():
    monitor = PerformanceMonitor()

    monitor.clear()

    assert monitor.count == 0


def test_names_empty_monitor():
    monitor = PerformanceMonitor()

    assert monitor.names() == []