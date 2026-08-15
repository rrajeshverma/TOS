from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from backtesting.backtest_application import BacktestApplication
from backtesting.backtest_config import BacktestConfig


def test_application_passes_initial_capital_to_engine():
    config = BacktestConfig(
        symbol="BTCUSDT",
        timeframe="30m",
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 12, 31),
        initial_capital=250000.0,
    )

    with patch("backtesting.backtest_application.HistoricalBacktestEngine") as mock_engine:
        mock_engine.return_value.run.return_value = 0

        application = BacktestApplication(config=config)

        application.run()

        mock_engine.assert_called_once()

        _, kwargs = mock_engine.call_args

        assert kwargs["initial_capital"] == Decimal("250000")
