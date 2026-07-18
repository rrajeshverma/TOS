from portfolio.strategy_loader import StrategyLoader


class DummyStrategy:
    pass


def test_create_strategy_loader():
    loader = StrategyLoader()

    assert loader is not None


def test_has_registry():
    loader = StrategyLoader()

    assert loader.registry is not None


def test_register_strategy():
    loader = StrategyLoader()

    strategy = DummyStrategy()

    loader.register("ORB", strategy)

    assert loader.contains("ORB")


def test_get_strategy():
    loader = StrategyLoader()

    strategy = DummyStrategy()

    loader.register("ORB", strategy)

    assert loader.get("ORB") is strategy


def test_unregister_strategy():
    loader = StrategyLoader()

    strategy = DummyStrategy()

    loader.register("ORB", strategy)
    loader.unregister("ORB")

    assert loader.contains("ORB") is False


def test_load_many():
    loader = StrategyLoader()

    strategies = {
        "ORB": DummyStrategy(),
        "VWAP": DummyStrategy(),
    }

    loader.load_many(strategies)

    assert loader.count() == 2


def test_load_alias():
    loader = StrategyLoader()

    strategies = {
        "ORB": DummyStrategy(),
    }

    loader.load(strategies)

    assert loader.count() == 1


def test_list_strategies():
    loader = StrategyLoader()

    loader.register("ORB", DummyStrategy())
    loader.register("VWAP", DummyStrategy())

    assert loader.list_strategies() == [
        "ORB",
        "VWAP",
    ]


def test_count():
    loader = StrategyLoader()

    loader.register("ORB", DummyStrategy())

    assert loader.count() == 1


def test_empty_loader():
    loader = StrategyLoader()

    assert loader.is_empty()


def test_not_empty_loader():
    loader = StrategyLoader()

    loader.register("ORB", DummyStrategy())

    assert loader.is_empty() is False


def test_clear():
    loader = StrategyLoader()

    loader.register("ORB", DummyStrategy())
    loader.register("VWAP", DummyStrategy())

    loader.clear()

    assert loader.count() == 0