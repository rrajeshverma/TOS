from portfolio.strategy_context import StrategyContext
from portfolio.strategy_loader import StrategyLoader
from portfolio.strategy_factory import StrategyFactory
from portfolio.strategy_performance import StrategyPerformance
from portfolio.strategy_ranker import StrategyRanker


class FakeStrategy:

    def execute(self):
        return "OK"


# -------------------------
# Strategy Context
# -------------------------


def test_context_set_get():

    ctx = StrategyContext()

    ctx.set("symbol", "NIFTY")

    assert ctx.get("symbol") == "NIFTY"


def test_context_default():

    ctx = StrategyContext()

    assert ctx.get("missing", 10) == 10


def test_context_contains():

    ctx = StrategyContext()

    ctx.set("x", 1)

    assert ctx.contains("x")


def test_context_remove():

    ctx = StrategyContext()

    ctx.set("x", 1)
    ctx.remove("x")

    assert not ctx.contains("x")


def test_context_size():

    ctx = StrategyContext()

    ctx.set("a", 1)
    ctx.set("b", 2)

    assert ctx.size() == 2


# -------------------------
# Loader
# -------------------------


def test_loader_register():

    loader = StrategyLoader()

    loader.register(
        "S1",
        FakeStrategy(),
    )

    assert loader.contains("S1")


def test_loader_get():

    loader = StrategyLoader()

    strategy = FakeStrategy()

    loader.register(
        "S1",
        strategy,
    )

    assert loader.get("S1") == strategy


def test_loader_load_many():

    loader = StrategyLoader()

    loader.load_many(
        {
            "A": FakeStrategy(),
            "B": FakeStrategy(),
        }
    )

    assert loader.count() == 2


def test_loader_clear():

    loader = StrategyLoader()

    loader.register(
        "A",
        FakeStrategy(),
    )

    loader.clear()

    assert loader.is_empty()


# -------------------------
# Factory
# -------------------------


def test_factory_create():

    factory = StrategyFactory()

    strategy = FakeStrategy()

    factory.register(
        "S1",
        strategy,
    )

    assert factory.create("S1") == strategy


def test_factory_count():

    factory = StrategyFactory()

    factory.register(
        "S1",
        FakeStrategy(),
    )

    assert factory.count() == 1


# -------------------------
# Performance
# -------------------------


def test_add_trade():

    perf = StrategyPerformance()

    perf.add_trade(100)

    assert perf.total_trades() == 1


def test_net_profit():

    perf = StrategyPerformance()

    perf.add_trade(100)
    perf.add_trade(-50)

    assert perf.net_profit() == 50


def test_win_rate():

    perf = StrategyPerformance()

    perf.add_trade(100)
    perf.add_trade(-50)

    assert perf.win_rate() == 50


def test_profit_factor():

    perf = StrategyPerformance()

    perf.add_trade(100)
    perf.add_trade(-50)

    assert perf.profit_factor() == 2


# -------------------------
# Ranker
# -------------------------


def test_ranker_add():

    ranker = StrategyRanker()

    ranker.add_strategy(
        "A",
        90,
    )

    assert ranker.get_score("A") == 90


def test_ranker_order():

    ranker = StrategyRanker()

    ranker.add_strategy("A", 50)
    ranker.add_strategy("B", 90)

    assert ranker.rank()[0][0] == "B"


def test_best_strategy():

    ranker = StrategyRanker()

    ranker.add_strategy("A", 50)
    ranker.add_strategy("B", 90)

    assert ranker.best_strategy() == "B"


def test_ranker_summary():

    ranker = StrategyRanker()

    result = ranker.summary()

    assert "ranking" in result