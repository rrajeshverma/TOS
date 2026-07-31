from approval.trade_approval_engine import TradeApprovalEngine
from approval.trade_request import TradeRequest
from risk.risk_decision import RiskDecision


def create_request():
    return TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )


def approved_risk():
    return RiskDecision(
        approved=True,
        reason="Risk OK",
        risk_score=20,
        metadata={},
    )


def rejected_risk():
    return RiskDecision(
        approved=False,
        reason="Risk rejected",
        risk_score=90,
        metadata={},
    )


def test_engine_can_be_created():
    engine = TradeApprovalEngine()

    assert engine is not None


def test_valid_trade_is_approved():
    engine = TradeApprovalEngine()

    result = engine.approve(
        create_request(),
        approved_risk(),
    )

    assert result.approved is True


def test_rejected_risk_blocks_trade():
    engine = TradeApprovalEngine()

    result = engine.approve(
        create_request(),
        rejected_risk(),
    )

    assert result.approved is False


def test_invalid_order_blocks_trade():
    engine = TradeApprovalEngine()

    request = TradeRequest(
        symbol="",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    result = engine.approve(
        request,
        approved_risk(),
    )

    assert result.approved is False


def test_approval_contains_metadata():
    engine = TradeApprovalEngine()

    result = engine.approve(
        create_request(),
        approved_risk(),
    )

    assert isinstance(
        result.metadata,
        dict,
    )


def test_approval_reason_is_present():
    engine = TradeApprovalEngine()

    result = engine.approve(
        create_request(),
        approved_risk(),
    )

    assert result.reason != ""
