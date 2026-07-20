from datetime import datetime


class RuntimeStatus:
    def __init__(self):
        self._running = False
        self._started_at = None

    @property
    def is_running(self):
        return self._running

    @property
    def started_at(self):
        return self._started_at

    def start(self):
        self._running = True
        self._started_at = datetime.now()

    def stop(self):
        self._running = False

    def uptime_seconds(self):
        if not self._running or self._started_at is None:
            return 0

        return int((datetime.now() - self._started_at).total_seconds())

    def __repr__(self):
        return f"RuntimeStatus(" f"running={self._running})"
