"""
=========================================================
Trading Operating System (TOS)
Module      : Decision Engine
Version     : 1.0.0
Author       : Rajesh Varma
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
    Signal,
)
from shared.logger import get_logger
from strategies.ema_vwap_rsi_strategy import (
    EMAVWAPRSIStrategy,
)
from utils.id_generator import generate_decision_id


class DecisionEngine:
    """
    Generates strategy decisions.
    """

    from strategies.base_strategy import BaseStrategy

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
        Evaluate trading conditions.
        """

        signal = self._strategy.generate_signal(
            market,
            indicators,
        )

        status = (
            DecisionStatus.VALID if signal != Signal.NONE else DecisionStatus.NO_SIGNAL
        )

        reasons = []

        if signal == Signal.BUY_CE:
            reasons.extend(
                (
                    "Bullish EMA breakout",
                    "Above VWAP",
                    "RSI > 55",
                )
            )

        elif signal == Signal.BUY_PE:
            reasons.extend(
                (
                    "Bearish EMA breakdown",
                    "Below VWAP",
                    "RSI < 45",
                )
            )

        decision = Decision(
            decision_id=generate_decision_id(),
            timestamp=market.timestamp,
            market=market,
            indicator_set=indicators,
            signal=signal,
            status=status,
            reasons=tuple(reasons),
        )

        self._logger.info(
            "Decision created: %s",
            decision.signal,
        )

        return decision
