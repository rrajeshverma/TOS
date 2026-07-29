import importlib

from strategies.loader import StrategyLoader


def test_loader_can_import_discovered_plugins():
    loader = StrategyLoader()

    modules = loader.load()

    assert len(modules) > 0

    for module in modules:
        assert module.__name__.startswith("strategies.plugins.")
        assert module is importlib.import_module(module.__name__)
