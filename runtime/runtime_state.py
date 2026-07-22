"""
Runtime state manager.
"""


class RuntimeState:
    """Represents the runtime state."""

    def __init__(self) -> None:
        self.status = "created"

    def running(self) -> None:
        self.status = "running"

    def stopped(self) -> None:
        self.status = "stopped"

    def restart(self) -> None:
        self.running()

    def reset(self) -> None:
        self.status = "created"