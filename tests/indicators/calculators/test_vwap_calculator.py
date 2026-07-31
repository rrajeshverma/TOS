import pytest

from indicators.calculators.vwap_calculator import VwapCalculator


def test_can_create_vwap_calculator():
    assert VwapCalculator() is not None


def test_has_calculate_method():
    calc = VwapCalculator()
    assert callable(calc.calculate)


def test_rejects_none_prices():
    calc = VwapCalculator()

    with pytest.raises(ValueError):
        calc.calculate(None, None)


def test_rejects_empty_prices():
    calc = VwapCalculator()

    with pytest.raises(ValueError):
        calc.calculate([], [])


def test_rejects_length_mismatch():
    calc = VwapCalculator()

    with pytest.raises(ValueError):
        calc.calculate([1, 2], [100])


def test_returns_float():
    calc = VwapCalculator()

    result = calc.calculate([100.0] * 5, [1000] * 5)

    assert isinstance(result, float)


def test_repeatable():
    calc = VwapCalculator()

    prices = [100.0] * 5
    volumes = [1000] * 5

    assert calc.calculate(prices, volumes) == calc.calculate(prices, volumes)


def test_stateless():
    calc = VwapCalculator()

    calc.calculate([100.0], [100])

    assert vars(calc) == {}
