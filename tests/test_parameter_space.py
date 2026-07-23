import pytest

from optimizer.parameter_space import ParameterSpace


def test_parameter_space_is_empty():
    space = ParameterSpace()

    assert len(space) == 0
    assert space.count() == 0
    assert list(space.generate()) == []


def test_add_parameter():
    space = ParameterSpace()

    space.add("ema", [20, 30, 40])

    assert "ema" in space
    assert len(space) == 1


def test_remove_parameter():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    space.remove("ema")

    assert "ema" not in space
    assert len(space) == 0


def test_clear():
    space = ParameterSpace()

    space.add("ema", [20])
    space.add("rsi", [50])

    space.clear()

    assert len(space) == 0


def test_duplicate_parameter_raises():
    space = ParameterSpace()

    space.add("ema", [20])

    with pytest.raises(ValueError):
        space.add("ema", [30])


@pytest.mark.parametrize("name", ["", None])
def test_invalid_name(name):
    space = ParameterSpace()

    with pytest.raises(ValueError):
        space.add(name, [1])


@pytest.mark.parametrize("values", [[], (), set()])
def test_empty_values(values):
    space = ParameterSpace()

    with pytest.raises(ValueError):
        space.add("ema", values)


def test_generate_single_parameter():
    space = ParameterSpace()

    space.add("ema", [20, 30])

    combinations = list(space.generate())

    assert combinations == [
        {"ema": 20},
        {"ema": 30},
    ]


def test_generate_multiple_parameters():
    space = ParameterSpace()

    space.add("ema", [20, 30])
    space.add("rsi", [50, 60])

    combinations = list(space.generate())

    assert combinations == [
        {"ema": 20, "rsi": 50},
        {"ema": 20, "rsi": 60},
        {"ema": 30, "rsi": 50},
        {"ema": 30, "rsi": 60},
    ]


def test_count():
    space = ParameterSpace()

    space.add("ema", [20, 30, 40])
    space.add("rsi", [50, 60])

    assert space.count() == 6


def test_iterator():
    space = ParameterSpace()

    space.add("ema", [20])
    space.add("rsi", [50])

    assert list(iter(space)) == [
        ("ema", [20]),
        ("rsi", [50]),
    ]


def test_parameters_property():
    space = ParameterSpace()

    space.add("ema", [20])

    assert space.parameters == {"ema": [20]}


def test_generation_order():
    space = ParameterSpace()

    space.add("a", [1, 2])
    space.add("b", [10, 20])

    combinations = list(space.generate())

    assert combinations[0] == {"a": 1, "b": 10}
    assert combinations[-1] == {"a": 2, "b": 20}
