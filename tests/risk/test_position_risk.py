from risk.position_risk import PositionRiskCalculator


def test_position_risk_calculator_can_be_created():
    calculator = PositionRiskCalculator()

    assert calculator is not None


def test_calculates_position_value():
    calculator = PositionRiskCalculator()

    result = calculator.calculate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
            "stop_loss": 19900,
        },
        capital=500000,
    )

    assert result["position_value"] == 200000


def test_calculates_risk_amount():
    calculator = PositionRiskCalculator()

    result = calculator.calculate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
            "stop_loss": 19900,
        },
        capital=500000,
    )

    assert result["risk_amount"] == 1000


def test_calculates_risk_percentage():
    calculator = PositionRiskCalculator()

    result = calculator.calculate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
            "stop_loss": 19900,
        },
        capital=500000,
    )

    assert result["risk_percentage"] == 0.2


def test_missing_stop_loss_defaults_to_zero_risk():
    calculator = PositionRiskCalculator()

    result = calculator.calculate(
        position={
            "symbol": "NIFTY",
            "quantity": 10,
            "price": 20000,
        },
        capital=500000,
    )

    assert result["risk_amount"] == 0


def test_rejects_invalid_capital():
    calculator = PositionRiskCalculator()

    try:
        calculator.calculate(
            position={
                "quantity": 10,
                "price": 20000,
            },
            capital=0,
        )

        assert False

    except ValueError:
        assert True
