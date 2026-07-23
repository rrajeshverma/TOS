import pytest

from indicators.calculators.ema_calculator import EmaCalculator


def test_can_create_ema_calculator():
    calculator = EmaCalculator()

    assert calculator is not None


def test_calculator_has_calculate_method():
    calculator = EmaCalculator()

    assert callable(calculator.calculate)


def test_calculate_requires_prices():
    calculator = EmaCalculator()

    with pytest.raises(ValueError):
        calculator.calculate([], period=9)


def test_calculate_rejects_none_prices():
    calculator = EmaCalculator()

    with pytest.raises(ValueError):
        calculator.calculate(None, period=9)


def test_calculate_rejects_invalid_prices():
    calculator = EmaCalculator()

    with pytest.raises(TypeError):
        calculator.calculate(object(), period=9)


def test_calculate_requires_positive_period():
    calculator = EmaCalculator()

    with pytest.raises(ValueError):
        calculator.calculate([100.0], period=0)


def test_calculate_rejects_negative_period():
    calculator = EmaCalculator()

    with pytest.raises(ValueError):
        calculator.calculate([100.0], period=-1)


def test_calculate_returns_float():
    calculator = EmaCalculator()

    result = calculator.calculate([100.0] * 9, period=9)

    assert isinstance(result, float)


def test_calculate_returns_last_price_for_constant_series():
    calculator = EmaCalculator()

    result = calculator.calculate([100.0] * 20, period=9)

    assert result == pytest.approx(100.0)


def test_calculate_is_repeatable():
    calculator = EmaCalculator()

    prices = [100.0] * 20

    first = calculator.calculate(prices, period=9)
    second = calculator.calculate(prices, period=9)

    assert first == second


def test_calculate_does_not_modify_input():
    calculator = EmaCalculator()

    prices = [100.0] * 20
    original = prices.copy()

    calculator.calculate(prices, period=9)

    assert prices == original


def test_calculate_handles_exact_period():
    calculator = EmaCalculator()

    result = calculator.calculate([100.0] * 9, period=9)

    assert isinstance(result, float)


def test_calculate_handles_large_input():
    calculator = EmaCalculator()

    result = calculator.calculate([100.0] * 1000, period=9)

    assert isinstance(result, float)


def test_calculate_returns_finite_number():
    import math

    calculator = EmaCalculator()

    result = calculator.calculate([100.0] * 20, period=9)

    assert math.isfinite(result)


def test_calculate_is_stateless():
    calculator = EmaCalculator()

    calculator.calculate([100.0] * 20, period=9)

    assert vars(calculator) == {}


def test_calculate_accepts_integer_prices():
    calculator = EmaCalculator()

    result = calculator.calculate([100] * 20, period=9)

    assert isinstance(result, float)


def test_calculate_accepts_float_prices():
    calculator = EmaCalculator()

    result = calculator.calculate([100.5] * 20, period=9)

    assert isinstance(result, float)


def test_calculate_preserves_precision():
    calculator = EmaCalculator()

    result = calculator.calculate([100.123456] * 20, period=9)

    assert result == pytest.approx(100.123456)


def test_calculate_handles_single_value_when_period_one():
    calculator = EmaCalculator()

    assert calculator.calculate([100.0], period=1) == 100.0


def test_calculate_public_api_is_stable():
    calculator = EmaCalculator()

    assert hasattr(calculator, "calculate")
