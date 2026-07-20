import math

from analytics.payoff_ratio import PayoffRatio


def test_zero_average_win():
    ratio = PayoffRatio()

    assert ratio.calculate(
        average_win=0,
        average_loss=100,
    ) == 0.0


def test_zero_average_loss():
    ratio = PayoffRatio()

    assert ratio.calculate(
        average_win=100,
        average_loss=0,
    ) == 0.0


def test_equal_values():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=100,
        average_loss=100,
    )

    assert math.isclose(result, 1.0)


def test_double_payoff():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=200,
        average_loss=100,
    )

    assert math.isclose(result, 2.0)


def test_half_payoff():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=100,
        average_loss=200,
    )

    assert math.isclose(result, 0.5)


def test_negative_average_loss():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=150,
        average_loss=-75,
    )

    assert math.isclose(result, 2.0)


def test_decimal_values():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=123.45,
        average_loss=61.725,
    )

    assert math.isclose(result, 2.0)


def test_large_numbers():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=100000,
        average_loss=25000,
    )

    assert math.isclose(result, 4.0)


def test_result_is_float():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=10,
        average_loss=5,
    )

    assert isinstance(result, float)


def test_precision():
    ratio = PayoffRatio()

    result = ratio.calculate(
        average_win=99.999,
        average_loss=33.333,
    )

    assert math.isclose(
        result,
        3.0,
        rel_tol=1e-9,
    )