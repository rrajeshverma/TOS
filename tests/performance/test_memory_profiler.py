from performance.memory_profiler import MemoryProfiler


def test_profiler_initializes_stopped():
    profiler = MemoryProfiler()

    assert profiler.is_running is False


def test_start_sets_running():
    profiler = MemoryProfiler()

    profiler.start()

    assert profiler.is_running is True

    profiler.stop()


def test_stop_sets_not_running():
    profiler = MemoryProfiler()

    profiler.start()
    profiler.stop()

    assert profiler.is_running is False


def test_current_memory_returns_integer():
    profiler = MemoryProfiler()

    profiler.start()

    assert isinstance(profiler.current_memory(), int)

    profiler.stop()


def test_peak_memory_returns_integer():
    profiler = MemoryProfiler()

    profiler.start()

    assert isinstance(profiler.peak_memory(), int)

    profiler.stop()


def test_snapshot_returns_snapshot():
    profiler = MemoryProfiler()

    profiler.start()

    snapshot = profiler.snapshot()

    assert snapshot is not None

    profiler.stop()


def test_snapshot_after_stop_returns_none():
    profiler = MemoryProfiler()

    profiler.start()
    profiler.stop()

    assert profiler.snapshot() is None


def test_current_memory_after_stop_returns_zero():
    profiler = MemoryProfiler()

    profiler.start()
    profiler.stop()

    assert profiler.current_memory() == 0


def test_peak_memory_after_stop_returns_zero():
    profiler = MemoryProfiler()

    profiler.start()
    profiler.stop()

    assert profiler.peak_memory() == 0


def test_reset_peak():
    profiler = MemoryProfiler()

    profiler.start()

    profiler.reset_peak()

    profiler.stop()


def test_multiple_start_calls():
    profiler = MemoryProfiler()

    profiler.start()
    profiler.start()

    assert profiler.is_running

    profiler.stop()


def test_multiple_stop_calls():
    profiler = MemoryProfiler()

    profiler.start()

    profiler.stop()
    profiler.stop()

    assert profiler.is_running is False


def test_allocate_memory():
    profiler = MemoryProfiler()

    profiler.start()

    data = [i for i in range(10000)]

    assert profiler.current_memory() > 0

    del data

    profiler.stop()


def test_peak_memory_is_non_negative():
    profiler = MemoryProfiler()

    profiler.start()

    _ = [i for i in range(10000)]

    assert profiler.peak_memory() > 0
    assert profiler.current_memory() > 0

    profiler.stop()


def test_profiler_reusable():
    profiler = MemoryProfiler()

    profiler.start()
    profiler.stop()

    profiler.start()

    assert profiler.is_running

    profiler.stop()


def test_memory_profiler_snapshot(): ...


def test_memory_profiler_peak(): ...


def test_memory_profiler_growth(): ...


def test_memory_profiler_reset(): ...


def test_memory_profiler_summary(): ...
