import math

from analytics.volatility import Volatility


def test_empty_returns():
    volatility = Volatility()

    assert volatility.calculate([]) == 0.0


def test_single_return():
    volatility = Volatility()

    assert volatility.calculate([0.05]) == 0.0


def test_constant_returns():
    volatility = Volatility()

    returns = [0.02] * 10

    assert volatility.calculate(returns) == 0.0


def test_positive_returns():
    volatility = Volatility()

    returns = [
        0.01,
        0.02,
        0.03,
        0.02,
        0.01,
    ]

    assert volatility.calculate(returns) > 0


def test_negative_returns():
    volatility = Volatility()

    returns = [
        -0.01,
        -0.02,
        -0.01,
        -0.03,
    ]

    assert volatility.calculate(returns) > 0


def test_mixed_returns():
    volatility = Volatility()

    returns = [
        0.02,
        -0.01,
        0.03,
        -0.02,
        0.01,
    ]

    assert volatility.calculate(returns) > 0


def test_decimal_returns():
    volatility = Volatility()

    returns = [
        0.0125,
        0.0185,
        -0.0042,
        0.0091,
    ]

    assert isinstance(
        volatility.calculate(returns),
        float,
    )


def test_large_dataset():
    volatility = Volatility()

    returns = [0.01] * 500 + [-0.005] * 500

    assert volatility.calculate(returns) > 0


def test_known_standard_deviation():
    volatility = Volatility()

    returns = [
        1.0,
        2.0,
        3.0,
    ]

    result = volatility.calculate(returns)

    assert math.isclose(
        result,
        1.0,
        rel_tol=1e-9,
    )


def test_result_is_float():
    volatility = Volatility()

    result = volatility.calculate(
        [0.01, 0.02, -0.01],
    )

    assert isinstance(
        result,
        float,
    )