from runtime.trading_runtime import TradingRuntime
from trading.execution_mode import ExecutionMode


class RuntimeFactory:
    """Creates the appropriate runtime for the selected execution mode."""

    def create(self, mode: ExecutionMode, services: dict):
        if mode is ExecutionMode.PAPER:
            return TradingRuntime(
                services=services,
                mode=mode,
            )

        if mode is ExecutionMode.LIVE:
            return TradingRuntime(
                services=services,
                mode=mode,
            )

        raise ValueError(f"Unsupported execution mode: {mode}")
