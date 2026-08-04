"""
=========================================================
Trading Operating System (TOS)

Module      : Decision Engine
Version     : 2.0.0
Author      : Rajesh Varma
Description : Generates trading decisions from
              Market + IndicatorSet.
=========================================================
"""

from __future__ import annotations

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from shared.enums import (
    DecisionStatus,
)
from shared.logger import get_logger
from strategies.base_strategy import BaseStrategy
from strategies.ema_vwap_rsi_strategy import (
    EMAVWAPRSIStrategy,
)
from utils.id_generator import generate_decision_id


class DecisionEngine:
    """
    Converts StrategyResult into an immutable Decision.
    """

    def __init__(
        self,
        strategy: BaseStrategy | None = None,
    ) -> None:
        self._logger = get_logger(__name__)

        self._strategy = strategy or EMAVWAPRSIStrategy()

    def evaluate(
        self,
        market: Market,
        indicators: IndicatorSet,
    ) -> Decision:
        """
        Evaluate strategy and create a Decision.
        """

        result = self._strategy.analyze(
            market,
            indicators,
        )

        status = DecisionStatus.VALID if result.has_signal else DecisionStatus.NO_SIGNAL

        decision = Decision(
            decision_id=generate_decision_id(),
            timestamp=market.timestamp,
            market=market,
            indicator_set=indicators,
            signal=result.signal,
            status=status,
            reasons=result.reasons,
        )

        self._logger.info(
            "Decision created: %s",
            decision.signal,
        )

        return decision
