from portfolio.exposure import ExposureCalculator


def test_calculator_can_be_created():

    calculator = ExposureCalculator()

    assert calculator is not None


def test_calculates_total_exposure():

    calculator = ExposureCalculator()

    result = calculator.calculate(
        positions=[
            {
                "symbol": "NIFTY",
                "quantity": 10,
                "price": 20000,
            }
        ]
    )

    assert (
        result["total_exposure"]
        == 200000
    )


def test_calculates_multiple_positions():

    calculator = ExposureCalculator()

    result = calculator.calculate(
        positions=[
            {
                "symbol": "NIFTY",
                "quantity": 10,
                "price": 20000,
            },
            {
                "symbol": "BANKNIFTY",
                "quantity": 5,
                "price": 40000,
            },
        ]
    )

    assert (
        result["total_exposure"]
        == 400000
    )


def test_calculates_exposure_percentage():

    calculator = ExposureCalculator()

    result = calculator.calculate(
        positions=[
            {
                "symbol": "NIFTY",
                "quantity": 10,
                "price": 20000,
            }
        ],
        capital=500000,
    )

    assert (
        result["exposure_percentage"]
        == 40
    )


def test_empty_positions_return_zero():

    calculator = ExposureCalculator()

    result = calculator.calculate(
        positions=[]
    )

    assert (
        result["total_exposure"]
        == 0
    )


def test_rejects_negative_capital():

    calculator = ExposureCalculator()

    try:
        calculator.calculate(
            positions=[],
            capital=-1,
        )

        assert False

    except ValueError:
        assert True
