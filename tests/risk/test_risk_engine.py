from risk.risk_engine import RiskEngine


def test_risk_engine_can_be_created():

    engine = RiskEngine()

    assert engine is not None


def test_risk_engine_approves_safe_trade():

    engine = RiskEngine(
        max_exposure_percentage=60,
        max_loss=10000,
    )

    decision = engine.evaluate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
            "stop_loss": 19900,
        },
        exposure=200000,
        capital=500000,
        current_loss=5000,
    )

    assert decision.approved is True


def test_risk_engine_rejects_high_exposure():

    engine = RiskEngine(
        max_exposure_percentage=50,
        max_loss=10000,
    )

    decision = engine.evaluate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
        },
        exposure=400000,
        capital=500000,
        current_loss=1000,
    )

    assert decision.approved is False


def test_risk_engine_rejects_high_loss():

    engine = RiskEngine(
        max_loss=5000,
    )

    decision = engine.evaluate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
        },
        exposure=100000,
        capital=500000,
        current_loss=10000,
    )

    assert decision.approved is False


def test_risk_engine_contains_metadata():

    engine = RiskEngine()

    decision = engine.evaluate(
        position={
            "symbol": "NIFTY",
            "quantity": 1,
            "price": 20000,
        },
        exposure=20000,
        capital=500000,
        current_loss=0,
    )

    assert isinstance(
        decision.metadata,
        dict,
    )


def test_risk_engine_returns_risk_score():

    engine = RiskEngine()

    decision = engine.evaluate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
            "stop_loss": 19900,
        },
        exposure=200000,
        capital=500000,
        current_loss=0,
    )

    assert decision.risk_score >= 0
