"""
Execution Gate

Final safety check before an order is executed.
"""

from approval.approval_decision import ApprovalDecision


class ExecutionGate:
    """
    Prevents execution unless a trade has been approved.
    """

    def __init__(
        self,
        decision: ApprovalDecision,
    ) -> None:
        self._decision = decision

    def can_execute(self) -> bool:
        """
        Returns True only when the approval decision allows execution.
        """
        return self._decision.approved

    @property
    def decision(self) -> ApprovalDecision:
        return self._decision
