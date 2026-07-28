from strategies.decision import StrategyDecision


def test_decision_can_be_created():

    decision = StrategyDecision(
        strategy="NIFTY_ORB",
        signal="BUY",
        confidence=85,
        metadata={},
    )

    assert decision.strategy == "NIFTY_ORB"
    assert decision.signal == "BUY"
    assert decision.confidence == 85



def test_decision_contains_metadata():

    decision = StrategyDecision(
        strategy="NIFTY_ORB",
        signal="BUY",
        confidence=85,
        metadata={
            "price": 24510,
        },
    )

    assert (
        decision.metadata["price"]
        == 24510
    )



def test_decision_is_immutable():

    decision = StrategyDecision(
        strategy="NIFTY_ORB",
        signal="BUY",
        confidence=85,
        metadata={},
    )

    try:
        decision.signal = "SELL"
        assert False

    except Exception:
        assert True



def test_decision_requires_strategy():

    try:
        StrategyDecision(
            strategy=None,
            signal="BUY",
            confidence=85,
            metadata={},
        )

        assert False

    except ValueError:
        assert True



def test_decision_requires_signal():

    try:
        StrategyDecision(
            strategy="NIFTY_ORB",
            signal=None,
            confidence=85,
            metadata={},
        )

        assert False

    except ValueError:
        assert True



def test_decision_confidence_range():

    try:
        StrategyDecision(
            strategy="NIFTY_ORB",
            signal="BUY",
            confidence=120,
            metadata={},
        )

        assert False

    except ValueError:
        assert True
