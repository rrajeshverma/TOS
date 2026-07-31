from strategy.orb_strategy import OrbStrategy
from domain.indicator_set import IndicatorSet


def indicators(rsi=50.0):
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=rsi,
        volume_average=1000.0,
    )


def test_buy_when_rsi_low():
    strategy = OrbStrategy()

    assert strategy.decide(indicators(rsi=25.0)) == "BUY"


def test_sell_when_rsi_high():
    strategy = OrbStrategy()

    assert strategy.decide(indicators(rsi=75.0)) == "SELL"


def test_hold_when_rsi_mid():
    strategy = OrbStrategy()

    assert strategy.decide(indicators(rsi=50.0)) == "HOLD"


def test_repeatable():
    strategy = OrbStrategy()
    data = indicators(rsi=25.0)

    assert strategy.decide(data) == strategy.decide(data)


def test_stateless():
    strategy = OrbStrategy()

    strategy.decide(indicators())

    assert vars(strategy) == {}
