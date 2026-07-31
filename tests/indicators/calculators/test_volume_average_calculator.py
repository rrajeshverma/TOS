import pytest

from indicators.calculators.volume_average_calculator import VolumeAverageCalculator


def test_can_create_volume_average_calculator():
    assert VolumeAverageCalculator() is not None


def test_has_calculate_method():
    calc = VolumeAverageCalculator()

    assert callable(calc.calculate)


def test_rejects_none():
    calc = VolumeAverageCalculator()

    with pytest.raises(ValueError):
        calc.calculate(None)


def test_rejects_empty():
    calc = VolumeAverageCalculator()

    with pytest.raises(ValueError):
        calc.calculate([])


def test_returns_float():
    calc = VolumeAverageCalculator()

    result = calc.calculate([1000] * 20)

    assert isinstance(result, float)


def test_repeatable():
    calc = VolumeAverageCalculator()

    volumes = [1000] * 20

    assert calc.calculate(volumes) == calc.calculate(volumes)


def test_stateless():
    calc = VolumeAverageCalculator()

    calc.calculate([1000] * 20)

    assert vars(calc) == {}
