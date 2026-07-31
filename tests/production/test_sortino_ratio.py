import math

from analytics.sortino_ratio import SortinoRatio


def test_empty_returns():
    ratio = SortinoRatio()

    assert ratio.calculate([]) == 0.0


def test_single_return():
    ratio = SortinoRatio()

    assert ratio.calculate([0.05]) == 0.0


def test_all_positive_returns():
    ratio = SortinoRatio()

    returns = [
        0.01,
        0.02,
        0.03,
        0.04,
    ]

    assert ratio.calculate(returns) == 0.0


def test_all_negative_returns():
    ratio = SortinoRatio()

    returns = [
        -0.01,
        -0.02,
        -0.03,
        -0.01,
    ]

    assert ratio.calculate(returns) < 0


def test_mixed_returns():
    ratio = SortinoRatio()

    returns = [
        0.02,
        -0.01,
        0.03,
        -0.02,
        0.01,
    ]

    assert isinstance(
        ratio.calculate(returns),
        float,
    )


def test_zero_mean_returns():
    ratio = SortinoRatio()

    returns = [
        0.01,
        -0.01,
        0.01,
        -0.01,
    ]

    assert math.isclose(
        ratio.calculate(returns),
        0.0,
        abs_tol=1e-9,
    )


def test_decimal_returns():
    ratio = SortinoRatio()

    returns = [
        0.0125,
        0.0185,
        -0.0042,
        0.0091,
    ]

    assert isinstance(
        ratio.calculate(returns),
        float,
    )


def test_large_dataset():
    ratio = SortinoRatio()

    returns = [0.01] * 500 + [-0.005] * 500

    assert isinstance(
        ratio.calculate(returns),
        float,
    )


def test_custom_risk_free_rate():
    ratio = SortinoRatio()

    returns = [
        0.05,
        0.06,
        0.04,
        0.05,
    ]

    result = ratio.calculate(
        returns,
        risk_free_rate=0.02,
    )

    assert isinstance(
        result,
        float,
    )


def test_result_is_float():
    ratio = SortinoRatio()

    result = ratio.calculate(
        [0.01, -0.02, 0.03],
    )

    assert isinstance(
        result,
        float,
    )
