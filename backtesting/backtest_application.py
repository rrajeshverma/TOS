"""
Backtest application entry point.
"""

from __future__ import annotations

from pathlib import Path

from backtesting.backtest_trade_journal import BacktestTradeJournal
from backtesting.csv_data_source import CSVDataSource
from backtesting.historical_backtest_engine import HistoricalBacktestEngine
from backtesting.historical_data_feed import HistoricalDataFeed
from backtesting.replay_runner import ReplayRunner
from config.runtime_config import RuntimeConfig
from runtime.runtime_mode import RuntimeMode
from runtime.startup import Startup


class BacktestApplication:
    """
    Builds and runs the historical backtest workflow.
    """

    DEFAULT_DATA_FILE = Path(
        "data/historical/btc/BTCUSDT_30m.csv",
    )

    def run(self) -> int:
        startup = Startup(
            RuntimeConfig(
                broker="paper",
                market_data="paper",
                mode="PAPER",
                portfolio="backtest",
            )
        )

        startup.initialize_services()

        backtest_journal = BacktestTradeJournal()
        startup.services["trading_pipeline"]._trade_journal = backtest_journal

        runtime = startup.services["trading_runtime"]

        runtime.mode = RuntimeMode.BACKTEST

        source = CSVDataSource(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
        )

        candles = source.load(
            self.DEFAULT_DATA_FILE,
        )

        feed = HistoricalDataFeed(candles)

        runner = ReplayRunner(
            runtime=runtime,
            feed=feed,
        )

        engine = HistoricalBacktestEngine(
            runtime=runtime,
            replay_runner=runner,
        )

        engine.run()
        return 0
