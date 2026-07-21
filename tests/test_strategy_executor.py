from portfolio.strategy_executor import StrategyExecutor


class DummyStrategy:
    def __init__(self, signal):
        self.signal = signal

    def execute(self, context=None):
        if context is None:
            return self.signal

        return (self.signal, context)

def test_create_executor():
    executor = StrategyExecutor()

    assert executor is not None


def test_execute():
    executor = StrategyExecutor()

    strategy = DummyStrategy("BUY")

    assert executor.execute(strategy) == "BUY"


def test_execute_many():
    executor = StrategyExecutor()

    strategies = [
        DummyStrategy("BUY"),
        DummyStrategy("SELL"),
    ]

    assert executor.execute_many(strategies) == [
        "BUY",
        "SELL",
    ]


def test_execute_first():
    executor = StrategyExecutor()

    strategies = [
        DummyStrategy("BUY"),
        DummyStrategy("SELL"),
    ]

    assert executor.execute_first(strategies) == "BUY"


def test_execute_last():
    executor = StrategyExecutor()

    strategies = [
        DummyStrategy("BUY"),
        DummyStrategy("SELL"),
    ]

    assert executor.execute_last(strategies) == "SELL"


def test_execute_empty():
    executor = StrategyExecutor()

    assert executor.execute_many([]) == []


def test_count():
    executor = StrategyExecutor()

    strategies = [
        DummyStrategy("BUY"),
        DummyStrategy("SELL"),
    ]

    assert executor.count(strategies) == 2

def test_execute_with_context():
    executor = StrategyExecutor()

    strategy = DummyStrategy("BUY")

    assert executor.execute(strategy, "MARKET") == (
        "BUY",
        "MARKET",
    )


def test_execute_first_empty():
    executor = StrategyExecutor()

    assert executor.execute_first([]) is None


def test_execute_last_empty():
    executor = StrategyExecutor()

    assert executor.execute_last([]) is None
