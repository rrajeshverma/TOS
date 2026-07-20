from portfolio.strategy_factory import StrategyFactory


class DummyStrategy:
    pass


def test_create_factory():
    factory = StrategyFactory()

    assert factory is not None


def test_has_loader():
    factory = StrategyFactory()

    assert factory.loader is not None


def test_register():
    factory = StrategyFactory()

    strategy = DummyStrategy()

    factory.register(
        "ORB",
        strategy,
    )

    assert factory.contains("ORB")


def test_create():
    factory = StrategyFactory()

    strategy = DummyStrategy()

    factory.register(
        "ORB",
        strategy,
    )

    assert factory.create("ORB") is strategy


def test_create_all():
    factory = StrategyFactory()

    s1 = DummyStrategy()
    s2 = DummyStrategy()

    factory.register("ORB", s1)
    factory.register("VWAP", s2)

    assert factory.create_all() == [
        s1,
        s2,
    ]


def test_count():
    factory = StrategyFactory()

    factory.register(
        "ORB",
        DummyStrategy(),
    )

    assert factory.count() == 1


def test_list():
    factory = StrategyFactory()

    factory.register(
        "ORB",
        DummyStrategy(),
    )
    factory.register(
        "VWAP",
        DummyStrategy(),
    )

    assert factory.list_strategies() == [
        "ORB",
        "VWAP",
    ]


def test_clear():
    factory = StrategyFactory()

    factory.register(
        "ORB",
        DummyStrategy(),
    )

    factory.clear()

    assert factory.count() == 0
