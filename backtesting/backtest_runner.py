from backtesting.backtest_engine import BacktestEngine


class BacktestRunner:
    """
    Coordinates the complete backtest workflow.

    Current Sprint:
    Feed -> Engine -> Signals

    Future Sprint:
    Feed -> Engine -> TradeSimulator -> BacktestResult
    """

    def __init__(self, feed, strategy):
        self.feed = feed
        self.strategy = strategy

    def run(self):
        engine = BacktestEngine(self.feed, self.strategy)
        return engine.run()