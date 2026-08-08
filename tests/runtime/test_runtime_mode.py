from runtime.runtime_mode import RuntimeMode


def test_runtime_mode_values():
    assert RuntimeMode.VERSION == "version"
    assert RuntimeMode.HEALTH == "health"
    assert RuntimeMode.VALIDATE == "validate"
    assert RuntimeMode.PAPER == "paper"
    assert RuntimeMode.LIVE == "live"
    assert RuntimeMode.REPLAY == "replay"
    assert RuntimeMode.BACKTEST == "backtest"


def test_runtime_mode_count():
    assert len(RuntimeMode) == 7


def test_runtime_mode_lookup():
    assert RuntimeMode("paper") is RuntimeMode.PAPER
    assert RuntimeMode("live") is RuntimeMode.LIVE
    assert RuntimeMode("backtest") is RuntimeMode.BACKTEST
