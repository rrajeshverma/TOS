import pytest

from indicators.calculators.vwap_calculator import VwapCalculator


def test_constant_price_returns_same_price():
    calc = VwapCalculator()

    assert calc.calculate([100] * 10, [1000] * 10) == pytest.approx(100.0)


def test_result_between_min_and_max():
    calc = VwapCalculator()

    prices = [100, 105, 110]
    volumes = [100, 100, 100]

    result = calc.calculate(prices, volumes)

    assert min(prices) <= result <= max(prices)


def test_accepts_integer_prices():
    calc = VwapCalculator()

    assert isinstance(calc.calculate([100, 101], [10, 20]), float)


def test_accepts_float_prices():
    calc = VwapCalculator()

    assert isinstance(calc.calculate([100.5, 101.5], [10, 20]), float)


def test_does_not_modify_inputs():
    calc = VwapCalculator()

    prices = [100, 101]
    volumes = [10, 20]

    p = prices.copy()
    v = volumes.copy()

    calc.calculate(prices, volumes)

    assert prices == p
    assert volumes == v
