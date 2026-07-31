class StrategyLifecycle:
    def __init__(self):
        self._started = False

    def initialize(self, strategy):
        if hasattr(strategy, "initialize"):
            strategy.initialize()

    def start(self):
        self._started = True

    def stop(self):
        self._started = False

    def restart(self):
        self.stop()
        self.start()

    def is_started(self):
        return self._started

    def shutdown(self, strategy):
        if hasattr(strategy, "shutdown"):
            strategy.shutdown()
