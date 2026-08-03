"""
Replay session.
"""

from __future__ import annotations

from backtesting.replay_clock import ReplayClock


class ReplaySession:
    """
    Coordinates a historical replay session.
    """

    def __init__(
        self,
        clock: ReplayClock,
    ) -> None:
        self._clock = clock
        self._processed = 0

    @property
    def clock(self) -> ReplayClock:
        return self._clock

    @property
    def processed_candles(self) -> int:
        return self._processed

    def process_next(self) -> None:
        """
        Record one processed candle.
        """
        self._processed += 1

    def reset(self) -> None:
        """
        Reset replay session.
        """
        self._processed = 0
        self._clock.reset()
