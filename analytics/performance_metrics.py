class PerformanceMetrics:
    @staticmethod
    def total_return(trades):
        return sum(trades)

    @staticmethod
    def average_trade(trades):
        return sum(trades) / len(trades) if trades else 0

    @staticmethod
    def best_trade(trades):
        return max(trades) if trades else 0

    @staticmethod
    def worst_trade(trades):
        return min(trades) if trades else 0

    @staticmethod
    def positive_trade_count(trades):
        return sum(1 for trade in trades if trade > 0)

    @staticmethod
    def negative_trade_count(trades):
        return sum(1 for trade in trades if trade < 0)

    @staticmethod
    def win_rate(trades):
        if not trades:
            return 0
        return PerformanceMetrics.positive_trade_count(trades) / len(trades) * 100
