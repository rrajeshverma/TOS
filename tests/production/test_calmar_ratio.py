import math

from analytics.calmar_ratio import CalmarRatio


def test_zero_return():
    ratio = CalmarRatio()

    assert (
        ratio.calculate(
            annual_return=0.0,
            max_drawdown=0.10,
        )
        == 0.0
    )


def test_zero_drawdown():
    ratio = CalmarRatio()

    assert (
        ratio.calculate(
            annual_return=0.20,
            max_drawdown=0.0,
        )
        == 0.0
    )


def test_positive_values():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.24,
        max_drawdown=0.12,
    )

    assert math.isclose(
        result,
        2.0,
        rel_tol=1e-9,
    )


def test_negative_return():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=-0.12,
        max_drawdown=0.06,
    )

    assert math.isclose(
        result,
        -2.0,
        rel_tol=1e-9,
    )


def test_small_drawdown():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.15,
        max_drawdown=0.03,
    )

    assert math.isclose(
        result,
        5.0,
        rel_tol=1e-9,
    )


def test_large_drawdown():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.15,
        max_drawdown=0.30,
    )

    assert math.isclose(
        result,
        0.5,
        rel_tol=1e-9,
    )


def test_negative_drawdown():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.20,
        max_drawdown=-0.10,
    )

    assert math.isclose(
        result,
        2.0,
        rel_tol=1e-9,
    )


def test_result_is_float():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.18,
        max_drawdown=0.09,
    )

    assert isinstance(
        result,
        float,
    )


def test_precision():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.123456,
        max_drawdown=0.061728,
    )

    assert math.isclose(
        result,
        2.0,
        rel_tol=1e-9,
    )


def test_equal_return_and_drawdown():
    ratio = CalmarRatio()

    result = ratio.calculate(
        annual_return=0.25,
        max_drawdown=0.25,
    )

    assert math.isclose(
        result,
        1.0,
        rel_tol=1e-9,
    )
