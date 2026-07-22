"""
Application lifecycle manager.
"""


class Lifecycle:
    """Controls runtime lifecycle."""

    def __init__(self) -> None:
        self.state = "created"

    def start(self) -> None:
        self.state = "running"

    def stop(self) -> None:
        self.state = "stopped"

    def restart(self) -> None:
        self.stop()
        self.start()