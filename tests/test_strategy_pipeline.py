from portfolio.strategy_pipeline import StrategyPipeline


class DummyStrategy:
    def __init__(self, value):
        self.value = value

    def execute(self, context=None):
        return self.value


def test_create_pipeline():
    pipeline = StrategyPipeline()

    assert pipeline is not None


def test_add_strategy():
    pipeline = StrategyPipeline()

    s = DummyStrategy("BUY")

    pipeline.add(s)

    assert pipeline.count() == 1


def test_remove_strategy():
    pipeline = StrategyPipeline()

    s = DummyStrategy("BUY")

    pipeline.add(s)
    pipeline.remove(s)

    assert pipeline.count() == 0


def test_clear():
    pipeline = StrategyPipeline()

    pipeline.add(DummyStrategy("A"))
    pipeline.add(DummyStrategy("B"))

    pipeline.clear()

    assert pipeline.is_empty()


def test_execute():
    pipeline = StrategyPipeline()

    pipeline.add(DummyStrategy("BUY"))
    pipeline.add(DummyStrategy("SELL"))

    assert pipeline.execute() == [
        "BUY",
        "SELL",
    ]


def test_contains():
    pipeline = StrategyPipeline()

    s = DummyStrategy("BUY")

    pipeline.add(s)

    assert pipeline.contains(s)


def test_first():
    pipeline = StrategyPipeline()

    s1 = DummyStrategy("BUY")
    s2 = DummyStrategy("SELL")

    pipeline.add(s1)
    pipeline.add(s2)

    assert pipeline.first() is s1


def test_last():
    pipeline = StrategyPipeline()

    s1 = DummyStrategy("BUY")
    s2 = DummyStrategy("SELL")

    pipeline.add(s1)
    pipeline.add(s2)

    assert pipeline.last() is s2


def test_strategies():
    pipeline = StrategyPipeline()

    s1 = DummyStrategy("BUY")
    s2 = DummyStrategy("SELL")

    pipeline.add(s1)
    pipeline.add(s2)

    assert pipeline.strategies() == [
        s1,
        s2,
    ]


def test_empty():
    pipeline = StrategyPipeline()

    assert pipeline.is_empty()


def test_execute_empty():
    pipeline = StrategyPipeline()

    assert pipeline.execute() == []
