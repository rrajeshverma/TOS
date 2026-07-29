"""
TOS Strategy Manager

Coordinates the strategy framework.
"""

from __future__ import annotations

from strategies.registry import StrategyRegistry
from strategies.strategy_engine import StrategyEngine


class StrategyManager:
    """
    Coordinates strategy registration and execution.
    """

    def __init__(self) -> None:
        self.registry = StrategyRegistry()
        self.engine = StrategyEngine(self.registry)
