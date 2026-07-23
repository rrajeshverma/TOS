import pytest

from indicators.calculators.ema_calculator import EmaCalculator


def test_ema_single_value():
    calc = EmaCalculator()

    assert calc.calculate([100.0], period=1) == pytest.approx(100.0)


def test_ema_constant_series():
    calc = EmaCalculator()

    prices = [100.0] * 50

    assert calc.calculate(prices, period=10) == pytest.approx(100.0)


def test_ema_never_exceeds_max_price():
    calc = EmaCalculator()

    prices = [10, 20, 30, 40, 50]

    ema = calc.calculate(prices, period=5)

    assert ema <= max(prices)


def test_ema_never_below_min_price():
    calc = EmaCalculator()

    prices = [10, 20, 30, 40, 50]

    ema = calc.calculate(prices, period=5)

    assert ema >= min(prices)
