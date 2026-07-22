import math

from analytics.expected_shortfall import ExpectedShortfall


def test_empty_returns():
    es = ExpectedShortfall()

    assert es.calculate([]) == 0.0


def test_single_return():
    es = ExpectedShortfall()

    assert es.calculate([-0.05]) == 0.05


def test_all_positive_returns():
    es = ExpectedShortfall()

    assert es.calculate([0.01, 0.02, 0.03]) == 0.0


def test_all_negative_returns():
    es = ExpectedShortfall()

    returns = [-0.01, -0.02, -0.03, -0.04]

    assert math.isclose(
        es.calculate(returns),
        0.04,
    )


def test_mixed_returns():
    es = ExpectedShortfall()

    returns = [
        0.02,
        -0.01,
        -0.03,
        0.01,
        -0.02,
    ]

    assert es.calculate(returns) > 0


def test_custom_confidence():
    es = ExpectedShortfall()

    returns = [
        -0.05,
        -0.04,
        -0.03,
        -0.02,
        -0.01,
    ]

    assert (
        es.calculate(
            returns,
            confidence=0.99,
        )
        > 0
    )


def test_result_is_float():
    es = ExpectedShortfall()

    result = es.calculate(
        [0.01, -0.02],
    )

    assert isinstance(result, float)


def test_decimal_returns():
    es = ExpectedShortfall()

    result = es.calculate(
        [
            0.0123,
            -0.0456,
            0.0345,
        ],
    )

    assert isinstance(result, float)


def test_large_dataset():
    es = ExpectedShortfall()

    returns = [-0.01] * 1000

    assert es.calculate(returns) == 0.01


def test_zero_losses():
    es = ExpectedShortfall()

    assert es.calculate([0.0] * 50) == 0.0
