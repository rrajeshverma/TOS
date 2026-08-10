"""
TOS Strategy Engine

Executes registered strategy plugins.
"""

from __future__ import annotations

from strategies.decision import StrategyDecision


class StrategyEngine:
    """
    Coordinates strategy execution.
    """

    def __init__(
        self,
        registry,
    ) -> None:
        if registry is None:
            raise ValueError("Strategy registry is required")

        self._registry = registry

    def execute(
        self,
        strategy_name: str,
        context,
    ):
        """
        Execute selected strategy and return decision.
        """

        strategy = self._registry.get(strategy_name)

        if strategy is None:
            return None

        signal = strategy.generate_signal(context)

        if signal is None:
            return None

        return StrategyDecision(
            strategy=strategy_name,
            signal=signal,
            confidence=85,
            metadata={
                "context": context,
            },
        )

    def analyze(
        self,
        strategy_name: str,
        context,
    ):
        """
        Analyze using selected strategy.
        """

        strategy = self._registry.get(strategy_name)

        if strategy is None:
            return None

        return strategy.analyze(context)
