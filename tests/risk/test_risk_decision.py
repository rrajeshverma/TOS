from risk.risk_decision import RiskDecision


def test_risk_decision_can_be_created():
    decision = RiskDecision(
        approved=True,
        reason="Within limits",
        risk_score=20,
        metadata={},
    )

    assert decision is not None


def test_risk_decision_stores_approval():
    decision = RiskDecision(
        approved=True,
        reason="Approved",
        risk_score=10,
        metadata={},
    )

    assert decision.approved is True


def test_risk_decision_stores_rejection():
    decision = RiskDecision(
        approved=False,
        reason="Exposure exceeded",
        risk_score=90,
        metadata={},
    )

    assert decision.approved is False
    assert decision.reason == "Exposure exceeded"


def test_risk_decision_has_risk_score():
    decision = RiskDecision(
        approved=True,
        reason="Safe",
        risk_score=25,
        metadata={},
    )

    assert decision.risk_score == 25


def test_risk_decision_metadata_is_dict():
    decision = RiskDecision(
        approved=True,
        reason="Safe",
        risk_score=25,
        metadata={"source": "risk_engine"},
    )

    assert isinstance(
        decision.metadata,
        dict,
    )


def test_risk_decision_is_immutable():
    decision = RiskDecision(
        approved=True,
        reason="Safe",
        risk_score=25,
        metadata={},
    )

    try:
        decision.approved = False
        assert False

    except Exception:
        assert True
