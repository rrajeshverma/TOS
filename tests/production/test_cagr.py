import math

from analytics.cagr import CAGR


def test_same_value():
    cagr = CAGR()

    assert (
        cagr.calculate(
            beginning_value=100,
            ending_value=100,
            years=5,
        )
        == 0.0
    )


def test_one_year_growth():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=100,
        ending_value=120,
        years=1,
    )

    assert math.isclose(
        result,
        0.20,
        rel_tol=1e-9,
    )


def test_two_year_growth():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=100,
        ending_value=144,
        years=2,
    )

    assert math.isclose(
        result,
        0.20,
        rel_tol=1e-9,
    )


def test_loss():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=100,
        ending_value=81,
        years=2,
    )

    assert math.isclose(
        result,
        -0.10,
        rel_tol=1e-9,
    )


def test_zero_beginning_value():
    cagr = CAGR()

    assert (
        cagr.calculate(
            beginning_value=0,
            ending_value=100,
            years=5,
        )
        == 0.0
    )


def test_zero_years():
    cagr = CAGR()

    assert (
        cagr.calculate(
            beginning_value=100,
            ending_value=120,
            years=0,
        )
        == 0.0
    )


def test_fractional_years():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=100,
        ending_value=110,
        years=0.5,
    )

    assert result > 0


def test_large_growth():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=100,
        ending_value=1000,
        years=10,
    )

    assert result > 0


def test_result_is_float():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=100,
        ending_value=200,
        years=5,
    )

    assert isinstance(
        result,
        float,
    )


def test_precision():
    cagr = CAGR()

    result = cagr.calculate(
        beginning_value=250,
        ending_value=500,
        years=5,
    )

    assert math.isclose(
        result,
        0.1486983549970351,
        rel_tol=1e-9,
    )
