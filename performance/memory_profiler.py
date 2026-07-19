import tracemalloc


class MemoryProfiler:
    def __init__(self):
        self._started = False

    @property
    def is_running(self):
        return self._started

    def start(self):
        if not tracemalloc.is_tracing():
            tracemalloc.start()

        self._started = True

    def stop(self):
        if tracemalloc.is_tracing():
            tracemalloc.stop()

        self._started = False

    def current_memory(self):
        if not tracemalloc.is_tracing():
            return 0

        current, _ = tracemalloc.get_traced_memory()
        return current

    def peak_memory(self):
        if not tracemalloc.is_tracing():
            return 0

        _, peak = tracemalloc.get_traced_memory()
        return peak

    def reset_peak(self):
        if tracemalloc.is_tracing():
            tracemalloc.reset_peak()

    def snapshot(self):
        if not tracemalloc.is_tracing():
            return None

        return tracemalloc.take_snapshot()