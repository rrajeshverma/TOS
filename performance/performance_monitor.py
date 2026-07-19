from performance.execution_timer import ExecutionTimer


class PerformanceMonitor:
    def __init__(self):
        self._timers = {}

    def start(self, name: str):
        timer = ExecutionTimer()
        timer.start()
        self._timers[name] = timer
        return timer

    def stop(self, name: str):
        timer = self._timers[name]
        timer.stop()
        return timer.elapsed

    def elapsed(self, name: str):
        return self._timers[name].elapsed

    def exists(self, name: str):
        return name in self._timers

    def remove(self, name: str):
        self._timers.pop(name, None)

    def clear(self):
        self._timers.clear()

    @property
    def count(self):
        return len(self._timers)

    def names(self):
        return list(self._timers.keys())