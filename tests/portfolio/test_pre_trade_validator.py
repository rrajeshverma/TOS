from portfolio.pre_trade_validator import PreTradeValidator


class FakeRisk:
    def __init__(self, allowed=True):
        self.allowed = allowed

    def can_open_position(self):
        return self.allowed


def test_allows_trade_when_risk_available():
    validator = PreTradeValidator(risk=FakeRisk(True))

    assert validator.validate() is True


def test_blocks_trade_when_risk_exhausted():
    validator = PreTradeValidator(risk=FakeRisk(False))

    assert validator.validate() is False
