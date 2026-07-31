from trading.execution_mode import ExecutionMode


class ExecutionModeController:
    def __init__(
        self,
        mode,
        *,
        paper_runner=None,
        live_runtime=None,
    ):
        if not isinstance(mode, ExecutionMode):
            raise ValueError(f"Unsupported execution mode: {mode}")

        self.mode = mode
        self._running = False

        if mode is ExecutionMode.PAPER:
            self.runtime = paper_runner
        elif mode is ExecutionMode.LIVE:
            self.runtime = live_runtime
        else:
            raise ValueError(f"Unsupported execution mode: {mode}")

    def start(self):
        if self.runtime is None:
            raise RuntimeError("No runtime configured")

        if self._running:
            raise RuntimeError("Runtime already started")

        self.runtime.start()
        self._running = True

    def stop(self):
        if not self._running:
            raise RuntimeError("Runtime not running")

        self.runtime.stop()
        self._running = False

    def status(self):
        return "running" if self._running else "stopped"

    @property
    def is_running(self):
        return self._running