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

        if mode is ExecutionMode.PAPER:
            self.runtime = paper_runner
        elif mode is ExecutionMode.LIVE:
            self.runtime = live_runtime
        else:
            raise ValueError(f"Unsupported execution mode: {mode}")

    def start(self):
        if self.runtime is None:
            raise RuntimeError("No runtime configured")

        self.runtime.start()

    def stop(self):
        if self.runtime is None:
            raise RuntimeError("No runtime configured")

        self.runtime.stop()