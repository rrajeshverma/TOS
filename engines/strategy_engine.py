"""
=========================================================
Trading Operating System (TOS)
Module      : Strategy Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Orchestrates the complete strategy pipeline.
=========================================================
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from domain.decision import Decision
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.indicator_engine import IndicatorEngine
from engines.market_engine import MarketEngine
from shared.logger import get_logger


class StrategyEngine:
    """
    Executes the complete trading strategy pipeline.

    Raw Market Data
            │
            ▼
      MarketEngine
            │
            ▼
     IndicatorEngine
            │
            ▼
      DecisionEngine
            │
            ▼
         Decision
    """

    def __init__(
        self,
        market_engine: MarketEngine | None = None,
        indicator_engine: IndicatorEngine | None = None,
        decision_engine: DecisionEngine | None = None,
    ) -> None:
        self._logger = get_logger(__name__)

        self._market_engine = market_engine or MarketEngine()
        self._indicator_engine = indicator_engine or IndicatorEngine()
        self._decision_engine = decision_engine or DecisionEngine()

    def evaluate(
        self,
        raw_market: Mapping[str, Any],
        history: Sequence[Market],
    ) -> Decision:
        """
        Execute the complete strategy pipeline.
        """

        market = self._market_engine.build_market(raw_market)

        indicators = self._indicator_engine.calculate(history)

        decision = self._decision_engine.evaluate(
            market,
            indicators,
        )

        self._logger.info(
            "Strategy decision: %s",
            decision.signal,
        )

        return decision

    def decide(
        self,
        market: Market,
        indicators,
    ) -> Decision:
        """
        Generate a trading decision from validated inputs.
        """

        return self._decision_engine.evaluate(
            market,
            indicators,
        )
