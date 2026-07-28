from strategies.context import StrategyContext


def test_context_can_be_created():

    context = StrategyContext(
        market="MARKET",
        indicators="INDICATORS",
        positions="POSITIONS",
        risk_state="RISK",
        account="ACCOUNT",
    )

    assert context.market == "MARKET"
    assert context.indicators == "INDICATORS"
    assert context.positions == "POSITIONS"
    assert context.risk_state == "RISK"
    assert context.account == "ACCOUNT"


def test_context_is_immutable():

    context = StrategyContext(
        market="MARKET",
        indicators="INDICATORS",
        positions="POSITIONS",
        risk_state="RISK",
        account="ACCOUNT",
    )

    try:
        context.market = "NEW"
        assert False
    except Exception:
        assert True


def test_context_requires_market():

    try:
        StrategyContext(
            market=None,
            indicators="INDICATORS",
            positions="POSITIONS",
            risk_state="RISK",
            account="ACCOUNT",
        )
        assert False

    except ValueError:
        assert True


def test_context_requires_indicators():

    try:
        StrategyContext(
            market="MARKET",
            indicators=None,
            positions="POSITIONS",
            risk_state="RISK",
            account="ACCOUNT",
        )
        assert False

    except ValueError:
        assert True


def test_context_requires_positions():

    try:
        StrategyContext(
            market="MARKET",
            indicators="INDICATORS",
            positions=None,
            risk_state="RISK",
            account="ACCOUNT",
        )
        assert False

    except ValueError:
        assert True


def test_context_requires_account():

    try:
        StrategyContext(
            market="MARKET",
            indicators="INDICATORS",
            positions="POSITIONS",
            risk_state="RISK",
            account=None,
        )
        assert False

    except ValueError:
        assert True
