from backtesting.backtest_engine import BacktestEngine
from backtesting.trade_simulator import TradeSimulator


class BacktestRunner:
    """
    Coordinates the complete backtest workflow.

    Current:
        Feed -> Engine -> Signals

    Future:
        Feed -> Engine -> TradeSimulator -> BacktestResult
    """

    def __init__(self, feed, strategy):
        self.feed = feed
        self.strategy = strategy
        self.trade_simulator = TradeSimulator()

    def run(self):
        engine = BacktestEngine(self.feed, self.strategy)
        return engine.run()
