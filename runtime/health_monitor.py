"""
Runtime health monitor.
"""

from datetime import datetime


class HealthMonitor:
    """Tracks runtime health."""

    def __init__(self) -> None:
        self.healthy = True
        self.last_check = None

    def mark_healthy(self) -> None:
        self.healthy = True

    def mark_unhealthy(self) -> None:
        self.healthy = False

    def update(self) -> None:
        self.last_check = datetime.now()

    def reset(self) -> None:
        self.healthy = True
        self.last_check = None
