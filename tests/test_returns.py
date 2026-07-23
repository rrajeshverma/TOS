from math import isclose

from analytics.returns import Returns


def test_zero_return():
    returns = Returns()

    assert returns.calculate(100000, 100000) == 0.0


def test_positive_return():
    returns = Returns()

    assert returns.calculate(110000, 100000) == 10.0


def test_negative_return():
    returns = Returns()

    assert returns.calculate(95000, 100000) == -5.0


def test_double_capital():
    returns = Returns()

    assert returns.calculate(200000, 100000) == 100.0


def test_cumulative_return_initially_zero():
    returns = Returns()

    assert returns.cumulative_return(100000, 100000) == 0.0


def test_cumulative_return_positive():
    returns = Returns()

    assert returns.cumulative_return(125000, 100000) == 25.0


def test_cumulative_return_negative():
    returns = Returns()

    assert returns.cumulative_return(90000, 100000) == -10.0


def test_calculate_and_cumulative_are_equal():
    returns = Returns()

    assert returns.calculate(118000, 100000) == returns.cumulative_return(
        118000, 100000
    )


def test_cagr_zero_growth():
    returns = Returns()

    assert returns.cagr(100000, 100000, 5) == 0.0


def test_cagr_one_year():
    returns = Returns()

    assert isclose(
        returns.cagr(110000, 100000, 1),
        10.0,
        rel_tol=1e-6,
    )


def test_cagr_two_years():
    returns = Returns()

    result = returns.cagr(121000, 100000, 2)

    assert isclose(result, 10.0, rel_tol=1e-6)


def test_cagr_invalid_years():
    returns = Returns()

    assert returns.cagr(120000, 100000, 0) == 0.0


def test_calculate_zero_initial_value():
    returns = Returns()

    assert returns.calculate(100000, 0) == 0.0
