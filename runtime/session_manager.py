"""
Trading session manager.
"""


class SessionManager:
    """Manages trading session lifecycle."""

    def __init__(self) -> None:
        self.status = "closed"

    def open(self) -> None:
        self.status = "open"

    def close(self) -> None:
        self.status = "closed"

    def restart(self) -> None:
        self.close()
        self.open()

    def is_open(self) -> bool:
        return self.status == "open"