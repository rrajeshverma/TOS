"""
Application shutdown manager.
"""


class Shutdown:
    """Handles graceful shutdown."""

    def __init__(self) -> None:
        self.broker_closed = False
        self.logs_flushed = False
        self.state_saved = False

    def close_broker(self) -> None:
        self.broker_closed = True

    def flush_logs(self) -> None:
        self.logs_flushed = True

    def save_state(self) -> None:
        self.state_saved = True