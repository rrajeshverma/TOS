"""
=========================================================
Trading Operating System (TOS)
Module      : Risk Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Evaluates whether a strategy decision
              is allowed to become a trade.
=========================================================
"""

from __future__ import annotations

from config.risk import (
    MAX_DAILY_LOSS,
    MAX_TRADES_PER_DAY,
)
from domain.decision import Decision
from domain.risk import Risk
from shared.enums import (
    DecisionStatus,
    Signal,
)
from shared.logger import get_logger


class RiskEngine:
    """
    Evaluates trading risk.
    """

    def __init__(self) -> None:

        self._logger = get_logger(__name__)

    def evaluate(
        self,
        decision: Decision,
        trades_today: int,
        daily_loss,
    ) -> Risk:

        reasons = []

        approved = True

        if decision.status != DecisionStatus.VALID:
            approved = False
            reasons.append("Decision not valid")

        if decision.signal == Signal.NONE:
            approved = False
            reasons.append("No trading signal")

        if trades_today >= MAX_TRADES_PER_DAY:
            approved = False
            reasons.append("Maximum trades reached")

        if daily_loss >= MAX_DAILY_LOSS:
            approved = False
            reasons.append("Daily loss limit reached")

        risk = Risk(
            decision=decision,
            approved=approved,
            reasons=tuple(reasons),
        )

        self._logger.info(
            "Risk Approved: %s",
            risk.approved,
        )

        return risk
