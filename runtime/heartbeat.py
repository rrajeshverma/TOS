"""
Heartbeat monitor.
"""

from datetime import datetime


class Heartbeat:
    """Tracks application heartbeat."""

    def __init__(self, timeout: int = 60) -> None:
        self.timeout = timeout
        self.last_heartbeat = None

    def beat(self) -> None:
        self.last_heartbeat = datetime.now()
