import math

import pytest

from analytics.sharpe_ratio import SharpeRatio


def test_empty_returns():
    sharpe = SharpeRatio()

    assert sharpe.calculate([]) == 0.0


def test_single_return():
    sharpe = SharpeRatio()

    assert sharpe.calculate([0.05]) == 0.0


def test_constant_returns():
    sharpe = SharpeRatio()

    assert sharpe.calculate([0.01] * 10) == 0.0


def test_positive_returns():
    sharpe = SharpeRatio()

    returns = [
        0.01,
        0.02,
        0.03,
        0.02,
        0.01,
    ]

    result = sharpe.calculate(returns)

    assert result > 0


def test_negative_returns():
    sharpe = SharpeRatio()

    returns = [
        -0.01,
        -0.02,
        -0.01,
        -0.03,
    ]

    result = sharpe.calculate(returns)

    assert result < 0


def test_mixed_returns():
    sharpe = SharpeRatio()

    returns = [
        0.02,
        -0.01,
        0.03,
        -0.02,
        0.01,
    ]

    assert isinstance(
        sharpe.calculate(returns),
        float,
    )


def test_zero_mean_returns():
    sharpe = SharpeRatio()

    returns = [
        0.01,
        -0.01,
        0.01,
        -0.01,
    ]

    assert math.isclose(
        sharpe.calculate(returns),
        0.0,
        abs_tol=1e-9,
    )


def test_decimal_returns():
    sharpe = SharpeRatio()

    returns = [
        0.0125,
        0.0185,
        -0.0042,
        0.0091,
    ]

    assert isinstance(
        sharpe.calculate(returns),
        float,
    )


def test_large_dataset():
    sharpe = SharpeRatio()

    returns = [0.01] * 500 + [-0.005] * 500

    assert isinstance(
        sharpe.calculate(returns),
        float,
    )


def test_custom_risk_free_rate():
    sharpe = SharpeRatio()

    returns = [
        0.05,
        0.06,
        0.04,
        0.05,
    ]

    result = sharpe.calculate(
        returns,
        risk_free_rate=0.02,
    )

    assert isinstance(result, float)


def test_zero_volatility_with_risk_free():
    sharpe = SharpeRatio()

    returns = [0.02] * 20

    assert (
        sharpe.calculate(
            returns,
            risk_free_rate=0.02,
        )
        == 0.0
    )


def test_result_is_float():
    sharpe = SharpeRatio()

    result = sharpe.calculate(
        [0.01, 0.02, -0.01],
    )

    assert isinstance(result, float)
