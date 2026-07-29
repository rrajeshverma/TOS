from strategies.loader import StrategyLoader


def test_discover_finds_builtin_plugins():
    loader = StrategyLoader()

    plugins = loader.discover()

    assert "ema" in plugins
    assert "orb" in plugins
    assert "sample_strategy" in plugins
    assert "vwap" in plugins