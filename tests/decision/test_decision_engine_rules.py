from decision.decision_engine import DecisionEngine
from domain.indicator_set import IndicatorSet


def indicators(rsi=50.0):
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=rsi,
        volume_average=1000.0,
    )


def test_low_rsi_returns_buy():
    engine = DecisionEngine()

    assert engine.decide(indicators(rsi=25.0)) == "BUY"


def test_high_rsi_returns_sell():
    engine = DecisionEngine()

    assert engine.decide(indicators(rsi=75.0)) == "SELL"


def test_mid_rsi_returns_hold():
    engine = DecisionEngine()

    assert engine.decide(indicators(rsi=50.0)) == "HOLD"


def test_buy_rule_repeatable():
    engine = DecisionEngine()
    data = indicators(rsi=25.0)

    assert engine.decide(data) == engine.decide(data)


def test_sell_rule_repeatable():
    engine = DecisionEngine()
    data = indicators(rsi=75.0)

    assert engine.decide(data) == engine.decide(data)
