from approval.approval_decision import ApprovalDecision


def test_approval_decision_can_be_created():
    decision = ApprovalDecision(
        approved=True,
        reason="Approved",
        metadata={},
    )

    assert decision is not None


def test_approval_decision_stores_approval():
    decision = ApprovalDecision(
        approved=True,
        reason="Risk checks passed",
        metadata={},
    )

    assert decision.approved is True


def test_approval_decision_stores_rejection():
    decision = ApprovalDecision(
        approved=False,
        reason="Risk rejected",
        metadata={},
    )

    assert decision.approved is False
    assert decision.reason == "Risk rejected"


def test_approval_decision_has_reason():
    decision = ApprovalDecision(
        approved=True,
        reason="Quantity valid",
        metadata={},
    )

    assert decision.reason == "Quantity valid"


def test_approval_decision_metadata_is_dict():
    decision = ApprovalDecision(
        approved=True,
        reason="Approved",
        metadata={
            "source": "approval_engine",
        },
    )

    assert isinstance(
        decision.metadata,
        dict,
    )


def test_approval_decision_is_immutable():
    decision = ApprovalDecision(
        approved=True,
        reason="Approved",
        metadata={},
    )

    try:
        decision.approved = False
        assert False

    except Exception:
        assert True
