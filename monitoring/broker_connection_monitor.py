"""
Broker connection monitor.
"""

from __future__ import annotations


class BrokerConnectionMonitor:
    """Monitors broker connection status."""

    def __init__(self) -> None:
        self._connected = False

    def connect(self) -> None:
        """Mark broker as connected."""

        self._connected = True

    def disconnect(self) -> None:
        """Mark broker as disconnected."""

        self._connected = False

    def is_connected(self) -> bool:
        """Return broker connection status."""

        return self._connected
