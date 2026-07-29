"""
TOS Metrics Collector

Collects runtime production metrics.
"""

from __future__ import annotations


class MetricsCollector:
    """
    Tracks trading runtime metrics.
    """

    def __init__(self) -> None:
        self._metrics = {
            "orders": 0,
            "successful_orders": 0,
            "failed_orders": 0,
            "risk_blocks": 0,
            "recoveries": 0,
        }

    def increment(
        self,
        metric: str,
    ) -> None:
        """
        Increment metric counter.
        """

        if metric not in self._metrics:
            raise ValueError(f"Unknown metric: {metric}")

        self._metrics[metric] += 1

    def get(
        self,
        metric: str,
    ) -> int:
        """
        Return metric value.
        """

        return self._metrics.get(
            metric,
            0,
        )

    def snapshot(
        self,
    ) -> dict:
        """
        Return metrics snapshot.
        """

        return dict(self._metrics)

    def reset(
        self,
    ) -> None:
        """
        Reset all metrics.
        """

        for key in self._metrics:
            self._metrics[key] = 0
