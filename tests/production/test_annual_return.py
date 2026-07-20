import math

from analytics.annual_return import AnnualReturn


def test_same_value():
    annual = AnnualReturn()

    assert annual.calculate(
        beginning_value=100,
        ending_value=100,
    ) == 0.0


def test_positive_return():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=100,
        ending_value=120,
    )

    assert math.isclose(
        result,
        0.20,
        rel_tol=1e-9,
    )


def test_negative_return():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=100,
        ending_value=80,
    )

    assert math.isclose(
        result,
        -0.20,
        rel_tol=1e-9,
    )


def test_double_value():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=100,
        ending_value=200,
    )

    assert math.isclose(
        result,
        1.0,
        rel_tol=1e-9,
    )


def test_half_value():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=200,
        ending_value=100,
    )

    assert math.isclose(
        result,
        -0.5,
        rel_tol=1e-9,
    )


def test_zero_beginning_value():
    annual = AnnualReturn()

    assert annual.calculate(
        beginning_value=0,
        ending_value=100,
    ) == 0.0


def test_large_return():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=100,
        ending_value=1000,
    )

    assert result == 9.0


def test_decimal_values():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=123.45,
        ending_value=150.00,
    )

    assert isinstance(
        result,
        float,
    )


def test_result_is_float():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=100,
        ending_value=101,
    )

    assert isinstance(
        result,
        float,
    )


def test_precision():
    annual = AnnualReturn()

    result = annual.calculate(
        beginning_value=250,
        ending_value=375,
    )

    assert math.isclose(
        result,
        0.5,
        rel_tol=1e-9,
    )