import pytest

from strategies.base_strategy import BaseStrategy


class TestStrategy(BaseStrategy):

    def name(self):
        return "TEST_STRATEGY"

    def analyze(self, market):
        return "ANALYZED"

    def generate_signal(self, market):
        return "BUY"


def test_strategy_can_return_name():

    strategy = TestStrategy()

    assert (
        strategy.name()
        == "TEST_STRATEGY"
    )


def test_strategy_can_analyze_market():

    strategy = TestStrategy()

    result = strategy.analyze(
        None
    )

    assert (
        result
        == "ANALYZED"
    )


def test_strategy_can_generate_signal():

    strategy = TestStrategy()

    signal = strategy.generate_signal(
        None
    )

    assert (
        signal
        == "BUY"
    )


def test_base_strategy_cannot_be_used_directly():

    strategy = BaseStrategy()

    with pytest.raises(
        NotImplementedError
    ):
        strategy.name()


def test_base_strategy_requires_analyze():

    strategy = BaseStrategy()

    with pytest.raises(
        NotImplementedError
    ):
        strategy.analyze(None)


def test_base_strategy_requires_signal_generation():

    strategy = BaseStrategy()

    with pytest.raises(
        NotImplementedError
    ):
        strategy.generate_signal(None)
