"""
TOS Broker Health Monitor

Tracks broker connectivity and health status.
"""

from __future__ import annotations


class BrokerHealthMonitor:
    """
    Monitors broker runtime health.
    """

    def __init__(self) -> None:
        self._connected = False
        self._latency = None
        self._failures = 0

    def mark_connected(
        self,
        latency_ms: float,
    ) -> None:
        """
        Record healthy broker connection.
        """

        self._connected = True
        self._latency = latency_ms

    def mark_disconnected(
        self,
    ) -> None:
        """
        Record broker disconnect.
        """

        self._connected = False

    def record_failure(
        self,
    ) -> None:
        """
        Increment broker failures.
        """

        self._failures += 1

    @property
    def is_healthy(
        self,
    ) -> bool:
        """
        Return broker health state.
        """

        return self._connected and self._failures == 0

    def latency(
        self,
    ):
        """
        Return latest latency.
        """

        return self._latency

    def failures(
        self,
    ) -> int:
        """
        Return failure count.
        """

        return self._failures

    def reset(
        self,
    ) -> None:
        """
        Reset health state.
        """

        self._connected = False
        self._latency = None
        self._failures = 0
