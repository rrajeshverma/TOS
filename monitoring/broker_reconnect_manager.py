"""
Broker reconnect manager.
"""

from __future__ import annotations

from monitoring.broker_connection_monitor import BrokerConnectionMonitor
from monitoring.reconnect_policy import ReconnectPolicy


class BrokerReconnectManager:
    """Coordinates broker reconnection decisions."""

    def __init__(
        self,
        monitor: BrokerConnectionMonitor,
        policy: ReconnectPolicy,
    ) -> None:
        self._monitor = monitor
        self._policy = policy

    def should_reconnect(self) -> bool:
        """Return True if a reconnect attempt should be made."""

        return not self._monitor.is_connected() and self._policy.can_retry()

    def record_failure(self) -> None:
        """Record a failed reconnect attempt."""

        self._policy.record_failure()

    def reset(self) -> None:
        """Reset reconnect attempts after successful connection."""

        self._policy.reset()
