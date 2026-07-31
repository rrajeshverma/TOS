class TradeSupervisor:
    """
    Controls live trading state.
    """

    def __init__(self):
        self._running = False
        self._paused = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def is_running(self):
        return self._running

    def is_paused(self):
        return self._paused

    def status(self):
        return {
            "running": self._running,
            "paused": self._paused,
        }
