from decimal import Decimal


from shared.enums import Signal
from strategies.delta_india_strategy import DeltaIndiaStrategy
from tests.helpers.domain_factory import (
    make_indicator_set,
    make_market,
)


def test_strategy_name():
    strategy = DeltaIndiaStrategy()

    assert strategy.name() == "DELTA_INDIA"


def test_returns_strategy_result():
    strategy = DeltaIndiaStrategy()

    result = strategy.analyze(
        make_market(),
        make_indicator_set(),
    )

    assert result.signal == Signal.BUY_CE
    assert result.has_signal
    assert len(result.reasons) > 0


def test_big_candle_returns_no_signal():
    strategy = DeltaIndiaStrategy()

    market = make_market(
        open=Decimal("100"),
        close=Decimal("350"),  # body = 250
    )

    indicators = make_indicator_set()

    result = strategy.analyze(
        market,
        indicators,
    )

    assert result.signal == Signal.NONE
    assert "Big candle rejected" in result.reasons
