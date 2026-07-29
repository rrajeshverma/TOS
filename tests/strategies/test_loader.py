import pytest

from strategies.loader import StrategyLoader


def test_loader_starts_empty():
    loader = StrategyLoader()

    assert loader.plugins == []


def test_loader_add_plugin():
    loader = StrategyLoader()

    plugin = object()

    loader.add(plugin)

    assert loader.plugins == [plugin]


def test_loader_rejects_none():
    loader = StrategyLoader()

    with pytest.raises(ValueError):
        loader.add(None)
