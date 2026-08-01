"""
TOS Strategy Plugin Framework

Base contract for all trading strategies.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseStrategy(ABC):
    """
    Base contract for every trading strategy.
    """

    @abstractmethod
    def name(self) -> str:
        """Return strategy name."""

    @abstractmethod
    def analyze(
        self,
        market,
        indicators,
    ):
        """
        Analyze market and indicators.
        """

    @abstractmethod
    def generate_signal(
        self,
        market,
        indicators,
    ):
        """
        Generate BUY / SELL / HOLD signal.
        """
