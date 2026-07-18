class StrategyScheduler:
    def __init__(self):
        self._enabled = True

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self):
        return self._enabled

    def should_run(self):
        return self._enabled

    def run(self, pipeline, context=None):
        if not self.should_run():
            return []

        return pipeline.execute(context)