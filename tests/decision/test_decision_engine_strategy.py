from decision.decision_engine import DecisionEngine
from domain.indicator_set import IndicatorSet
from strategy.strategy import Strategy
from strategy.strategy_registry import StrategyRegistry


class BuyStrategy(Strategy):
    def decide(self, indicators):
        return "BUY"


def indicators():
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=50.0,
        volume_average=1000.0,
    )


def test_engine_uses_registered_strategy():
    registry = StrategyRegistry()
    registry.register(BuyStrategy())

    engine = DecisionEngine(registry)

    assert engine.decide(indicators()) == "BUY"


def test_requires_registry():
    registry = StrategyRegistry()

    engine = DecisionEngine(registry)

    assert engine is not None


def test_no_registered_strategy_returns_hold():
    registry = StrategyRegistry()

    engine = DecisionEngine(registry)

    assert engine.decide(indicators()) == "HOLD"


def test_repeatable():
    registry = StrategyRegistry()
    registry.register(BuyStrategy())

    engine = DecisionEngine(registry)

    assert engine.decide(indicators()) == engine.decide(indicators())


def test_engine_stateless():
    registry = StrategyRegistry()

    engine = DecisionEngine(registry)

    engine.decide(indicators())

    assert vars(engine) == {"_registry": registry}
