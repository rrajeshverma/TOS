"""
Replay clock for historical backtesting.
"""

from __future__ import annotations

from datetime import datetime


class ReplayClock:
    """
    Controls replay time during backtesting.
    """

    def __init__(self) -> None:
        self._current: datetime | None = None

    @property
    def now(self) -> datetime | None:
        """
        Return current replay time.
        """
        return self._current

    def advance(
        self,
        timestamp: datetime,
    ) -> None:
        """
        Advance replay clock.
        """
        self._current = timestamp

    def reset(self) -> None:
        """
        Reset replay clock.
        """
        self._current = None
