import math

from analytics.value_at_risk import ValueAtRisk


def test_empty_returns():
    var = ValueAtRisk()

    assert var.calculate([]) == 0.0


def test_single_return():
    var = ValueAtRisk()

    assert var.calculate([-0.05]) == 0.05


def test_all_positive_returns():
    var = ValueAtRisk()

    returns = [
        0.01,
        0.02,
        0.03,
        0.04,
    ]

    assert var.calculate(returns) == 0.0


def test_all_negative_returns():
    var = ValueAtRisk()

    returns = [
        -0.01,
        -0.02,
        -0.03,
        -0.04,
    ]

    assert math.isclose(
        var.calculate(returns),
        0.04,
    )


def test_mixed_returns():
    var = ValueAtRisk()

    returns = [
        0.02,
        -0.01,
        0.01,
        -0.03,
        -0.02,
    ]

    assert var.calculate(returns) > 0


def test_custom_confidence():
    var = ValueAtRisk()

    returns = [
        -0.05,
        -0.04,
        -0.03,
        -0.02,
        -0.01,
    ]

    result = var.calculate(
        returns,
        confidence=0.99,
    )

    assert result > 0


def test_result_is_float():
    var = ValueAtRisk()

    result = var.calculate(
        [0.01, -0.02],
    )

    assert isinstance(result, float)


def test_decimal_returns():
    var = ValueAtRisk()

    result = var.calculate(
        [
            0.0123,
            -0.0456,
            0.0345,
        ],
    )

    assert isinstance(result, float)


def test_large_dataset():
    var = ValueAtRisk()

    returns = [-0.01] * 1000

    assert var.calculate(returns) == 0.01


def test_zero_losses():
    var = ValueAtRisk()

    returns = [0.0] * 50

    assert var.calculate(returns) == 0.0