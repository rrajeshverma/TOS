import pytest

from indicators.calculators.volume_average_calculator import VolumeAverageCalculator


def test_constant_volume_returns_same_value():
    calc = VolumeAverageCalculator()

    assert calc.calculate([1000] * 20) == pytest.approx(1000.0)


def test_average_between_min_and_max():
    calc = VolumeAverageCalculator()

    volumes = [100, 200, 300]

    result = calc.calculate(volumes)

    assert min(volumes) <= result <= max(volumes)


def test_accepts_integer_values():
    calc = VolumeAverageCalculator()

    assert isinstance(calc.calculate([100, 200]), float)


def test_accepts_float_values():
    calc = VolumeAverageCalculator()

    assert isinstance(calc.calculate([100.5, 200.5]), float)


def test_does_not_modify_input():
    calc = VolumeAverageCalculator()

    volumes = [100, 200, 300]
    original = volumes.copy()

    calc.calculate(volumes)

    assert volumes == original
