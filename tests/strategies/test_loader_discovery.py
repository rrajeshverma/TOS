from strategies.loader import StrategyLoader


def test_loader_discovers_builtin_plugins():
    loader = StrategyLoader()

    plugins = loader.discover()

    assert plugins == [
        "ema",
        "orb",
        "sample_strategy",
        "vwap",
    ]