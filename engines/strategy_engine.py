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

from collections.abc import Mapping
from typing import Any

from domain.decision import Decision
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

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

        self._market_engine = MarketEngine()
        self._indicator_engine = IndicatorEngine()
        self._decision_engine = DecisionEngine()

    def evaluate(
        self,
        raw_market: Mapping[str, Any],
        history,
    ) -> Decision:
        """
        Execute complete strategy pipeline.
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
