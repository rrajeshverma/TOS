from unittest.mock import Mock

from approval.approval_decision import ApprovalDecision
from execution.execution_gate import ExecutionGate


def create_decision(
    approved=True,
    reason="",
):
    return ApprovalDecision(
        approved=approved,
        reason=reason,
        metadata={},
    )


def test_can_execute_returns_true_for_approved():
    decision = create_decision(
        approved=True,
    )

    gate = ExecutionGate(
        decision,
    )

    assert gate.can_execute() is True


def test_can_execute_returns_false_for_rejected():
    decision = create_decision(
        approved=False,
        reason="Risk failed",
    )

    gate = ExecutionGate(
        decision,
    )

    assert gate.can_execute() is False


def test_decision_property_returns_same_object():
    decision = create_decision()

    gate = ExecutionGate(
        decision,
    )

    assert gate.decision is decision


def test_multiple_calls_are_consistent():
    decision = create_decision()

    gate = ExecutionGate(
        decision,
    )

    assert gate.can_execute()
    assert gate.can_execute()
    assert gate.can_execute()


def test_gate_does_not_modify_decision():
    decision = create_decision(
        approved=True,
        reason="Approved",
    )

    gate = ExecutionGate(
        decision,
    )

    gate.can_execute()

    assert decision.approved is True
    assert decision.reason == "Approved"


def test_false_decision_remains_false():
    decision = create_decision(
        approved=False,
        reason="Rejected",
    )

    gate = ExecutionGate(
        decision,
    )

    gate.can_execute()

    assert decision.approved is False


def test_gate_accepts_mock_decision():
    decision = Mock()
    decision.approved = True

    gate = ExecutionGate(
        decision,
    )

    assert gate.can_execute() is True


def test_gate_accepts_mock_rejected_decision():
    decision = Mock()
    decision.approved = False

    gate = ExecutionGate(
        decision,
    )

    assert gate.can_execute() is False
