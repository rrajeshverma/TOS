"""
Signal handler for graceful shutdown.
"""


class SignalHandler:
    """Handles runtime shutdown signals."""

    def __init__(self) -> None:
        self.signal_received: str | None = None

    def register(self, signal_name: str) -> None:
        self.signal_received = signal_name

    def is_shutdown_requested(self) -> bool:
        return self.signal_received in ("SIGINT", "SIGTERM")

    def reset(self) -> None:
        self.signal_received = None