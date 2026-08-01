"""
Trading time filter.
"""

from __future__ import annotations

from datetime import time


class TimeFilter:
    """
    Validates whether trading is allowed
    within the configured trading window.
    """

    def __init__(
        self,
        start: time,
        end: time,
    ) -> None:
        self._start = start
        self._end = end

    def allow(
        self,
        current: time,
    ) -> bool:
        """
        Return True if current time
        is inside trading window.
        """

        return self._start <= current <= self._end
