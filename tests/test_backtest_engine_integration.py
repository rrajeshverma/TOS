from backtesting.backtest_engine import BacktestEngine
from backtesting.backtest_result import BacktestResult


def test_run_returns_backtest_result():
    engine = BacktestEngine()

    result = engine.run()

    assert isinstance(result, BacktestResult)


def test_empty_run_has_zero_trades():
    engine = BacktestEngine()

    result = engine.run()

    assert result.total_trades == 0
    assert result.net_pnl == 0