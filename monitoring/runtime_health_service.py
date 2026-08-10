"""
Runtime health service.
"""

from __future__ import annotations

from monitoring.broker_connection_monitor import (
    BrokerConnectionMonitor,
)
from monitoring.broker_reconnect_manager import (
    BrokerReconnectManager,
)
from monitoring.runtime_health_report import RuntimeHealthReport


class RuntimeHealthService:
    """Provides runtime health information."""

    def __init__(
        self,
        monitor: BrokerConnectionMonitor,
        reconnect_manager: BrokerReconnectManager,
    ) -> None:
        self._monitor = monitor
        self._reconnect_manager = reconnect_manager

    def status(self) -> RuntimeHealthReport:
        """Return runtime health."""

        return RuntimeHealthReport(
            broker=("CONNECTED" if self._monitor.is_connected() else "DISCONNECTED"),
            reconnect=("AVAILABLE" if self._reconnect_manager.should_reconnect() else "BLOCKED"),
        )
