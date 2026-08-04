from domain.strategy_result import StrategyResult
from shared.enums import Signal


def test_has_signal():
    result = StrategyResult(
        signal=Signal.BUY_CE,
        reasons=(),
    )

    assert result.has_signal


def test_no_signal():
    result = StrategyResult(
        signal=Signal.NONE,
        reasons=(),
    )

    assert not result.has_signal
