"""
TOS Risk Engine

Central risk decision coordinator.
"""

from __future__ import annotations

from risk.exposure_limit import ExposureLimitGuard
from risk.loss_guard import LossGuard
from risk.position_risk import PositionRiskCalculator
from risk.risk_decision import RiskDecision


class RiskEngine:
    """
    Evaluates trade risk.
    """

    def __init__(
        self,
        max_exposure_percentage: float = 100,
        max_loss: float = 10000,
    ) -> None:
        self.position_risk = PositionRiskCalculator()

        self.exposure_guard = ExposureLimitGuard(max_exposure_percentage)

        self.loss_guard = LossGuard(max_loss)

    def evaluate(
        self,
        position: dict,
        exposure: float,
        capital: float,
        current_loss: float,
    ) -> RiskDecision:
        """
        Evaluate complete risk.
        """

        position_result = self.position_risk.calculate(
            position,
            capital,
        )

        exposure_result = self.exposure_guard.check(
            exposure,
            capital,
        )

        loss_result = self.loss_guard.check(
            current_loss,
        )

        approved = exposure_result["approved"] and loss_result["approved"]

        reason = "Approved"

        if not exposure_result["approved"]:
            reason = "Exposure limit exceeded"

        elif not loss_result["approved"]:
            reason = "Loss limit exceeded"

        return RiskDecision(
            approved=approved,
            reason=reason,
            risk_score=int(position_result["risk_percentage"]),
            metadata={
                "position": position_result,
                "exposure": exposure_result,
                "loss": loss_result,
            },
        )
