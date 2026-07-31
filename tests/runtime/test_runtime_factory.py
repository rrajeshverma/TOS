import pytest

from runtime.runtime_factory import RuntimeFactory
from runtime.trading_runtime import TradingRuntime
from trading.execution_mode import ExecutionMode


def test_creates_paper_runtime():
    factory = RuntimeFactory()

    runtime = factory.create(
        ExecutionMode.PAPER,
        {},
    )

    assert isinstance(runtime, TradingRuntime)


def test_creates_live_runtime():
    factory = RuntimeFactory()

    runtime = factory.create(
        ExecutionMode.LIVE,
        {},
    )

    assert isinstance(runtime, TradingRuntime)


def test_invalid_mode_raises():
    factory = RuntimeFactory()

    with pytest.raises(ValueError):
        factory.create(
            "INVALID",
            {},
        )
