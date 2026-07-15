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

from domain.market import Market
from domain.indicator_set import IndicatorSet
from domain.decision import Decision

from shared.enums import (
    Signal,
    DecisionStatus,
)

from shared.logger import get_logger

from utils.id_generator import generate_decision_id


class DecisionEngine:
    """
    Generates strategy decisions.
    """

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def evaluate(
        self,
        market: Market,
        indicators: IndicatorSet,
    ) -> Decision:
        """
        Evaluate trading conditions.
        """

        signal = Signal.NONE
        status = DecisionStatus.NO_SIGNAL
        reasons = []

        # BUY CE
        if (
            market.close > indicators.ema_high
            and market.close > indicators.vwap
            and indicators.rsi > 55
        ):
            signal = Signal.BUY_CE
            status = DecisionStatus.VALID

            reasons.append("Bullish EMA breakout")
            reasons.append("Above VWAP")
            reasons.append("RSI > 55")

        # BUY PE
        elif (
            market.close < indicators.ema_low
            and market.close < indicators.vwap
            and indicators.rsi < 45
        ):
            signal = Signal.BUY_PE
            status = DecisionStatus.VALID

            reasons.append("Bearish EMA breakdown")
            reasons.append("Below VWAP")
            reasons.append("RSI < 45")

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