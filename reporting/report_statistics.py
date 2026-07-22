class ReportStatistics:
    @staticmethod
    def trade_count(trades):
        return len(trades)

    @staticmethod
    def total_profit(trades):
        return sum(trades)

    @staticmethod
    def average_profit(trades):
        return sum(trades) / len(trades) if trades else 0

    @staticmethod
    def best_trade(trades):
        return max(trades) if trades else 0

    @staticmethod
    def worst_trade(trades):
        return min(trades) if trades else 0

    @staticmethod
    def win_count(trades):
        return sum(1 for t in trades if t > 0)

    @staticmethod
    def loss_count(trades):
        return sum(1 for t in trades if t < 0)

    @staticmethod
    def win_rate(trades):
        if not trades:
            return 0
        return ReportStatistics.win_count(trades) / len(trades) * 100
