"""
Runtime health report.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeHealthReport:
    """Immutable runtime health snapshot."""

    broker: str
    reconnect: str

    @property
    def healthy(self) -> bool:
        """Return overall health."""

        return self.broker == "CONNECTED"
