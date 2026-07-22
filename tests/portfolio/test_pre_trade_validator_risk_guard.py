from portfolio.pre_trade_validator import PreTradeValidator


class FakeRisk:

    def can_open_position(self):
        return True


class FakeRiskGuard:

    def __init__(self, allowed=True):
        self.allowed = allowed

    def can_trade(self):
        return self.allowed


def test_allows_when_risk_and_guard_allow():

    validator = PreTradeValidator(
        risk=FakeRisk(),
        risk_guard=FakeRiskGuard(True),
    )

    assert validator.validate() is True


def test_blocks_when_risk_guard_blocks():

    validator = PreTradeValidator(
        risk=FakeRisk(),
        risk_guard=FakeRiskGuard(False),
    )

    assert validator.validate() is False