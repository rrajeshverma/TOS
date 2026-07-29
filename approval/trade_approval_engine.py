"""
TOS Trade Approval Engine

Coordinates order validation and risk approval.
"""

from __future__ import annotations

from approval.approval_decision import ApprovalDecision
from approval.order_validator import OrderValidator


class TradeApprovalEngine:
    """
    Approves or rejects trade requests.
    """

    def __init__(
        self,
        validator=None,
    ) -> None:
        self.validator = validator or OrderValidator()

    def approve(
        self,
        request,
        risk_decision,
    ) -> ApprovalDecision:
        """
        Evaluate trade approval.
        """

        validation = self.validator.validate(request)

        if not validation["valid"]:
            return ApprovalDecision(
                approved=False,
                reason="; ".join(validation["errors"]),
                metadata={
                    "validation": validation,
                },
            )

        if not risk_decision.approved:
            return ApprovalDecision(
                approved=False,
                reason=risk_decision.reason,
                metadata={
                    "risk": risk_decision,
                },
            )

        return ApprovalDecision(
            approved=True,
            reason="Trade approved",
            metadata={
                "validation": validation,
                "risk": risk_decision,
            },
        )
