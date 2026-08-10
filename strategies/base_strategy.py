"""
TOS Strategy Plugin Framework

Base contract for all trading strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.strategy_result import StrategyResult


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
    ) -> StrategyResult:
        """
        Analyze market and indicators and return a StrategyResult.
        """
