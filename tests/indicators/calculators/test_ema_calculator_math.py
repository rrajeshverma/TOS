import pytest

from indicators.calculators.ema_calculator import EmaCalculator


def test_period_one_returns_last_price():
    calc = EmaCalculator()

    assert calc.calculate([10, 20, 30], period=1) == 30.0


def test_constant_series_returns_constant():
    calc = EmaCalculator()

    assert calc.calculate([100] * 20, period=9) == pytest.approx(100.0)


def test_ema_of_rising_prices_is_between_first_and_last():
    calc = EmaCalculator()

    ema = calc.calculate([10, 20, 30, 40, 50], period=3)

    assert 10 < ema <= 50


def test_ema_returns_float():
    calc = EmaCalculator()

    assert isinstance(calc.calculate([1, 2, 3, 4, 5], period=3), float)
