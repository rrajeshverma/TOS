"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Quality Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Evaluates whether a strategy decision
              meets the minimum quality requirements
              before risk assessment.
=========================================================
"""

from __future__ import annotations

from domain.decision import Decision
from domain.trade_quality import TradeQuality
from shared.enums import DecisionStatus, Signal
from shared.logger import get_logger

from config.risk import MAX_TRADES_PER_DAY


class TradeQualityEngine:
    """
    Evaluates trade quality before risk assessment.
    """

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def evaluate(
        self,
        decision: Decision,
        trades_today: int,
    ) -> TradeQuality:
        """
        Evaluate whether the strategy decision
        is good enough to continue.
        """

        approved = True
        reasons: list[str] = []

        if decision.status != DecisionStatus.VALID:
            approved = False
            reasons.append("Decision not valid")

        if decision.signal == Signal.NONE:
            approved = False
            reasons.append("No trading signal")

        if trades_today >= MAX_TRADES_PER_DAY:
            approved = False
            reasons.append("Maximum daily trades reached")

        quality = TradeQuality(
            approved=approved,
            reasons=tuple(reasons),
        )

        self._logger.info(
            "Trade Quality Approved: %s",
            quality.approved,
        )

        return quality
