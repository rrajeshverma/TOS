class BacktestEngine:
    def __init__(self, feed, strategy=None):
        self.feed = feed
        self.strategy = strategy

    def run(self):
        results = []

        for candle in self.feed:
            if self.strategy is not None:
                signal = self.strategy.on_candle(candle)

                if signal is not None:
                    results.append(signal)

        return results
