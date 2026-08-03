from datetime import datetime

import pytest

from backtesting.backtest_config import BacktestConfig


def test_create_backtest_config():
    config = BacktestConfig(
        symbol="NIFTY",
        timeframe="5m",
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 12, 31),
    )

    assert config.symbol == "NIFTY"
    assert config.timeframe == "5m"
    assert config.initial_capital == 100000.0
    assert config.max_trades_per_day == 2
    assert config.risk_reward == 2.0


def test_empty_symbol_raises():
    with pytest.raises(ValueError):
        BacktestConfig(
            symbol="",
            timeframe="5m",
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 12, 31),
        )


def test_empty_timeframe_raises():
    with pytest.raises(ValueError):
        BacktestConfig(
            symbol="NIFTY",
            timeframe="",
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 12, 31),
        )


def test_invalid_dates_raise():
    with pytest.raises(ValueError):
        BacktestConfig(
            symbol="NIFTY",
            timeframe="5m",
            start_date=datetime(2025, 12, 31),
            end_date=datetime(2025, 1, 1),
        )


def test_invalid_initial_capital_raises():
    with pytest.raises(ValueError):
        BacktestConfig(
            symbol="NIFTY",
            timeframe="5m",
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 12, 31),
            initial_capital=0,
        )
