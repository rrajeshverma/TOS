"""
Run BTC historical replay through TOS.
"""

from __future__ import annotations

from backtesting.backtest_context import BacktestContext
from backtesting.csv_data_source import CSVDataSource
from backtesting.historical_backtest_engine import HistoricalBacktestEngine
from backtesting.historical_data_feed import HistoricalDataFeed
from backtesting.replay_runner import ReplayRunner
from runtime.runtime_mode import RuntimeMode
from runtime.startup import Startup


def main() -> None:
    print("=" * 60)
    print("TOS Historical BTC Replay")
    print("=" * 60)

    startup = Startup()
    startup.initialize_services()

    runtime = startup.services["trading_runtime"]
    runtime.mode = RuntimeMode.BACKTEST

    source = CSVDataSource(
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="30m",
    )

    feed = HistoricalDataFeed(
        source.load(
            "data/historical/btc/BTCUSDT_30m.csv",
        )
    )

    context = BacktestContext()

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
        context=context,
    )

    engine = HistoricalBacktestEngine(
        runtime=runtime,
        replay_runner=runner,
    )

    processed = engine.run()

    print("=" * 60)
    print(f"Replay Complete : {processed} candles")
    print("=" * 60)


if __name__ == "__main__":
    main()
