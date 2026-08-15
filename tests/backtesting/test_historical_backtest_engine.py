from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from backtesting.historical_backtest_engine import HistoricalBacktestEngine
from domain.trade import Trade
from shared.enums import TradeStatus


def make_trade(pnl: Decimal) -> Trade:
    return Trade(
        trade_id="T1",
        risk=Mock(),
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target=Decimal("120"),
        quantity=1,
        entry_time=datetime(2026, 1, 1, 9, 15),
        status=TradeStatus.CLOSED,
        pnl=pnl,
    )


def test_engine_builds_equity_curve_from_completed_trades():
    runner = Mock()
    runner.run.return_value = 5
    runner.context.trade_ledger.trades = [
        make_trade(Decimal("100")),
        make_trade(Decimal("-40")),
        make_trade(Decimal("60")),
    ]

    engine = HistoricalBacktestEngine(
        runtime=Mock(),
        replay_runner=runner,
    )

    assert engine.run() == 5

    assert engine.equity_curve.values() == [
        Decimal("100"),
        Decimal("60"),
        Decimal("120"),
    ]


def test_engine_passes_initial_capital_to_statistics():
    runner = Mock()
    runner.run.return_value = 5
    runner.context.trade_ledger.trades = [
        make_trade(Decimal("100")),
        make_trade(Decimal("-40")),
        make_trade(Decimal("-100")),
    ]

    engine = HistoricalBacktestEngine(
        runtime=Mock(),
        replay_runner=runner,
        initial_capital=Decimal("1000"),
    )

    engine.run()

    assert engine.statistics.maximum_drawdown == Decimal("140")
    assert engine.statistics.maximum_drawdown_percentage == Decimal("14")
