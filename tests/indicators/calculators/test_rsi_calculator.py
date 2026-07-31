import pytest

from indicators.calculators.rsi_calculator import RsiCalculator


def test_can_create_rsi_calculator():
    assert RsiCalculator() is not None


def test_has_calculate_method():
    calc = RsiCalculator()
    assert callable(calc.calculate)


def test_rejects_none_prices():
    calc = RsiCalculator()

    with pytest.raises(ValueError):
        calc.calculate(None, period=14)


def test_rejects_empty_prices():
    calc = RsiCalculator()

    with pytest.raises(ValueError):
        calc.calculate([], period=14)


def test_rejects_invalid_period():
    calc = RsiCalculator()

    with pytest.raises(ValueError):
        calc.calculate([100.0], period=0)


def test_returns_float():
    calc = RsiCalculator()

    result = calc.calculate([100.0] * 20, period=14)

    assert isinstance(result, float)


def test_constant_series_returns_valid_rsi():
    calc = RsiCalculator()

    result = calc.calculate([100.0] * 20, period=14)

    assert 0.0 <= result <= 100.0


def test_calculate_is_repeatable():
    calc = RsiCalculator()

    prices = [100.0] * 20

    assert calc.calculate(prices, 14) == calc.calculate(prices, 14)


def test_calculator_is_stateless():
    calc = RsiCalculator()

    calc.calculate([100.0] * 20, 14)

    assert vars(calc) == {}


def test_constant_prices_return_50():
    calc = RsiCalculator()

    assert calc.calculate([100.0] * 20, 14) == pytest.approx(50.0)


def test_rsi_is_between_0_and_100():
    calc = RsiCalculator()

    rsi = calc.calculate([10, 20, 30, 40, 50], 14)

    assert 0.0 <= rsi <= 100.0


def test_period_one_returns_valid_value():
    calc = RsiCalculator()

    rsi = calc.calculate([100.0], 1)

    assert 0.0 <= rsi <= 100.0


def test_repeatable():
    calc = RsiCalculator()

    prices = [100.0] * 20

    assert calc.calculate(prices, 14) == calc.calculate(prices, 14)


def test_rsi_never_negative():
    calc = RsiCalculator()

    assert calc.calculate([10, 20, 30], 3) >= 0.0


def test_rsi_never_exceeds_100():
    calc = RsiCalculator()

    assert calc.calculate([10, 20, 30], 3) <= 100.0


def test_accepts_integer_prices():
    calc = RsiCalculator()

    assert isinstance(calc.calculate([1, 2, 3, 4], 3), float)


def test_accepts_float_prices():
    calc = RsiCalculator()

    assert isinstance(calc.calculate([1.1, 2.2, 3.3], 3), float)


def test_does_not_modify_input():
    calc = RsiCalculator()

    prices = [10, 20, 30]
    original = prices.copy()

    calc.calculate(prices, 3)

    assert prices == original
